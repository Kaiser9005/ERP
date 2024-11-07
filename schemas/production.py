from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List, Dict
from datetime import date, datetime
from enum import Enum

class CultureType(str, Enum):
    PALMIER = "PALMIER"
    PAPAYE = "PAPAYE"

class ParcelleStatus(str, Enum):
    EN_PREPARATION = "EN_PREPARATION"
    ACTIVE = "ACTIVE"
    EN_REPOS = "EN_REPOS"

class QualiteRecolte(str, Enum):
    A = "A"
    B = "B"
    C = "C"

class CoordoneesGPS(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

class ConditionsMeteo(BaseModel):
    temperature: float
    humidite: float = Field(..., ge=0, le=100)
    precipitation: Optional[float] = Field(None, ge=0)

class ParcelleBase(BaseModel):
    code: str
    culture_type: CultureType
    surface_hectares: float = Field(..., gt=0)
    coordonnees_gps: Optional[CoordoneesGPS]
    statut: ParcelleStatus = ParcelleStatus.EN_PREPARATION

class ParcelleCreate(ParcelleBase):
    date_plantation: date
    responsable_id: UUID4
    metadata: Optional[Dict] = None

class ParcelleUpdate(BaseModel):
    culture_type: Optional[CultureType] = None
    surface_hectares: Optional[float] = Field(None, gt=0)
    statut: Optional[ParcelleStatus] = None
    responsable_id: Optional[UUID4] = None
    metadata: Optional[Dict] = None

class ParcelleInDB(ParcelleBase):
    id: UUID4
    date_plantation: date
    responsable_id: UUID4
    metadata: Optional[Dict]

    class Config:
        orm_mode = True

class CycleCultureBase(BaseModel):
    parcelle_id: UUID4
    date_debut: date
    date_fin: Optional[date]
    rendement_prevu: Optional[float] = Field(None, gt=0)
    rendement_reel: Optional[float] = Field(None, gt=0)
    notes: Optional[str]
    metadata: Optional[Dict] = None

class CycleCultureCreate(CycleCultureBase):
    pass

class CycleCultureUpdate(BaseModel):
    date_fin: Optional[date]
    rendement_reel: Optional[float] = Field(None, gt=0)
    notes: Optional[str]
    metadata: Optional[Dict]

class CycleCultureInDB(CycleCultureBase):
    id: UUID4

    class Config:
        orm_mode = True

class RecolteBase(BaseModel):
    parcelle_id: UUID4
    cycle_culture_id: Optional[UUID4]
    date_recolte: datetime
    quantite_kg: float = Field(..., gt=0)
    qualite: QualiteRecolte
    conditions_meteo: Optional[ConditionsMeteo]
    equipe_recolte: List[UUID4]
    notes: Optional[str]
    metadata: Optional[Dict] = None

class RecolteCreate(RecolteBase):
    pass

class RecolteUpdate(BaseModel):
    quantite_kg: Optional[float] = Field(None, gt=0)
    qualite: Optional[QualiteRecolte]
    conditions_meteo: Optional[ConditionsMeteo]
    notes: Optional[str]
    metadata: Optional[Dict]

class RecolteInDB(RecolteBase):
    id: UUID4

    class Config:
        orm_mode = True

class ProductionEventBase(BaseModel):
    parcelle_id: UUID4
    type: str
    date_debut: datetime
    date_fin: Optional[datetime]
    description: Optional[str]
    statut: Optional[str]
    responsable_id: Optional[UUID4]
    metadata: Optional[Dict] = None

class ProductionEventCreate(ProductionEventBase):
    pass

class ProductionEventUpdate(BaseModel):
    date_fin: Optional[datetime]
    description: Optional[str]
    statut: Optional[str]
    metadata: Optional[Dict]

class ProductionEventInDB(ProductionEventBase):
    id: UUID4

    class Config:
        orm_mode = True

class ProductionStats(BaseModel):
    total_surface: float
    parcelles_actives: int
    recolte_en_cours: int
    production_mensuelle: float  # en kg
    rendement_moyen: float  # kg/hectare
