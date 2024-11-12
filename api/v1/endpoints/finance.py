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
    finance_service = FinanceService(db)
    return await finance_service.get_budgets(periode)

@router.post("/budgets", response_model=BudgetResponse)
async def create_budget(
    budget: BudgetCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau budget"""
    finance_service = FinanceService(db)
    return await finance_service.create_budget(budget)

@router.put("/budgets/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: str,
    budget_update: BudgetUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Met à jour un budget existant"""
    try:
        finance_service = FinanceService(db)
        return await finance_service.update_budget(budget_id, budget_update)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Nouvelles routes pour l'analyse budgétaire et les projections

@router.get("/budgets/analysis/{periode}")
async def get_budget_analysis(
    periode: str,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère l'analyse budgétaire détaillée pour une période"""
    finance_service = FinanceService(db)
    return await finance_service.get_budget_analysis(periode)

@router.get("/projections")
async def get_financial_projections(
    months_ahead: Optional[int] = 3,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les projections financières avec impact météo"""
    finance_service = FinanceService(db)
    return await finance_service.get_financial_projections(months_ahead)

# Documentation Swagger

@router.get("/docs/models")
def get_models_doc():
    """Documentation des modèles de données finance"""
    return {
        "Transaction": {
            "description": "Représente une transaction financière",
            "fields": {
                "reference": "Référence unique de la transaction",
                "date_transaction": "Date et heure de la transaction",
                "type_transaction": "Type (RECETTE, DEPENSE, VIREMENT)",
                "categorie": "Catégorie (VENTE, ACHAT_INTRANT, etc.)",
                "montant": "Montant de la transaction",
                "devise": "Devise (défaut: XAF)",
                "description": "Description détaillée",
                "statut": "Statut (EN_ATTENTE, VALIDEE, etc.)",
                "piece_jointe": "Chemin vers le document justificatif"
            }
        },
        "Budget": {
            "description": "Représente un budget par catégorie et période",
            "fields": {
                "periode": "Période au format YYYY-MM",
                "categorie": "Catégorie budgétaire",
                "montant_prevu": "Montant budgété",
                "montant_realise": "Montant effectivement réalisé",
                "notes": "Notes et commentaires",
                "metadata": "Données supplémentaires"
            }
        }
    }

@router.get("/docs/endpoints")
def get_endpoints_doc():
    """Documentation des endpoints finance"""
    return {
        "/transactions": {
            "POST": "Crée une nouvelle transaction avec pièce jointe optionnelle",
            "GET": "Liste les transactions avec filtres"
        },
        "/stats": {
            "GET": "Statistiques financières globales"
        },
        "/budgets": {
            "POST": "Crée un nouveau budget",
            "GET": "Liste les budgets par période"
        },
        "/budgets/{id}": {
            "PUT": "Met à jour un budget existant"
        },
        "/budgets/analysis/{periode}": {
            "GET": "Analyse détaillée du budget avec impact météo"
        },
        "/projections": {
            "GET": "Projections financières avec impact météo"
        }
    }
