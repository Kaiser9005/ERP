from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....db.database import get_db
from ....schemas.agriculture import (
    ParcelleCreate, ParcelleUpdate, ParcelleInDB,
    CycleCultureCreate, CycleCultureUpdate, CycleCultureInDB,
    RecolteCreate, RecolteUpdate, RecolteInDB
)
from ....models.agriculture.parcelle import Parcelle, CycleCulture, Recolte
from ....core.security import get_current_user
from uuid import UUID

router = APIRouter()

# Endpoints Parcelles

@router.post("/parcelles/", response_model=ParcelleInDB)
def create_parcelle(
    parcelle: ParcelleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer une nouvelle parcelle"""
    db_parcelle = Parcelle(**parcelle.dict())
    db.add(db_parcelle)
    db.commit()
    db.refresh(db_parcelle)
    return db_parcelle

@router.get("/parcelles/", response_model=List[ParcelleInDB])
def list_parcelles(
    skip: int = 0,
    limit: int = 100,
    culture_type: Optional[str] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Liste des parcelles avec filtres optionnels"""
    query = db.query(Parcelle)
    if culture_type:
        query = query.filter(Parcelle.culture_type == culture_type)
    if statut:
        query = query.filter(Parcelle.statut == statut)
    return query.offset(skip).limit(limit).all()

@router.get("/parcelles/{parcelle_id}", response_model=ParcelleInDB)
def get_parcelle(
    parcelle_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir les détails d'une parcelle"""
    parcelle = db.query(Parcelle).filter(Parcelle.id == parcelle_id).first()
    if not parcelle:
        raise HTTPException(status_code=404, detail="Parcelle non trouvée")
    return parcelle

@router.put("/parcelles/{parcelle_id}", response_model=ParcelleInDB)
def update_parcelle(
    parcelle_id: UUID,
    parcelle_update: ParcelleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une parcelle"""
    db_parcelle = db.query(Parcelle).filter(Parcelle.id == parcelle_id).first()
    if not db_parcelle:
        raise HTTPException(status_code=404, detail="Parcelle non trouvée")

    for field, value in parcelle_update.dict(exclude_unset=True).items():
        setattr(db_parcelle, field, value)

    db.commit()
    db.refresh(db_parcelle)
    return db_parcelle

# Endpoints Cycles de Culture

@router.post("/cycles-culture/", response_model=CycleCultureInDB)
def create_cycle_culture(
    cycle: CycleCultureCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouveau cycle de culture"""
    db_cycle = CycleCulture(**cycle.dict())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle

@router.get("/cycles-culture/", response_model=List[CycleCultureInDB])
def list_cycles_culture(
    skip: int = 0,
    limit: int = 100,
    parcelle_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Liste des cycles de culture"""
    query = db.query(CycleCulture)
    if parcelle_id:
        query = query.filter(CycleCulture.parcelle_id == parcelle_id)
    return query.offset(skip).limit(limit).all()

# Endpoints Récoltes

@router.post("/recoltes/", response_model=RecolteInDB)
def create_recolte(
    recolte: RecolteCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Enregistrer une nouvelle récolte"""
    db_recolte = Recolte(**recolte.dict())
    db.add(db_recolte)
    db.commit()
    db.refresh(db_recolte)
    return db_recolte

@router.get("/recoltes/", response_model=List[RecolteInDB])
def list_recoltes(
    skip: int = 0,
    limit: int = 100,
    parcelle_id: Optional[UUID] = None,
    date_debut: Optional[str] = None,
    date_fin: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Liste des récoltes avec filtres"""
    query = db.query(Recolte)
    if parcelle_id:
        query = query.filter(Recolte.parcelle_id == parcelle_id)
    if date_debut:
        query = query.filter(Recolte.date_recolte >= date_debut)
    if date_fin:
        query = query.filter(Recolte.date_recolte <= date_fin)
    return query.offset(skip).limit(limit).all()

@router.get("/recoltes/{recolte_id}", response_model=RecolteInDB)
def get_recolte(
    recolte_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir les détails d'une récolte"""
    recolte = db.query(Recolte).filter(Recolte.id == recolte_id).first()
    if not recolte:
        raise HTTPException(status_code=404, detail="Récolte non trouvée")
    return recolte

@router.put("/recoltes/{recolte_id}", response_model=RecolteInDB)
def update_recolte(
    recolte_id: UUID,
    recolte_update: RecolteUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Mettre à jour une récolte"""
    db_recolte = db.query(Recolte).filter(Recolte.id == recolte_id).first()
    if not db_recolte:
        raise HTTPException(status_code=404, detail="Récolte non trouvée")

    for field, value in recolte_update.dict(exclude_unset=True).items():
        setattr(db_recolte, field, value)

    db.commit()
    db.refresh(db_recolte)
    return db_recolte
