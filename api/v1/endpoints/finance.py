from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from db.database import get_db
from models.auth import Utilisateur
from models.finance import Transaction, Compte, Budget
from schemas.finance import (
    TransactionCreate, TransactionUpdate, TransactionResponse,
    CompteCreate, CompteUpdate, CompteResponse,
    BudgetCreate, BudgetUpdate, BudgetResponse
)
from api.v1.endpoints.auth import get_current_user
from services.finance_service import FinanceService
from services.storage_service import StorageService

router = APIRouter()

@router.get("/stats")
async def get_finance_stats(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les statistiques financières"""
    finance_service = FinanceService(db)
    return await finance_service.get_stats()

@router.get("/transactions", response_model=List[TransactionResponse])
async def get_transactions(
    type: Optional[str] = None,
    statut: Optional[str] = None,
    date_debut: Optional[datetime] = None,
    date_fin: Optional[datetime] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des transactions"""
    query = db.query(Transaction)
    if type:
        query = query.filter(Transaction.type_transaction == type)
    if statut:
        query = query.filter(Transaction.statut == statut)
    if date_debut:
        query = query.filter(Transaction.date_transaction >= date_debut)
    if date_fin:
        query = query.filter(Transaction.date_transaction <= date_fin)
    return query.order_by(Transaction.date_transaction.desc()).offset(skip).limit(limit).all()

@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction: TransactionCreate,
    piece_jointe: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée une nouvelle transaction"""
    finance_service = FinanceService(db)
    
    # Gérer le fichier joint si présent
    if piece_jointe:
        storage = StorageService()
        file_path = await storage.save_file(
            piece_jointe,
            f"transactions/{datetime.now().year}/{datetime.now().month}"
        )
        transaction.piece_jointe = file_path
    
    return await finance_service.create_transaction(transaction)

@router.get("/comptes", response_model=List[CompteResponse])
async def get_comptes(
    type: Optional[str] = None,
    actif: bool = True,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des comptes"""
    query = db.query(Compte)
    if type:
        query = query.filter(Compte.type_compte == type)
    if actif is not None:
        query = query.filter(Compte.actif == actif)
    return query.all()

@router.post("/comptes", response_model=CompteResponse)
async def create_compte(
    compte: CompteCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau compte"""
    db_compte = Compte(**compte.dict())
    db.add(db_compte)
    db.commit()
    db.refresh(db_compte)
    return db_compte

@router.get("/budgets", response_model=List[BudgetResponse])
async def get_budgets(
    periode: Optional[str] = None,
    categorie: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des budgets"""
    query = db.query(Budget)
    if periode:
        query = query.filter(Budget.periode == periode)
    if categorie:
        query = query.filter(Budget.categorie == categorie)
    return query.all()

@router.post("/budgets", response_model=BudgetResponse)
async def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau budget"""
    db_budget = Budget(**budget.dict())
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget