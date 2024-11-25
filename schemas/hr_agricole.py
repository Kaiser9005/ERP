"""
Schémas Pydantic pour la validation des données RH agricoles
"""

from pydantic import BaseModel, UUID4, Field, validator
from typing import Optional, List, Dict, Any
from datetime import date, datetime
from enum import Enum

class TypePersonnel(str, Enum):
    """Types de personnel agricole"""
    PERMANENT = "PERMANENT"
    SAISONNIER = "SAISONNIER"
    TEMPORAIRE = "TEMPORAIRE"
    STAGIAIRE = "STAGIAIRE"

class SpecialiteAgricole(str, Enum):
    """Spécialités agricoles"""
    CULTURE = "CULTURE"
    ELEVAGE = "ELEVAGE"
    MARAICHAGE = "MARAICHAGE"
    ARBORICULTURE = "ARBORICULTURE"
    MAINTENANCE = "MAINTENANCE"
    LOGISTIQUE = "LOGISTIQUE"

class NiveauCompetence(str, Enum):
    """Niveaux de compétence"""
    DEBUTANT = "DEBUTANT"
    INTERMEDIAIRE = "INTERMEDIAIRE"
    AVANCE = "AVANCE"
    EXPERT = "EXPERT"

class TypeCertification(str, Enum):
    """Types de certifications agricoles"""
    PHYTOSANITAIRE = "PHYTOSANITAIRE"
    SECURITE = "SECURITE"
    CONDUITE_ENGINS = "CONDUITE_ENGINS"
    BIO = "BIO"
    QUALITE = "QUALITE"

class CompetenceAgricoleBase(BaseModel):
    """Schéma de base pour une compétence agricole"""
    specialite: SpecialiteAgricole
    niveau: NiveauCompetence
    cultures: List[str] = Field(default_factory=list)
    equipements: List[str] = Field(default_factory=list)
    date_acquisition: date
    date_mise_a_jour: Optional[date]
    validite: Optional[date]
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

    @validator('validite')
    def validite_future(cls, v):
        if v and v < date.today():
            raise ValueError("La date de validité doit être dans le futur")
        return v

class CompetenceAgricoleCreate(CompetenceAgricoleBase):
    """Schéma pour la création d'une compétence agricole"""
    employe_id: UUID4

class CompetenceAgricoleUpdate(CompetenceAgricoleBase):
    """Schéma pour la mise à jour d'une compétence agricole"""
    pass

class CompetenceAgricoleInDB(CompetenceAgricoleBase):
    """Schéma pour une compétence agricole en DB"""
    id: UUID4
    employe_id: UUID4

    class Config:
        orm_mode = True

class CertificationAgricoleBase(BaseModel):
    """Schéma de base pour une certification agricole"""
    type_certification: TypeCertification
    organisme: str
    numero: Optional[str]
    date_obtention: date
    date_expiration: Optional[date]
    niveau: Optional[str]
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

    @validator('date_expiration')
    def expiration_future(cls, v):
        if v and v < date.today():
            raise ValueError("La date d'expiration doit être dans le futur")
        return v

class CertificationAgricoleCreate(CertificationAgricoleBase):
    """Schéma pour la création d'une certification agricole"""
    competence_id: UUID4
    document_id: Optional[UUID4]

class CertificationAgricoleUpdate(CertificationAgricoleBase):
    """Schéma pour la mise à jour d'une certification agricole"""
    document_id: Optional[UUID4]

class CertificationAgricoleInDB(CertificationAgricoleBase):
    """Schéma pour une certification agricole en DB"""
    id: UUID4
    competence_id: UUID4
    document_id: Optional[UUID4]

    class Config:
        orm_mode = True

class AffectationParcelleBase(BaseModel):
    """Schéma de base pour une affectation à une parcelle"""
    date_debut: date
    date_fin: Optional[date]
    role: str
    responsabilites: List[str] = Field(default_factory=list)
    objectifs: Dict[str, Any] = Field(default_factory=dict)
    restrictions_meteo: List[str] = Field(default_factory=list)
    equipements_requis: List[str] = Field(default_factory=list)
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

    @validator('date_fin')
    def date_fin_valide(cls, v, values):
        if v and 'date_debut' in values and v < values['date_debut']:
            raise ValueError("La date de fin doit être postérieure à la date de début")
        return v

