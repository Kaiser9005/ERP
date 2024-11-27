"""
Tests pour le service d'unification du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta

from services.ml.tableau_bord.unification import TableauBordUnifieService

@pytest.mark.asyncio
async def test_get_unified_dashboard_data(test_data):
    """Test de récupération des données unifiées du tableau de bord"""
    # Configuration des mocks
    cache_service = AsyncMock()
    cache_service.get.return_value = None  # Pas de cache au premier appel
    
    service = TableauBordUnifieService(
        hr_service=test_data["hr_service"],
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
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
    assert "projects" in modules

    # Vérification du cache
    cache_service.get.assert_called_once()
    cache_service.set.assert_called_once()

@pytest.mark.asyncio
async def test_cache_behavior(test_data):
    """Test du comportement du cache"""
    # Configuration des mocks
    cache_service = AsyncMock()
    cached_data = {
        "timestamp": datetime.now().isoformat(),
        "modules": {},
        "alerts": [],
        "predictions": {}
    }
    cache_service.get.return_value = cached_data

    service = TableauBordUnifieService(
        hr_service=test_data["hr_service"],
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=cache_service
    )

    # Premier appel - devrait utiliser le cache
    data1 = await service.get_unified_dashboard_data()
    assert data1 == cached_data
    
    # Vérification que les services n'ont pas été appelés
    test_data["hr_service"].get_total_employees.assert_not_called()
    test_data["production_service"].get_daily_production.assert_not_called()

@pytest.mark.asyncio
async def test_get_hr_summary(test_data):
    """Test du résumé RH"""
    service = TableauBordUnifieService(
        hr_service=test_data["hr_service"],
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=AsyncMock()
    )

    summary = await service._get_hr_summary()
    assert "total_employees" in summary
    assert "active_contracts" in summary
    assert "completed_trainings" in summary
    assert "training_completion_rate" in summary
    assert "recent_activities" in summary

    # Vérification des appels
    test_data["hr_service"].get_total_employees.assert_called_once()
    test_data["hr_service"].get_active_contracts_count.assert_called_once()
    test_data["hr_service"].get_completed_trainings_count.assert_called_once()

@pytest.mark.asyncio
async def test_get_production_summary(test_data):
    """Test du résumé de production"""
    service = TableauBordUnifieService(
        hr_service=test_data["hr_service"],
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=AsyncMock()
    )

    summary = await service._get_production_summary()
    assert "daily_production" in summary
    assert "efficiency_rate" in summary
    assert "active_sensors" in summary
    assert "quality_metrics" in summary
    assert "recent_activities" in summary

@pytest.mark.asyncio
async def test_get_module_details_invalid_module(test_data):
    """Test de la gestion des erreurs pour un module invalide"""
    service = TableauBordUnifieService(
        hr_service=test_data["hr_service"],
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=AsyncMock()
    )

    with pytest.raises(ValueError, match="Module inconnu"):
        await service.get_module_details("invalid_module")

@pytest.mark.asyncio
async def test_get_module_details_error_handling(test_data):
    """Test de la gestion des erreurs lors de la récupération des détails"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_detailed_analytics.side_effect = Exception("Erreur HR")

    service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=AsyncMock()
    )

    with pytest.raises(Exception):
        await service.get_module_details("hr")

@pytest.mark.asyncio
async def test_unified_data_error_handling(test_data):
    """Test de la gestion des erreurs lors de la récupération des données unifiées"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_total_employees.side_effect = Exception("Erreur HR")

    service = TableauBordUnifieService(
        hr_service=hr_service,
        production_service=test_data["production_service"],
        finance_service=test_data["finance_service"],
        inventory_service=test_data["inventory_service"],
        weather_service=test_data["weather_service"],
        projects_ml_service=test_data["projects_ml_service"],
        cache_service=AsyncMock()
    )

    # Le service devrait continuer à fonctionner même si un module échoue
    data = await service.get_unified_dashboard_data()
    assert "modules" in data
    assert "hr" in data["modules"]
    assert data["modules"]["hr"] == {}  # Module en échec retourne un dict vide
