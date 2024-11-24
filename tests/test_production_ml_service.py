"""
Tests pour le service ML de production
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.production_ml_service import ProductionMLService
from models.production import (
    Parcelle,
    CycleCulture,
    Recolte,
    ProductionEvent,
    CultureType,
    QualiteRecolte
)

@pytest.fixture
def ml_service(db_session):
    """Fixture du service ML"""
    return ProductionMLService(db_session)

@pytest.fixture
def parcelle(db_session):
    """Fixture d'une parcelle test"""
    parcelle = Parcelle(
        code="P001",
        culture_type=CultureType.PALMIER,
        surface_hectares=Decimal("10.5"),
        date_plantation=date(2023, 1, 1)
    )
    db_session.add(parcelle)
    db_session.commit()
    return parcelle

@pytest.fixture
def cycle_culture(db_session, parcelle):
    """Fixture d'un cycle de culture"""
    cycle = CycleCulture(
        parcelle_id=parcelle.id,
        date_debut=date(2023, 1, 1),
        date_fin=date(2023, 12, 31),
        rendement_prevu=Decimal("1000.00"),
        rendement_reel=Decimal("950.00")
    )
    db_session.add(cycle)
    db_session.commit()
    return cycle

@pytest.fixture
def recoltes(db_session, parcelle, cycle_culture):
    """Fixture des récoltes"""
    recoltes = []
    for i in range(3):
        recolte = Recolte(
            parcelle_id=parcelle.id,
            cycle_culture_id=cycle_culture.id,
            date_recolte=datetime(2023, 1, 1) + timedelta(days=i*30),
            quantite_kg=Decimal("300.00"),
            qualite=QualiteRecolte.A,
            conditions_meteo={
                "temperature": 25.0,
                "humidite": 70.0,
                "precipitation": 10.0
            }
        )
        recoltes.append(recolte)
        db_session.add(recolte)
    db_session.commit()
    return recoltes

async def test_predict_rendement(ml_service, parcelle, recoltes):
    """Test de la prédiction de rendement"""
    # Prédiction
    prediction = await ml_service.predict_rendement(
        parcelle_id=parcelle.id,
        date_debut=date(2023, 1, 1),
        date_fin=date(2023, 12, 31)
    )
    
    # Vérifications
    assert "rendement_prevu" in prediction
    assert isinstance(prediction["rendement_prevu"], float)
    assert prediction["rendement_prevu"] > 0
    
    assert "intervalle_confiance" in prediction
    assert "min" in prediction["intervalle_confiance"]
    assert "max" in prediction["intervalle_confiance"]
    
    assert "facteurs_impact" in prediction
    assert len(prediction["facteurs_impact"]) > 0

async def test_optimize_cycle_culture(ml_service, parcelle):
    """Test de l'optimisation du cycle de culture"""
    # Optimisation
    optimisation = await ml_service.optimize_cycle_culture(
        parcelle_id=parcelle.id,
        date_debut=date(2024, 1, 1)
    )
    
    # Vérifications
    assert "date_debut_optimale" in optimisation
    assert isinstance(optimisation["date_debut_optimale"], date)
    
    assert "date_fin_prevue" in optimisation
    assert isinstance(optimisation["date_fin_prevue"], date)
    
    assert "etapes" in optimisation
    assert len(optimisation["etapes"]) > 0
    for etape in optimisation["etapes"]:
        assert "etape" in etape
        assert "date_debut" in etape
        assert "date_fin" in etape
        assert "conditions_optimales" in etape

async def test_analyze_meteo_impact(ml_service, parcelle, recoltes):
    """Test de l'analyse de l'impact météo"""
    # Analyse
    analyse = await ml_service.analyze_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date(2023, 1, 1),
        date_fin=date(2023, 12, 31)
    )
    
    # Vérifications
    assert "impact_score" in analyse
    assert isinstance(analyse["impact_score"], float)
    assert 0 <= analyse["impact_score"] <= 1
    
    assert "correlations" in analyse
    assert "temperature" in analyse["correlations"]
    assert "humidite" in analyse["correlations"]
    assert "precipitation" in analyse["correlations"]
    
    assert "conditions_critiques" in analyse
    assert len(analyse["conditions_critiques"]) > 0
    
    assert "recommandations" in analyse
    assert len(analyse["recommandations"]) > 0

