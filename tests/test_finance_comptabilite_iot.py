"""
Tests pour le module d'intégration IoT finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.finance_comptabilite.iot import GestionIoT
from models.iot_sensor import IoTSensor, SensorData
from models.production import Parcelle

@pytest.fixture
def iot_service(db_session):
    """Fixture du service IoT"""
    return GestionIoT(db_session)

@pytest.fixture
def parcelle(db_session):
    """Fixture d'une parcelle test"""
    parcelle = Parcelle(
        code="P001",
        surface=10.5,
        culture_actuelle="BLE"
    )
    db_session.add(parcelle)
    db_session.commit()
    return parcelle

@pytest.fixture
def sensors(db_session, parcelle):
    """Fixture des capteurs test"""
    sensors = []
    
    # Différents types de capteurs
    types = ["HUMIDITE", "TEMPERATURE", "PH", "NUTRIMENTS"]
    for sensor_type in types:
        sensor = IoTSensor(
            parcelle_id=parcelle.id,
            type=sensor_type,
            code=f"SENSOR_{sensor_type}",
            actif=True
        )
        sensors.append(sensor)
        db_session.add(sensor)
        
    db_session.commit()
    return sensors

@pytest.fixture
def sensor_data(db_session, sensors):
    """Fixture des données capteurs test"""
    data = []
    now = datetime.now(datetime.timezone.utc)
    
    # Valeurs par type de capteur
    values = {
        "HUMIDITE": [65, 75, 80],
        "TEMPERATURE": [25, 30, 35],
        "PH": [6.5, 7.0, 7.5],
        "NUTRIMENTS": [150, 175, 200]
    }
    
    for sensor in sensors:
        for i, value in enumerate(values[sensor.type]):
            reading = SensorData(
                sensor_id=sensor.id,
                value=value,
                timestamp=now - timedelta(hours=i)
            )
            data.append(reading)
            db_session.add(reading)
            
    db_session.commit()
    return data

async def test_get_iot_analysis_ml(iot_service, parcelle, sensors, sensor_data, mocker):
    """Test de l'analyse ML des données IoT"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "sensor_trends": {
                    "confidence": 0.85,
                    "forecast": {"TEMPERATURE": "hausse"},
                    "patterns": ["pattern1"]
                },
                "sensor_alerts": {
                    "TEMPERATURE": {
                        "probability": 0.9,
                        "severity": "HIGH",
                        "impact": {"cost": 500}
                    }
                },
                "financial_impact": {
                    "TEMPERATURE": {
                        "score": 75,
                        "predictions": {"cost": 1000},
                        "confidence": 0.8,
                        "adjusted_costs": {"CLIMATISATION": 800}
                    }
                },
                "recommendations": [
                    {
                        "type": "IOT",
                        "priority": "HIGH",
                        "description": "Action requise",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "sensor_optimizations": {
                "TEMPERATURE": {
                    "actions": ["Optimiser climatisation"],
                    "savings": 300,
                    "timeline": "1M"
                }
            }
        }
    )
    
    # Test
    analysis = await iot_service._get_iot_analysis(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "alertes" in analysis
    assert "mesures" in analysis
    assert "tendances" in analysis
    assert "recommendations" in analysis
    assert "impact_financier" in analysis
    assert "provisions_suggeres" in analysis
    assert "ml_analysis" in analysis
    assert "optimization" in analysis
    
    # Vérification ML
    assert "sensor_trends" in analysis["ml_analysis"]
    assert "sensor_alerts" in analysis["ml_analysis"]
    assert "financial_impact" in analysis["ml_analysis"]
    assert len(analysis["recommendations"]) > 0

async def test_analyser_tendance_ml(iot_service, sensor_data, mocker):
    """Test de l'analyse ML des tendances"""
    # Mock analyse ML
    analyse_ml = {
        "sensor_trends": {
            "confidence": 0.85,
            "forecast": {"TEMPERATURE": "hausse"},
            "patterns": ["pattern1"]
        }
    }
    
    # Test
    tendance = await iot_service._analyser_tendance_ml(sensor_data, analyse_ml)
    
    # Vérification
    assert "direction" in tendance
    assert "intensite" in tendance
    assert "volatility" in tendance
    assert "fiabilite" in tendance
    assert "stabilite" in tendance
    assert "ml_confidence" in tendance
    assert "ml_forecast" in tendance
    assert "ml_patterns" in tendance

