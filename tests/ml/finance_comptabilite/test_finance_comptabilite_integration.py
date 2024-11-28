"""
Tests pour le service d'intégration finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.finance_comptabilite_integration_service import (
    FinanceComptabiliteIntegrationService,
    ValidationResult,
    MeteoImpact,
    AnalyticData,
    CloturePeriode
)
from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    TypeCompte
)
from models.production import Parcelle, CycleCulture
from models.iot_sensor import IoTSensor, SensorData

@pytest.fixture
def integration_service(db_session):
    """Fixture du service d'intégration"""
    return FinanceComptabiliteIntegrationService(db_session)

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
def cycle_culture(db_session, parcelle):
    """Fixture d'un cycle de culture test"""
    cycle = CycleCulture(
        parcelle_id=parcelle.id,
        culture="BLE",
        date_debut=date.today() - timedelta(days=60),
        date_fin=date.today() + timedelta(days=30)
    )
    db_session.add(cycle)
    db_session.commit()
    return cycle

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

@pytest.fixture
def ecritures(db_session, parcelle):
    """Fixture des écritures test"""
    ecritures = []
    
    # Écritures de charges
    categories = ["INTRANT", "MATERIEL", "MAIN_OEUVRE"]
    for i, cat in enumerate(categories):
        ecriture = EcritureComptable(
            parcelle_id=parcelle.id,
            categorie=cat,
            type_compte=TypeCompte.CHARGE,
            montant=Decimal(str((i + 1) * 1000)),
            date=date.today()
        )
        ecritures.append(ecriture)
        db_session.add(ecriture)
        
    # Écritures de produits
    ecriture_produit = EcritureComptable(
        parcelle_id=parcelle.id,
        categorie="VENTE",
        type_compte=TypeCompte.PRODUIT,
        montant=Decimal("5000"),
        date=date.today()
    )
    ecritures.append(ecriture_produit)
    db_session.add(ecriture_produit)
        
    db_session.commit()
    return ecritures

async def test_get_analyse_parcelle_ml(
    integration_service,
    parcelle,
    cycle_culture,
    sensors,
    sensor_data,
    ecritures,
    mocker
):
    """Test de l'analyse ML d'une parcelle"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "predictions": {
                    "costs": 5000,
                    "margin": 2000
                },
                "recommendations": [
                    {
                        "type": "COST",
                        "priority": "HIGH",
                        "description": "Optimisation possible",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "potential_savings": 1000,
            "implementation_plan": [
                {
                    "category": "INTRANT",
                    "actions": ["Optimiser achats"],
                    "savings": 500
                }
            ]
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance',
        return_value={
            "predictions": [
                {
                    "month": "2024-02",
                    "costs": 5000,
                    "margin": 2000
                }
            ]
        }
    )
    
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(integration_service, 'cache', mock_cache)
    
    # Test
    analyse = await integration_service.get_analyse_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today() - timedelta(days=30),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "parcelle" in analyse
    assert "periode" in analyse
    assert "couts" in analyse
    assert "meteo_impact" in analyse
    assert "iot_analysis" in analyse
    assert "rentabilite" in analyse
    assert "ml_analysis" in analyse
    assert "optimization" in analyse
    assert "performance" in analyse
    assert "recommendations" in analyse
    
    # Vérification ML
    assert "predictions" in analyse["ml_analysis"]
    assert "recommendations" in analyse["ml_analysis"]
    assert len(analyse["recommendations"]) > 0
    
    # Vérification cache
    assert mock_cache.set.called

async def test_get_couts_parcelle_ml(
    integration_service,
    parcelle,
    ecritures,
    mocker
):
    """Test de l'analyse ML des coûts"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "cost_recommendations": [
                    {
                        "priority": "HIGH",
                        "description": "Optimisation coûts",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "cost_optimizations": [
                {
                    "description": "Optimisation test",
                    "actions": ["Action 1"],
                    "savings": 500
                }
            ]
        }
    )
    
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(integration_service, 'cache', mock_cache)
    
    # Test
    couts = await integration_service._get_couts_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "details" in couts
    assert "total" in couts
    assert "ml_analysis" in couts
    assert "optimization" in couts
    assert "recommendations" in couts
    
    # Vérification ML
    assert len(couts["recommendations"]) > 0
    
    # Vérification cache
    assert mock_cache.set.called

