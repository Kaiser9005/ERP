from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from models.hr_formation import Formation, SessionFormation, ParticipationFormation, Evaluation
from models.hr import Employee
from schemas.hr_formation import (
    FormationCreate, FormationUpdate,
    SessionFormationCreate, SessionFormationUpdate,
    ParticipationFormationCreate, ParticipationFormationUpdate,
    EvaluationCreate, EvaluationUpdate
)

class HRFormationService:
    """Service pour la gestion des formations et évaluations"""

    def __init__(self, db: Session):
        self.db = db

    # Formation CRUD
    def create_formation(self, formation: FormationCreate) -> Formation:
        """Créer une nouvelle formation"""
        db_formation = Formation(**formation.dict())
        self.db.add(db_formation)
        self.db.commit()
        self.db.refresh(db_formation)
        return db_formation

    def get_formation(self, formation_id: UUID) -> Optional[Formation]:
        """Récupérer une formation par son ID"""
        return self.db.query(Formation).filter(Formation.id == str(formation_id)).first()

    def get_formations(
        self,
        skip: int = 0,
        limit: int = 100,
        type: Optional[str] = None
    ) -> List[Formation]:
        """Récupérer la liste des formations avec filtres optionnels"""
        query = self.db.query(Formation)
        if type:
            query = query.filter(Formation.type == type)
        return query.offset(skip).limit(limit).all()

    def update_formation(
        self,
        formation_id: UUID,
        formation: FormationUpdate
    ) -> Optional[Formation]:
        """Mettre à jour une formation"""
        db_formation = self.get_formation(formation_id)
        if db_formation:
            for key, value in formation.dict(exclude_unset=True).items():
                setattr(db_formation, key, value)
            self.db.commit()
            self.db.refresh(db_formation)
        return db_formation

    def delete_formation(self, formation_id: UUID) -> bool:
        """Supprimer une formation"""
        db_formation = self.get_formation(formation_id)
        if db_formation:
            self.db.delete(db_formation)
            self.db.commit()
            return True
        return False

    # Session Formation CRUD
    def create_session(self, session: SessionFormationCreate) -> SessionFormation:
        """Créer une nouvelle session de formation"""
        db_session = SessionFormation(**session.dict())
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session

    def get_session(self, session_id: UUID) -> Optional[SessionFormation]:
        """Récupérer une session par son ID"""
        return self.db.query(SessionFormation).filter(
            SessionFormation.id == str(session_id)
        ).first()

    def get_sessions(
        self,
        skip: int = 0,
        limit: int = 100,
        formation_id: Optional[UUID] = None,
        statut: Optional[str] = None,
        date_debut: Optional[datetime] = None
    ) -> List[SessionFormation]:
        """Récupérer la liste des sessions avec filtres optionnels"""
        query = self.db.query(SessionFormation)
        if formation_id:
            query = query.filter(SessionFormation.formation_id == str(formation_id))
        if statut:
            query = query.filter(SessionFormation.statut == statut)
        if date_debut:
            query = query.filter(SessionFormation.date_debut >= date_debut)
        return query.offset(skip).limit(limit).all()

    def update_session(
        self,
        session_id: UUID,
        session: SessionFormationUpdate
    ) -> Optional[SessionFormation]:
        """Mettre à jour une session"""
        db_session = self.get_session(session_id)
        if db_session:
            for key, value in session.dict(exclude_unset=True).items():
                setattr(db_session, key, value)
            self.db.commit()
            self.db.refresh(db_session)
        return db_session

    def delete_session(self, session_id: UUID) -> bool:
        """Supprimer une session"""
        db_session = self.get_session(session_id)
        if db_session:
            self.db.delete(db_session)
            self.db.commit()
            return True
        return False

    # Participation Formation CRUD
    def create_participation(
        self,
        participation: ParticipationFormationCreate
    ) -> ParticipationFormation:
        """Créer une nouvelle participation"""
        db_participation = ParticipationFormation(**participation.dict())
        self.db.add(db_participation)
        self.db.commit()
        self.db.refresh(db_participation)
        return db_participation

    def get_participation(
        self,
        participation_id: UUID
    ) -> Optional[ParticipationFormation]:
        """Récupérer une participation par son ID"""
        return self.db.query(ParticipationFormation).filter(
            ParticipationFormation.id == str(participation_id)
        ).first()

    def get_participations(
        self,
        skip: int = 0,
        limit: int = 100,
        session_id: Optional[UUID] = None,
        employee_id: Optional[UUID] = None,
        statut: Optional[str] = None
    ) -> List[ParticipationFormation]:
        """Récupérer la liste des participations avec filtres optionnels"""
        query = self.db.query(ParticipationFormation)
        if session_id:
            query = query.filter(ParticipationFormation.session_id == str(session_id))
        if employee_id:
            query = query.filter(ParticipationFormation.employee_id == str(employee_id))
        if statut:
            query = query.filter(ParticipationFormation.statut == statut)
        return query.offset(skip).limit(limit).all()

    def update_participation(
        self,
        participation_id: UUID,
        participation: ParticipationFormationUpdate
    ) -> Optional[ParticipationFormation]:
        """Mettre à jour une participation"""
        db_participation = self.get_participation(participation_id)
        if db_participation:
            for key, value in participation.dict(exclude_unset=True).items():
                setattr(db_participation, key, value)
            self.db.commit()
            self.db.refresh(db_participation)
        return db_participation

    def delete_participation(self, participation_id: UUID) -> bool:
        """Supprimer une participation"""
        db_participation = self.get_participation(participation_id)
        if db_participation:
            self.db.delete(db_participation)
            self.db.commit()
            return True
        return False

    # Evaluation CRUD
    def create_evaluation(self, evaluation: EvaluationCreate) -> Evaluation:
        """Créer une nouvelle évaluation"""
        db_evaluation = Evaluation(**evaluation.dict())
        self.db.add(db_evaluation)
        self.db.commit()
        self.db.refresh(db_evaluation)
        return db_evaluation

    def get_evaluation(self, evaluation_id: UUID) -> Optional[Evaluation]:
        """Récupérer une évaluation par son ID"""
        return self.db.query(Evaluation).filter(
            Evaluation.id == str(evaluation_id)
        ).first()

    def get_evaluations(
        self,
        skip: int = 0,
        limit: int = 100,
        employee_id: Optional[UUID] = None,
        evaluateur_id: Optional[UUID] = None,
        type: Optional[str] = None,
        statut: Optional[str] = None,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None
    ) -> List[Evaluation]:
        """Récupérer la liste des évaluations avec filtres optionnels"""
        query = self.db.query(Evaluation)
        if employee_id:
            query = query.filter(Evaluation.employee_id == str(employee_id))
        if evaluateur_id:
            query = query.filter(Evaluation.evaluateur_id == str(evaluateur_id))
        if type:
            query = query.filter(Evaluation.type == type)
        if statut:
            query = query.filter(Evaluation.statut == statut)
        if date_debut:
            query = query.filter(Evaluation.date_evaluation >= date_debut)
        if date_fin:
            query = query.filter(Evaluation.date_evaluation <= date_fin)
        return query.offset(skip).limit(limit).all()

    def update_evaluation(
        self,
        evaluation_id: UUID,
        evaluation: EvaluationUpdate
    ) -> Optional[Evaluation]:
        """Mettre à jour une évaluation"""
        db_evaluation = self.get_evaluation(evaluation_id)
        if db_evaluation:
            for key, value in evaluation.dict(exclude_unset=True).items():
                setattr(db_evaluation, key, value)
            self.db.commit()
            self.db.refresh(db_evaluation)
        return db_evaluation

    def delete_evaluation(self, evaluation_id: UUID) -> bool:
        """Supprimer une évaluation"""
        db_evaluation = self.get_evaluation(evaluation_id)
        if db_evaluation:
            self.db.delete(db_evaluation)
            self.db.commit()
            return True
        return False

    # Méthodes métier spécifiques
    def get_employee_formations(
        self,
        employee_id: UUID,
        statut: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Récupérer l'historique des formations d'un employé"""
        query = self.db.query(
            Formation,
            SessionFormation,
            ParticipationFormation
        ).join(
            SessionFormation,
            Formation.id == SessionFormation.formation_id
        ).join(
            ParticipationFormation,
            SessionFormation.id == ParticipationFormation.session_id
        ).filter(
            ParticipationFormation.employee_id == str(employee_id)
        )

        if statut:
            query = query.filter(ParticipationFormation.statut == statut)
        if type:
            query = query.filter(Formation.type == type)

        results = []
        for formation, session, participation in query.all():
            results.append({
                "formation": formation,
                "session": session,
                "participation": participation
            })
        return results

    def get_employee_evaluations_summary(
        self,
        employee_id: UUID,
        date_debut: Optional[datetime] = None,
        date_fin: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Récupérer un résumé des évaluations d'un employé"""
        query = self.db.query(Evaluation).filter(
            Evaluation.employee_id == str(employee_id)
        )

        if date_debut:
            query = query.filter(Evaluation.date_evaluation >= date_debut)
        if date_fin:
            query = query.filter(Evaluation.date_evaluation <= date_fin)

        evaluations = query.all()
        
        if not evaluations:
            return {
                "nombre_evaluations": 0,
                "moyenne_globale": None,
                "progression": None,
                "points_forts": [],
                "points_amelioration": []
            }

        # Calcul des statistiques
        notes = [e.note_globale for e in evaluations if e.note_globale is not None]
        moyenne = sum(notes) / len(notes) if notes else None
        
        # Analyse de la progression
        if len(notes) >= 2:
            progression = notes[-1] - notes[0]
        else:
            progression = None

        # Agrégation des points forts et d'amélioration
        points_forts = []
        points_amelioration = []
        for e in evaluations:
            if e.points_forts:
                points_forts.extend(e.points_forts.split(','))
            if e.points_amelioration:
                points_amelioration.extend(e.points_amelioration.split(','))

        return {
            "nombre_evaluations": len(evaluations),
            "moyenne_globale": moyenne,
            "progression": progression,
            "points_forts": list(set(points_forts)),
            "points_amelioration": list(set(points_amelioration))
        }

    def get_formation_statistics(
        self,
        formation_id: UUID
    ) -> Dict[str, Any]:
        """Récupérer les statistiques d'une formation"""
        sessions = self.db.query(SessionFormation).filter(
            SessionFormation.formation_id == str(formation_id)
        ).all()

        if not sessions:
            return {
                "nombre_sessions": 0,
                "nombre_participants": 0,
                "taux_reussite": None,
                "note_moyenne": None
            }

        participations = []
        for session in sessions:
            participations.extend(
                self.db.query(ParticipationFormation).filter(
                    ParticipationFormation.session_id == session.id
                ).all()
            )

        nombre_participants = len(participations)
        if nombre_participants == 0:
            return {
                "nombre_sessions": len(sessions),
                "nombre_participants": 0,
                "taux_reussite": None,
                "note_moyenne": None
            }

        certifications = [p for p in participations if p.certification_obtenue]
        notes = [p.note for p in participations if p.note is not None]

        return {
            "nombre_sessions": len(sessions),
            "nombre_participants": nombre_participants,
            "taux_reussite": len(certifications) / nombre_participants * 100 if certifications else 0,
            "note_moyenne": sum(notes) / len(notes) if notes else None
        }
