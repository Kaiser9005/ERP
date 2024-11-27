"""
Fixtures pour les tests ML.
"""

import pytest
from datetime import datetime
from unittest.mock import AsyncMock
from typing import Dict, Any

from .utils import (
    generate_test_predictions,
    generate_test_alerts,
    clear_test_cache,
    clear_test_data,
    clear_test_models
)

@pytest.fixture(autouse=True)
def cleanup_test_directories():
    """Nettoie les répertoires de test avant et après chaque test."""
    clear_test_cache()
    clear_test_data()
    clear_test_models()
    yield
    clear_test_cache()
    clear_test_data()
    clear_test_models()

@pytest.fixture
def ml_predictions() -> Dict[str, Any]:
    """Génère des prédictions ML de test."""
    return generate_test_predictions()

@pytest.fixture
def ml_alerts() -> Dict[str, Any]:
    """Génère des alertes ML de test."""
    return generate_test_alerts()

@pytest.fixture
def mock_ml_services():
    """Mock des services ML."""
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

    return {
        "hr": hr_service,
        "production": production_service,
        "finance": finance_service,
        "inventory": inventory_service,
        "weather": weather_service,
        "projects_ml": projects_ml_service,
        "cache": cache_service
    }

@pytest.fixture
def mock_ml_cache_data():
    """Données de cache ML de test."""
    return {
        "modules": {
            "production": {
                "daily_production": 1000,
                "efficiency_rate": 0.92,
                "active_sensors": 10
            },
            "hr": {
                "total_employees": 100,
                "active_contracts": 95,
                "training_completion": 0.85
            },
            "finance": {
                "daily_revenue": 50000,
                "monthly_expenses": 40000,
                "cash_flow": 10000
            },
            "inventory": {
                "total_items": 500,
                "total_value": 100000
            }
        },
        "alerts": [
            {"type": "production", "message": "Alerte Production", "priority": 1},
            {"type": "hr", "message": "Alerte RH", "priority": 2},
            {"type": "finance", "message": "Alerte Finance", "priority": 3}
        ],
        "predictions": {
            "production": {
                "yield_prediction": 1200,
                "quality_prediction": 0.95
            },
            "finance": {
                "revenue_prediction": 150000,
                "expense_prediction": 120000
            },
            "inventory": {
                "stock_level_predictions": {"item_1": 100}
            },
            "hr": {
                "turnover_prediction": 0.15
            }
        },
        "timestamp": datetime.now().isoformat()
    }
