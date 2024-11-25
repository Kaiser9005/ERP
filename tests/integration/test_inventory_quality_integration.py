"""Tests d'intégration pour la qualité et traçabilité de l'Inventaire."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.inventory import (
    Produit,
    Stock,
    MouvementStock,
    ControleQualite,
    Certification,
    TraceabiliteLot
)
from models.iot_sensor import IoTSensor, SensorType
from services.inventory_service import InventoryService
from services.iot_service import IoTService
from schemas.inventaire import (
    ControleQualiteCreate,
    CertificationCreate,
    TraceabiliteLotCreate,
    MouvementStockCreate
)

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test."""
    # Création d'un produit de test
    produit = Produit(
        code="P001",
        nom="Huile de Palme",
        type="RECOLTE",
        unite="litres",
        normes_qualite={
            "acidite_max": 0.5,
            "humidite_max": 0.1,
            "impuretes_max": 0.05
        }
    )
    test_session.add(produit)

    # Création d'un entrepôt de test
    entrepot = Stock(
        code="E001",
        nom="Entrepôt Principal",
        capacite=10000,
        certifications=[
            {
                "type": "ISO9001",
                "date_obtention": datetime.utcnow().isoformat(),
                "validite_mois": 24,
                "organisme": "Bureau Veritas"
            }
        ]
    )
    test_session.add(entrepot)

    # Création des capteurs qualité
    sensors = [
        IoTSensor(
            code=f"SENSOR00{i}",
            type=sensor_type,
            status="ACTIF",
            stock_id=1,
            config={},
            seuils_alerte={
                "min": min_val,
                "max": max_val
            }
        )
        for i, (sensor_type, min_val, max_val) in enumerate([
            (SensorType.ACIDITE, 0.0, 0.5),
            (SensorType.HUMIDITE_PRODUIT, 0.0, 0.1)
        ], 1)
    ]
    for sensor in sensors:
        test_session.add(sensor)

    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(TraceabiliteLot).delete()
    test_session.query(ControleQualite).delete()
    test_session.query(MouvementStock).delete()
    test_session.query(IoTSensor).delete()
    test_session.query(Stock).delete()
    test_session.query(Produit).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_quality_control_workflow(test_db: Session):
    """Test du workflow de contrôle qualité."""
    inventory_service = InventoryService(
        test_db,
        iot_service=IoTService(test_db)
    )
    
    # 1. Création d'un lot
    lot = await inventory_service.create_mouvement(
        MouvementStockCreate(
            type_mouvement="ENTREE",
            produit_id=test_db.query(Produit).first().id,
            entrepot_destination_id=test_db.query(Stock).first().id,
            quantite=1000,
            numero_lot="LOT001"
        ),
        "SYSTEM"
    )

    # 2. Contrôle qualité initial
    controle = await inventory_service.create_controle_qualite(
        ControleQualiteCreate(
            lot_id=lot.id,
            date_controle=datetime.utcnow(),
            controleur="LAB001",
            resultats={
                "acidite": 0.3,
                "humidite": 0.08,
                "impuretes": 0.03
            },
            conforme=True
        )
    )
    
    assert controle.conforme == True
    assert controle.resultats["acidite"] <= test_db.query(Produit).first().normes_qualite["acidite_max"]

    # 3. Suivi qualité continu
    for _ in range(3):  # Simulation sur 3 jours
        await inventory_service.record_quality_reading(
            lot.id,
            {
                "acidite": 0.35,
                "humidite": 0.09,
                "date_lecture": datetime.utcnow()
            }
        )

    lectures = await inventory_service.get_quality_readings(lot.id)
    assert len(lectures) == 3

