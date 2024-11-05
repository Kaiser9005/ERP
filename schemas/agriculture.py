from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List, Dict
from datetime import date, datetime
from enum import Enum

class CultureType(str, Enum):
    PALMIER = "PALMIER"
    PAPAYE = "PAPAYE"

class ParcelleStatus(str, Enum):
    ACTIVE = "ACTIVE"
    EN_REPOS = "EN_REPOS"
    EN_PREPARATION = "EN_PREPARATION"

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
    coordonnees_gps: CoordoneesGPS
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
    date_debut: date
    date_fin: Optional[date]
    rendement_prevu: Optional[float] = Field(None, gt=0)
    rendement_reel: Optional[float] = Field(None, gt=0)
    notes: Optional[str]

class CycleCultureCreate(CycleCultureBase):
    parcelle_id: UUID4
    metadata: Optional[Dict] = None

class CycleCultureUpdate(BaseModel):
    date_fin: Optional[date]
    rendement_reel: Optional[float] = Field(None, gt=0)
    notes: Optional[str]
    metadata: Optional[Dict]

class CycleCultureInDB(CycleCultureBase):
    id: UUID4
    parcelle_id: UUID4
    metadata: Optional[Dict]

    class Config:
        orm_mode = True

class RecolteBase(BaseModel):
    date_recolte: datetime
    quantite_kg: float = Field(..., gt=0)
    qualite: QualiteRecolte
    conditions_meteo: ConditionsMeteo
    notes: Optional[str]

class RecolteCreate(RecolteBase):
    parcelle_id: UUID4
    equipe_recolte: List[UUID4]
    metadata: Optional[Dict] = None

class RecolteUpdate(BaseModel):
    quantite_kg: Optional[float] = Field(None, gt=0)
    qualite: Optional[QualiteRecolte]
    notes: Optional[str]
    metadata: Optional[Dict]

class RecolteInDB(RecolteBase):
    id: UUID4
    parcelle_id: UUID4
    equipe_recolte: List[UUID4]
    metadata: Optional[Dict]

    class Config:
        orm_mode = True

    @validator('quantite_kg')
    def validate_quantite(cls, v):
        if v <= 0:
            raise ValueError('La quantité doit être supérieure à 0')
        return v