async def test_predict_qualite(ml_service, parcelle, recoltes):
    """Test de la prédiction de qualité"""
    # Prédiction
    prediction = await ml_service.predict_qualite(
        parcelle_id=parcelle.id,
        date_recolte=date(2024, 1, 1)
    )
    
    # Vérifications
    assert "qualite_prevue" in prediction
    assert isinstance(prediction["qualite_prevue"], QualiteRecolte)
    
    assert "probabilites" in prediction
    assert QualiteRecolte.A in prediction["probabilites"]
    assert QualiteRecolte.B in prediction["probabilites"]
    assert QualiteRecolte.C in prediction["probabilites"]
    
    assert "facteurs_impact" in prediction
    assert len(prediction["facteurs_impact"]) > 0

async def test_historique_rendements(ml_service, parcelle, recoltes):
    """Test de la récupération de l'historique des rendements"""
    historique = await ml_service._get_historique_rendements(parcelle.id)
    
    assert len(historique) == len(recoltes)
    for h in historique:
        assert "date" in h
        assert "quantite" in h
        assert "qualite" in h
        assert "conditions_meteo" in h

async def test_historique_cycles(ml_service, parcelle, cycle_culture):
    """Test de la récupération de l'historique des cycles"""
    historique = await ml_service._get_historique_cycles(parcelle.id)
    
    assert len(historique) == 1
    assert "date_debut" in historique[0]
    assert "date_fin" in historique[0]
    assert "rendement_prevu" in historique[0]
    assert "rendement_reel" in historique[0]

async def test_historique_qualite(ml_service, parcelle, recoltes):
    """Test de la récupération de l'historique de qualité"""
    historique = await ml_service._get_historique_qualite(parcelle.id)
    
    assert len(historique) == len(recoltes)
    for h in historique:
        assert "date" in h
        assert "qualite" in h
        assert "conditions_meteo" in h
        assert "quantite" in h

async def test_calculate_features(ml_service):
    """Test du calcul des features"""
    # Données de test
    historique = [
        {"quantite": 100.0},
        {"quantite": 200.0}
    ]
    meteo = [
        {"temperature": 25.0, "humidite": 70.0, "precipitation": 10.0},
        {"temperature": 26.0, "humidite": 75.0, "precipitation": 5.0}
    ]
    iot_data = [
        {"valeur": 50.0},
        {"valeur": 55.0}
    ]
    
    # Calcul features
    features = ml_service._calculate_features(historique, meteo, iot_data)
    
    # Vérifications
    assert len(features) == 9  # 3 features par source de données
    assert all(isinstance(f, float) for f in features)

async def test_calculate_confidence(ml_service):
    """Test du calcul de l'intervalle de confiance"""
    # Données de test
    prediction = 1000.0
    historique = [
        {"quantite": 900.0},
        {"quantite": 1100.0}
    ]
    
    # Calcul intervalle
    intervalle = ml_service._calculate_confidence(prediction, historique)
    
    # Vérifications
    assert "min" in intervalle
    assert "max" in intervalle
    assert intervalle["min"] < prediction < intervalle["max"]

async def test_analyze_meteo_correlations(ml_service):
    """Test de l'analyse des corrélations météo"""
    # Données de test
    meteo = [
        {"temperature": 25.0, "humidite": 70.0, "precipitation": 10.0},
        {"temperature": 26.0, "humidite": 75.0, "precipitation": 5.0}
    ]
    recoltes = []  # À compléter avec des données de test
    
    # Analyse
    correlations = ml_service._analyze_meteo_correlations(meteo, recoltes)
    
    # Vérifications
    assert "temperature" in correlations
    assert "humidite" in correlations
    assert "precipitation" in correlations
    assert all(0 <= v <= 1 for v in correlations.values())

async def test_identify_critical_conditions(ml_service):
    """Test de l'identification des conditions critiques"""
    # Données de test
    meteo = [
        {"temperature": 35.0, "humidite": 40.0, "precipitation": 0.0},
        {"temperature": 25.0, "humidite": 70.0, "precipitation": 10.0}
    ]
    recoltes = []  # À compléter avec des données de test
    
    # Identification
    conditions = ml_service._identify_critical_conditions(meteo, recoltes)
    
    # Vérifications
    assert len(conditions) > 0
    for condition in conditions:
        assert "condition" in condition
        assert "seuil" in condition
        assert "impact" in condition
        assert "frequence" in condition
