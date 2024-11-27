from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from services.hr_formation_service import HRFormationService
from schemas.hr_formation import (
    Formation, FormationCreate, FormationUpdate,
    SessionFormation, SessionFormationCreate, SessionFormationUpdate,
    ParticipationFormation, ParticipationFormationCreate, ParticipationFormationUpdate,
    Evaluation, EvaluationCreate, EvaluationUpdate
)

router = APIRouter(prefix="/hr/formation", tags=["Formation et Évaluation"])

# Endpoints Formation
@router.post("/formations/", response_model=Formation)
def create_formation(
    formation: FormationCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle formation"""
    service = HRFormationService(db)
    return service.create_formation(formation)

@router.get("/formations/", response_model=List[Formation])
def get_formations(
    skip: int = 0,
    limit: int = 100,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des formations"""
    service = HRFormationService(db)
    return service.get_formations(skip=skip, limit=limit, type=type)

@router.get("/formations/{formation_id}", response_model=Formation)
def get_formation(
    formation_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupérer une formation par son ID"""
    service = HRFormationService(db)
    formation = service.get_formation(formation_id)
    if not formation:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return formation

@router.put("/formations/{formation_id}", response_model=Formation)
def update_formation(
    formation_id: UUID,
    formation: FormationUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une formation"""
    service = HRFormationService(db)
    updated = service.update_formation(formation_id, formation)
    if not updated:
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return updated

@router.delete("/formations/{formation_id}")
def delete_formation(
    formation_id: UUID,
    db: Session = Depends(get_db)
):
    """Supprimer une formation"""
    service = HRFormationService(db)
    if not service.delete_formation(formation_id):
        raise HTTPException(status_code=404, detail="Formation non trouvée")
    return {"message": "Formation supprimée"}

# Endpoints Session Formation
@router.post("/sessions/", response_model=SessionFormation)
def create_session(
    session: SessionFormationCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle session de formation"""
    service = HRFormationService(db)
    return service.create_session(session)

@router.get("/sessions/", response_model=List[SessionFormation])
def get_sessions(
    skip: int = 0,
    limit: int = 100,
    formation_id: Optional[UUID] = None,
    statut: Optional[str] = None,
    date_debut: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des sessions"""
    service = HRFormationService(db)
    return service.get_sessions(
        skip=skip,
        limit=limit,
        formation_id=formation_id,
        statut=statut,
        date_debut=date_debut
    )

@router.get("/sessions/{session_id}", response_model=SessionFormation)
def get_session(
    session_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupérer une session par son ID"""
    service = HRFormationService(db)
    session = service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return session

@router.put("/sessions/{session_id}", response_model=SessionFormation)
def update_session(
    session_id: UUID,
    session: SessionFormationUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une session"""
    service = HRFormationService(db)
    updated = service.update_session(session_id, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return updated

@router.delete("/sessions/{session_id}")
def delete_session(
    session_id: UUID,
    db: Session = Depends(get_db)
):
    """Supprimer une session"""
    service = HRFormationService(db)
    if not service.delete_session(session_id):
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return {"message": "Session supprimée"}

# Endpoints Participation Formation
@router.post("/participations/", response_model=ParticipationFormation)
def create_participation(
    participation: ParticipationFormationCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle participation"""
    service = HRFormationService(db)
    return service.create_participation(participation)

@router.get("/participations/", response_model=List[ParticipationFormation])
def get_participations(
    skip: int = 0,
    limit: int = 100,
    session_id: Optional[UUID] = None,
    employee_id: Optional[UUID] = None,
    statut: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des participations"""
    service = HRFormationService(db)
    return service.get_participations(
        skip=skip,
        limit=limit,
        session_id=session_id,
        employee_id=employee_id,
        statut=statut
    )

@router.get("/participations/{participation_id}", response_model=ParticipationFormation)
def get_participation(
    participation_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupérer une participation par son ID"""
    service = HRFormationService(db)
    participation = service.get_participation(participation_id)
    if not participation:
        raise HTTPException(status_code=404, detail="Participation non trouvée")
    return participation

@router.put("/participations/{participation_id}", response_model=ParticipationFormation)
def update_participation(
    participation_id: UUID,
    participation: ParticipationFormationUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une participation"""
    service = HRFormationService(db)
    updated = service.update_participation(participation_id, participation)
    if not updated:
        raise HTTPException(status_code=404, detail="Participation non trouvée")
    return updated

@router.delete("/participations/{participation_id}")
def delete_participation(
    participation_id: UUID,
    db: Session = Depends(get_db)
):
    """Supprimer une participation"""
    service = HRFormationService(db)
    if not service.delete_participation(participation_id):
        raise HTTPException(status_code=404, detail="Participation non trouvée")
    return {"message": "Participation supprimée"}

# Endpoints Evaluation
@router.post("/evaluations/", response_model=Evaluation)
def create_evaluation(
    evaluation: EvaluationCreate,
    db: Session = Depends(get_db)
):
    """Créer une nouvelle évaluation"""
    service = HRFormationService(db)
    return service.create_evaluation(evaluation)

@router.get("/evaluations/", response_model=List[Evaluation])
def get_evaluations(
    skip: int = 0,
    limit: int = 100,
    employee_id: Optional[UUID] = None,
    evaluateur_id: Optional[UUID] = None,
    type: Optional[str] = None,
    statut: Optional[str] = None,
    date_debut: Optional[datetime] = None,
    date_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Récupérer la liste des évaluations"""
    service = HRFormationService(db)
    return service.get_evaluations(
        skip=skip,
        limit=limit,
        employee_id=employee_id,
        evaluateur_id=evaluateur_id,
        type=type,
        statut=statut,
        date_debut=date_debut,
        date_fin=date_fin
    )

@router.get("/evaluations/{evaluation_id}", response_model=Evaluation)
def get_evaluation(
    evaluation_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupérer une évaluation par son ID"""
    service = HRFormationService(db)
    evaluation = service.get_evaluation(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Évaluation non trouvée")
    return evaluation

@router.put("/evaluations/{evaluation_id}", response_model=Evaluation)
def update_evaluation(
    evaluation_id: UUID,
    evaluation: EvaluationUpdate,
    db: Session = Depends(get_db)
):
    """Mettre à jour une évaluation"""
    service = HRFormationService(db)
    updated = service.update_evaluation(evaluation_id, evaluation)
    if not updated:
        raise HTTPException(status_code=404, detail="Évaluation non trouvée")
    return updated

@router.delete("/evaluations/{evaluation_id}")
def delete_evaluation(
    evaluation_id: UUID,
    db: Session = Depends(get_db)
):
    """Supprimer une évaluation"""
    service = HRFormationService(db)
    if not service.delete_evaluation(evaluation_id):
        raise HTTPException(status_code=404, detail="Évaluation non trouvée")
    return {"message": "Évaluation supprimée"}

# Endpoints Statistiques et Rapports
@router.get("/employee/{employee_id}/formations")
def get_employee_formations_history(
    employee_id: UUID,
    statut: Optional[str] = None,
    type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Récupérer l'historique des formations d'un employé"""
    service = HRFormationService(db)
    return service.get_employee_formations(
        employee_id=employee_id,
        statut=statut,
        type=type
    )

@router.get("/employee/{employee_id}/evaluations/summary")
def get_employee_evaluations_summary(
    employee_id: UUID,
    date_debut: Optional[datetime] = None,
    date_fin: Optional[datetime] = None,
    db: Session = Depends(get_db)
):
    """Récupérer un résumé des évaluations d'un employé"""
    service = HRFormationService(db)
    return service.get_employee_evaluations_summary(
        employee_id=employee_id,
        date_debut=date_debut,
        date_fin=date_fin
    )

@router.get("/formations/{formation_id}/statistics")
def get_formation_statistics(
    formation_id: UUID,
    db: Session = Depends(get_db)
):
    """Récupérer les statistiques d'une formation"""
    service = HRFormationService(db)
    return service.get_formation_statistics(formation_id)
