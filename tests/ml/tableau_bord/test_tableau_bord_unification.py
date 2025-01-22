"""
Tests pour le service d'unification du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from services.ml.tableau_bord.unification import TableauBordUnifieService

@pytest.mark.asyncio
async def test_get_unified_dashboard_data(mock_ml_services):
    """Test de récupération des données unifiées du tableau de bord"""
    # Configuration des mocks
    cache_service = mock_ml_services["cache_service"]
    cache_service.get.return_value = None  # Pas de cache au premier appel
    
    service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr_service"],
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=cache_service
    )
    
    data = await service.get_unified_dashboard_data()

    # Vérifications de base
    assert isinstance(data, dict)
    assert "timestamp" in data
    assert "modules" in data
    assert "alerts" in data
    assert "predictions" in data

    # Vérification des modules
    modules = data["modules"]
    assert "hr" in modules
    assert "production" in modules
    assert "finance" in modules
    assert "inventory" in modules
    assert "weather" in modules
    assert "projets" in modules

    # Vérification du cache
    cache_service.get.assert_called_once()
    cache_service.set.assert_called_once()

@pytest.mark.asyncio
async def test_cache_behavior(mock_ml_services, mock_ml_cache_data):
    """Test du comportement du cache"""
    # Configuration des mocks
    cache_service = mock_ml_services["cache_service"]
    cache_service.get.return_value = mock_ml_cache_data

    service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr_service"],
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=cache_service
    )

    # Premier appel - devrait utiliser le cache
    data1 = await service.get_unified_dashboard_data()
    assert data1 == mock_ml_cache_data
    
    # Vérification que les services n'ont pas été appelés
    mock_ml_services["hr_service"].get_total_employees.assert_not_called()
    mock_ml_services["production_service"].get_daily_production.assert_not_called()

@pytest.mark.asyncio
async def test_get_hr_summary(mock_ml_services):
    """Test du résumé RH"""
    service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr_service"],
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=mock_ml_services["cache_service"]
    )

    summary = await service._get_hr_summary()
    assert "total_employees" in summary
    assert "active_contracts" in summary
    assert "completed_trainings" in summary
    assert "training_completion_rate" in summary
    assert "recent_activities" in summary

    # Vérification des appels
    mock_ml_services["hr_service"].get_total_employees.assert_called_once()
    mock_ml_services["hr_service"].get_active_contracts_count.assert_called_once()
    mock_ml_services["hr_service"].get_completed_trainings_count.assert_called_once()

@pytest.mark.asyncio
async def test_get_production_summary(mock_ml_services):
    """Test du résumé de production"""
    service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr_service"],
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=mock_ml_services["cache_service"]
    )

    summary = await service._get_production_summary()
    assert "daily_production" in summary
    assert "efficiency_rate" in summary
    assert "active_sensors" in summary
    assert "quality_metrics" in summary
    assert "recent_activities" in summary

@pytest.mark.asyncio
async def test_get_module_details_invalid_module(mock_ml_services):
    """Test de la gestion des erreurs pour un module invalide"""
    service = TableauBordUnifieService(
        hr_service=mock_ml_services["hr_service"],
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=mock_ml_services["cache_service"]
    )

    with pytest.raises(ValueError, match="Module inconnu"):
        await service.get_module_details("invalid_module")

@pytest.mark.asyncio
async def test_get_module_details_error_handling(mock_ml_services):
    """Test de la gestion des erreurs lors de la récupération des détails"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_detailed_analytics.side_effect = Exception("Erreur HR")

    service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=mock_ml_services["cache_service"]
    )

    with pytest.raises(Exception):
        await service.get_module_details("hr")

@pytest.mark.asyncio
async def test_unified_data_error_handling(mock_ml_services):
    """Test de la gestion des erreurs lors de la récupération des données unifiées"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_total_employees.side_effect = Exception("Erreur HR")

    service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=mock_ml_services["production_service"],
        finance_service=mock_ml_services["finance_service"],
        inventory_service=mock_ml_services["inventory_service"],
        weather_service=mock_ml_services["weather_service"],
        projets_ml=mock_ml_services["projets_ml"],
        cache_service=mock_ml_services["cache_service"]
    )

    # Le service devrait continuer à fonctionner même si un module échoue
    data = await service.get_unified_dashboard_data()
    assert "modules" in data
    assert "hr" in data["modules"]
    assert data["modules"]["hr"] == {}  # Module en échec retourne un dict vide