class AffectationParcelleCreate(AffectationParcelleBase):
    """Schéma pour la création d'une affectation"""
    employe_id: UUID4
    parcelle_id: UUID4

class AffectationParcelleUpdate(AffectationParcelleBase):
    """Schéma pour la mise à jour d'une affectation"""
    pass

class AffectationParcelleInDB(AffectationParcelleBase):
    """Schéma pour une affectation en DB"""
    id: UUID4
    employe_id: UUID4
    parcelle_id: UUID4

    class Config:
        orm_mode = True

class ConditionTravailAgricoleBase(BaseModel):
    """Schéma de base pour les conditions de travail agricole"""
    date: date
    temperature: Optional[float] = Field(None, ge=-50, le=50)
    humidite: Optional[int] = Field(None, ge=0, le=100)
    precipitation: bool = False
    vent: Optional[float] = Field(None, ge=0)
    exposition_soleil: Optional[int] = Field(None, ge=0)
    charge_physique: Optional[int] = Field(None, ge=1, le=10)
    equipements_protection: List[str] = Field(default_factory=list)
    incidents: List[Dict[str, Any]] = Field(default_factory=list)
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

class ConditionTravailAgricoleCreate(ConditionTravailAgricoleBase):
    """Schéma pour la création de conditions de travail"""
    employe_id: UUID4

class ConditionTravailAgricoleUpdate(ConditionTravailAgricoleBase):
    """Schéma pour la mise à jour de conditions de travail"""
    pass

class ConditionTravailAgricoleInDB(ConditionTravailAgricoleBase):
    """Schéma pour des conditions de travail en DB"""
    id: UUID4
    employe_id: UUID4

    class Config:
        orm_mode = True

class FormationAgricoleBase(BaseModel):
    """Schéma de base pour une formation agricole"""
    specialite: SpecialiteAgricole
    cultures_concernees: List[str] = Field(default_factory=list)
    equipements_concernes: List[str] = Field(default_factory=list)
    conditions_meteo: Dict[str, Any] = Field(default_factory=dict)
    pratiques_specifiques: List[str] = Field(default_factory=list)
    evaluation_terrain: bool = False
    resultats_evaluation: Dict[str, Any] = Field(default_factory=dict)
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

class FormationAgricoleCreate(FormationAgricoleBase):
    """Schéma pour la création d'une formation agricole"""
    formation_id: UUID4

class FormationAgricoleUpdate(FormationAgricoleBase):
    """Schéma pour la mise à jour d'une formation agricole"""
    pass

class FormationAgricoleInDB(FormationAgricoleBase):
    """Schéma pour une formation agricole en DB"""
    id: UUID4
    formation_id: UUID4

    class Config:
        orm_mode = True

class EvaluationAgricoleBase(BaseModel):
    """Schéma de base pour une évaluation agricole"""
    performances_cultures: Dict[str, Any] = Field(default_factory=dict)
    maitrise_equipements: Dict[str, Any] = Field(default_factory=dict)
    respect_securite: Dict[str, Any] = Field(default_factory=dict)
    adaptabilite_meteo: Dict[str, Any] = Field(default_factory=dict)
    gestion_ressources: Dict[str, Any] = Field(default_factory=dict)
    qualite_travail: Dict[str, Any] = Field(default_factory=dict)
    commentaire: Optional[str]
    donnees_supplementaires: Dict[str, Any] = Field(default_factory=dict)

class EvaluationAgricoleCreate(EvaluationAgricoleBase):
    """Schéma pour la création d'une évaluation agricole"""
    evaluation_id: UUID4

class EvaluationAgricoleUpdate(EvaluationAgricoleBase):
    """Schéma pour la mise à jour d'une évaluation agricole"""
    pass

class EvaluationAgricoleInDB(EvaluationAgricoleBase):
    """Schéma pour une évaluation agricole en DB"""
    id: UUID4
    evaluation_id: UUID4

    class Config:
        orm_mode = True
