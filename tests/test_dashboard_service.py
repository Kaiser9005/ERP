import pytest
from services.dashboard_service import DashboardService
from datetime import datetime, timedelta

def test_get_stats(db, test_user, test_data):
    """Test de récupération des statistiques globales"""
    service = DashboardService(db)
    stats = await service.get_stats()

    # Vérification de la structure
    assert "production" in stats
    assert "inventory" in stats
    assert "finance" in stats
    assert "hr" in stats

    # Vérification des statistiques de production
    production = stats["production"]
    assert "total" in production
    assert "variation" in production
    assert production["total"] > 0  # Dû aux récoltes de test
    assert isinstance(production["variation"]["value"], (int, float))
    assert production["variation"]["type"] in ["increase", "decrease"]

    # Vérification des statistiques d'inventaire
    inventory = stats["inventory"]
    assert "value" in inventory
    assert "variation" in inventory
    assert inventory["value"] > 0  # Dû au stock de test

def test_calculate_variation():
    """Test du calcul des variations"""
    service = DashboardService(None)  # Pas besoin de DB pour ce test

    # Test augmentation
    variation = service._calculate_variation(100, 50)
    assert variation["value"] == 100.0  # (100-50)/50 * 100
    assert variation["type"] == "increase"

    # Test diminution
    variation = service._calculate_variation(50, 100)
    assert variation["value"] == 50.0  # abs((50-100)/100 * 100)
    assert variation["type"] == "decrease"

    # Test valeur précédente nulle
    variation = service._calculate_variation(100, 0)
    assert variation["value"] == 0
    assert variation["type"] == "increase"

def test_production_stats(db, test_user, test_data):
    """Test spécifique des statistiques de production"""
    service = DashboardService(db)
    now = datetime.utcnow()
    last_month = now - timedelta(days=30)

    stats = await service._get_production_stats(now, last_month)
    assert "total" in stats
    assert "variation" in stats
    assert stats["total"] > 0  # Dû aux récoltes de test

def test_inventory_stats(db, test_user, test_data):
    """Test spécifique des statistiques d'inventaire"""
    service = DashboardService(db)
    stats = await service._get_inventory_stats()
    
    assert "value" in stats
    assert "variation" in stats
    assert stats["value"] == test_data["stock"].quantite * test_data["stock"].valeur_unitaire

def test_hr_stats(db, test_user, test_data):
    """Test spécifique des statistiques RH"""
    service = DashboardService(db)
    stats = await service._get_hr_stats()
    
    assert "activeEmployees" in stats
    assert "variation" in stats
    assert stats["activeEmployees"] >= 1  # Au moins l'utilisateur de test