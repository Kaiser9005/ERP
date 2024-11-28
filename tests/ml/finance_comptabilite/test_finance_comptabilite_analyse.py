"""
Tests pour le module d'analyse finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from models.comptabilite import CompteComptable, EcritureComptable, TypeCompte
from models.finance import Transaction
from models.production import Parcelle

@pytest.fixture
def analyse_service(db_session):
    """Fixture du service d'analyse"""
    return AnalyseFinanceCompta(db_session)

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
def transactions(db_session, parcelle):
    """Fixture des transactions test"""
    transactions = []
    
    # Recettes
    for i in range(3):
        transaction = Transaction(
            parcelle_id=parcelle.id,
            type_transaction="RECETTE",
            montant=Decimal("1000.00"),
            date_transaction=date(2024, 1, 1) + timedelta(days=i),
            statut="VALIDEE"
        )
        transactions.append(transaction)
        db_session.add(transaction)
        
    # Dépenses
    for i in range(2):
        transaction = Transaction(
            parcelle_id=parcelle.id,
            type_transaction="DEPENSE",
            montant=Decimal("500.00"),
            date_transaction=date(2024, 1, 1) + timedelta(days=i),
            statut="VALIDEE"
        )
        transactions.append(transaction)
        db_session.add(transaction)
        
    db_session.commit()
    return transactions

@pytest.fixture
def ecritures(db_session, parcelle):
    """Fixture des écritures test"""
    ecritures = []
    
    # Débits
    for i in range(2):
        ecriture = EcritureComptable(
            parcelle_id=parcelle.id,
            debit=Decimal("500.00"),
            date_ecriture=date(2024, 1, 1) + timedelta(days=i),
            statut="VALIDEE"
        )
        ecritures.append(ecriture)
        db_session.add(ecriture)
        
    # Crédits
    for i in range(3):
        ecriture = EcritureComptable(
            parcelle_id=parcelle.id,
            credit=Decimal("1000.00"),
            date_ecriture=date(2024, 1, 1) + timedelta(days=i),
            statut="VALIDEE"
        )
        ecritures.append(ecriture)
        db_session.add(ecriture)
        
    db_session.commit()
    return ecritures

async def test_get_analyse_parcelle_basic(analyse_service, parcelle, transactions, ecritures):
    """Test de l'analyse basique d'une parcelle"""
    analyse = await analyse_service.get_analyse_parcelle(
        parcelle_id=parcelle.id,
        include_predictions=False
    )
    
    # Vérification structure
    assert "parcelle" in analyse
    assert "periode" in analyse
    assert "indicateurs" in analyse
    assert "transactions" in analyse
    assert "comptabilite" in analyse
    assert "ml_analysis" not in analyse
    
    # Vérification parcelle
    assert analyse["parcelle"]["id"] == parcelle.id
    assert analyse["parcelle"]["surface"] == parcelle.surface
    
    # Vérification transactions
    assert analyse["transactions"]["count"] == len(transactions)
    assert analyse["transactions"]["total_recettes"] == 3000  # 3 x 1000
    assert analyse["transactions"]["total_depenses"] == 1000  # 2 x 500
    
    # Vérification comptabilité
    assert analyse["comptabilite"]["count"] == len(ecritures)
    assert analyse["comptabilite"]["total_debit"] == 1000  # 2 x 500
    assert analyse["comptabilite"]["total_credit"] == 3000  # 3 x 1000

