"""
Tests d'intégration pour les composants ML du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, patch

from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.ml.tableau_bord.alertes import get_critical_alerts
from services.ml.tableau_bord.predictions import get_ml_predictions

@pytest.mark.asyncio
async def test_tableau_bord_ml_integration():
    """Test d'intégration des composants ML du tableau de bord"""
    # Configuration des données de test
    production_predictions = {
        "yield_prediction": 1200,
        "quality_prediction": 0.95
    }
    
    finance_predictions = {
        "revenue_prediction": 150000,
        "expense_prediction": 120000
    }
    
    inventory_predictions = {
        "stock_level_predictions": {"item_1": 100}
    }
    
    hr_predictions = {
        "turnover_prediction": 0.15
    }

    production_alerts = [
        {"type": "production", "message": "Alerte Production", "priority": 1}
    ]
    
    finance_alerts = [
        {"type": "finance", "message": "Alerte Finance", "priority": 2}
    ]

    # Configuration des mocks
    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = production_predictions
    projects_ml_service.get_finance_predictions.return_value = finance_predictions
    projects_ml_service.get_inventory_predictions.return_value = inventory_predictions
    projects_ml_service.get_hr_predictions.return_value = hr_predictions

    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = []
    hr_service.get_total_employees.return_value = 100
    hr_service.get_active_contracts_count.return_value = 95
    hr_service.get_completed_trainings_count.return_value = 50
    hr_service.get_training_completion_rate.return_value = 0.85
    hr_service.get_recent_activities.return_value = []

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = production_alerts
    production_service.get_daily_production.return_value = 1000
    production_service.get_efficiency_rate.return_value = 0.92
    production_service.get_active_sensors_count.return_value = 10
    production_service.get_quality_metrics.return_value = {"defect_rate": 0.02}
    production_service.get_recent_activities.return_value = []

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = finance_alerts
    finance_service.get_daily_revenue.return_value = 50000
    finance_service.get_monthly_expenses.return_value = 40000
    finance_service.get_cash_flow.return_value = 10000
    finance_service.get_budget_status.return_value = "on_track"
    finance_service.get_recent_transactions.return_value = []

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = []
    inventory_service.get_total_items.return_value = 500
    inventory_service.get_low_stock_items.return_value = []
    inventory_service.get_total_stock_value.return_value = 100000
    inventory_service.get_recent_movements.return_value = []

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = []
    weather_service.get_current_conditions.return_value = {}
    weather_service.get_daily_forecast.return_value = []
    weather_service.get_active_alerts.return_value = []
    weather_service.get_production_impact.return_value = {}

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

    # Récupération des données unifiées
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérifications
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert "timestamp" in dashboard_data

    # Vérification des alertes
    alerts = dashboard_data["alerts"]
    assert len(alerts) == 2  # Production + Finance
    assert alerts[0]["type"] == "finance"  # Priorité plus élevée
    assert alerts[1]["type"] == "production"

    # Vérification des prédictions
    predictions = dashboard_data["predictions"]
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions
    assert "hr" in predictions

    # Vérification des modules
    modules = dashboard_data["modules"]
    assert "hr" in modules
    assert "production" in modules
    assert "finance" in modules
    assert "inventory" in modules
    assert "weather" in modules
    assert "projects" in modules

@pytest.mark.asyncio
async def test_tableau_bord_ml_cache():
    """Test du cache pour les données ML du tableau de bord"""
    # Configuration du mock de cache
    cached_data = {
        "timestamp": "2024-01-01T00:00:00",
        "modules": {},
        "alerts": [],
        "predictions": {}
    }

    cache_service = AsyncMock()
    cache_service.get.return_value = cached_data

    # Configuration des autres services
    hr_service = AsyncMock()
    production_service = AsyncMock()
    finance_service = AsyncMock()
    inventory_service = AsyncMock()
    weather_service = AsyncMock()
    projects_ml_service = AsyncMock()

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

    # Premier appel - devrait utiliser le cache
    data1 = await unified_service.get_unified_dashboard_data()
    assert data1 == cached_data

    # Vérification qu'aucun service n'a été appelé
    hr_service.get_total_employees.assert_not_called()
    production_service.get_daily_production.assert_not_called()
    finance_service.get_daily_revenue.assert_not_called()
    inventory_service.get_total_items.assert_not_called()

    # Configuration du cache pour simuler une expiration
    cache_service.get.return_value = None

    # Deuxième appel - devrait régénérer les données
    data2 = await unified_service.get_unified_dashboard_data()
    assert data2 != cached_data

    # Vérification que les services ont été appelés
    hr_service.get_total_employees.assert_called_once()
    production_service.get_daily_production.assert_called_once()
    finance_service.get_daily_revenue.assert_called_once()
    inventory_service.get_total_items.assert_called_once()
