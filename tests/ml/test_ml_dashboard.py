"""
Tests unitaires pour le tableau de bord ML.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, patch

from services.ml.tableau_bord.unification import TableauBordUnifieService
from services.ml.tableau_bord.alertes import get_critical_alerts
from services.ml.tableau_bord.predictions import get_ml_predictions

from .utils import (
    generate_test_predictions,
    generate_test_alerts,
    calculate_metrics,
    format_test_results
)

@pytest.mark.ml_unit
async def test_get_ml_predictions(mock_ml_services):
    """Test de la récupération des prédictions ML."""
    predictions = await get_ml_predictions(mock_ml_services["projects_ml"])

    assert "production" in predictions
    assert predictions["production"]["yield_prediction"] == 1200
    assert predictions["production"]["quality_prediction"] == 0.95

    assert "finance" in predictions
    assert predictions["finance"]["revenue_prediction"] == 150000
    assert predictions["finance"]["expense_prediction"] == 120000

    assert "inventory" in predictions
    assert "stock_level_predictions" in predictions["inventory"]

    assert "hr" in predictions
    assert predictions["hr"]["turnover_prediction"] == 0.15

@pytest.mark.ml_unit
async def test_get_critical_alerts(mock_ml_services):
    """Test de la récupération des alertes critiques."""
    alerts = await get_critical_alerts(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"]
    )

    assert len(alerts) == 3
    assert alerts[0]["type"] == "finance"  # Priorité la plus haute
    assert alerts[1]["type"] == "hr"
    assert alerts[2]["type"] == "production"

@pytest.mark.ml_unit
async def test_unified_dashboard_data(mock_ml_services):
    """Test de la récupération des données unifiées du tableau de bord."""
    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    data = await unified_service.get_unified_dashboard_data()

    assert "modules" in data
    assert "alerts" in data
    assert "predictions" in data
    assert "timestamp" in data

    # Vérification des modules
    modules = data["modules"]
    assert modules["hr"]["total_employees"] == 100
    assert modules["production"]["daily_production"] == 1000
    assert modules["finance"]["daily_revenue"] == 50000
    assert modules["inventory"]["total_items"] == 500

@pytest.mark.ml_unit
async def test_cache_behavior(mock_ml_services, mock_ml_cache_data):
    """Test du comportement du cache."""
    mock_ml_services["cache"].get.return_value = mock_ml_cache_data

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Premier appel - devrait utiliser le cache
    data1 = await unified_service.get_unified_dashboard_data()
    assert data1 == mock_ml_cache_data

    # Vérification que les services n'ont pas été appelés
    mock_ml_services["hr"].get_total_employees.assert_not_called()
    mock_ml_services["production"].get_daily_production.assert_not_called()

@pytest.mark.ml_unit
async def test_cache_expiration(mock_ml_services, mock_ml_cache_data):
    """Test de l'expiration du cache."""
    # Données de cache expirées (plus de 15 minutes)
    expired_data = mock_ml_cache_data.copy()
    expired_data["timestamp"] = (
        datetime.now() - timedelta(minutes=16)
    ).isoformat()
    
    mock_ml_services["cache"].get.return_value = expired_data

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # L'appel devrait régénérer les données
    await unified_service.get_unified_dashboard_data()

    # Vérification que les services ont été appelés
    mock_ml_services["hr"].get_total_employees.assert_called_once()
    mock_ml_services["production"].get_daily_production.assert_called_once()

@pytest.mark.ml_unit
async def test_error_handling(mock_ml_services):
    """Test de la gestion des erreurs."""
    # Configuration d'un service qui échoue
    mock_ml_services["hr"].get_total_employees.side_effect = Exception("Erreur HR")
    mock_ml_services["hr"].get_critical_alerts.side_effect = Exception("Erreur HR")

    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    data = await unified_service.get_unified_dashboard_data()

    # Vérification que le tableau de bord continue de fonctionner
    assert "modules" in data
    assert "alerts" in data
    assert "predictions" in data
    assert data["modules"]["hr"] == {}  # Module en échec retourne un dict vide
    assert len(data["alerts"]) == 2  # Seulement les alertes des autres services

@pytest.mark.ml_unit
async def test_metrics_calculation(ml_predictions):
    """Test du calcul des métriques."""
    # Génération de données actuelles simulées
    actuals = generate_test_predictions()
    
    # Calcul des métriques
    metrics = calculate_metrics(ml_predictions, actuals)
    
    assert "production_mape" in metrics
    assert "finance_mape" in metrics
    assert "hr_mae" in metrics
    
    # Vérification que les métriques sont dans des plages raisonnables
    assert 0 <= metrics["production_mape"] <= 100
    assert 0 <= metrics["finance_mape"] <= 100
    assert 0 <= metrics["hr_mae"] <= 1

@pytest.mark.ml_unit
def test_results_formatting(ml_predictions):
    """Test du formatage des résultats."""
    formatted = format_test_results(ml_predictions)
    
    assert "=== PRODUCTION ===" in formatted
    assert "=== FINANCE ===" in formatted
    assert "=== INVENTORY ===" in formatted
    assert "=== HR ===" in formatted
    
    # Vérification que les valeurs clés sont présentes
    assert "yield_prediction" in formatted
    assert "revenue_prediction" in formatted
    assert "stock_level_predictions" in formatted
    assert "turnover_prediction" in formatted
