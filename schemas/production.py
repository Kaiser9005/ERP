from pydantic import BaseModel, UUID4
from datetime import date
from typing import Optional, List, Dict
from models.production import CultureType, ParcelleStatus, QualiteRecolte

class ParcelleBase(BaseModel):
    code: str
    culture_type: CultureType
    surface_hectares: float
    date_plantation: date
    statut: ParcelleStatus
    coordonnees_gps: Optional[Dict[str, float]]
    responsable_id: UUID4

class ParcelleCreate(ParcelleBase):
    pass

class ParcelleUpdate(ParcelleBase):
    code: Optional[str] = None
    culture_type: Optional[CultureType] = None
    surface_hectares: Optional[float] = None
    date_plantation: Optional[date] = None
    statut: Optional[ParcelleStatus] = None
    coordonnees_gps: Optional[Dict[str, float]] = None
    responsable_id: Optional[UUID4] = None

class ParcelleResponse(ParcelleBase):
    id: UUID4
    
    class Config:
        orm_mode = True

class CycleCultureBase(BaseModel):
    parcelle_id: UUID4
    date_debut: date
    date_fin: Optional[date]
    rendement_prevu: Optional[float]
    rendement_reel: Optional[float]
    notes: Optional[str]

class CycleCultureCreate(CycleCultureBase):
    pass

class CycleCultureResponse(CycleCultureBase):
    id: UUID4
    
    class Config:
        orm_mode = True

class RecolteBase(BaseModel):
    parcelle_id: UUID4
    date_recolte: date
    quantite_kg: float
    qualite: QualiteRecolte
    equipe_recolte: List[UUID4]
    conditions_meteo: Optional[Dict[str, str]]
    notes: Optional[str]

class RecolteCreate(RecolteBase):
    pass

class RecolteResponse(RecolteBase):
    id: UUID4
    
    class Config:
        orm_mode = True