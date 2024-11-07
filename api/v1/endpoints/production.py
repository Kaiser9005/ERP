from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ....db.database import get_db
from ....schemas.production import (
    ParcelleCreate, ParcelleUpdate, ParcelleInDB,
    CycleCultureCreate, CycleCultureUpdate, CycleCultureInDB,
    RecolteCreate, RecolteUpdate, RecolteInDB,
    ProductionEventCreate, ProductionEventUpdate, ProductionEventInDB,
    ProductionStats
)
from ....models.production import Parcelle, CycleCulture, Recolte, ProductionEvent
from ....core.security import get_current_user
from uuid import UUID
from datetime import date, datetime, timedelta
from sqlalchemy import func

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
    """Liste des parcelles avec filtres"""
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
def get_production_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """Obtenir les statistiques de production"""
    total_surface = db.query(func.sum(Parcelle.surface_hectares)).scalar() or 0
    parcelles_actives = db.query(Parcelle).filter(Parcelle.statut == "ACTIVE").count()

    # Récoltes du mois en cours
    debut_mois = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    fin_mois = (debut_mois + timedelta(days=32)).replace(day=1) - timedelta(seconds=1)

    production_mensuelle = db.query(func.sum(Recolte.quantite_kg))\
        .filter(Recolte.date_recolte.between(debut_mois, fin_mois))\
        .scalar() or 0

    # Calcul du rendement moyen
    rendement_moyen = production_mensuelle / total_surface if total_surface > 0 else 0

    return ProductionStats(
        total_surface=total_surface,
        parcelles_actives=parcelles_actives,
        recolte_en_cours=db.query(Recolte).filter(Recolte.date_recolte >= debut_mois).count(),
        production_mensuelle=production_mensuelle,
        rendement_moyen=rendement_moyen
    )
