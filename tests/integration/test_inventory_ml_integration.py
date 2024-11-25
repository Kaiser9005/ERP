"""Tests d'intégration pour les fonctionnalités ML de l'Inventaire."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import numpy as np

from models.inventory import Produit, Stock, MouvementStock
from models.iot_sensor import IoTSensor, SensorType
from services.inventory_service import InventoryService
from services.iot_service import IoTService
from services.weather_service import WeatherService
from services.cache_service import CacheService
from schemas.inventaire import (
    PredictionDemande,
    OptimisationStock,
    RecommandationReapprovisionnement
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
        delai_reapprovisionnement=5,
        stock_securite=1000,
        conditions_stockage={
            "temperature_min": 15,
            "temperature_max": 25,
            "humidite_min": 30,
            "humidite_max": 60
        }
    )
    test_session.add(produit)

    # Création d'un entrepôt de test
    entrepot = Stock(
        code="E001",
        nom="Entrepôt Principal",
        capacite=10000,
        cout_stockage_unitaire=2.0
    )
    test_session.add(entrepot)

    # Création des capteurs IoT
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
            (SensorType.TEMPERATURE_AIR, 15, 25),
            (SensorType.HUMIDITE_AIR, 30, 60)
        ], 1)
    ]
    for sensor in sensors:
        test_session.add(sensor)

    test_session.commit()

    # Création de l'historique des mouvements
    dates = [datetime.utcnow() - timedelta(days=i) for i in range(90, 0, -1)]
    for date in dates:
        mouvement = MouvementStock(
            type_mouvement="SORTIE",
            produit_id=1,
            entrepot_source_id=1,
            quantite=np.random.normal(500, 100),  # Demande avec variation
            date_mouvement=date,
            conditions_stockage={
                "temperature": np.random.normal(20, 2),
                "humidite": np.random.normal(45, 5)
            }
        )
        test_session.add(mouvement)
    
    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(MouvementStock).delete()
    test_session.query(IoTSensor).delete()
    test_session.query(Stock).delete()
    test_session.query(Produit).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_demand_prediction(test_db: Session):
    """Test des prédictions de demande."""
    inventory_service = InventoryService(
        test_db,
        weather_service=WeatherService(),
        cache_service=CacheService()
    )
    
    # 1. Prédiction de la demande
    predictions = await inventory_service.predict_demand(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=30
    )
    
    assert isinstance(predictions, list)
    assert len(predictions) == 30
    assert all(isinstance(p, PredictionDemande) for p in predictions)
    assert all(p.quantite > 0 for p in predictions)
    assert all(0.0 <= p.confiance <= 1.0 for p in predictions)

@pytest.mark.asyncio
async def test_stock_optimization(test_db: Session):
    """Test de l'optimisation des niveaux de stock."""
    inventory_service = InventoryService(test_db)
    
    # 1. Calcul des niveaux optimaux
    optimization = await inventory_service.optimize_stock_levels(
        stock_id=test_db.query(Stock).first().id
    )
    
    assert isinstance(optimization, OptimisationStock)
    assert optimization.stock_optimal > 0
    assert optimization.cout_total > 0
    assert len(optimization.recommendations) > 0

@pytest.mark.asyncio
async def test_weather_impact_prediction(test_db: Session):
    """Test des prédictions d'impact météo."""
    inventory_service = InventoryService(
        test_db,
        weather_service=WeatherService()
    )
    
    # 1. Prédiction de l'impact météo
    impact = await inventory_service.predict_weather_impact(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=7
    )
    
    assert len(impact) == 7
    assert all(
        "temperature" in day and "humidite" in day and "impact_stockage" in day
        for day in impact
    )

@pytest.mark.asyncio
async def test_reorder_recommendations(test_db: Session):
    """Test des recommandations de réapprovisionnement."""
    inventory_service = InventoryService(test_db)
    
    # 1. Génération des recommandations
    recommendations = await inventory_service.get_reorder_recommendations(
        stock_id=test_db.query(Stock).first().id
    )
    
    assert isinstance(recommendations, list)
    assert all(isinstance(r, RecommandationReapprovisionnement) for r in recommendations)
    assert all(r.quantite_recommandee > 0 for r in recommendations)
    assert all(r.priorite in ["HAUTE", "MOYENNE", "BASSE"] for r in recommendations)

