"""
Endpoints API pour la gestion des fonctionnalités RH agricoles
"""

from datetime import date
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.database import get_db
from services.hr_agricole_service import HRAgricoleService
from schemas.hr_agricole import (
    CompetenceAgricoleCreate, CompetenceAgricoleUpdate, CompetenceAgricoleInDB,
    CertificationAgricoleCreate, CertificationAgricoleUpdate, CertificationAgricoleInDB,
    AffectationParcelleCreate, AffectationParcelleUpdate, AffectationParcelleInDB,
    ConditionTravailAgricoleCreate, ConditionTravailAgricoleUpdate, ConditionTravailAgricoleInDB,
    FormationAgricoleCreate, FormationAgricoleUpdate, FormationAgricoleInDB,
    EvaluationAgricoleCreate, EvaluationAgricoleUpdate, EvaluationAgricoleInDB
)

router = APIRouter(prefix="/hr-agricole", tags=["RH Agricole"])

# Dépendances
def get_hr_agricole_service(db: Session = Depends(get_db)) -> HRAgricoleService:
    return HRAgricoleService(db)

# Endpoints Compétences
@router.post("/competences/", response_model=CompetenceAgricoleInDB, status_code=status.HTTP_201_CREATED)
def create_competence(
    competence: CompetenceAgricoleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle compétence agricole"""
    return service.create_competence(competence)

@router.get("/competences/{competence_id}", response_model=CompetenceAgricoleInDB)
def get_competence(
    competence_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une compétence par son ID"""
    competence = service.get_competence(competence_id)
    if not competence:
        raise HTTPException(status_code=404, detail="Compétence non trouvée")
    return competence

@router.get("/employes/{employe_id}/competences/", response_model=List[CompetenceAgricoleInDB])
def get_competences_employe(
    employe_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère toutes les compétences d'un employé"""
    return service.get_competences_employe(employe_id)

@router.put("/competences/{competence_id}", response_model=CompetenceAgricoleInDB)
def update_competence(
    competence_id: str,
    competence: CompetenceAgricoleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une compétence"""
    updated = service.update_competence(competence_id, competence)
    if not updated:
        raise HTTPException(status_code=404, detail="Compétence non trouvée")
    return updated

# Endpoints Certifications
@router.post("/certifications/", response_model=CertificationAgricoleInDB, status_code=status.HTTP_201_CREATED)
def create_certification(
    certification: CertificationAgricoleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle certification agricole"""
    return service.create_certification(certification)

@router.get("/certifications/{certification_id}", response_model=CertificationAgricoleInDB)
def get_certification(
    certification_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une certification par son ID"""
    certification = service.get_certification(certification_id)
    if not certification:
        raise HTTPException(status_code=404, detail="Certification non trouvée")
    return certification

@router.get("/competences/{competence_id}/certifications/", response_model=List[CertificationAgricoleInDB])
def get_certifications_competence(
    competence_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère toutes les certifications d'une compétence"""
    return service.get_certifications_competence(competence_id)

@router.put("/certifications/{certification_id}", response_model=CertificationAgricoleInDB)
def update_certification(
    certification_id: str,
    certification: CertificationAgricoleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une certification"""
    updated = service.update_certification(certification_id, certification)
    if not updated:
        raise HTTPException(status_code=404, detail="Certification non trouvée")
    return updated

# Endpoints Affectations
@router.post("/affectations/", response_model=AffectationParcelleInDB, status_code=status.HTTP_201_CREATED)
def create_affectation(
    affectation: AffectationParcelleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle affectation"""
    return service.create_affectation(affectation)

@router.get("/affectations/{affectation_id}", response_model=AffectationParcelleInDB)
def get_affectation(
    affectation_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une affectation par son ID"""
    affectation = service.get_affectation(affectation_id)
    if not affectation:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    return affectation

@router.get("/employes/{employe_id}/affectations/", response_model=List[AffectationParcelleInDB])
def get_affectations_employe(
    employe_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère toutes les affectations d'un employé"""
    return service.get_affectations_employe(employe_id)

@router.get("/parcelles/{parcelle_id}/affectations/", response_model=List[AffectationParcelleInDB])
def get_affectations_parcelle(
    parcelle_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère toutes les affectations d'une parcelle"""
    return service.get_affectations_parcelle(parcelle_id)

@router.put("/affectations/{affectation_id}", response_model=AffectationParcelleInDB)
def update_affectation(
    affectation_id: str,
    affectation: AffectationParcelleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une affectation"""
    updated = service.update_affectation(affectation_id, affectation)
    if not updated:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    return updated

# Endpoints Conditions de travail
@router.post("/conditions-travail/", response_model=ConditionTravailAgricoleInDB, status_code=status.HTTP_201_CREATED)
def create_condition_travail(
    condition: ConditionTravailAgricoleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle condition de travail"""
    return service.create_condition_travail(condition)

@router.get("/conditions-travail/{condition_id}", response_model=ConditionTravailAgricoleInDB)
def get_condition_travail(
    condition_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une condition de travail par son ID"""
    condition = service.get_condition_travail(condition_id)
    if not condition:
        raise HTTPException(status_code=404, detail="Condition de travail non trouvée")
    return condition

@router.get("/employes/{employe_id}/conditions-travail/", response_model=List[ConditionTravailAgricoleInDB])
def get_conditions_travail_employe(
    employe_id: str,
    date_debut: date,
    date_fin: date,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère les conditions de travail d'un employé sur une période"""
    return service.get_conditions_travail_employe(employe_id, date_debut, date_fin)

@router.put("/conditions-travail/{condition_id}", response_model=ConditionTravailAgricoleInDB)
def update_condition_travail(
    condition_id: str,
    condition: ConditionTravailAgricoleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une condition de travail"""
    updated = service.update_condition_travail(condition_id, condition)
    if not updated:
        raise HTTPException(status_code=404, detail="Condition de travail non trouvée")
    return updated

# Endpoints Formations agricoles
@router.post("/formations-agricoles/", response_model=FormationAgricoleInDB, status_code=status.HTTP_201_CREATED)
def create_formation_agricole(
    formation: FormationAgricoleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle formation agricole"""
    return service.create_formation_agricole(formation)

@router.get("/formations-agricoles/{formation_id}", response_model=FormationAgricoleInDB)
def get_formation_agricole(
    formation_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une formation agricole par son ID"""
    formation = service.get_formation_agricole(formation_id)
    if not formation:
        raise HTTPException(status_code=404, detail="Formation agricole non trouvée")
    return formation

@router.get("/formations/{formation_id}/details-agricoles/", response_model=List[FormationAgricoleInDB])
def get_formations_agricoles_formation(
    formation_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère les détails agricoles d'une formation"""
    return service.get_formations_agricoles_formation(formation_id)

@router.put("/formations-agricoles/{formation_id}", response_model=FormationAgricoleInDB)
def update_formation_agricole(
    formation_id: str,
    formation: FormationAgricoleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une formation agricole"""
    updated = service.update_formation_agricole(formation_id, formation)
    if not updated:
        raise HTTPException(status_code=404, detail="Formation agricole non trouvée")
    return updated

# Endpoints Évaluations agricoles
@router.post("/evaluations-agricoles/", response_model=EvaluationAgricoleInDB, status_code=status.HTTP_201_CREATED)
def create_evaluation_agricole(
    evaluation: EvaluationAgricoleCreate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Crée une nouvelle évaluation agricole"""
    return service.create_evaluation_agricole(evaluation)

@router.get("/evaluations-agricoles/{evaluation_id}", response_model=EvaluationAgricoleInDB)
def get_evaluation_agricole(
    evaluation_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère une évaluation agricole par son ID"""
    evaluation = service.get_evaluation_agricole(evaluation_id)
    if not evaluation:
        raise HTTPException(status_code=404, detail="Évaluation agricole non trouvée")
    return evaluation

@router.get("/evaluations/{evaluation_id}/details-agricoles/", response_model=List[EvaluationAgricoleInDB])
def get_evaluations_agricoles_evaluation(
    evaluation_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère les détails agricoles d'une évaluation"""
    return service.get_evaluations_agricoles_evaluation(evaluation_id)

@router.put("/evaluations-agricoles/{evaluation_id}", response_model=EvaluationAgricoleInDB)
def update_evaluation_agricole(
    evaluation_id: str,
    evaluation: EvaluationAgricoleUpdate,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Met à jour une évaluation agricole"""
    updated = service.update_evaluation_agricole(evaluation_id, evaluation)
    if not updated:
        raise HTTPException(status_code=404, detail="Évaluation agricole non trouvée")
    return updated

# Endpoints utilitaires
@router.get("/competences/{competence_id}/validite/")
def check_competence_validite(
    competence_id: str,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Vérifie si une compétence est toujours valide"""
    return {"valide": service.check_competence_validite(competence_id)}

@router.get("/competences/a-renouveler/", response_model=List[CompetenceAgricoleInDB])
def get_competences_a_renouveler(
    delai_jours: int = 30,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère les compétences à renouveler dans un délai donné"""
    return service.get_competences_a_renouveler(delai_jours)

@router.get("/certifications/a-renouveler/", response_model=List[CertificationAgricoleInDB])
def get_certifications_a_renouveler(
    delai_jours: int = 30,
    service: HRAgricoleService = Depends(get_hr_agricole_service)
):
    """Récupère les certifications à renouveler dans un délai donné"""
    return service.get_certifications_a_renouveler(delai_jours)