async def test_get_analyse_parcelle_with_ml(
    analyse_service,
    parcelle,
    transactions,
    ecritures,
    mocker
):
    """Test de l'analyse avec ML d'une parcelle"""
    # Mock des services externes
    mocker.patch(
        'services.iot_service.IoTService.get_parcelle_data',
        return_value={
            "temperature_avg": 25,
            "humidity_avg": 65,
            "soil_moisture_avg": 45
        }
    )
    
    mocker.patch(
        'services.weather_service.WeatherService.get_historical_data',
        return_value={
            "temperature_avg": 22,
            "precipitation_avg": 50,
            "wind_speed_avg": 15
        }
    )
    
    # Analyse
    analyse = await analyse_service.get_analyse_parcelle(
        parcelle_id=parcelle.id,
        include_predictions=True
    )
    
    # Vérification ML
    assert "ml_analysis" in analyse
    assert "predictions" in analyse["ml_analysis"]
    assert "risks" in analyse["ml_analysis"]
    assert "recommendations" in analyse["ml_analysis"]
    assert "confidence_scores" in analyse["ml_analysis"]
    
    # Vérification prédictions
    predictions = analyse["ml_analysis"]["predictions"]
    assert "revenue" in predictions
    assert "costs" in predictions
    assert "margin" in predictions
    assert "growth_potential" in predictions
    assert "risk_score" in predictions
    
    # Vérification risques
    risks = analyse["ml_analysis"]["risks"]
    assert len(risks) > 0
    for risk in risks:
        assert "type" in risk
        assert "severity" in risk
        assert "probability" in risk
        assert "impact" in risk
        assert "mitigation" in risk
        
    # Vérification recommandations
    recommendations = analyse["ml_analysis"]["recommendations"]
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_predict_performance(analyse_service, parcelle, mocker):
    """Test des prédictions de performance"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_long_term_forecast',
        return_value=[{
            "temperature_avg": 22,
            "precipitation_avg": 50,
            "wind_speed_avg": 15
        }]
    )
    
    mocker.patch(
        'services.iot_service.IoTService.get_parcelle_data',
        return_value={
            "temperature_avg": 25,
            "humidity_avg": 65,
            "soil_moisture_avg": 45
        }
    )
    
    # Prédiction
    predictions = await analyse_service.predict_performance(
        parcelle_id=parcelle.id,
        months_ahead=3
    )
    
    # Vérification structure
    assert "predictions" in predictions
    assert "risk_factors" in predictions
    assert "recommendations" in predictions
    
    # Vérification prédictions mensuelles
    assert len(predictions["predictions"]) == 3
    for pred in predictions["predictions"]:
        assert "month" in pred
        assert "revenue" in pred
        assert "costs" in pred
        assert "margin" in pred
        assert "confidence" in pred
        assert "weather_impact" in pred
        
    # Vérification facteurs de risque
    assert len(predictions["risk_factors"]) > 0
    
    # Vérification recommandations
    assert len(predictions["recommendations"]) > 0
    for rec in predictions["recommendations"]:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec
        assert "expected_impact" in rec

async def test_optimize_costs(analyse_service, parcelle, mocker):
    """Test de l'optimisation des coûts"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_forecast_impact',
        return_value={
            "score": 0.2,
            "factors": ["precipitation"]
        }
    )
    
    mocker.patch(
        'services.iot_service.IoTService.get_latest_data',
        return_value={
            "temperature": 25,
            "humidity": 65,
            "soil_moisture": 45
        }
    )
    
    # Optimisation
    optimization = await analyse_service.optimize_costs(
        parcelle_id=parcelle.id,
        target_date=date(2024, 2, 1)
    )
    
    # Vérification structure
    assert "current_costs" in optimization
    assert "optimized_costs" in optimization
    assert "potential_savings" in optimization
    assert "implementation_plan" in optimization
    assert "risk_assessment" in optimization
    
    # Vérification plan
    assert len(optimization["implementation_plan"]) > 0
    for step in optimization["implementation_plan"]:
        assert "category" in step
        assert "current" in step
        assert "target" in step
        assert "actions" in step
        
    # Vérification risques
    assert len(optimization["risk_assessment"]) > 0
    for risk in optimization["risk_assessment"]:
        assert "category" in risk
        assert "risk_level" in risk
        assert "description" in risk

async def test_prepare_ml_features(analyse_service, transactions, ecritures):
    """Test de la préparation des features ML"""
    # Données test
    iot_data = {
        "temperature_avg": 25,
        "humidity_avg": 65,
        "soil_moisture_avg": 45
    }
    
    weather_data = {
        "temperature_avg": 22,
        "precipitation_avg": 50,
        "wind_speed_avg": 15
    }
    
    # Préparation features
    features = analyse_service._prepare_ml_features(
        transactions,
        ecritures,
        iot_data,
        weather_data
    )
    
    # Vérification
    assert isinstance(features, np.ndarray)
    assert len(features) == 12  # 3 + 3 + 3 + 3 features
    assert all(isinstance(f, (int, float)) for f in features)

async def test_run_ml_predictions(analyse_service):
    """Test des prédictions ML"""
    # Features test
    features = np.array([1.0] * 12)  # 12 features
    
    # Prédiction
    predictions = await analyse_service._run_ml_predictions(features)
    
    # Vérification
    assert "revenue" in predictions
    assert "costs" in predictions
    assert "margin" in predictions
    assert "growth_potential" in predictions
    assert "risk_score" in predictions
    
    assert all(isinstance(v, (int, float)) for v in predictions.values())
    assert predictions["margin"] == predictions["revenue"] - predictions["costs"]

async def test_analyze_ml_risks(analyse_service, parcelle):
    """Test de l'analyse des risques ML"""
    # Données test
    predictions = {
        "revenue": 10000,
        "costs": 8000,
        "margin": 2000,
        "growth_potential": 0.15,
        "risk_score": 0.25
    }
    
    weather_data = {
        "temperature_avg": 22,
        "precipitation_avg": 150,  # Précipitations élevées
        "wind_speed_avg": 15
    }
    
    # Analyse risques
    risks = await analyse_service._analyze_ml_risks(
        parcelle.id,
        predictions,
        weather_data
    )
    
    # Vérification
    assert len(risks) > 0
    for risk in risks:
        assert "type" in risk
        assert "severity" in risk
        assert "description" in risk
        assert "probability" in risk
        assert "impact" in risk
        assert "mitigation" in risk
        
    # Vérification risque météo
    weather_risks = [r for r in risks if r["type"] == "WEATHER"]
    assert len(weather_risks) > 0
    assert any("précipitations" in r["description"].lower() for r in weather_risks)

