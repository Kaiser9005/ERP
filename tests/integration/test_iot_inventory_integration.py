"""Tests d'intégration IoT-Inventaire."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi import HTTPException
import json

from models.inventory import Stock
from models.iot_sensor import IoTSensor, SensorType, SensorStatus
from services.inventory_service import InventoryService
from services.iot_service import IoTService
from services.iot_monitoring_service import IoTMonitoringService
from services.cache_service import CacheService
from services.weather_service import WeatherService
from schemas.iot_monitoring import (
    MaintenanceRecommendation,
    AlertConfiguration,
    MonitoringDashboard
)

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test."""
    # Création d'un stock de test
    stock = Stock(
        code="S001",
        nom="Stock Principal",
        conditions_stockage={
            "temperature_min": 15,
            "temperature_max": 25,
            "humidite_min": 30,
            "humidite_max": 60
        }
    )
    test_session.add(stock)

    # Création des capteurs IoT
    sensors = [
        IoTSensor(
            code=f"SENSOR00{i}",
            type=sensor_type,
            status=SensorStatus.ACTIF,
            stock_id=stock.id,
            config={},
            seuils_alerte={
                "min": min_val,
                "max": max_val,
                "critique_min": min_val - 5,
                "critique_max": max_val + 5
            }
        )
        for i, (sensor_type, min_val, max_val) in enumerate([
            (SensorType.TEMPERATURE_AIR, 15, 25),
            (SensorType.HUMIDITE_AIR, 30, 60),
            (SensorType.LUMINOSITE, 100, 1000)
        ], 1)
    ]
    for sensor in sensors:
        test_session.add(sensor)

    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(IoTSensor).delete()
    test_session.query(Stock).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_realtime_monitoring_with_cache(test_db: Session):
    """Test du monitoring temps réel avec cache Redis."""
    # Services
    cache_service = CacheService()
    iot_service = IoTService(test_db)
    monitoring_service = IoTMonitoringService(
        test_db,
        iot_service=iot_service,
        cache_service=cache_service
    )

    # 1. Récupération du stock et des capteurs
    stock = test_db.query(Stock).first()
    sensors = test_db.query(IoTSensor).all()

    # 2. Simulation de données temps réel
    for sensor in sensors:
        await iot_service.create_reading(
            sensor.id,
            {
                "valeur": 20 if sensor.type == SensorType.TEMPERATURE_AIR else 45,
                "unite": "°C" if sensor.type == SensorType.TEMPERATURE_AIR else "%",
                "qualite_signal": 95,
                "niveau_batterie": 80
            }
        )

    # 3. Vérification du cache
    dashboard_key = f"dashboard:stock:{stock.id}"
    cached_data = await cache_service.get(dashboard_key)
    assert cached_data is not None
    
    dashboard = MonitoringDashboard(**json.loads(cached_data))
    assert len(dashboard.sensors_data) == len(sensors)
    assert dashboard.last_update is not None

@pytest.mark.asyncio
async def test_maintenance_recommendations(test_db: Session):
    """Test des recommandations de maintenance automatiques."""
    monitoring_service = IoTMonitoringService(
        test_db,
        iot_service=IoTService(test_db),
        weather_service=WeatherService()
    )

    # 1. Simulation d'un capteur en maintenance
    sensor = test_db.query(IoTSensor).first()
    sensor.status = SensorStatus.MAINTENANCE
    sensor.derniere_maintenance = datetime.utcnow() - timedelta(days=60)
    test_db.commit()

    # 2. Récupération des recommandations
    recommendations = await monitoring_service.get_maintenance_recommendations(
        test_db.query(Stock).first().id
    )
    
    assert len(recommendations) > 0
    assert any(r.sensor_id == sensor.id for r in recommendations)
    assert any(r.priority == "HIGH" for r in recommendations)

@pytest.mark.asyncio
async def test_alert_webhooks(test_db: Session):
    """Test des webhooks d'alertes."""
    monitoring_service = IoTMonitoringService(
        test_db,
        iot_service=IoTService(test_db)
    )

    # 1. Configuration des alertes
    stock = test_db.query(Stock).first()
    alert_config = AlertConfiguration(
        stock_id=stock.id,
        webhook_url="http://test-webhook.com/alerts",
        alert_types=["TEMPERATURE", "HUMIDITY"],
        threshold_percentage=10
    )
    await monitoring_service.configure_alerts(alert_config)

    # 2. Simulation d'une condition hors limites
    temp_sensor = test_db.query(IoTSensor).filter(
        IoTSensor.type == SensorType.TEMPERATURE_AIR
    ).first()
    
    await monitoring_service.iot_service.create_reading(
        temp_sensor.id,
        {
            "valeur": 30,  # Au-dessus du max (25)
            "unite": "°C",
            "qualite_signal": 95,
            "niveau_batterie": 80
        }
    )

    # 3. Vérification des alertes générées
    alerts = await monitoring_service.get_active_alerts(stock.id)
    assert len(alerts) > 0
    assert alerts[0].type == "TEMPERATURE"
    assert alerts[0].severity == "HIGH"

@pytest.mark.asyncio
async def test_security_and_audit(test_db: Session):
    """Test de la sécurité et de l'audit."""
    monitoring_service = IoTMonitoringService(test_db)

    # 1. Test des permissions
    with pytest.raises(HTTPException) as exc_info:
        await monitoring_service.configure_alerts(
            AlertConfiguration(
                stock_id="invalid_id",
                webhook_url="http://test.com",
                alert_types=["TEMPERATURE"]
            ),
            user_id="unauthorized_user"
        )
    assert exc_info.value.status_code == 403

    # 2. Vérification de l'audit trail
    stock = test_db.query(Stock).first()
    sensor = test_db.query(IoTSensor).first()
    
    await monitoring_service.update_sensor_config(
        sensor.id,
        {"seuils_alerte": {"min": 10, "max": 30}},
        user_id="test_user"
    )

    audit_logs = await monitoring_service.get_audit_logs(
        stock.id,
        start_date=datetime.utcnow() - timedelta(minutes=5)
    )
    
    assert len(audit_logs) > 0
    assert audit_logs[0].user_id == "test_user"
    assert audit_logs[0].action == "UPDATE_SENSOR_CONFIG"

@pytest.mark.asyncio
async def test_ml_predictions_integration(test_db: Session):
    """Test de l'intégration des prédictions ML."""
    monitoring_service = IoTMonitoringService(
        test_db,
        iot_service=IoTService(test_db),
        weather_service=WeatherService()
    )

    # 1. Récupération des données historiques
    stock = test_db.query(Stock).first()
    historical_data = await monitoring_service.get_historical_data(
        stock.id,
        start_date=datetime.utcnow() - timedelta(days=30)
    )

    # 2. Génération des prédictions
    predictions = await monitoring_service.predict_storage_conditions(
        stock.id,
        horizon_hours=24
    )

    assert len(predictions) > 0
    assert all(
        "temperature" in pred and "humidity" in pred
        for pred in predictions
    )

    # 3. Vérification des recommandations basées sur ML
    recommendations = await monitoring_service.get_ml_recommendations(stock.id)
    assert len(recommendations) > 0
    assert all(
        rec.confidence_score >= 0 and rec.confidence_score <= 1
        for rec in recommendations
    )
