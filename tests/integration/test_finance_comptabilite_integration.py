"""
Tests d'intégration pour le service Finance-Comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session

from services.finance_comptabilite import (
    FinanceComptabiliteIntegrationService,
    ValidationResult,
    MeteoImpact,
    AnalyticData,
    CloturePeriode
)
from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    TypeCompte,
    StatutEcriture
)
from models.finance import Transaction, Budget, CategorieTransaction
from models.production import Parcelle
from models.iot_sensor import IoTSensor, SensorData

@pytest.fixture
def service(db_session: Session):
    """Fixture du service d'intégration"""
    return FinanceComptabiliteIntegrationService(db_session)

@pytest.fixture
def parcelle(db_session: Session):
    """Fixture d'une parcelle de test"""
    parcelle = Parcelle(
        code="P001",
        surface=10.5,
        culture_actuelle="BLE"
    )
    db_session.add(parcelle)
    db_session.commit()
    return parcelle

@pytest.fixture
def compte_charge(db_session: Session):
    """Fixture d'un compte de charge"""
    compte = CompteComptable(
        numero="601",
        libelle="Achats stockés - Matières premières",
        type_compte=TypeCompte.CHARGE
    )
    db_session.add(compte)
    db_session.commit()
    return compte

@pytest.fixture
def compte_produit(db_session: Session):
    """Fixture d'un compte de produit"""
    compte = CompteComptable(
        numero="701",
        libelle="Ventes de produits finis",
        type_compte=TypeCompte.PRODUIT
    )
    db_session.add(compte)
    db_session.commit()
    return compte

@pytest.fixture
def sensor(db_session: Session, parcelle: Parcelle):
    """Fixture d'un capteur IoT"""
    sensor = IoTSensor(
        type="HUMIDITE",
        parcelle_id=parcelle.id,
        actif=True
    )
    db_session.add(sensor)
    db_session.commit()
    
    # Ajout de données
    for i in range(10):
        data = SensorData(
            sensor_id=sensor.id,
            value=60 + i,  # Valeurs croissantes
            timestamp=datetime.utcnow() - timedelta(hours=i)
        )
        db_session.add(data)
    db_session.commit()
    
    return sensor

async def test_analyse_parcelle_complete(
    service: FinanceComptabiliteIntegrationService,
    parcelle: Parcelle,
    compte_charge: CompteComptable,
    compte_produit: CompteComptable,
    sensor: IoTSensor,
    db_session: Session
):
    """Test d'une analyse complète de parcelle"""
    # Création d'écritures comptables
    ecriture_charge = EcritureComptable(
        compte_id=compte_charge.id,
        parcelle_id=parcelle.id,
        date_ecriture=date.today(),
        libelle="Achat semences",
        debit=Decimal("1000.00"),
        credit=Decimal("0.00"),
        statut=StatutEcriture.VALIDEE
    )
    
    ecriture_produit = EcritureComptable(
        compte_id=compte_produit.id,
        parcelle_id=parcelle.id,
        date_ecriture=date.today(),
        libelle="Vente récolte",
        debit=Decimal("0.00"),
        credit=Decimal("2000.00"),
        statut=StatutEcriture.VALIDEE
    )
    
    db_session.add(ecriture_charge)
    db_session.add(ecriture_produit)
    db_session.commit()
    
    # Exécution de l'analyse
    analyse = await service.get_analyse_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today() - timedelta(days=30),
        date_fin=date.today()
    )
    
    # Vérifications
    assert analyse["parcelle"]["id"] == parcelle.id
    assert analyse["parcelle"]["surface"] == 10.5
    
    # Vérification des coûts
    assert analyse["couts"]["total"] == 1000.0
    assert analyse["couts"]["par_hectare"] == pytest.approx(95.24, rel=1e-2)
    
    # Vérification impact météo
    assert "score" in analyse["meteo_impact"]
    assert "facteurs" in analyse["meteo_impact"]
    
    # Vérification données IoT
    assert "mesures" in analyse["iot_analysis"]
    assert "HUMIDITE" in analyse["iot_analysis"]["mesures"]
    assert analyse["iot_analysis"]["mesures"]["HUMIDITE"]["min"] == 60
    assert analyse["iot_analysis"]["mesures"]["HUMIDITE"]["max"] == 69
    
    # Vérification rentabilité
    assert analyse["rentabilite"]["revenus"] == 2000.0
    assert analyse["rentabilite"]["charges"] == 1000.0
    assert analyse["rentabilite"]["marge_brute"] == 1000.0

async def test_cloture_mensuelle(
    service: FinanceComptabiliteIntegrationService,
    parcelle: Parcelle,
    compte_charge: CompteComptable,
    compte_produit: CompteComptable,
    db_session: Session
):
    """Test d'une clôture mensuelle"""
    # Création d'écritures équilibrées
    ecriture1 = EcritureComptable(
        compte_id=compte_charge.id,
        parcelle_id=parcelle.id,
        date_ecriture=date.today(),
        libelle="Charge 1",
        debit=Decimal("1000.00"),
        credit=Decimal("0.00"),
        statut=StatutEcriture.VALIDEE,
        periode=date.today().strftime("%Y-%m")
    )
    
    ecriture2 = EcritureComptable(
        compte_id=compte_produit.id,
        parcelle_id=parcelle.id,
        date_ecriture=date.today(),
        libelle="Produit 1",
        debit=Decimal("0.00"),
        credit=Decimal("1000.00"),
        statut=StatutEcriture.VALIDEE,
        periode=date.today().strftime("%Y-%m")
    )
    
    db_session.add(ecriture1)
    db_session.add(ecriture2)
    db_session.commit()
    
    # Exécution de la clôture
    periode = date.today().strftime("%Y-%m")
    resultat = await service.executer_cloture_mensuelle(
        periode=periode,
        utilisateur_id="TEST"
    )
    
    # Vérifications
    assert resultat["periode"] == periode
    assert resultat["statut"] == "CLOTURE"
    assert resultat["totaux"]["charges"]["Charge 1"] == 1000.0
    assert resultat["totaux"]["produits"]["Produit 1"] == 1000.0
    
    # Vérification que les écritures sont gelées
    ecritures = db_session.query(EcritureComptable).filter(
        EcritureComptable.periode == periode
    ).all()
    
    for ecriture in ecritures:
        assert not ecriture.modifiable

async def test_integration_meteo_iot(
    service: FinanceComptabiliteIntegrationService,
    parcelle: Parcelle,
    sensor: IoTSensor,
    db_session: Session
):
    """Test de l'intégration météo-IoT"""
    # Analyse IoT
    iot_analyse = await service.get_iot_analysis(
        parcelle_id=parcelle.id,
        date_debut=date.today() - timedelta(days=1),
        date_fin=date.today()
    )
    
    # Vérification tendance IoT
    assert "tendances" in iot_analyse
    assert "HUMIDITE" in iot_analyse["tendances"]
    assert iot_analyse["tendances"]["HUMIDITE"]["direction"] == "hausse"
    
    # Impact météo
    meteo_impact = await service.get_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date.today() - timedelta(days=1),
        date_fin=date.today()
    )
    
    # Vérification provisions suggérées
    if meteo_impact["score"] > 0:
        assert "provisions_suggeres" in meteo_impact
        for categorie, provision in meteo_impact["provisions_suggeres"].items():
            assert provision > 0