async def test_get_meteo_impact_ml(
    integration_service,
    parcelle,
    mocker
):
    """Test de l'analyse ML de l'impact météo"""
    # Mock des services
    mocker.patch(
        'services.weather_service.WeatherService.get_period_stats',
        return_value={
            "precipitation": 250,
            "temperature_avg": 32
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "weather_recommendations": [
                    {
                        "priority": "HIGH",
                        "description": "Action météo",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "weather_optimizations": [
                {
                    "description": "Optimisation météo",
                    "actions": ["Action 1"],
                    "impact": {"savings": 300}
                }
            ]
        }
    )
    
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(integration_service, 'cache', mock_cache)
    
    # Test
    impact = await integration_service.get_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "data" in impact
    assert "ml_analysis" in impact
    assert "optimization" in impact
    assert "recommendations" in impact
    
    # Vérification ML
    assert len(impact["recommendations"]) > 0
    
    # Vérification cache
    assert mock_cache.set.called

async def test_get_iot_analysis_ml(
    integration_service,
    parcelle,
    sensors,
    sensor_data,
    mocker
):
    """Test de l'analyse ML des données IoT"""
    # Mock des services
    mocker.patch(
        'services.iot_service.IoTService.get_period_data',
        return_value={
            "TEMPERATURE": {
                "values": [25, 30, 35],
                "alerts": ["Température élevée"]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "iot_recommendations": [
                    {
                        "priority": "HIGH",
                        "description": "Action IoT",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "iot_optimizations": [
                {
                    "description": "Optimisation IoT",
                    "actions": ["Action 1"],
                    "savings": 200
                }
            ]
        }
    )
    
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(integration_service, 'cache', mock_cache)
    
    # Test
    analysis = await integration_service.get_iot_analysis(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "data" in analysis
    assert "ml_analysis" in analysis
    assert "optimization" in analysis
    assert "recommendations" in analysis
    
    # Vérification ML
    assert len(analysis["recommendations"]) > 0
    
    # Vérification cache
    assert mock_cache.set.called

async def test_calculer_rentabilite_parcelle_ml(
    integration_service,
    parcelle,
    ecritures,
    mocker
):
    """Test du calcul ML de la rentabilité"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "profitability_recommendations": [
                    {
                        "priority": "HIGH",
                        "description": "Action rentabilité",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "profitability_optimizations": [
                {
                    "description": "Optimisation rentabilité",
                    "actions": ["Action 1"],
                    "impact": {"margin": 500}
                }
            ]
        }
    )
    
    # Données test
    couts = {
        "total": 3000,
        "details": {
            "INTRANT": {"montant": 2000},
            "MATERIEL": {"montant": 1000}
        }
    }
    
    meteo_impact = {
        "score": 75,
        "couts_additionnels": {"IRRIGATION": 500}
    }
    
    # Test
    rentabilite = await integration_service._calculer_rentabilite_parcelle(
        parcelle_id=parcelle.id,
        couts=couts,
        meteo_impact=meteo_impact,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "produits" in rentabilite
    assert "charges" in rentabilite
    assert "marge" in rentabilite
    assert "roi" in rentabilite
    assert "ml_analysis" in rentabilite
    assert "optimization" in rentabilite
    assert "recommendations" in rentabilite
    
    # Vérification ML
    assert len(rentabilite["recommendations"]) > 0

async def test_generer_recommendations_ml(integration_service):
    """Test de la génération des recommandations ML"""
    # Données test
    base_analysis = {
        "couts": {
            "total": 5000,
            "details": {
                "INTRANT": {"montant": 3000}
            }
        }
    }
    
    analyse_ml = {
        "ml_analysis": {
            "recommendations": [
                {
                    "type": "COST",
                    "priority": "HIGH",
                    "description": "Optimisation possible",
                    "actions": ["Action 1"]
                }
            ]
        }
    }
    
    optimization = {
        "potential_savings": 1500,
        "implementation_plan": [
            {
                "category": "INTRANT",
                "actions": ["Optimiser achats"],
                "savings": 500
            }
        ]
    }
    
    performance = {
        "predictions": [
            {
                "month": "2024-02",
                "margin": -1000
            }
        ]
    }
    
    # Test
    recommendations = await integration_service._generer_recommendations_ml(
        base_analysis,
        analyse_ml,
        optimization,
        performance
    )
    
    # Vérification
    assert len(recommendations) > 0
    
    # Vérification types
    ml_recs = [r for r in recommendations if r["type"] == "ML"]
    assert len(ml_recs) > 0
    
    opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
    assert len(opt_recs) > 0
    
    perf_recs = [r for r in recommendations if r["type"] == "PERFORMANCE"]
    assert len(perf_recs) > 0
