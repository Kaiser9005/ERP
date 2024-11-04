import pytest
from datetime import datetime
from sqlalchemy.orm import Session
from services.inventory_service import InventoryService
from models.inventory import Produit, Stock, MouvementStock, Entrepot
from models.inventory import CategoryProduit, UniteMesure, TypeMouvement

def test_get_inventory_stats(db: Session, test_user: dict):
    """Test de récupération des statistiques d'inventaire"""
    service = InventoryService(db)
    
    # Créer des données de test
    produit = Produit(
        code="PRD001",
        nom="Test Produit",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        seuil_alerte=100,
        prix_unitaire=1500
    )
    db.add(produit)
    db.commit()

    entrepot = Entrepot(
        code="ENT001",
        nom="Entrepôt Test",
        responsable_id=test_user.id
    )
    db.add(entrepot)
    db.commit()

    stock = Stock(
        produit_id=produit.id,
        entrepot_id=entrepot.id,
        quantite=500,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    stats = await service.get_stats()
    assert "totalValue" in stats
    assert "turnoverRate" in stats
    assert "alerts" in stats
    assert stats["totalValue"] == 750000  # 500 * 1500

def test_create_mouvement(db: Session, test_user: dict):
    """Test de création d'un mouvement de stock"""
    service = InventoryService(db)
    
    # Créer les données nécessaires
    produit = Produit(
        code="PRD002",
        nom="Test Produit 2",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        seuil_alerte=100,
        prix_unitaire=1500
    )
    db.add(produit)

    entrepot = Entrepot(
        code="ENT002",
        nom="Entrepôt Test 2",
        responsable_id=test_user.id
    )
    db.add(entrepot)
    db.commit()

    # Test entrée de stock
    mouvement_data = {
        "produit_id": str(produit.id),
        "type_mouvement": TypeMouvement.ENTREE,
        "quantite": 100,
        "entrepot_destination_id": str(entrepot.id),
        "cout_unitaire": 1500
    }

    mouvement = await service.create_mouvement(mouvement_data, test_user.id)
    assert mouvement.quantite == 100

    # Vérifier le stock
    stock = db.query(Stock).filter(
        Stock.produit_id == produit.id,
        Stock.entrepot_id == entrepot.id
    ).first()
    assert stock.quantite == 100
    assert stock.valeur_unitaire == 1500

def test_handle_sortie(db: Session, test_user: dict):
    """Test de gestion d'une sortie de stock"""
    service = InventoryService(db)
    
    # Créer un stock initial
    produit = Produit(
        code="PRD003",
        nom="Test Produit 3",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        seuil_alerte=100,
        prix_unitaire=1500
    )
    db.add(produit)

    entrepot = Entrepot(
        code="ENT003",
        nom="Entrepôt Test 3",
        responsable_id=test_user.id
    )
    db.add(entrepot)

    stock = Stock(
        produit_id=produit.id,
        entrepot_id=entrepot.id,
        quantite=200,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    # Test sortie de stock
    mouvement_data = {
        "produit_id": str(produit.id),
        "type_mouvement": TypeMouvement.SORTIE,
        "quantite": 50,
        "entrepot_source_id": str(entrepot.id)
    }

    mouvement = await service.create_mouvement(mouvement_data, test_user.id)
    assert mouvement.quantite == 50

    # Vérifier le stock
    db.refresh(stock)
    assert stock.quantite == 150

def test_handle_transfert(db: Session, test_user: dict):
    """Test de gestion d'un transfert de stock"""
    service = InventoryService(db)
    
    # Créer les données nécessaires
    produit = Produit(
        code="PRD004",
        nom="Test Produit 4",
        categorie=CategoryProduit.INTRANT,
        unite_mesure=UniteMesure.KG,
        seuil_alerte=100,
        prix_unitaire=1500
    )
    db.add(produit)

    entrepot_source = Entrepot(
        code="ENT004",
        nom="Entrepôt Source",
        responsable_id=test_user.id
    )
    db.add(entrepot_source)

    entrepot_dest = Entrepot(
        code="ENT005",
        nom="Entrepôt Destination",
        responsable_id=test_user.id
    )
    db.add(entrepot_dest)

    stock_source = Stock(
        produit_id=produit.id,
        entrepot_id=entrepot_source.id,
        quantite=200,
        valeur_unitaire=1500
    )
    db.add(stock_source)
    db.commit()

    # Test transfert
    mouvement_data = {
        "produit_id": str(produit.id),
        "type_mouvement": TypeMouvement.TRANSFERT,
        "quantite": 75,
        "entrepot_source_id": str(entrepot_source.id),
        "entrepot_destination_id": str(entrepot_dest.id)
    }

    mouvement = await service.create_mouvement(mouvement_data, test_user.id)
    assert mouvement.quantite == 75

    # Vérifier les stocks
    db.refresh(stock_source)
    assert stock_source.quantite == 125

    stock_dest = db.query(Stock).filter(
        Stock.produit_id == produit.id,
        Stock.entrepot_id == entrepot_dest.id
    ).first()
    assert stock_dest.quantite == 75