@pytest.mark.asyncio
async def test_storage_conditions_prediction(test_db: Session):
    """Test des prédictions de conditions de stockage."""
    inventory_service = InventoryService(
        test_db,
        iot_service=IoTService(test_db),
        weather_service=WeatherService()
    )
    
    # 1. Prédiction des conditions
    conditions = await inventory_service.predict_storage_conditions(
        stock_id=test_db.query(Stock).first().id,
        horizon_heures=24
    )
    
    assert len(conditions) == 24
    assert all(
        "temperature" in c and "humidite" in c and "qualite_prediction" in c
        for c in conditions
    )

@pytest.mark.asyncio
async def test_ml_model_retraining(test_db: Session):
    """Test du réentraînement des modèles ML."""
    inventory_service = InventoryService(test_db)
    
    # 1. Réentraînement des modèles
    training_result = await inventory_service.retrain_ml_models(
        produit_id=test_db.query(Produit).first().id
    )
    
    assert training_result["status"] == "success"
    assert "metrics" in training_result
    assert all(
        metric in training_result["metrics"]
        for metric in ["mae", "rmse", "r2_score"]
    )

@pytest.mark.asyncio
async def test_anomaly_detection(test_db: Session):
    """Test de la détection d'anomalies."""
    inventory_service = InventoryService(
        test_db,
        iot_service=IoTService(test_db)
    )
    
    # 1. Détection des anomalies
    anomalies = await inventory_service.detect_stock_anomalies(
        stock_id=test_db.query(Stock).first().id,
        periode_jours=30
    )
    
    assert isinstance(anomalies, list)
    assert all(
        "date" in a and "type" in a and "severite" in a and "description" in a
        for a in anomalies
    )

@pytest.mark.asyncio
async def test_seasonal_pattern_analysis(test_db: Session):
    """Test de l'analyse des patterns saisonniers."""
    inventory_service = InventoryService(test_db)
    
    # 1. Analyse des patterns
    patterns = await inventory_service.analyze_seasonal_patterns(
        produit_id=test_db.query(Produit).first().id
    )
    
    assert "daily" in patterns
    assert "weekly" in patterns
    assert "monthly" in patterns
    assert all(p["score"] >= 0 and p["score"] <= 1 for p in patterns.values())

@pytest.mark.asyncio
async def test_ml_cache_integration(test_db: Session):
    """Test de l'intégration du cache pour les prédictions ML."""
    inventory_service = InventoryService(
        test_db,
        cache_service=CacheService()
    )
    
    # 1. Première prédiction (devrait calculer)
    start_time = datetime.now(datetime.timezone.utc)
    prediction1 = await inventory_service.predict_demand(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=7
    )
    time1 = datetime.now(datetime.timezone.utc) - start_time
    
    # 2. Deuxième prédiction (devrait utiliser le cache)
    start_time = datetime.now(datetime.timezone.utc)
    prediction1 = await inventory_service.predict_demand(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=7
    )
    time1 = datetime.now(datetime.timezone.utc) - start_time
    
    # 2. Deuxième prédiction (devrait utiliser le cache)
    start_time = datetime.now(datetime.timezone.utc)
    prediction2 = await inventory_service.predict_demand(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=7
    )
    time2 = datetime.now(datetime.timezone.utc) - start_time
    
    assert prediction1 == prediction2
    assert time2 < time1  # Le cache devrait être plus rapide
    prediction2 = await inventory_service.predict_demand(
        produit_id=test_db.query(Produit).first().id,
        horizon_jours=7
    )
    time2 = datetime.now(datetime.timezone.utc) - start_time
    
    assert prediction1 == prediction2
    assert time2 < time1  # Le cache devrait être plus rapide
