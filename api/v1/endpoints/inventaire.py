from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.inventory import Produit, MouvementStock, Stock
from schemas.inventaire import (
    ProduitCreate, ProduitResponse,
    MouvementStockCreate, MouvementStockResponse,
    StockResponse
)

router = APIRouter()

@router.get("/produits", response_model=List[ProduitResponse])
def get_produits(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(Produit).offset(skip).limit(limit).all()

@router.post("/produits", response_model=ProduitResponse)
def create_produit(
    produit: ProduitCreate,
    db: Session = Depends(get_db)
):
    db_produit = Produit(**produit.dict())
    db.add(db_produit)
    db.commit()
    db.refresh(db_produit)
    return db_produit

@router.get("/stocks", response_model=List[StockResponse])
def get_stocks(
    entrepot_id: str = None,
    produit_id: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Stock)
    if entrepot_id:
        query = query.filter(Stock.entrepot_id == entrepot_id)
    if produit_id:
        query = query.filter(Stock.produit_id == produit_id)
    return query.all()

@router.post("/mouvements", response_model=MouvementStockResponse)
def create_mouvement(
    mouvement: MouvementStockCreate,
    db: Session = Depends(get_db)
):
    db_mouvement = MouvementStock(**mouvement.dict())
    db.add(db_mouvement)
    db.commit()
    db.refresh(db_mouvement)
    return db_mouvement