"""
Tests pour le service de prédictions ML du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock

from services.ml.tableau_bord.predictions import get_ml_predictions, TableauBordPredictionsService

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

    # Configuration des mocks
    db = MagicMock()
    production_ml = AsyncMock()
    inventory_ml = AsyncMock()
    finance_service = AsyncMock()
    comptabilite_service = AsyncMock()
    projets_ml = AsyncMock()
    hr_analytics = AsyncMock()
    finance_comptabilite = AsyncMock()
    cache_service = AsyncMock()
    cache_service.get.return_value = None

    # Configuration des retours
    projets_ml._get_production_predictions = AsyncMock(return_value=production_predictions)
    projets_ml._get_finance_predictions = AsyncMock(return_value=finance_predictions)
    projets_ml._get_inventory_predictions = AsyncMock(return_value=inventory_predictions)
    projets_ml._get_hr_predictions = AsyncMock(return_value=hr_predictions)

    # Exécution
    service = TableauBordPredictionsService(
        db=db,
        production_ml=production_ml,
        inventory_ml=inventory_ml,
        finance_service=finance_service,
        comptabilite_service=comptabilite_service,
        projets_ml=projets_ml,
        hr_analytics=hr_analytics,
        finance_comptabilite=finance_comptabilite,
        cache_service=cache_service
    )
    predictions = await service.get_ml_predictions()

    # Vérifications
    assert "production" in predictions
    assert "finance" in predictions
    assert "inventory" in predictions
    assert "hr" in predictions

    assert predictions["production"] == production_predictions
    assert predictions["finance"] == finance_predictions
    assert predictions["inventory"] == inventory_predictions
    assert predictions["hr"] == hr_predictions

@pytest.mark.asyncio
async def test_get_ml_predictions_error_handling():
    """Test de la gestion des erreurs lors de la récupération des prédictions"""
    # Configuration du mock avec une méthode qui échoue
    projets_ml = AsyncMock()
    projets_ml._get_production_predictions = AsyncMock(side_effect=Exception("Erreur ML Production"))
    projets_ml._get_finance_predictions = AsyncMock(return_value={})
    projets_ml._get_inventory_predictions = AsyncMock(return_value={})
    projets_ml._get_hr_predictions = AsyncMock(return_value={})

    cache_service = AsyncMock()
    cache_service.get.return_value = None

    # Exécution
    service = TableauBordPredictionsService(
        db=MagicMock(),
        production_ml=AsyncMock(),
        inventory_ml=AsyncMock(),
        finance_service=AsyncMock(),
        comptabilite_service=AsyncMock(),
        projets_ml=projets_ml,
        hr_analytics=AsyncMock(),
        finance_comptabilite=AsyncMock(),
        cache_service=cache_service
    )
    predictions = await service.get_ml_predictions()

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
    projets_ml = AsyncMock()
    projets_ml._get_production_predictions = AsyncMock(return_value={})
    projets_ml._get_finance_predictions = AsyncMock(return_value={})
    projets_ml._get_inventory_predictions = AsyncMock(return_value={})
    projets_ml._get_hr_predictions = AsyncMock(return_value={})

    cache_service = AsyncMock()
    cache_service.get.return_value = None

    # Exécution
    service = TableauBordPredictionsService(
        db=MagicMock(),
        production_ml=AsyncMock(),
        inventory_ml=AsyncMock(),
        finance_service=AsyncMock(),
        comptabilite_service=AsyncMock(),
        projets_ml=projets_ml,
        hr_analytics=AsyncMock(),
        finance_comptabilite=AsyncMock(),
        cache_service=cache_service
    )
    predictions = await service.get_ml_predictions()

    # Vérifications
    assert all(isinstance(predictions[module], dict) for module in predictions)
    assert all(len(predictions[module]) == 0 for module in predictions)

@pytest.mark.asyncio
async def test_get_ml_predictions_partial_results():
    """Test avec certains modules retournant des résultats partiels"""
    # Configuration du mock avec des résultats partiels
    projets_ml = AsyncMock()
    projets_ml._get_production_predictions = AsyncMock(return_value={
        "yield_prediction": 1200  # Seulement une métrique
    })
    projets_ml._get_finance_predictions = AsyncMock(return_value={
        "revenue_prediction": 150000,
        "expense_prediction": 120000  # Manque cash_flow_prediction
    })
    projets_ml._get_inventory_predictions = AsyncMock(return_value={})  # Aucune prédiction
    projets_ml._get_hr_predictions = AsyncMock(return_value={
        "turnover_prediction": 0.15
    })

    cache_service = AsyncMock()
    cache_service.get.return_value = None

    # Exécution
    service = TableauBordPredictionsService(
        db=MagicMock(),
        production_ml=AsyncMock(),
        inventory_ml=AsyncMock(),
        finance_service=AsyncMock(),
        comptabilite_service=AsyncMock(),
        projets_ml=projets_ml,
        hr_analytics=AsyncMock(),
        finance_comptabilite=AsyncMock(),
        cache_service=cache_service
    )
    predictions = await service.get_ml_predictions()

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

@pytest.mark.asyncio
async def test_get_ml_predictions_with_cache():
    """Test de l'utilisation du cache"""
    # Configuration des mocks
    projets_ml = AsyncMock()
    cache_service = AsyncMock()
    
    # Configuration du cache pour retourner des données
    cached_data = {
        "production": {"cached": True},
        "finance": {"cached": True},
        "inventory": {"cached": True},
        "hr": {"cached": True}
    }
    cache_service.get.return_value = cached_data

    # Exécution
    service = TableauBordPredictionsService(
        db=MagicMock(),
        production_ml=AsyncMock(),
        inventory_ml=AsyncMock(),
        finance_service=AsyncMock(),
        comptabilite_service=AsyncMock(),
        projets_ml=projets_ml,
        hr_analytics=AsyncMock(),
        finance_comptabilite=AsyncMock(),
        cache_service=cache_service
    )
    predictions = await service.get_ml_predictions()

    # Vérifications
    assert predictions == cached_data
    cache_service.get.assert_called_once()
    assert not hasattr(projets_ml, '_get_production_predictions_called')
    assert not hasattr(projets_ml, '_get_finance_predictions_called')
    assert not hasattr(projets_ml, '_get_inventory_predictions_called')
    assert not hasattr(projets_ml, '_get_hr_predictions_called')
