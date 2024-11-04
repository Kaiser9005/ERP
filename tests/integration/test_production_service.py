import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.production_service import ProductionService
from models.production import Parcelle, CycleCulture, Recolte, CultureType, ParcelleStatus

def test_get_production_stats(db: Session, test_user: dict):
    """Test de récupération des statistiques de production"""
    service = ProductionService(db)
    
    # Créer des données de test
    parcelle = Parcelle(
        code="P001",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.5,
        date_plantation=datetime.now().date(),
        statut=ParcelleStatus.ACTIVE,
        responsable_id=test_user.id
    )
    db.add(parcelle)
    db.commit()

    # Créer des récoltes
    for i in range(3):
        recolte = Recolte(
            parcelle_id=parcelle.id,
            date_recolte=(datetime.now() - timedelta(days=i)).date(),
            quantite_kg=500 + i * 100,
            qualite="A",
            equipe_recolte=[str(test_user.id)]
        )
        db.add(recolte)
    db.commit()

    stats = await service.get_stats()
    assert "total" in stats
    assert "variation" in stats
    assert "parcelles_actives" in stats
    assert stats["total"] > 0

def test_create_parcelle(db: Session, test_user: dict):
    """Test de création d'une parcelle"""
    service = ProductionService(db)
    
    parcelle_data = {
        "code": "P002",
        "culture_type": CultureType.PALMIER,
        "surface_hectares": 15.0,
        "date_plantation": datetime.now().date(),
        "responsable_id": test_user.id
    }

    parcelle = await service.create_parcelle(parcelle_data)
    assert parcelle.code == "P002"
    assert parcelle.surface_hectares == 15.0
    assert parcelle.statut == ParcelleStatus.EN_PREPARATION

def test_create_cycle_culture(db: Session, test_user: dict):
    """Test de création d'un cycle de culture"""
    service = ProductionService(db)
    
    # Créer une parcelle
    parcelle = Parcelle(
        code="P003",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.0,
        date_plantation=datetime.now().date(),
        responsable_id=test_user.id
    )
    db.add(parcelle)
    db.commit()

    cycle_data = {
        "parcelle_id": str(parcelle.id),
        "date_debut": datetime.now().date(),
        "date_fin": (datetime.now() + timedelta(days=90)).date(),
        "rendement_prevu": 1500.0
    }

    cycle = await service.create_cycle_culture(cycle_data)
    assert cycle.parcelle_id == parcelle.id
    assert cycle.rendement_prevu == 1500.0

def test_create_recolte(db: Session, test_user: dict):
    """Test de création d'une récolte"""
    service = ProductionService(db)
    
    # Créer une parcelle
    parcelle = Parcelle(
        code="P004",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.0,
        date_plantation=datetime.now().date(),
        responsable_id=test_user.id
    )
    db.add(parcelle)
    db.commit()

    recolte_data = {
        "parcelle_id": str(parcelle.id),
        "date_recolte": datetime.now().date(),
        "quantite_kg": 750.0,
        "qualite": "A",
        "equipe_recolte": [str(test_user.id)],
        "conditions_meteo": {
            "temperature": 25,
            "humidite": 80
        }
    }

    recolte = await service.create_recolte(recolte_data)
    assert recolte.parcelle_id == parcelle.id
    assert recolte.quantite_kg == 750.0
    assert recolte.qualite == "A"

def test_get_parcelle_stats(db: Session, test_user: dict):
    """Test de récupération des statistiques d'une parcelle"""
    service = ProductionService(db)
    
    # Créer une parcelle avec des récoltes
    parcelle = Parcelle(
        code="P005",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.0,
        date_plantation=datetime.now().date(),
        responsable_id=test_user.id
    )
    db.add(parcelle)
    db.commit()

    # Ajouter des récoltes
    for i in range(3):
        recolte = Recolte(
            parcelle_id=parcelle.id,
            date_recolte=(datetime.now() - timedelta(days=i)).date(),
            quantite_kg=500.0,
            qualite="A",
            equipe_recolte=[str(test_user.id)]
        )
        db.add(recolte)
    db.commit()

    stats = await service.get_parcelle_stats(str(parcelle.id))
    assert "total_recolte" in stats
    assert "rendement" in stats
    assert stats["total_recolte"] == 1500.0  # 3 * 500kg