async def test_generate_ml_recommendations(analyse_service, parcelle):
    """Test de la génération de recommandations ML"""
    # Données test
    predictions = {
        "revenue": 10000,
        "costs": 9000,  # Coûts élevés
        "margin": 1000,
        "growth_potential": 0.15,
        "risk_score": 0.25
    }
    
    # Génération recommandations
    recommendations = await analyse_service._generate_ml_recommendations(
        parcelle.id,
        predictions
    )
    
    # Vérification
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec
        assert "expected_impact" in rec
        
    # Vérification recommandation coûts
    cost_recs = [r for r in recommendations if r["type"] == "COST"]
    assert len(cost_recs) > 0
    
    # Vérification recommandation croissance
    growth_recs = [r for r in recommendations if r["type"] == "GROWTH"]
    assert len(growth_recs) > 0

async def test_get_historical_data(analyse_service, parcelle, transactions, ecritures):
    """Test de la récupération des données historiques"""
    # Récupération données
    historical = await analyse_service._get_historical_data(
        parcelle_id=parcelle.id,
        months_back=12
    )
    
    # Vérification structure
    assert "transactions" in historical
    assert "ecritures" in historical
    assert "monthly_stats" in historical
    
    # Vérification transactions
    assert len(historical["transactions"]) == len(transactions)
    
    # Vérification écritures
    assert len(historical["ecritures"]) == len(ecritures)
    
    # Vérification stats mensuelles
    assert len(historical["monthly_stats"]) > 0
    for stat in historical["monthly_stats"]:
        assert "month" in stat
        assert "revenue" in stat
        assert "costs" in stat
        assert "debit" in stat
        assert "credit" in stat

async def test_calculate_monthly_stats(analyse_service, transactions, ecritures):
    """Test du calcul des stats mensuelles"""
    # Calcul stats
    stats = analyse_service._calculate_monthly_stats(
        transactions,
        ecritures
    )
    
    # Vérification
    assert len(stats) > 0
    for stat in stats:
        assert "month" in stat
        assert "revenue" in stat
        assert "costs" in stat
        assert "debit" in stat
        assert "credit" in stat
        
    # Vérification totaux
    total_revenue = sum(s["revenue"] for s in stats)
    total_costs = sum(s["costs"] for s in stats)
    assert total_revenue == 3000  # 3 x 1000
    assert total_costs == 1000  # 2 x 500

async def test_predict_month_performance(analyse_service, parcelle, mocker):
    """Test de la prédiction mensuelle"""
    # Mock service météo
    mocker.patch(
        'services.weather_service.WeatherService.get_forecast_impact',
        return_value={
            "score": 0.2,
            "factors": ["precipitation"]
        }
    )
    
    # Features test
    features = np.array([1.0] * 12)  # 12 features
    
    # Prédiction
    prediction = await analyse_service._predict_month_performance(
        parcelle_id=parcelle.id,
        target_date=date(2024, 2, 1),
        features=features
    )
    
    # Vérification
    assert "revenue" in prediction
    assert "costs" in prediction
    assert "confidence" in prediction
    assert "weather_impact" in prediction
    
    assert prediction["revenue"] > prediction["costs"]  # Marge positive
    assert 0 <= prediction["confidence"] <= 1
    assert isinstance(prediction["weather_impact"], (int, float))

async def test_optimize_with_ml(analyse_service):
    """Test de l'optimisation ML"""
    # Données test
    current_costs = {
        "TRANSPORT": 2000,
        "MAINTENANCE": 1500,
        "INTRANTS": 3000
    }
    
    weather_impact = {
        "score": 0.2,
        "factors": ["precipitation"]
    }
    
    iot_data = {
        "temperature": 25,
        "humidity": 65,
        "soil_moisture": 45
    }
    
    # Optimisation
    optimization = await analyse_service._optimize_with_ml(
        current_costs,
        weather_impact,
        iot_data
    )
    
    # Vérification structure
    assert "costs" in optimization
    assert "savings" in optimization
    assert "plan" in optimization
    assert "risks" in optimization
    
    # Vérification optimisation
    for category in current_costs:
        assert category in optimization["costs"]
        assert optimization["costs"][category] < current_costs[category]
        assert category in optimization["savings"]
        
    # Vérification plan
    assert len(optimization["plan"]) > 0
    for step in optimization["plan"]:
        assert "category" in step
        assert "current" in step
        assert "target" in step
        assert "actions" in step
        
    # Vérification risques
    assert len(optimization["risks"]) > 0
    for risk in optimization["risks"]:
        assert "category" in risk
        assert "risk_level" in risk
        assert "description" in risk
