from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import date
from uuid import UUID

from db.database import get_db
from services.comptabilite_service import ComptabiliteService
from schemas.comptabilite import (
    CompteComptableCreate, CompteComptableUpdate, CompteComptableResponse,
    EcritureComptableCreate, EcritureComptableUpdate, EcritureComptableResponse,
    JournalComptableCreate, JournalComptableResponse,
    ExerciceComptableCreate, ExerciceComptableResponse,
    LigneGrandLivre, CompteBalance, BilanResponse, CompteResultatResponse
)

router = APIRouter(prefix="/comptabilite", tags=["comptabilite"])

# [Garder tous les endpoints existants jusqu'à get_compte_resultat]

# Nouveaux endpoints pour les statistiques et analyses
@router.get("/stats")
async def get_stats(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Récupère les statistiques financières"""
    service = ComptabiliteService(db)
    try:
        return await service.get_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/budget/analysis")
async def get_budget_analysis(
    periode: str = Query(..., description="Période d'analyse (format: YYYY-MM)"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Analyse détaillée du budget pour une période"""
    service = ComptabiliteService(db)
    try:
        return await service.get_budget_analysis(periode)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/cashflow")
async def get_cashflow(
    days: int = Query(30, description="Nombre de jours d'historique", ge=1, le=365),
    db: Session = Depends(get_db)
) -> List[Dict[str, Any]]:
    """Récupère les données de trésorerie sur une période"""
    service = ComptabiliteService(db)
    try:
        return await service.get_cashflow(days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoints pour les comptes comptables
@router.post("/comptes", response_model=CompteComptableResponse)
async def create_compte(
    compte: CompteComptableCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau compte comptable"""
    service = ComptabiliteService(db)
    return await service.create_compte(compte.dict())

@router.get("/comptes", response_model=List[CompteComptableResponse])
async def list_comptes(
    type_compte: Optional[str] = None,
    actif: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Liste les comptes comptables avec filtres optionnels"""
    service = ComptabiliteService(db)
    return await service.get_comptes(type_compte=type_compte, actif=actif)

@router.get("/comptes/{compte_id}", response_model=CompteComptableResponse)
async def get_compte(
    compte_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupère les détails d'un compte comptable"""
    service = ComptabiliteService(db)
    compte = await service.get_compte(compte_id)
    if not compte:
        raise HTTPException(status_code=404, detail="Compte non trouvé")
    return compte

@router.patch("/comptes/{compte_id}", response_model=CompteComptableResponse)
async def update_compte(
    compte_id: UUID,
    compte_update: CompteComptableUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour un compte comptable"""
    service = ComptabiliteService(db)
    try:
        return await service.update_compte(compte_id, compte_update.dict(exclude_unset=True))
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints pour les écritures comptables
@router.post("/ecritures", response_model=EcritureComptableResponse)
async def create_ecriture(
    ecriture: EcritureComptableCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle écriture comptable"""
    service = ComptabiliteService(db)
    try:
        return await service.create_ecriture(ecriture.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/ecritures", response_model=List[EcritureComptableResponse])
async def list_ecritures(
    compte_id: Optional[UUID] = None,
    journal_id: Optional[UUID] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Liste les écritures comptables avec filtres"""
    service = ComptabiliteService(db)
    return await service.get_ecritures(
        compte_id=compte_id,
        journal_id=journal_id,
        date_debut=date_debut,
        date_fin=date_fin,
        statut=statut
    )

@router.post("/ecritures/{ecriture_id}/valider")
async def valider_ecriture(
    ecriture_id: UUID,
    validee_par_id: UUID,
    db: Session = Depends(get_db)
):
    """Valide une écriture comptable"""
    service = ComptabiliteService(db)
    try:
        return await service.valider_ecriture(ecriture_id, validee_par_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints pour les journaux comptables
@router.post("/journaux", response_model=JournalComptableResponse)
async def create_journal(
    journal: JournalComptableCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouveau journal comptable"""
    service = ComptabiliteService(db)
    return await service.create_journal(journal.dict())

@router.get("/journaux", response_model=List[JournalComptableResponse])
async def list_journaux(
    type_journal: Optional[str] = None,
    actif: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Liste les journaux comptables"""
    service = ComptabiliteService(db)
    return await service.get_journaux(type_journal=type_journal, actif=actif)

# Endpoints pour les exercices comptables
@router.post("/exercices", response_model=ExerciceComptableResponse)
async def create_exercice(
    exercice: ExerciceComptableCreate,
    db: Session = Depends(get_db)
):
    """Crée un nouvel exercice comptable"""
    service = ComptabiliteService(db)
    try:
        return await service.create_exercice(exercice.dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/exercices/{annee}/cloturer")
async def cloturer_exercice(
    annee: str,
    cloture_par_id: UUID,
    db: Session = Depends(get_db)
):
    """Clôture un exercice comptable"""
    service = ComptabiliteService(db)
    try:
        return await service.cloturer_exercice(annee, cloture_par_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Endpoints pour les rapports comptables
@router.get("/grand-livre", response_model=List[LigneGrandLivre])
async def get_grand_livre(
    compte_id: Optional[UUID] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Génère le grand livre"""
    service = ComptabiliteService(db)
    return await service.get_grand_livre(
        compte_id=compte_id,
        date_debut=date_debut,
        date_fin=date_fin
    )

@router.get("/balance", response_model=List[CompteBalance])
async def get_balance(
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Génère la balance générale"""
    service = ComptabiliteService(db)
    return await service.get_balance_generale(
        date_debut=date_debut,
        date_fin=date_fin
    )

@router.get("/bilan", response_model=BilanResponse)
async def get_bilan(
    date_fin: date = Query(..., description="Date de fin pour le bilan"),
    db: Session = Depends(get_db)
):
    """Génère le bilan comptable"""
    service = ComptabiliteService(db)
    return await service.get_bilan(date_fin=date_fin)

@router.get("/compte-resultat", response_model=CompteResultatResponse)
async def get_compte_resultat(
    date_debut: date = Query(..., description="Date de début de l'exercice"),
    date_fin: date = Query(..., description="Date de fin de l'exercice"),
    db: Session = Depends(get_db)
):
    """Génère le compte de résultat"""
    service = ComptabiliteService(db)
    return await service.get_compte_resultat(
        date_debut=date_debut,
        date_fin=date_fin
    )
