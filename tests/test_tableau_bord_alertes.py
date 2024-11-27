"""
Tests pour le service d'alertes du tableau de bord.
"""

import pytest
from unittest.mock import AsyncMock

from services.ml.tableau_bord.alertes import get_critical_alerts

@pytest.mark.asyncio
async def test_get_critical_alerts():
    """Test de récupération et tri des alertes critiques"""
    # Configuration des mocks avec différentes priorités
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = [
        {"type": "hr", "message": "Alerte RH", "priority": 2}
    ]

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = [
        {"type": "production", "message": "Alerte Production", "priority": 1}
    ]

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = [
        {"type": "finance", "message": "Alerte Finance", "priority": 3}
    ]

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = [
        {"type": "inventory", "message": "Alerte Stock", "priority": 1}
    ]

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = [
        {"type": "weather", "message": "Alerte Météo", "priority": 2}
    ]

    # Exécution
    alerts = await get_critical_alerts(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service
    )

    # Vérifications
    assert len(alerts) == 5  # Une alerte de chaque service
    
    # Vérification du tri par priorité (ordre décroissant)
    priorities = [alert["priority"] for alert in alerts]
    assert priorities == sorted(priorities, reverse=True)
    
    # Vérification que la première alerte est celle de plus haute priorité
    assert alerts[0]["type"] == "finance"  # Priorité 3
    
    # Vérification des appels aux services
    hr_service.get_critical_alerts.assert_called_once()
    production_service.get_critical_alerts.assert_called_once()
    finance_service.get_critical_alerts.assert_called_once()
    inventory_service.get_critical_alerts.assert_called_once()
    weather_service.get_critical_alerts.assert_called_once()

@pytest.mark.asyncio
async def test_get_critical_alerts_empty():
    """Test avec aucune alerte"""
    # Configuration des mocks pour retourner des listes vides
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = []

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = []

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = []

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = []

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = []

    # Exécution
    alerts = await get_critical_alerts(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service
    )

    # Vérifications
    assert len(alerts) == 0
    assert isinstance(alerts, list)

@pytest.mark.asyncio
async def test_get_critical_alerts_error_handling():
    """Test de la gestion des erreurs"""
    # Configuration d'un service qui échoue
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.side_effect = Exception("Erreur HR")

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = [
        {"type": "production", "message": "Alerte Production", "priority": 1}
    ]

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = [
        {"type": "finance", "message": "Alerte Finance", "priority": 2}
    ]

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = [
        {"type": "inventory", "message": "Alerte Stock", "priority": 1}
    ]

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = [
        {"type": "weather", "message": "Alerte Météo", "priority": 2}
    ]

    # Exécution
    alerts = await get_critical_alerts(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service
    )

    # Vérifications
    assert len(alerts) == 4  # Les alertes des services fonctionnels
    assert all(alert["type"] != "hr" for alert in alerts)  # Pas d'alertes HR

@pytest.mark.asyncio
async def test_get_critical_alerts_priority_validation():
    """Test de la validation des priorités"""
    # Configuration avec des priorités invalides ou manquantes
    hr_service = AsyncMock()
    hr_service.get_critical_alerts.return_value = [
        {"type": "hr", "message": "Alerte sans priorité"}  # Priorité manquante
    ]

    production_service = AsyncMock()
    production_service.get_critical_alerts.return_value = [
        {"type": "production", "message": "Alerte Production", "priority": "haute"}  # Priorité non numérique
    ]

    finance_service = AsyncMock()
    finance_service.get_critical_alerts.return_value = [
        {"type": "finance", "message": "Alerte Finance", "priority": 1}  # Priorité valide
    ]

    inventory_service = AsyncMock()
    inventory_service.get_critical_alerts.return_value = []

    weather_service = AsyncMock()
    weather_service.get_critical_alerts.return_value = []

    # Exécution
    alerts = await get_critical_alerts(
        hr_service=hr_service,
        production_service=production_service,
        finance_service=finance_service,
        inventory_service=inventory_service,
        weather_service=weather_service
    )

    # Vérifications
    assert len(alerts) > 0
    # Les alertes avec priorités invalides devraient avoir une priorité par défaut de 0
    assert all(isinstance(alert.get("priority", 0), (int, float)) for alert in alerts)
