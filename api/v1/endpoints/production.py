from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.production import Parcelle, CycleCulture, Recolte
from schemas.production import (
    ParcelleCreate, ParcelleResponse, ParcelleUpdate,
    CycleCultureCreate, CycleCultureResponse,
    RecolteCreate, RecolteResponse
)

router = APIRouter()

# Endpoints Parcelles
@router.get("/parcelles", response_model=List[ParcelleResponse])
def get_parcelles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(Parcelle).offset(skip).limit(limit).all()

@router.post("/parcelles", response_model=ParcelleResponse)
def create_parcelle(
    parcelle: ParcelleCreate,
    db: Session = Depends(get_db)
):
    db_parcelle = Parcelle(**parcelle.dict())
    db.add(db_parcelle)
    db.commit()
    db.refresh(db_parcelle)
    return db_parcelle

@router.get("/parcelles/{parcelle_id}", response_model=ParcelleResponse)
def get_parcelle(parcelle_id: str, db: Session = Depends(get_db)):
    parcelle = db.query(Parcelle).filter(Parcelle.id == parcelle_id).first()
    if not parcelle:
        raise HTTPException(status_code=404, detail="Parcelle non trouvée")
    return parcelle

@router.put("/parcelles/{parcelle_id}", response_model=ParcelleResponse)
def update_parcelle(
    parcelle_id: str,
    parcelle: ParcelleUpdate,
    db: Session = Depends(get_db)
):
    db_parcelle = db.query(Parcelle).filter(Parcelle.id == parcelle_id).first()
    if not db_parcelle:
        raise HTTPException(status_code=404, detail="Parcelle non trouvée")
    
    for key, value in parcelle.dict(exclude_unset=True).items():
        setattr(db_parcelle, key, value)
    
    db.commit()
    db.refresh(db_parcelle)
    return db_parcelle

# Endpoints Cycles de Culture
@router.get("/cycles", response_model=List[CycleCultureResponse])
def get_cycles(
    parcelle_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(CycleCulture)
    if parcelle_id:
        query = query.filter(CycleCulture.parcelle_id == parcelle_id)
    return query.offset(skip).limit(limit).all()

@router.post("/cycles", response_model=CycleCultureResponse)
def create_cycle(
    cycle: CycleCultureCreate,
    db: Session = Depends(get_db)
):
    db_cycle = CycleCulture(**cycle.dict())
    db.add(db_cycle)
    db.commit()
    db.refresh(db_cycle)
    return db_cycle

# Endpoints Récoltes
@router.get("/recoltes", response_model=List[RecolteResponse])
def get_recoltes(
    parcelle_id: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(Recolte)
    if parcelle_id:
        query = query.filter(Recolte.parcelle_id == parcelle_id)
    return query.offset(skip).limit(limit).all()

@router.post("/recoltes", response_model=RecolteResponse)
def create_recolte(
    recolte: RecolteCreate,
    db: Session = Depends(get_db)
):
    db_recolte = Recolte(**recolte.dict())
    db.add(db_recolte)
    db.commit()
    db.refresh(db_recolte)
    return db_recolte