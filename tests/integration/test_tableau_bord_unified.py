"""
Tests d'intégration pour le tableau de bord unifié avec ML.
"""

import pytest
from datetime import datetime
from services.ml.tableau_bord.unification import TableauBordUnifieService

@pytest.mark.integration
async def test_tableau_bord_unified_integration(mock_ml_services, ml_test_data):
    """Test d'intégration du tableau de bord unifié avec les services ML"""
    # Configuration du service unifié avec les mocks
    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Récupération des données unifiées
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérification de la structure des données
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert "timestamp" in dashboard_data

    # Vérification des modules
    modules = dashboard_data["modules"]
    assert "hr" in modules
    assert modules["hr"]["total_employees"] == 100
    assert modules["hr"]["active_contracts"] == 95

    assert "production" in modules
    assert modules["production"]["daily_production"] == 1000
    assert modules["production"]["efficiency_rate"] == 0.92

    assert "finance" in modules
    assert modules["finance"]["daily_revenue"] == 50000
    assert modules["finance"]["monthly_expenses"] == 40000

    assert "inventory" in modules
    assert modules["inventory"]["total_items"] == 500
    assert modules["inventory"]["total_value"] == 100000

    # Vérification des alertes (triées par priorité)
    alerts = dashboard_data["alerts"]
    assert len(alerts) == 3
    assert alerts[0]["type"] == "finance"  # Priorité 3
    assert alerts[1]["type"] == "hr"      # Priorité 2
    assert alerts[2]["type"] == "production"  # Priorité 1

    # Vérification des prédictions ML
    predictions = dashboard_data["predictions"]
    assert predictions["production"]["yield_prediction"] == 1200
    assert predictions["finance"]["revenue_prediction"] == 150000
    assert "stock_level_predictions" in predictions["inventory"]
    assert predictions["hr"]["turnover_prediction"] == 0.15

    # Vérification du timestamp
    assert "timestamp" in dashboard_data
    timestamp = datetime.fromisoformat(dashboard_data["timestamp"])
    assert isinstance(timestamp, datetime)

@pytest.mark.integration
async def test_tableau_bord_unified_cache(mock_ml_services, mock_ml_cache_data):
    """Test du cache du tableau de bord unifié"""
    # Configuration du mock de cache pour retourner des données
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
    mock_ml_services["finance"].get_daily_revenue.assert_not_called()
    mock_ml_services["inventory"].get_total_items.assert_not_called()

    # Configuration du cache pour simuler une expiration
    mock_ml_services["cache"].get.return_value = None

    # Deuxième appel - devrait régénérer les données
    data2 = await unified_service.get_unified_dashboard_data()
    assert data2 != mock_ml_cache_data

    # Vérification que les services ont été appelés
    mock_ml_services["hr"].get_total_employees.assert_called_once()
    mock_ml_services["production"].get_daily_production.assert_called_once()
    mock_ml_services["finance"].get_daily_revenue.assert_called_once()
    mock_ml_services["inventory"].get_total_items.assert_called_once()

@pytest.mark.integration
async def test_tableau_bord_unified_error_handling(mock_ml_services):
    """Test de la gestion des erreurs dans le tableau de bord unifié"""
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

    # Récupération des données avec un service en échec
    dashboard_data = await unified_service.get_unified_dashboard_data()

    # Vérification que le tableau de bord continue de fonctionner
    assert "modules" in dashboard_data
    assert "alerts" in dashboard_data
    assert "predictions" in dashboard_data
    assert dashboard_data["modules"]["hr"] == {}  # Module en échec retourne un dict vide
    assert len(dashboard_data["alerts"]) == 2  # Seulement les alertes des autres services

@pytest.mark.integration
async def test_tableau_bord_unified_refresh(mock_ml_services):
    """Test du rafraîchissement des données du tableau de bord"""
    unified_service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr"],
        production_service=mock_ml_services["production"],
        finance_service=mock_ml_services["finance"],
        inventory_service=mock_ml_services["inventory"],
        weather_service=mock_ml_services["weather"],
        projects_ml_service=mock_ml_services["projects_ml"],
        cache_service=mock_ml_services["cache"]
    )

    # Premier appel pour remplir le cache
    await unified_service.get_unified_dashboard_data()

    # Modification des données mockées
    mock_ml_services["production"].get_daily_production.return_value = 2000
    mock_ml_services["finance"].get_daily_revenue.return_value = 75000

    # Rafraîchissement forcé des données
    refreshed_data = await unified_service.refresh_dashboard_data()

    # Vérification des nouvelles valeurs
    assert refreshed_data["modules"]["production"]["daily_production"] == 2000
    assert refreshed_data["modules"]["finance"]["daily_revenue"] == 75000

    # Vérification que le cache a été mis à jour
    mock_ml_services["cache"].set.assert_called()
