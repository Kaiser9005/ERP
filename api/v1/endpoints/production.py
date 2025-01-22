from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from models.hr import Employe
from db.database import get_db
from schemas.production import (
    ParcelleCreate, ParcelleUpdate, ParcelleInDB,
    CycleCultureCreate, CycleCultureUpdate, CycleCultureInDB,
    RecolteCreate, RecolteUpdate, RecolteInDB,
    ProductionEventCreate, ProductionEventUpdate, ProductionEventInDB,
    ProductionStats
)
from models.production import Parcelle, CycleCulture, Recolte, ProductionEvent
from core.security import get_current_user
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlalchemy import func

from services.production_service import ProductionService

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
    """Liste des parcelles avec filtres et nom du responsable"""
    query = db.query(Parcelle).join(Employe, Parcelle.responsable_id == Employe.id)
    if culture_type:
        query = query.filter(Parcelle.culture_type == culture_type)
    if statut:
        query = query.filter(Parcelle.statut == statut)
    
    parcelles = query.offset(skip).limit(limit).all()
    
    # Enrichir les données avec le nom du responsable
    parcelles_avec_responsable = []
    for parcelle in parcelles:
        parcelle_data = ParcelleInDB.model_validate(parcelle).dict()
        parcelle_data['nom_responsable'] = parcelle.responsable.nom if parcelle.responsable else None
        parcelles_avec_responsable.append(parcelle_data)
    
    return parcelles_avec_responsable

@router.get("/parcelles/{parcelle_id}", response_model=ParcelleInDB)
def get_parcelle(
    parcelle_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Détails d'une parcelle"""
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
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
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

# Endpoints Événements de Production

@router.post("/events/", response_model=ProductionEventInDB)
def create_production_event(
    event: ProductionEventCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Créer un nouvel événement de production"""
    db_event = ProductionEvent(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/events/", response_model=List[ProductionEventInDB])
def list_production_events(
    skip: int = 0,
    limit: int = 100,
    parcelle_id: Optional[UUID] = None,
    date_debut: Optional[date] = None,
    date_fin: Optional[date] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Liste des événements de production"""
    query = db.query(ProductionEvent)
    if parcelle_id:
        query = query.filter(ProductionEvent.parcelle_id == parcelle_id)
    if date_debut:
        query = query.filter(ProductionEvent.date_debut >= date_debut)
    if date_fin:
        query = query.filter(ProductionEvent.date_debut <= date_fin)
    return query.offset(skip).limit(limit).all()

# Endpoints Statistiques

@router.get("/stats/", response_model=ProductionStats)
async def get_production_stats(
    parcelle_id: Optional[UUID] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir les statistiques de production pour une parcelle spécifique ou pour l'ensemble des parcelles"""
    production_service = ProductionService(db)
    stats = await production_service.get_production_stats(parcelle_id=str(parcelle_id) if parcelle_id else None)
    return stats

@router.get("/graphique")
async def get_production_graph(
    periode: Optional[str] = Query("mois", description="Période d'agrégation: 'jour', 'semaine', 'mois'"),
    date_debut: Optional[date] = Query(None),
    date_fin: Optional[date] = Query(None),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir les données pour le graphique de production"""
    if not date_debut:
        date_debut = datetime.now().date() - timedelta(days=30)
    if not date_fin:
        date_fin = datetime.now().date()

    production_service = ProductionService(db)
    return await production_service.get_production_graph_data(
        periode=periode,
        date_debut=date_debut,
        date_fin=date_fin
    )
