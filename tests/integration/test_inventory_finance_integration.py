"""Tests d'intégration Inventaire-Finance."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from models.inventory import Produit, Stock, MouvementStock
from models.finance import Transaction, CoutStockage
from services.inventory_service import InventoryService
from services.finance_service import FinanceService
from schemas.inventaire import MouvementStockCreate
from schemas.finance import TransactionCreate

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test."""
    # Création d'un produit de test
    produit = Produit(
        code="P001",
        nom="Huile de Palme",
        type="RECOLTE",
        unite="litres",
        cout_stockage_unitaire=10.0,
        conditions_stockage={
            "temperature_min": 15,
            "temperature_max": 25,
            "humidite_min": 30,
            "humidite_max": 60
        }
    )
    test_session.add(produit)

    # Création d'un entrepôt de test
    entrepot = Stock(
        code="E001",
        nom="Entrepôt Principal",
        capacite=10000,
        cout_maintenance_mensuel=1000.0
    )
    test_session.add(entrepot)

    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(Transaction).delete()
    test_session.query(CoutStockage).delete()
    test_session.query(MouvementStock).delete()
    test_session.query(Stock).delete()
    test_session.query(Produit).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_stock_movement_financial_impact(test_db: Session):
    """Test de l'impact financier des mouvements de stock."""
    inventory_service = InventoryService(test_db)
    finance_service = FinanceService(test_db)
    
    # 1. Création d'un mouvement d'entrée en stock
    mouvement = await inventory_service.create_mouvement(
        MouvementStockCreate(
            type_mouvement="ENTREE",
            produit_id=test_db.query(Produit).first().id,
            entrepot_destination_id=test_db.query(Stock).first().id,
            quantite=1000,
            cout_unitaire=15.0
        ),
        "SYSTEM"
    )
    
    # 2. Vérification de la création de la transaction financière
    transactions = await finance_service.get_transactions(
        type_transaction="STOCK",
        reference_id=mouvement.id
    )
    assert len(transactions) == 1
    assert transactions[0].montant == 15000.0  # 1000 * 15.0

@pytest.mark.asyncio
async def test_storage_cost_calculation(test_db: Session):
    """Test du calcul des coûts de stockage."""
    inventory_service = InventoryService(test_db)
    finance_service = FinanceService(test_db)
    
    # 1. Création de plusieurs mouvements
    for quantite in [500, 300, -200]:
        await inventory_service.create_mouvement(
            MouvementStockCreate(
                type_mouvement="ENTREE" if quantite > 0 else "SORTIE",
                produit_id=test_db.query(Produit).first().id,
                entrepot_destination_id=test_db.query(Stock).first().id if quantite > 0 else None,
                entrepot_source_id=test_db.query(Stock).first().id if quantite < 0 else None,
                quantite=abs(quantite),
                cout_unitaire=15.0
            ),
            "SYSTEM"
        )

    # 2. Calcul des coûts de stockage mensuels
    couts = await finance_service.calculate_storage_costs(
        datetime.utcnow().replace(day=1),
        datetime.utcnow().replace(day=1) + timedelta(days=32)
    )
    
    assert len(couts) > 0
    assert couts[0].cout_total > 0

@pytest.mark.asyncio
async def test_inventory_valuation(test_db: Session):
    """Test de la valorisation des stocks."""
    inventory_service = InventoryService(test_db)
    finance_service = FinanceService(test_db)
    
    # 1. Création de mouvements avec différents coûts
    mouvements = [
        (500, 15.0),  # Entrée à 15.0
        (300, 16.0),  # Entrée à 16.0
        (-200, None)  # Sortie (FIFO)
    ]
    
    for quantite, cout in mouvements:
        await inventory_service.create_mouvement(
            MouvementStockCreate(
                type_mouvement="ENTREE" if quantite > 0 else "SORTIE",
                produit_id=test_db.query(Produit).first().id,
                entrepot_destination_id=test_db.query(Stock).first().id if quantite > 0 else None,
                entrepot_source_id=test_db.query(Stock).first().id if quantite < 0 else None,
                quantite=abs(quantite),
                cout_unitaire=cout
            ),
            "SYSTEM"
        )

    # 2. Calcul de la valeur du stock
    valeur = await finance_service.calculate_inventory_value(
        test_db.query(Stock).first().id
    )
    
    # Vérification de la valeur (FIFO)
    # Reste: 300 unités à 15.0 + 300 unités à 16.0
    expected_value = (300 * 15.0) + (300 * 16.0)
    assert valeur == expected_value

@pytest.mark.asyncio
async def test_maintenance_cost_allocation(test_db: Session):
    """Test de l'allocation des coûts de maintenance."""
    inventory_service = InventoryService(test_db)
    finance_service = FinanceService(test_db)
    
    # 1. Ajout de produits avec différentes occupations
    produits = [
        ("P002", "Produit 2", 2000),  # 40% de l'espace
        ("P003", "Produit 3", 3000)   # 60% de l'espace
    ]
    
    for code, nom, quantite in produits:
        produit = Produit(
            code=code,
            nom=nom,
            type="RECOLTE",
            unite="litres"
        )
        test_db.add(produit)
        test_db.commit()
        
        await inventory_service.create_mouvement(
            MouvementStockCreate(
                type_mouvement="ENTREE",
                produit_id=produit.id,
                entrepot_destination_id=test_db.query(Stock).first().id,
                quantite=quantite
            ),
            "SYSTEM"
        )

    # 2. Calcul de l'allocation des coûts
    allocations = await finance_service.allocate_maintenance_costs(
        test_db.query(Stock).first().id,
        datetime.utcnow().replace(day=1)
    )
    
    assert len(allocations) == 3  # 3 produits
    # Vérification des proportions
    total_cost = sum(a.cout_alloue for a in allocations)
    assert total_cost == test_db.query(Stock).first().cout_maintenance_mensuel

@pytest.mark.asyncio
async def test_stock_alerts_financial_impact(test_db: Session):
    """Test de l'impact financier des alertes de stock."""
    inventory_service = InventoryService(test_db)
    finance_service = FinanceService(test_db)
    
    # 1. Création d'un stock proche du minimum
    await inventory_service.create_mouvement(
        MouvementStockCreate(
            type_mouvement="ENTREE",
            produit_id=test_db.query(Produit).first().id,
            entrepot_destination_id=test_db.query(Stock).first().id,
            quantite=100,  # Quantité faible
            cout_unitaire=15.0
        ),
        "SYSTEM"
    )

    # 2. Génération des recommandations de réapprovisionnement
    recommendations = await finance_service.get_restock_recommendations(
        test_db.query(Stock).first().id
    )
    
    assert len(recommendations) > 0
    assert all(r.cout_estime > 0 for r in recommendations)
    assert all(r.economie_potentielle > 0 for r in recommendations)
