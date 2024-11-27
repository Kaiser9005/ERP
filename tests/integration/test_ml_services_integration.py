"""
Tests d'intégration pour les services ML du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, patch
from datetime import datetime

from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.ml.tableau_bord.alertes import get_critical_alerts
from services.ml.tableau_bord.predictions import get_ml_predictions

@pytest.mark.integration
async def test_ml_services_integration(test_data):
    """Test de l'intégration entre les services ML"""
    # Configuration des mocks
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = [
        {"type": "hr", "message": "Alerte RH", "priority": 2}
    ]
    hr_service.get_total_employees.return_value = 100
    hr_service.get_active_contracts_count.return_value = 95
    hr_service.get_completed_trainings_count.return_value = 50
    hr_service.get_training_completion_rate.return_value = 0.85

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = [
        {"type": "production", "message": "Alerte Production", "priority": 1}
    ]
    production_service.get_daily_production.return_value = 1000
    production_service.get_efficiency_rate.return_value = 0.92
    production_service.get_active_sensors_count.return_value = 10

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = [
        {"type": "finance", "message": "Alerte Finance", "priority": 3}
    ]
    finance_service.get_daily_revenue.return_value = 50000
    finance_service.get_monthly_expenses.return_value = 40000
    finance_service.get_cash_flow.return_value = 10000

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = []
    inventory_service.get_total_items.return_value = 500
    inventory_service.get_low_stock_items.return_value = []
    inventory_service.get_total_stock_value.return_value = 100000

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = []
    weather_service.get_current_conditions.return_value = {}
    weather_service.get_daily_forecast.return_value = []

    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = {
        "yield_prediction": 1200,
        "quality_prediction": 0.95
    }
    projects_ml_service.get_finance_predictions.return_value = {
        "revenue_prediction": 150000,
        "expense_prediction": 120000
    }
    projects_ml_service.get_inventory_predictions.return_value = {
        "stock_level_predictions": {"item_1": 100}
    }
    projects_ml_service.get_hr_predictions.return_value = {
        "turnover_prediction": 0.15
    }

    cache_service = AsyncMock()
    cache_service.get.return_value = None

    # Création du service unifié
    unified_service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service,
        projects_ml_service=projects_ml_service,
        cache_service=cache_service
    )

    # Test 1: Récupération des alertes critiques
    alerts = await get_critical_alerts(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service
    )

    # Vérification des alertes
    assert len(alerts) == 3
    assert alerts[0]["priority"] == 3  # Finance (plus haute priorité)
    assert alerts[1]["priority"] == 2  # RH
    assert alerts[2]["priority"] == 1  # Production

    # Test 2: Récupération des prédictions ML
    predictions = await get_ml_predictions(projects_ml_service)

    # Vérification des prédictions
    assert "production" in predictions
    assert predictions["production"]["yield_prediction"] == 1200
    assert "finance" in predictions
    assert predictions["finance"]["revenue_prediction"] == 150000
    assert "inventory" in predictions
    assert "hr" in predictions
    assert predictions["hr"]["turnover_prediction"] == 0.15

    # Test 3: Intégration complète via le service unifié
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérification des données unifiées
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert "timestamp" in dashboard_data

    # Vérification du cache
    cache_service.get.assert_called_once()
    cache_service.set.assert_called_once()

    # Test 4: Récupération des détails d'un module spécifique
    production_details = await unified_service.get_module_details("production")
    assert production_details is not None

    # Test 5: Vérification de la cohérence des données
    modules = dashboard_data["modules"]
    assert modules["production"]["daily_production"] == 1000
    assert modules["hr"]["total_employees"] == 100
    assert modules["finance"]["daily_revenue"] == 50000
    assert modules["inventory"]["total_items"] == 500

@pytest.mark.integration
async def test_ml_services_error_handling(test_data):
    """Test de la gestion des erreurs dans l'intégration des services ML"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.side_effect = Exception("Erreur HR")
    hr_service.get_total_employees.side_effect = Exception("Erreur HR")

    production_service = AsyncMock()
    finance_service = AsyncMock()
    inventory_service = AsyncMock()
    weather_service = AsyncMock()
    projects_ml_service = AsyncMock()
    cache_service = AsyncMock()
    cache_service.get.return_value = None

    unified_service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service,
        projects_ml_service=projects_ml_service,
        cache_service=cache_service
    )

    # Test de la récupération des données avec un service en échec
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérification que le dashboard continue de fonctionner
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert dashboard_data["modules"]["hr"] == {}  # Module en échec retourne un dict vide

@pytest.mark.integration
async def test_ml_services_cache_behavior(test_data):
    """Test du comportement du cache dans l'intégration des services ML"""
    # Configuration du mock de cache
    cached_data = {
        "modules": {},
        "alerts": [],
        "predictions": {},
        "timestamp": datetime.now().isoformat()
    }

    cache_service = AsyncMock()
    cache_service.get.return_value = cached_data

    unified_service = TableauBordUnifieService(
        hr_service=AsyncMock(),
        production_service=AsyncMock(),
        finance_service=AsyncMock(),
        inventory_service=AsyncMock(),
        weather_service=AsyncMock(),
        projects_ml_service=AsyncMock(),
        cache_service=cache_service
    )

    # Test de la récupération des données depuis le cache
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérification que les données viennent du cache
    assert dashboard_data == cached_data
    cache_service.get.assert_called_once()
    cache_service.set.assert_not_called()  # Pas de mise en cache car données déjà en cache
