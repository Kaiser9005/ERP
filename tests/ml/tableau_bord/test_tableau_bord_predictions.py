"""
Tests pour le service de prédictions ML du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock

from services.ml.tableau_bord.predictions import get_ml_predictions

@pytest.mark.asyncio
async def test_get_ml_predictions():
    """Test de récupération des prédictions ML"""
    # Configuration des données de test
    production_predictions = {
        "yield_prediction": 1200,
        "quality_prediction": 0.95,
        "maintenance_prediction": ["Machine A", "Machine C"]
    }
    
    finance_predictions = {
        "revenue_prediction": 150000,
        "expense_prediction": 120000,
        "cash_flow_prediction": 30000
    }
    
    inventory_predictions = {
        "stock_level_predictions": {"item_1": 100, "item_2": 50},
        "reorder_suggestions": ["item_3", "item_4"],
        "optimal_quantities": {"item_1": 150, "item_2": 75}
    }
    
    hr_predictions = {
        "turnover_prediction": 0.15,
        "hiring_needs": ["Developer", "Manager"],
        "training_recommendations": ["Python", "Leadership"]
    }

    # Configuration du mock
    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = production_predictions
    projects_ml_service.get_finance_predictions.return_value = finance_predictions
    projects_ml_service.get_inventory_predictions.return_value = inventory_predictions
    projects_ml_service.get_hr_predictions.return_value = hr_predictions

    # Exécution
    predictions = await get_ml_predictions(projects_ml_service)

    # Vérifications
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions
    assert "hr" in predictions

    assert predictions["production"] == production_predictions
    assert predictions["finance"] == finance_predictions
    assert predictions["inventory"] == inventory_predictions
    assert predictions["hr"] == hr_predictions

    # Vérification des appels aux méthodes
    projects_ml_service.get_production_predictions.assert_called_once()
    projects_ml_service.get_finance_predictions.assert_called_once()
    projects_ml_service.get_inventory_predictions.assert_called_once()
    projects_ml_service.get_hr_predictions.assert_called_once()

@pytest.mark.asyncio
async def test_get_ml_predictions_error_handling():
    """Test de la gestion des erreurs lors de la récupération des prédictions"""
    # Configuration du mock avec une méthode qui échoue
    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.side_effect = Exception("Erreur ML Production")
    projects_ml_service.get_finance_predictions.return_value = {}
    projects_ml_service.get_inventory_predictions.return_value = {}
    projects_ml_service.get_hr_predictions.return_value = {}

    # Exécution
    predictions = await get_ml_predictions(projects_ml_service)

    # Vérifications
    assert "production" in predictions
    assert predictions["production"] == {}  # Module en échec retourne un dict vide
    assert "finance" in predictions
    assert "inventory" in predictions
    assert "hr" in predictions

@pytest.mark.asyncio
async def test_get_ml_predictions_empty_results():
    """Test avec des prédictions vides"""
    # Configuration du mock pour retourner des résultats vides
    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = {}
    projects_ml_service.get_finance_predictions.return_value = {}
    projects_ml_service.get_inventory_predictions.return_value = {}
    projects_ml_service.get_hr_predictions.return_value = {}

    # Exécution
    predictions = await get_ml_predictions(projects_ml_service)

    # Vérifications
    assert all(isinstance(predictions[module], dict) for module in predictions)
    assert all(len(predictions[module]) == 0 for module in predictions)

@pytest.mark.asyncio
async def test_get_ml_predictions_partial_results():
    """Test avec certains modules retournant des résultats partiels"""
    # Configuration du mock avec des résultats partiels
    projects_ml_service = AsyncMock()
    projects_ml_service.get_production_predictions.return_value = {
        "yield_prediction": 1200  # Seulement une métrique
    }
    projects_ml_service.get_finance_predictions.return_value = {
        "revenue_prediction": 150000,
        "expense_prediction": 120000  # Manque cash_flow_prediction
    }
    projects_ml_service.get_inventory_predictions.return_value = {}  # Aucune prédiction
    projects_ml_service.get_hr_predictions.return_value = {
        "turnover_prediction": 0.15
    }

    # Exécution
    predictions = await get_ml_predictions(projects_ml_service)

    # Vérifications
    assert len(predictions["production"]) == 1
    assert len(predictions["finance"]) == 2
    assert len(predictions["inventory"]) == 0
    assert len(predictions["hr"]) == 1

    # Vérification des valeurs partielles
    assert predictions["production"]["yield_prediction"] == 1200
    assert predictions["finance"]["revenue_prediction"] == 150000
    assert predictions["finance"]["expense_prediction"] == 120000
    assert predictions["hr"]["turnover_prediction"] == 0.15
