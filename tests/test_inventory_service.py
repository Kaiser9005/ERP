import pytest
from datetime import datetime, timedelta
from services.inventory_service import InventoryService
from models.inventory import Produit, Stock, MouvementStock
from schemas.inventory import MouvementStockCreate

def test_get_stats(db, test_user, test_data):
    """Test de récupération des statistiques d'inventaire"""
    service = InventoryService(db)
    stats = await service.get_stats()

    assert "totalValue" in stats
    assert "turnoverRate" in stats
    assert "alerts" in stats
    assert "movements" in stats
    assert stats["totalValue"] > 0

def test_create_mouvement_entree(db, test_user, test_data):
    """Test de création d'un mouvement d'entrée"""
    service = InventoryService(db)
    
    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="ENTREE",
        quantite=100,
        entrepot_destination_id=test_data["entrepot"].id,
        cout_unitaire=1500
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None
    assert result.quantite == 100

    # Vérifier la mise à jour du stock
    stock = db.query(Stock).filter(
        Stock.produit_id == test_data["produit"].id,
        Stock.entrepot_id == test_data["entrepot"].id
    ).first()
    assert stock.quantite == 100
    assert stock.valeur_unitaire == 1500

def test_create_mouvement_sortie(db, test_user, test_data):
    """Test de création d'un mouvement de sortie"""
    service = InventoryService(db)
    
    # Créer un stock initial
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="SORTIE",
        quantite=50,
        entrepot_source_id=test_data["entrepot"].id
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None
    assert result.quantite == 50

    # Vérifier la mise à jour du stock
    db.refresh(stock)
    assert stock.quantite == 50

def test_create_mouvement_sortie_insuffisant(db, test_user, test_data):
    """Test de sortie avec stock insuffisant"""
    service = InventoryService(db)
    
    # Créer un stock initial
    stock = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=30,
        valeur_unitaire=1500
    )
    db.add(stock)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="SORTIE",
        quantite=50,
        entrepot_source_id=test_data["entrepot"].id
    )

    with pytest.raises(ValueError, match="Stock insuffisant"):
        await service.create_mouvement(mouvement, test_user.id)

def test_create_mouvement_transfert(db, test_user, test_data):
    """Test de création d'un mouvement de transfert"""
    service = InventoryService(db)
    
    # Créer un stock initial
    stock_source = Stock(
        produit_id=test_data["produit"].id,
        entrepot_id=test_data["entrepot"].id,
        quantite=100,
        valeur_unitaire=1500
    )
    db.add(stock_source)
    db.commit()

    # Créer un second entrepôt
    entrepot2 = Entrepot(
        code="E002",
        nom="Entrepôt 2",
        localisation="Zone B"
    )
    db.add(entrepot2)
    db.commit()

    mouvement = MouvementStockCreate(
        produit_id=test_data["produit"].id,
        type_mouvement="TRANSFERT",
        quantite=50,
        entrepot_source_id=test_data["entrepot"].id,
        entrepot_destination_id=entrepot2.id
    )

    result = await service.create_mouvement(mouvement, test_user.id)
    assert result.id is not None

    # Vérifier les stocks
    db.refresh(stock_source)
    assert stock_source.quantite == 50

    stock_dest = db.query(Stock).filter(
        Stock.produit_id == test_data["produit"].id,
        Stock.entrepot_id == entrepot2.id
    ).first()
    assert stock_dest.quantite == 50