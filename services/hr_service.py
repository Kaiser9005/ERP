"""Service de gestion des ressources humaines."""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.hr import (
    Employe, Contrat, Conge, Presence,
    DepartementType, StatutEmploye, TypeContrat, TypeConge, StatutConge, TypePresence
)
from models import (
    CompetenceAgricole, CertificationAgricole, AffectationParcelle,
    ConditionTravailAgricole, FormationAgricole, EvaluationAgricole,
    TypePersonnel, SpecialiteAgricole, NiveauCompetence, TypeCertification
)

class HRService:
    """Service de gestion des ressources humaines."""

    def __init__(self, db: Session):
        self.db = db

    async def get_stats(self) -> Dict[str, Any]:
        """Récupère les statistiques RH."""
        total = self.db.query(Employe).count()
        actifs = self.db.query(Employe).filter(
            Employe.statut == StatutEmploye.ACTIF
        ).count()
        en_conge = self.db.query(Employe).filter(
            Employe.statut == StatutEmploye.CONGE
        ).count()

        return {
            "effectif_total": total,
            "actifs": actifs,
            "en_conge": en_conge
        }

    async def creer_employe(self, employe_data: Dict[str, Any]) -> Employe:
        """Crée un nouvel employé."""
        employe = Employe(
            **employe_data,
            statut=StatutEmploye.ACTIF
        )
        self.db.add(employe)
        
        try:
            self.db.commit()
            self.db.refresh(employe)
            return employe
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def create_leave_request(self, conge_data: Dict[str, Any]) -> Conge:
        """Crée une demande de congé."""
        # Calcul du nombre de jours
        date_debut = conge_data["date_debut"]
        date_fin = conge_data["date_fin"]
        nb_jours = (date_fin - date_debut).days + 1

        conge = Conge(
            **conge_data,
            nb_jours=nb_jours,
            statut=StatutConge.EN_ATTENTE
        )
        self.db.add(conge)
        
        try:
            self.db.commit()
            self.db.refresh(conge)
            return conge
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def track_attendance(self, presence_data: Dict[str, Any]) -> Presence:
        """Enregistre une présence."""
        # Calcul des heures travaillées
        heure_arrivee = presence_data["heure_arrivee"]
        heure_depart = presence_data["heure_depart"]
        heures_travaillees = (heure_depart - heure_arrivee).total_seconds() / 3600

        presence = Presence(
            **presence_data,
            heures_travaillees=heures_travaillees
        )
        self.db.add(presence)
        
        try:
            self.db.commit()
            self.db.refresh(presence)
            return presence
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def approve_leave_request(
        self,
        conge_id: str,
        approuve_par_id: str
    ) -> Conge:
        """Approuve une demande de congé."""
        conge = self.db.query(Conge).filter(Conge.id == conge_id).first()
        if not conge:
            raise HTTPException(status_code=404, detail="Congé non trouvé")

        conge.statut = StatutConge.APPROUVE
        conge.approuve_par_id = approuve_par_id
        conge.date_approbation = datetime.utcnow()

        # Mise à jour du statut de l'employé à la date de début
        employe = self.db.query(Employe).filter(
            Employe.id == conge.employe_id
        ).first()
        
        if not employe:
            raise HTTPException(status_code=404, detail="Employé non trouvé")

        try:
            self.db.commit()
            self.db.refresh(conge)
            return conge
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def reject_leave_request(
        self,
        conge_id: str,
        rejete_par_id: str,
        motif_rejet: str
    ) -> Conge:
        """Rejette une demande de congé."""
        conge = self.db.query(Conge).filter(Conge.id == conge_id).first()
        if not conge:
            raise HTTPException(status_code=404, detail="Congé non trouvé")

        conge.statut = StatutConge.REJETE
        conge.rejete_par_id = rejete_par_id
        conge.motif_rejet = motif_rejet
        conge.date_rejet = datetime.utcnow()

        try:
            self.db.commit()
            self.db.refresh(conge)
            return conge
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_conges_employe(
        self,
        employe_id: str,
        annee: Optional[int] = None
    ) -> List[Conge]:
        """Récupère les congés d'un employé."""
        query = self.db.query(Conge).filter(Conge.employe_id == employe_id)
        
        if annee:
            query = query.filter(
                func.extract('year', Conge.date_debut) == annee
            )

        return query.all()

    async def get_presences_employe(
        self,
        employe_id: str,
        date_debut: datetime,
        date_fin: datetime
    ) -> List[Presence]:
        """Récupère les présences d'un employé."""
        return self.db.query(Presence).filter(
            Presence.employe_id == employe_id,
            Presence.date >= date_debut,
            Presence.date <= date_fin
        ).all()

    async def get_department_stats(
        self,
        departement: DepartementType
    ) -> Dict[str, Any]:
        """Récupère les statistiques d'un département."""
        employes = self.db.query(Employe).filter(
            Employe.departement == departement
        ).all()

        total = len(employes)
        actifs = sum(1 for e in employes if e.statut == StatutEmploye.ACTIF)
        en_conge = sum(1 for e in employes if e.statut == StatutEmploye.CONGE)

        # Calcul de la masse salariale
        masse_salariale = sum(e.salaire_base for e in employes)

        return {
            "departement": departement,
            "effectif_total": total,
            "actifs": actifs,
            "en_conge": en_conge,
            "masse_salariale": masse_salariale
        }

    async def add_competence_agricole(self, competence_data: Dict[str, Any]) -> CompetenceAgricole:
        """Ajoute une compétence agricole à un employé."""
        competence = CompetenceAgricole(**competence_data)
        self.db.add(competence)
        
        try:
            self.db.commit()
            self.db.refresh(competence)
            return competence
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def add_certification_agricole(self, certification_data: Dict[str, Any]) -> CertificationAgricole:
        """Ajoute une certification agricole."""
        certification = CertificationAgricole(**certification_data)
        self.db.add(certification)
        
        try:
            self.db.commit()
            self.db.refresh(certification)
            return certification
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def create_affectation_parcelle(self, affectation_data: Dict[str, Any]) -> AffectationParcelle:
        """Crée une affectation à une parcelle."""
        affectation = AffectationParcelle(**affectation_data)
        self.db.add(affectation)
        
        try:
            self.db.commit()
            self.db.refresh(affectation)
            return affectation
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def track_conditions_travail(self, conditions_data: Dict[str, Any]) -> ConditionTravailAgricole:
        """Enregistre les conditions de travail agricoles."""
        conditions = ConditionTravailAgricole(**conditions_data)
        self.db.add(conditions)
        
        try:
            self.db.commit()
            self.db.refresh(conditions)
            return conditions
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def add_formation_agricole_details(self, formation_data: Dict[str, Any]) -> FormationAgricole:
        """Ajoute les détails agricoles à une formation."""
        formation = FormationAgricole(**formation_data)
        self.db.add(formation)
        
        try:
            self.db.commit()
            self.db.refresh(formation)
            return formation
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def add_evaluation_agricole_details(self, evaluation_data: Dict[str, Any]) -> EvaluationAgricole:
        """Ajoute les détails agricoles à une évaluation."""
        evaluation = EvaluationAgricole(**evaluation_data)
        self.db.add(evaluation)
        
        try:
            self.db.commit()
            self.db.refresh(evaluation)
            return evaluation
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
