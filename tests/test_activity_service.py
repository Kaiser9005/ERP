import pytest
from services.activity_service import ActivityService
from models.production import Recolte
from models.inventory import MouvementStock
from datetime import datetime, timedelta

def test_get_recent_activities(db, test_user, test_data):
    """Test de récupération des activités récentes"""
    service = ActivityService(db)
    
    # Test avec limite par défaut
    activities = await service.get_recent_activities()
    assert len(activities) <= 10  # Limite par défaut
    
    if len(activities) > 0:
        activity = activities[0]
        assert "id" in activity
        assert "type" in activity
        assert "title" in activity
        assert "description" in activity
        assert "date" in activity
        assert "color" in activity

    # Test avec limite personnalisée
    activities = await service.get_recent_activities(limit=5)
    assert len(activities) <= 5

    # Vérification du tri par date
    if len(activities) > 1:
        date1 = datetime.fromisoformat(activities[0]["date"])
        date2 = datetime.fromisoformat(activities[1]["date"])
        assert date1 >= date2  # Ordre décroissant

def test_activity_types(db, test_user, test_data):
    """Test des différents types d'activités"""
    service = ActivityService(db)
    activities = await service.get_recent_activities()

    # Vérification des types d'activités
    activity_types = set(activity["type"] for activity in activities)
    assert "PRODUCTION" in activity_types  # Dû aux récoltes de test
    assert "INVENTORY" in activity_types  # Dû aux mouvements de stock de test