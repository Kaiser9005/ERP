"""
Tests d'intégration pour les composants ML du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.ml.tableau_bord.alertes import get_critical_alerts, AlertPriority
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
        {"type": "production", "message": "Alerte Production", "priority": AlertPriority.FAIBLE}
    ]
    
    finance_alerts = [
        {"type": "finance", "message": "Alerte Finance", "priority": AlertPriority.MOYENNE}
    ]

    # Configuration des mocks
    projets_ml = AsyncMock()
    projets_ml._get_production_predictions = AsyncMock(return_value=production_predictions)
    projets_ml._get_finance_predictions = AsyncMock(return_value=finance_predictions)
    projets_ml._get_inventory_predictions = AsyncMock(return_value=inventory_predictions)
    projets_ml._get_hr_predictions = AsyncMock(return_value=hr_predictions)
    projets_ml.get_active_projects_count = AsyncMock(return_value=5)
    projets_ml.get_completion_predictions = AsyncMock(return_value={})
    projets_ml.get_resource_optimization = AsyncMock(return_value={})
    projets_ml.get_recent_activities = AsyncMock(return_value=[])

    hr_service = AsyncMock()
    hr_service.get_critical_alerts = AsyncMock(return_value=[])
    hr_service.get_total_employees = AsyncMock(return_value=100)
    hr_service.get_active_contracts_count = AsyncMock(return_value=95)
    hr_service.get_completed_trainings_count = AsyncMock(return_value=50)
    hr_service.get_training_completion_rate = AsyncMock(return_value=0.85)
    hr_service.get_recent_activities = AsyncMock(return_value=[])

    production_service = AsyncMock()
    production_service.get_critical_alerts = AsyncMock(return_value=production_alerts)
    production_service.get_daily_production = AsyncMock(return_value=1000)
    production_service.get_efficiency_rate = AsyncMock(return_value=0.92)
    production_service.get_active_sensors_count = AsyncMock(return_value=10)
    production_service.get_quality_metrics = AsyncMock(return_value={"defect_rate": 0.02})
    production_service.get_recent_activities = AsyncMock(return_value=[])

    finance_service = AsyncMock()
    finance_service.get_critical_alerts = AsyncMock(return_value=finance_alerts)
    finance_service.get_daily_revenue = AsyncMock(return_value=50000)
    finance_service.get_monthly_expenses = AsyncMock(return_value=40000)
    finance_service.get_cash_flow = AsyncMock(return_value=10000)
    finance_service.get_budget_status = AsyncMock(return_value="on_track")
    finance_service.get_recent_transactions = AsyncMock(return_value=[])

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts = AsyncMock(return_value=[])
    inventory_service.get_total_items = AsyncMock(return_value=500)
    inventory_service.get_low_stock_items = AsyncMock(return_value=[])
    inventory_service.get_total_stock_value = AsyncMock(return_value=100000)
    inventory_service.get_recent_movements = AsyncMock(return_value=[])

    weather_service = AsyncMock()
    weather_service.get_critical_alerts = AsyncMock(return_value=[])
    weather_service.get_current_conditions = AsyncMock(return_value={})
    weather_service.get_daily_forecast = AsyncMock(return_value=[])
    weather_service.get_active_alerts = AsyncMock(return_value=[])
    weather_service.get_production_impact = AsyncMock(return_value={})

    cache_service = AsyncMock()
    cache_service.get = AsyncMock(return_value=None)
    cache_service.set = AsyncMock()

    # Création du service unifié
    unified_service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service,
        projets_ml=projets_ml,
        cache_service=cache_service
    )

    # Récupération des données unifiées
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérifications
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert "timestamp" in dashboard_data

    # Vérification des modules
    modules = dashboard_data["modules"]
    assert "hr" in modules
    assert "production" in modules
    assert "finance" in modules
    assert "inventory" in modules
    assert "weather" in modules
    assert "projets" in modules

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

@pytest.mark.asyncio
async def test_tableau_bord_ml_cache():
    """Test du cache pour les données ML du tableau de bord"""
    # Configuration du mock de cache
    cached_data = {
        "timestamp": datetime.now().isoformat(),
        "modules": {
            "hr": {"total_employees": 100},
            "production": {"daily_production": 1000},
            "finance": {"daily_revenue": 50000},
            "inventory": {"total_items": 500},
            "weather": {"current_conditions": {}},
            "projets": {"active_projects": 5}
        },
        "alerts": [],
        "predictions": {
            "production": {},
            "finance": {},
            "inventory": {},
            "hr": {}
        }
    }

    cache_service = AsyncMock()
    cache_service.get = AsyncMock(return_value=cached_data)
    cache_service.set = AsyncMock()

    # Configuration des autres services
    hr_service = AsyncMock()
    production_service = AsyncMock()
    finance_service = AsyncMock()
    inventory_service = AsyncMock()
    weather_service = AsyncMock()
    projets_ml = AsyncMock()

    # Création du service unifié
    unified_service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service,
        projets_ml=projets_ml,
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
    cache_service.get = AsyncMock(return_value=None)

    # Configuration des retours pour le second appel
    hr_service.get_total_employees = AsyncMock(return_value=100)
    hr_service.get_active_contracts_count = AsyncMock(return_value=95)
    hr_service.get_completed_trainings_count = AsyncMock(return_value=50)
    hr_service.get_training_completion_rate = AsyncMock(return_value=0.85)
    hr_service.get_recent_activities = AsyncMock(return_value=[])

    production_service.get_daily_production = AsyncMock(return_value=1000)
    production_service.get_efficiency_rate = AsyncMock(return_value=0.92)
    production_service.get_active_sensors_count = AsyncMock(return_value=10)
    production_service.get_quality_metrics = AsyncMock(return_value={"defect_rate": 0.02})
    production_service.get_recent_activities = AsyncMock(return_value=[])

    finance_service.get_daily_revenue = AsyncMock(return_value=50000)
    finance_service.get_monthly_expenses = AsyncMock(return_value=40000)
    finance_service.get_cash_flow = AsyncMock(return_value=10000)
    finance_service.get_budget_status = AsyncMock(return_value="on_track")
    finance_service.get_recent_transactions = AsyncMock(return_value=[])

    inventory_service.get_total_items = AsyncMock(return_value=500)
    inventory_service.get_low_stock_items = AsyncMock(return_value=[])
    inventory_service.get_total_stock_value = AsyncMock(return_value=100000)
    inventory_service.get_recent_movements = AsyncMock(return_value=[])

    projets_ml.get_active_projects_count = AsyncMock(return_value=5)
    projets_ml.get_completion_predictions = AsyncMock(return_value={})
    projets_ml.get_resource_optimization = AsyncMock(return_value={})
    projets_ml.get_recent_activities = AsyncMock(return_value=[])

    # Deuxième appel - devrait régénérer les données
    data2 = await unified_service.get_unified_dashboard_data()
    assert data2 != cached_data

    # Vérification que les services ont été appelés
    hr_service.get_total_employees.assert_called_once()
    production_service.get_daily_production.assert_called_once()
    finance_service.get_daily_revenue.assert_called_once()
    inventory_service.get_total_items.assert_called_once()

@pytest.mark.asyncio
async def test_tableau_bord_ml_error_handling():
    """Test de la gestion des erreurs dans le tableau de bord ML"""
    # Configuration des mocks avec des erreurs
    hr_service = AsyncMock()
    hr_service.get_total_employees = AsyncMock(side_effect=Exception("Erreur HR"))

    production_service = AsyncMock()
    finance_service = AsyncMock()
    inventory_service = AsyncMock()
    weather_service = AsyncMock()
    projets_ml = AsyncMock()
    cache_service = AsyncMock()
    cache_service.get = AsyncMock(return_value=None)

    unified_service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service,
        projets_ml=projets_ml,
        cache_service=cache_service
    )

    # Exécution
    data = await unified_service.get_unified_dashboard_data()

    # Vérifications
    assert "modules" in data
    assert "hr" in data["modules"]
    assert "error" in data["modules"]["hr"]
    assert "message" in data["modules"]["hr"]
    assert "Erreur HR" in data["modules"]["hr"]["message"]