@pytest.mark.asyncio
async def test_lot_traceability(test_db: Session):
    """Test de la traçabilité des lots."""
    inventory_service = InventoryService(test_db)
    
    # 1. Création d'un lot avec traçabilité
    lot = await inventory_service.create_lot_tracabilite(
        TraceabiliteLotCreate(
            produit_id=test_db.query(Produit).first().id,
            numero_lot="LOT002",
            date_production=datetime.utcnow(),
            origine={
                "parcelle": "P001",
                "date_recolte": datetime.utcnow().isoformat(),
                "producteur": "PROD001"
            }
        )
    )
    
    # 2. Ajout d'événements de traçabilité
    events = [
        ("RECOLTE", "Récolte effectuée"),
        ("TRANSPORT", "Transport vers entrepôt"),
        ("CONTROLE", "Contrôle qualité initial"),
        ("STOCKAGE", "Mise en stock")
    ]
    
    for type_event, description in events:
        await inventory_service.add_traceability_event(
            lot.id,
            type_event,
            description,
            datetime.utcnow()
        )

    # 3. Vérification de l'historique
    historique = await inventory_service.get_lot_history(lot.id)
    assert len(historique) == len(events)
    assert all(e.type_evenement in [t[0] for t in events] for e in historique)

@pytest.mark.asyncio
async def test_certification_management(test_db: Session):
    """Test de la gestion des certifications."""
    inventory_service = InventoryService(test_db)
    
    # 1. Ajout d'une certification
    certification = await inventory_service.add_certification(
        test_db.query(Stock).first().id,
        CertificationCreate(
            type="BIO",
            organisme="ECOCERT",
            date_obtention=datetime.utcnow(),
            validite_mois=12,
            criteres_evaluation={
                "pesticides": "CONFORME",
                "ogm": "CONFORME",
                "tracabilite": "CONFORME"
            }
        )
    )
    
    assert certification.type == "BIO"
    assert certification.validite_mois == 12

    # 2. Vérification des alertes d'expiration
    await inventory_service.add_certification(
        test_db.query(Stock).first().id,
        CertificationCreate(
            type="HACCP",
            organisme="SGS",
            date_obtention=datetime.utcnow() - timedelta(days=350),
            validite_mois=12
        )
    )
    
    alertes = await inventory_service.check_certification_expiration()
    assert len(alertes) == 1
    assert alertes[0].type_certification == "HACCP"

@pytest.mark.asyncio
async def test_quality_alerts(test_db: Session):
    """Test des alertes qualité."""
    inventory_service = InventoryService(
        test_db,
        iot_service=IoTService(test_db)
    )
    
    # 1. Simulation de lectures hors normes
    for sensor in test_db.query(IoTSensor).all():
        await inventory_service.iot_service.create_reading(
            sensor.id,
            {
                "valeur": 0.6 if sensor.type == SensorType.ACIDITE else 0.15,
                "unite": sensor.type.value,
                "qualite_signal": 95,
                "niveau_batterie": 80
            }
        )

    # 2. Vérification des alertes générées
    alertes = await inventory_service.get_quality_alerts()
    assert len(alertes) == 2  # Une alerte par capteur
    assert all(a.severite == "HAUTE" for a in alertes)

@pytest.mark.asyncio
async def test_quality_reporting(test_db: Session):
    """Test des rapports de qualité."""
    inventory_service = InventoryService(test_db)
    
    # 1. Création de plusieurs contrôles
    for i in range(5):
        await inventory_service.create_controle_qualite(
            ControleQualiteCreate(
                lot_id=1,
                date_controle=datetime.utcnow() - timedelta(days=i),
                controleur=f"LAB00{i}",
                resultats={
                    "acidite": 0.3 + (i * 0.05),
                    "humidite": 0.08,
                    "impuretes": 0.03
                },
                conforme=True
            )
        )

    # 2. Génération du rapport
    rapport = await inventory_service.generate_quality_report(
        test_db.query(Stock).first().id,
        datetime.now(datetime.timezone.utc) - timedelta(days=10),
        datetime.now(datetime.timezone.utc)
    )
    
    assert "tendances" in rapport
    assert "conformite" in rapport
    assert "recommandations" in rapport
    assert len(rapport["controles"]) == 5