async def test_generer_alertes_iot_ml(iot_service, sensor_data, mocker):
    """Test de la génération ML des alertes"""
    # Mock analyse ML
    analyse_ml = {
        "sensor_alerts": {
            "TEMPERATURE": {
                "probability": 0.9,
                "severity": "HIGH",
                "impact": {"cost": 500}
            }
        }
    }
    
    # Test
    alertes = await iot_service._generer_alertes_iot_ml(
        "TEMPERATURE",
        sensor_data,
        analyse_ml
    )
    
    # Vérification
    assert len(alertes) > 0
    for alerte in alertes:
        assert "type" in alerte
        assert "sensor" in alerte
        assert "message" in alerte
        assert "timestamp" in alerte
        assert "impact_financier" in alerte
        assert "ml_probability" in alerte
        assert "ml_severity" in alerte
        assert "ml_impact" in alerte

async def test_analyser_impact_financier_ml(iot_service, sensor_data, mocker):
    """Test de l'analyse ML de l'impact financier"""
    # Mock analyse ML
    analyse_ml = {
        "financial_impact": {
            "TEMPERATURE": {
                "score": 75,
                "predictions": {"cost": 1000},
                "confidence": 0.8,
                "adjusted_costs": {"CLIMATISATION": 800}
            }
        }
    }
    
    # Tendance test
    tendance = {
        "direction": "hausse",
        "intensite": 0.2,
        "volatility": 0.15
    }
    
    # Test
    impact = await iot_service._analyser_impact_financier_ml(
        "TEMPERATURE",
        sensor_data,
        tendance,
        analyse_ml
    )
    
    # Vérification
    assert "score" in impact
    assert "couts_potentiels" in impact
    assert "economies_potentielles" in impact
    assert "risques" in impact
    assert "opportunites" in impact
    assert "ml_predictions" in impact
    assert "ml_confidence" in impact

async def test_calculer_provision_iot_ml(iot_service, mocker):
    """Test du calcul ML des provisions"""
    # Données test
    impact = {
        "score": 75,
        "couts_potentiels": {"CLIMATISATION": 1000}
    }
    
    tendance = {
        "direction": "hausse",
        "intensite": 0.2,
        "fiabilite": "haute"
    }
    
    optimization = {
        "sensor_provisions": {
            "TEMPERATURE": {
                "amount": 900,
                "confidence": 0.85,
                "factors": ["factor1"],
                "timeline": "3M"
            }
        }
    }
    
    # Test
    provision = await iot_service._calculer_provision_iot_ml(
        "TEMPERATURE",
        impact,
        tendance,
        optimization
    )
    
    # Vérification
    assert provision is not None
    assert "montant" in provision
    assert "justification" in provision
    assert "score_impact" in provision
    assert "tendance" in provision
    assert "fiabilite" in provision
    assert "ml_confidence" in provision
    assert "ml_factors" in provision
    assert "ml_timeline" in provision

async def test_generate_iot_recommendations(iot_service):
    """Test de la génération des recommandations ML"""
    # Données test
    analysis = {
        "alertes": [
            {
                "message": "Alerte test",
                "ml_severity": "HIGH"
            }
        ]
    }
    
    analyse_ml = {
        "recommendations": [
            {
                "type": "IOT",
                "priority": "HIGH",
                "description": "Action requise",
                "actions": ["Action 1"]
            }
        ]
    }
    
    optimization = {
        "sensor_optimizations": {
            "TEMPERATURE": {
                "actions": ["Optimiser climatisation"],
                "savings": 300,
                "timeline": "1M"
            }
        }
    }
    
    # Test
    recommendations = await iot_service._generate_iot_recommendations(
        analysis,
        analyse_ml,
        optimization
    )
    
    # Vérification
    assert len(recommendations) > 0
    
    # Vérification types
    ml_recs = [r for r in recommendations if r["type"] == "ML"]
    assert len(ml_recs) > 0
    
    opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
    assert len(opt_recs) > 0
    
    alert_recs = [r for r in recommendations if r["type"] == "ALERT"]
    assert len(alert_recs) > 0

async def test_cache_iot_analysis(iot_service, parcelle, sensors, mocker):
    """Test du cache pour l'analyse IoT"""
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(iot_service, 'cache', mock_cache)
    
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "predictions": {}
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "sensor_optimizations": {}
        }
    )
    
    # Premier appel
    await iot_service._get_iot_analysis(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification cache
    assert mock_cache.set.called
    
    # Deuxième appel
    mock_cache.get.return_value = {"cached": True}
    result = await iot_service._get_iot_analysis(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification résultat du cache
    assert result == {"cached": True}
