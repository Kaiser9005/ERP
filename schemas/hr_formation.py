from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field

class FormationBase(BaseModel):
    """Schéma de base pour une formation"""
    titre: str = Field(..., description="Titre de la formation")
    description: Optional[str] = Field(None, description="Description détaillée de la formation")
    type: str = Field(..., description="Type de formation (technique, securite, agricole)")
    duree: int = Field(..., description="Durée de la formation en heures")
    competences_requises: Optional[Dict[str, Any]] = Field(None, description="Compétences requises pour suivre la formation")
    competences_acquises: Optional[Dict[str, Any]] = Field(None, description="Compétences acquises après la formation")
    materiel_requis: Optional[Dict[str, Any]] = Field(None, description="Matériel nécessaire pour la formation")
    conditions_meteo: Optional[Dict[str, Any]] = Field(None, description="Conditions météo requises/restrictions")

class FormationCreate(FormationBase):
    """Schéma pour la création d'une formation"""
    pass

class FormationUpdate(FormationBase):
    """Schéma pour la mise à jour d'une formation"""
    titre: Optional[str] = None
    type: Optional[str] = None
    duree: Optional[int] = None

class Formation(FormationBase):
    """Schéma complet d'une formation"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SessionFormationBase(BaseModel):
    """Schéma de base pour une session de formation"""
    formation_id: UUID = Field(..., description="ID de la formation")
    date_debut: datetime = Field(..., description="Date et heure de début")
    date_fin: datetime = Field(..., description="Date et heure de fin")
    lieu: Optional[str] = Field(None, description="Lieu de la formation")
    formateur: Optional[str] = Field(None, description="Nom du formateur")
    statut: str = Field("planifie", description="Statut de la session")
    nb_places: Optional[int] = Field(None, description="Nombre de places disponibles")
    notes: Optional[str] = Field(None, description="Notes supplémentaires")

class SessionFormationCreate(SessionFormationBase):
    """Schéma pour la création d'une session de formation"""
    pass

class SessionFormationUpdate(SessionFormationBase):
    """Schéma pour la mise à jour d'une session de formation"""
    formation_id: Optional[UUID] = None
    date_debut: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    statut: Optional[str] = None

class SessionFormation(SessionFormationBase):
    """Schéma complet d'une session de formation"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    formation: Formation

    class Config:
        orm_mode = True

class ParticipationFormationBase(BaseModel):
    """Schéma de base pour une participation à une formation"""
    session_id: UUID = Field(..., description="ID de la session de formation")
    employee_id: UUID = Field(..., description="ID de l'employé")
    statut: str = Field("inscrit", description="Statut de la participation")
    note: Optional[int] = Field(None, description="Note obtenue (sur 100)")
    commentaires: Optional[str] = Field(None, description="Commentaires sur la participation")
    certification_obtenue: bool = Field(False, description="Si la certification a été obtenue")
    date_certification: Optional[datetime] = Field(None, description="Date d'obtention de la certification")

class ParticipationFormationCreate(ParticipationFormationBase):
    """Schéma pour la création d'une participation"""
    pass

class ParticipationFormationUpdate(ParticipationFormationBase):
    """Schéma pour la mise à jour d'une participation"""
    session_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    statut: Optional[str] = None
    certification_obtenue: Optional[bool] = None

class ParticipationFormation(ParticipationFormationBase):
    """Schéma complet d'une participation"""
    id: UUID
    created_at: datetime
    updated_at: datetime
    session: SessionFormation

    class Config:
        orm_mode = True

class EvaluationBase(BaseModel):
    """Schéma de base pour une évaluation"""
    employee_id: UUID = Field(..., description="ID de l'employé évalué")
    evaluateur_id: UUID = Field(..., description="ID de l'évaluateur")
    date_evaluation: datetime = Field(..., description="Date de l'évaluation")
    type: str = Field(..., description="Type d'évaluation (periodique, formation, projet)")
    periode_debut: Optional[datetime] = Field(None, description="Début de la période évaluée")
    periode_fin: Optional[datetime] = Field(None, description="Fin de la période évaluée")
    competences: Dict[str, Any] = Field(..., description="Évaluation des compétences")
    objectifs: Dict[str, Any] = Field(..., description="Objectifs fixés/atteints")
    performances: Dict[str, Any] = Field(..., description="Métriques de performance")
    points_forts: Optional[str] = Field(None, description="Points forts identifiés")
    points_amelioration: Optional[str] = Field(None, description="Points à améliorer")
    plan_action: Optional[str] = Field(None, description="Plan d'action proposé")
    note_globale: int = Field(..., description="Note globale sur 100")
    statut: str = Field("brouillon", description="Statut de l'évaluation")

class EvaluationCreate(EvaluationBase):
    """Schéma pour la création d'une évaluation"""
    pass

class EvaluationUpdate(EvaluationBase):
    """Schéma pour la mise à jour d'une évaluation"""
    employee_id: Optional[UUID] = None
    evaluateur_id: Optional[UUID] = None
    date_evaluation: Optional[datetime] = None
    type: Optional[str] = None
    competences: Optional[Dict[str, Any]] = None
    objectifs: Optional[Dict[str, Any]] = None
    performances: Optional[Dict[str, Any]] = None
    note_globale: Optional[int] = None
    statut: Optional[str] = None

class Evaluation(EvaluationBase):
    """Schéma complet d'une évaluation"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
