from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class PrioriteTache(str, Enum):
    """Énumération des niveaux de priorité des tâches"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class StatutTache(str, Enum):
    """Énumération des statuts des tâches"""
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_ATTENTE = "EN_ATTENTE"
    TERMINEE = "TERMINEE"
    ANNULEE = "ANNULEE"

class CategorieTache(str, Enum):
    """Énumération des catégories de tâches"""
    PRODUCTION = "PRODUCTION"
    MAINTENANCE = "MAINTENANCE"
    RECOLTE = "RECOLTE"
    PLANTATION = "PLANTATION"
    IRRIGATION = "IRRIGATION"
    TRAITEMENT = "TRAITEMENT"
    AUTRE = "AUTRE"

class RessourceTacheBase(BaseModel):
    ressource_id: int
    quantite_requise: float
    quantite_utilisee: Optional[float] = 0

    class Config:
        from_attributes = True

class CommentaireTacheBase(BaseModel):
    contenu: str = Field(..., min_length=1, max_length=1000)

    class Config:
        from_attributes = True

class DependanceTacheBase(BaseModel):
    dependance_id: int
    type_dependance: str = "fin_vers_debut"

    class Config:
        from_attributes = True

class TacheBase(BaseModel):
    titre: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    statut: StatutTache = StatutTache.A_FAIRE
    priorite: PrioriteTache = PrioriteTache.MOYENNE
    categorie: CategorieTache = CategorieTache.AUTRE
    date_debut: Optional[datetime]
    date_fin_prevue: Optional[datetime]
    projet_id: int
    responsable_id: Optional[int]
    parcelle_id: Optional[int]
    dependant_meteo: bool = False
    min_temperature: Optional[float]
    max_temperature: Optional[float]
    max_wind_speed: Optional[float]
    max_precipitation: Optional[float]
    heures_estimees: Optional[float]

class TacheCreate(TacheBase):
    ressources: Optional[List[RessourceTacheBase]] = []
    dependances: Optional[List[DependanceTacheBase]] = []

    @field_validator('date_fin_prevue')
    @classmethod
    def date_fin_apres_debut(cls, v: Optional[datetime], info) -> Optional[datetime]:
        date_debut = info.data.get('date_debut')
        if date_debut and v and v < date_debut:
            raise ValueError("La date d'échéance doit être postérieure à la date de début")
        return v

    @field_validator('max_temperature')
    @classmethod
    def valider_plage_temperature(cls, v: Optional[float], info) -> Optional[float]:
        min_temp = info.data.get('min_temperature')
        if v is not None and min_temp is not None and v < min_temp:
            raise ValueError("La température maximale doit être supérieure à la température minimale")
        return v

class TacheUpdate(BaseModel):
    titre: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    statut: Optional[StatutTache]
    priorite: Optional[PrioriteTache]
    categorie: Optional[CategorieTache]
    date_debut: Optional[datetime]
    date_fin_prevue: Optional[datetime]
    responsable_id: Optional[int]
    dependant_meteo: Optional[bool]
    min_temperature: Optional[float]
    max_temperature: Optional[float]
    max_wind_speed: Optional[float]
    max_precipitation: Optional[float]
    heures_estimees: Optional[float]
    heures_reelles: Optional[float]
    pourcentage_completion: Optional[int] = Field(None, ge=0, le=100)

class RessourceTacheCreate(RessourceTacheBase):
    tache_id: int

class RessourceTacheUpdate(BaseModel):
    quantite_requise: Optional[float]
    quantite_utilisee: Optional[float]

class CommentaireTacheCreate(CommentaireTacheBase):
    tache_id: int
    auteur_id: int

class DependanceTacheCreate(DependanceTacheBase):
    tache_id: int

class RessourceTache(RessourceTacheBase):
    id: int
    tache_id: int
    date_creation: datetime
    date_modification: datetime

class CommentaireTache(CommentaireTacheBase):
    id: int
    tache_id: int
    auteur_id: int
    date_creation: datetime
    date_modification: datetime

class DependanceTache(DependanceTacheBase):
    id: int
    tache_id: int
    date_creation: datetime
    date_modification: datetime

class Tache(TacheBase):
    id: int
    date_fin_reelle: Optional[datetime]
    heures_reelles: Optional[float]
    pourcentage_completion: int
    date_creation: datetime
    date_modification: datetime
    ressources: List[RessourceTache] = []
    commentaires: List[CommentaireTache] = []
    dependances: List[DependanceTache] = []

    class Config:
        from_attributes = True

class TacheAvecMeteo(Tache):
    conditions_favorables: bool
    conditions_meteo: dict
    alertes_meteo: List[str]

class ListeTaches(BaseModel):
    taches: List[Tache]
    total: int
    page: int
    taille: int
    total_pages: int

    class Config:
        from_attributes = True