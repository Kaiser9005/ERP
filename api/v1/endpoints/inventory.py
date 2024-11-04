from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from models.auth import Utilisateur
from models.inventory import Produit, MouvementStock, Stock, Entrepot
from schemas.inventory import (
    ProduitCreate, ProduitResponse,
    MouvementStockCreate, MouvementStockResponse,
    StockResponse, EntrepotCreate, EntrepotResponse
)
from api.v1.endpoints.auth import get_current_user
from services.inventory_service import InventoryService

router = APIRouter()

@router.get("/stats")
async def get_inventory_stats(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les statistiques d'inventaire"""
    inventory_service = InventoryService(db)
    return await inventory_service.get_stats()

@router.get("/produits", response_model=List[ProduitResponse])
async def get_produits(
    categorie: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des produits"""
    query = db.query(Produit)
    if categorie:
        query = query.filter(Produit.categorie == categorie)
    return query.offset(skip).limit(limit).all()

@router.post("/produits", response_model=ProduitResponse)
async def create_produit(
    produit: ProduitCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau produit"""
    db_produit = Produit(**produit.dict())
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

@router.get("/stocks", response_model=List[StockResponse])
async def get_stocks(
    entrepot_id: Optional[str] = None,
    produit_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère l'état des stocks"""
    query = db.query(Stock)
    if entrepot_id:
        query = query.filter(Stock.entrepot_id == entrepot_id)
    if produit_id:
        query = query.filter(Stock.produit_id == produit_id)
    return query.all()

@router.post("/mouvements", response_model=MouvementStockResponse)
async def create_mouvement(
    mouvement: MouvementStockCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Enregistre un mouvement de stock"""
    inventory_service = InventoryService(db)
    return await inventory_service.create_mouvement(mouvement, current_user.id)

@router.get("/entrepots", response_model=List[EntrepotResponse])
async def get_entrepots(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des entrepôts"""
    return db.query(Entrepot).all()

@router.post("/entrepots", response_model=EntrepotResponse)
async def create_entrepot(
    entrepot: EntrepotCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouvel entrepôt"""
    db_entrepot = Entrepot(**entrepot.dict())
    db.add(db_entrepot)
    db.commit()
    db.refresh(db_entrepot)
    return db_entrepot