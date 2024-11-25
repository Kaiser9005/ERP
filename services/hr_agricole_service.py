"""
Service pour la gestion des fonctionnalités RH agricoles
"""

from typing import List, Optional, Dict, Any
from datetime import date, datetime, timedelta
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc

from models.hr_agricole import (
    CompetenceAgricole, CertificationAgricole, AffectationParcelle,
    ConditionTravailAgricole, FormationAgricole, EvaluationAgricole
)
from schemas.hr_agricole import (
    CompetenceAgricoleCreate, CompetenceAgricoleUpdate,
    CertificationAgricoleCreate, CertificationAgricoleUpdate,
    AffectationParcelleCreate, AffectationParcelleUpdate,
    ConditionTravailAgricoleCreate, ConditionTravailAgricoleUpdate,
    FormationAgricoleCreate, FormationAgricoleUpdate,
    EvaluationAgricoleCreate, EvaluationAgricoleUpdate
)

class HRAgricoleService:
    """Service pour la gestion des fonctionnalités RH agricoles"""

    def __init__(self, db: Session):
        self.db = db

    # Compétences agricoles
    def create_competence(self, competence: CompetenceAgricoleCreate) -> CompetenceAgricole:
        """Crée une nouvelle compétence agricole"""
        db_competence = CompetenceAgricole(**competence.dict())
        self.db.add(db_competence)
        self.db.commit()
        self.db.refresh(db_competence)
        return db_competence

    def get_competence(self, competence_id: UUID) -> Optional[CompetenceAgricole]:
        """Récupère une compétence par son ID"""
        return self.db.query(CompetenceAgricole).filter(CompetenceAgricole.id == competence_id).first()

    def get_competences_employe(self, employe_id: UUID) -> List[CompetenceAgricole]:
        """Récupère toutes les compétences d'un employé"""
        return self.db.query(CompetenceAgricole).filter(CompetenceAgricole.employe_id == employe_id).all()

    def update_competence(self, competence_id: UUID, competence: CompetenceAgricoleUpdate) -> Optional[CompetenceAgricole]:
        """Met à jour une compétence"""
        db_competence = self.get_competence(competence_id)
        if db_competence:
            for key, value in competence.dict(exclude_unset=True).items():
                setattr(db_competence, key, value)
            self.db.commit()
            self.db.refresh(db_competence)
        return db_competence

    # Certifications agricoles
    def create_certification(self, certification: CertificationAgricoleCreate) -> CertificationAgricole:
        """Crée une nouvelle certification agricole"""
        db_certification = CertificationAgricole(**certification.dict())
        self.db.add(db_certification)
        self.db.commit()
        self.db.refresh(db_certification)
        return db_certification

    def get_certification(self, certification_id: UUID) -> Optional[CertificationAgricole]:
        """Récupère une certification par son ID"""
        return self.db.query(CertificationAgricole).filter(CertificationAgricole.id == certification_id).first()

    def get_certifications_competence(self, competence_id: UUID) -> List[CertificationAgricole]:
        """Récupère toutes les certifications d'une compétence"""
        return self.db.query(CertificationAgricole).filter(CertificationAgricole.competence_id == competence_id).all()

    def update_certification(self, certification_id: UUID, certification: CertificationAgricoleUpdate) -> Optional[CertificationAgricole]:
        """Met à jour une certification"""
        db_certification = self.get_certification(certification_id)
        if db_certification:
            for key, value in certification.dict(exclude_unset=True).items():
                setattr(db_certification, key, value)
            self.db.commit()
            self.db.refresh(db_certification)
        return db_certification

    # Affectations parcelles
    def create_affectation(self, affectation: AffectationParcelleCreate) -> AffectationParcelle:
        """Crée une nouvelle affectation"""
        db_affectation = AffectationParcelle(**affectation.dict())
        self.db.add(db_affectation)
        self.db.commit()
        self.db.refresh(db_affectation)
        return db_affectation

    def get_affectation(self, affectation_id: UUID) -> Optional[AffectationParcelle]:
        """Récupère une affectation par son ID"""
        return self.db.query(AffectationParcelle).filter(AffectationParcelle.id == affectation_id).first()

    def get_affectations_employe(self, employe_id: UUID) -> List[AffectationParcelle]:
        """Récupère toutes les affectations d'un employé"""
        return self.db.query(AffectationParcelle).filter(AffectationParcelle.employe_id == employe_id).all()

    def get_affectations_parcelle(self, parcelle_id: UUID) -> List[AffectationParcelle]:
        """Récupère toutes les affectations d'une parcelle"""
        return self.db.query(AffectationParcelle).filter(AffectationParcelle.parcelle_id == parcelle_id).all()

    def update_affectation(self, affectation_id: UUID, affectation: AffectationParcelleUpdate) -> Optional[AffectationParcelle]:
        """Met à jour une affectation"""
        db_affectation = self.get_affectation(affectation_id)
        if db_affectation:
            for key, value in affectation.dict(exclude_unset=True).items():
                setattr(db_affectation, key, value)
            self.db.commit()
            self.db.refresh(db_affectation)
        return db_affectation

    # Conditions de travail
    def create_condition_travail(self, condition: ConditionTravailAgricoleCreate) -> ConditionTravailAgricole:
        """Crée une nouvelle condition de travail"""
        db_condition = ConditionTravailAgricole(**condition.dict())
        self.db.add(db_condition)
        self.db.commit()
        self.db.refresh(db_condition)
        return db_condition

    def get_condition_travail(self, condition_id: UUID) -> Optional[ConditionTravailAgricole]:
        """Récupère une condition de travail par son ID"""
        return self.db.query(ConditionTravailAgricole).filter(ConditionTravailAgricole.id == condition_id).first()

    def get_conditions_travail_employe(self, employe_id: UUID, date_debut: date, date_fin: date) -> List[ConditionTravailAgricole]:
        """Récupère les conditions de travail d'un employé sur une période"""
        return self.db.query(ConditionTravailAgricole).filter(
            and_(
                ConditionTravailAgricole.employe_id == employe_id,
                ConditionTravailAgricole.date >= date_debut,
                ConditionTravailAgricole.date <= date_fin
            )
        ).order_by(desc(ConditionTravailAgricole.date)).all()

    def update_condition_travail(self, condition_id: UUID, condition: ConditionTravailAgricoleUpdate) -> Optional[ConditionTravailAgricole]:
        """Met à jour une condition de travail"""
        db_condition = self.get_condition_travail(condition_id)
        if db_condition:
            for key, value in condition.dict(exclude_unset=True).items():
                setattr(db_condition, key, value)
            self.db.commit()
            self.db.refresh(db_condition)
        return db_condition

    # Formations agricoles
    def create_formation_agricole(self, formation: FormationAgricoleCreate) -> FormationAgricole:
        """Crée une nouvelle formation agricole"""
        db_formation = FormationAgricole(**formation.dict())
        self.db.add(db_formation)
        self.db.commit()
        self.db.refresh(db_formation)
        return db_formation

    def get_formation_agricole(self, formation_id: UUID) -> Optional[FormationAgricole]:
        """Récupère une formation agricole par son ID"""
        return self.db.query(FormationAgricole).filter(FormationAgricole.id == formation_id).first()

    def get_formations_agricoles_formation(self, formation_id: UUID) -> List[FormationAgricole]:
        """Récupère les détails agricoles d'une formation"""
        return self.db.query(FormationAgricole).filter(FormationAgricole.formation_id == formation_id).all()

    def update_formation_agricole(self, formation_id: UUID, formation: FormationAgricoleUpdate) -> Optional[FormationAgricole]:
        """Met à jour une formation agricole"""
        db_formation = self.get_formation_agricole(formation_id)
        if db_formation:
            for key, value in formation.dict(exclude_unset=True).items():
                setattr(db_formation, key, value)
            self.db.commit()
            self.db.refresh(db_formation)
        return db_formation

    # Évaluations agricoles
    def create_evaluation_agricole(self, evaluation: EvaluationAgricoleCreate) -> EvaluationAgricole:
        """Crée une nouvelle évaluation agricole"""
        db_evaluation = EvaluationAgricole(**evaluation.dict())
        self.db.add(db_evaluation)
        self.db.commit()
        self.db.refresh(db_evaluation)
        return db_evaluation

    def get_evaluation_agricole(self, evaluation_id: UUID) -> Optional[EvaluationAgricole]:
        """Récupère une évaluation agricole par son ID"""
        return self.db.query(EvaluationAgricole).filter(EvaluationAgricole.id == evaluation_id).first()

    def get_evaluations_agricoles_evaluation(self, evaluation_id: UUID) -> List[EvaluationAgricole]:
        """Récupère les détails agricoles d'une évaluation"""
        return self.db.query(EvaluationAgricole).filter(EvaluationAgricole.evaluation_id == evaluation_id).all()

    def update_evaluation_agricole(self, evaluation_id: UUID, evaluation: EvaluationAgricoleUpdate) -> Optional[EvaluationAgricole]:
        """Met à jour une évaluation agricole"""
        db_evaluation = self.get_evaluation_agricole(evaluation_id)
        if db_evaluation:
            for key, value in evaluation.dict(exclude_unset=True).items():
                setattr(db_evaluation, key, value)
            self.db.commit()
            self.db.refresh(db_evaluation)
        return db_evaluation

    # Méthodes utilitaires
    def check_competence_validite(self, competence_id: UUID) -> bool:
        """Vérifie si une compétence est toujours valide"""
        competence = self.get_competence(competence_id)
        if not competence or not competence.validite:
            return True
        return competence.validite >= date.today()

    def get_competences_a_renouveler(self, delai_jours: int = 30) -> List[CompetenceAgricole]:
        """Récupère les compétences à renouveler dans un délai donné"""
        date_limite = date.today() + timedelta(days=delai_jours)
        return self.db.query(CompetenceAgricole).filter(
            and_(
                CompetenceAgricole.validite.isnot(None),
                CompetenceAgricole.validite <= date_limite
            )
        ).all()

    def get_certifications_a_renouveler(self, delai_jours: int = 30) -> List[CertificationAgricole]:
        """Récupère les certifications à renouveler dans un délai donné"""
        date_limite = date.today() + timedelta(days=delai_jours)
        return self.db.query(CertificationAgricole).filter(
            and_(
                CertificationAgricole.date_expiration.isnot(None),
                CertificationAgricole.date_expiration <= date_limite
            )
        ).all()
