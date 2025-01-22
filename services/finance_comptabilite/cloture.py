"""
Service de gestion des clôtures comptables
"""

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import pandas as pd

from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    JournalComptable,
    ExerciceComptable,
    StatutEcriture
)
from services.cache_service import cache_result

class GestionCloture:
    """Service de gestion des clôtures comptables"""

    def __init__(self, db: Session):
        self.db = db
        self._cache_duration = timedelta(minutes=15)

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def executer_cloture_mensuelle(self,
                                       exercice_id: int,
                                       mois: int) -> Dict:
        """Exécute la clôture mensuelle"""
        exercice = self.db.query(ExerciceComptable).get(exercice_id)
        if not exercice:
            return {
                "status": "error",
                "message": "Exercice non trouvé"
            }

        # Vérification des conditions de clôture
        conditions = await self._verifier_conditions_cloture(exercice, mois)
        if not conditions["peut_cloturer"]:
            return {
                "status": "error",
                "message": conditions["message"]
            }

        # Validation des écritures en attente
        validation = await self._valider_ecritures_attente(exercice, mois)
        if not validation["success"]:
            return {
                "status": "error",
                "message": validation["message"]
            }

        # Calcul des totaux
        totaux = await self._calculer_totaux_mensuels(exercice, mois)

        # Génération des écritures de clôture
        ecritures_cloture = await self._generer_ecritures_cloture(
            exercice,
            mois,
            totaux
        )

        # Mise à jour du statut
        await self._mettre_a_jour_statut_periode(exercice, mois, "CLOTURE")

        return {
            "status": "success",
            "totaux": totaux,
            "ecritures_cloture": ecritures_cloture,
            "date_cloture": datetime.now(datetime.timezone.utc).isoformat()
        }

    async def _verifier_conditions_cloture(self,
                                         exercice: ExerciceComptable,
                                         mois: int) -> Dict:
        """Vérifie les conditions pour la clôture"""
        # Vérification du statut de l'exercice
        if exercice.statut == "CLOTURE":
            return {
                "peut_cloturer": False,
                "message": "L'exercice est déjà clôturé"
            }

        # Vérification des écritures en attente
        ecritures_attente = self.db.query(EcritureComptable).filter(
            EcritureComptable.exercice_id == exercice.id,
            EcritureComptable.date.month == mois,
            EcritureComptable.statut == "ATTENTE"
        ).count()

        if ecritures_attente > 0:
            return {
                "peut_cloturer": False,
                "message": f"{ecritures_attente} écritures en attente"
            }

        # Vérification de l'équilibre des comptes
        if not await self._verifier_equilibre_comptes(exercice, mois):
            return {
                "peut_cloturer": False,
                "message": "Les comptes ne sont pas équilibrés"
            }

        return {
            "peut_cloturer": True,
            "message": "OK"
        }

    async def _valider_ecritures_attente(self,
                                       exercice: ExerciceComptable,
                                       mois: int) -> Dict:
        """Valide les écritures en attente"""
        try:
            # Récupération des écritures en attente
            ecritures = self.db.query(EcritureComptable).filter(
                EcritureComptable.exercice_id == exercice.id,
                EcritureComptable.date.month == mois,
                EcritureComptable.statut == "ATTENTE"
            ).all()

            # Validation des écritures
            for ecriture in ecritures:
                ecriture.statut = "VALIDE"
                ecriture.date_validation = datetime.now(datetime.timezone.utc)

            self.db.commit()

            return {
                "success": True,
                "message": f"{len(ecritures)} écritures validées"
            }

        except Exception as e:
            self.db.rollback()
            return {
                "success": False,
                "message": f"Erreur lors de la validation : {str(e)}"
            }

    async def _calculer_totaux_mensuels(self,
                                      exercice: ExerciceComptable,
                                      mois: int) -> Dict[str, float]:
        """Calcule les totaux mensuels par type de compte"""
        totaux = {}
        
        # Récupération de toutes les écritures du mois
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.exercice_id == exercice.id,
            EcritureComptable.date.month == mois,
            EcritureComptable.statut == "VALIDE"
        ).all()

        # Calcul des totaux par type de compte
        for ecriture in ecritures:
            type_compte = ecriture.compte.type
            if type_compte not in totaux:
                totaux[type_compte] = 0
            totaux[type_compte] += ecriture.montant

        return totaux

    async def _generer_ecritures_cloture(self,
                                       exercice: ExerciceComptable,
                                       mois: int,
                                       totaux: Dict[str, float]) -> List[Dict]:
        """Génère les écritures de clôture"""
        ecritures_cloture = []
        date_cloture = datetime.now(datetime.timezone.utc)

        # Création des écritures de clôture
        for type_compte, total in totaux.items():
            if total != 0:
                ecriture = EcritureComptable(
                    exercice_id=exercice.id,
                    compte_id=self._get_compte_cloture(type_compte).id,
                    journal_id=self._get_journal_cloture().id,
                    date=date_cloture,
                    montant=-total,  # Contre-passation
                    libelle=f"Clôture {type_compte} - {mois}/{exercice.annee}",
                    statut="VALIDE",
                    date_validation=date_cloture
                )
                self.db.add(ecriture)
                ecritures_cloture.append({
                    "type": type_compte,
                    "montant": -total
                })

        self.db.commit()
        return ecritures_cloture

    async def _mettre_a_jour_statut_periode(self,
                                          exercice: ExerciceComptable,
                                          mois: int,
                                          statut: str) -> None:
        """Met à jour le statut d'une période"""
        exercice.periodes_status = exercice.periodes_status or {}
        exercice.periodes_status[str(mois)] = {
            "statut": statut,
            "date_maj": datetime.now(datetime.timezone.utc).isoformat()
        }
        self.db.commit()

    async def _verifier_equilibre_comptes(self,
                                        exercice: ExerciceComptable,
                                        mois: int) -> bool:
        """Vérifie l'équilibre des comptes"""
        totaux = await self._calculer_totaux_mensuels(exercice, mois)
        total_debit = sum(t for t in totaux.values() if t > 0)
        total_credit = abs(sum(t for t in totaux.values() if t < 0))
        return abs(total_debit - total_credit) < 0.01  # Tolérance pour les arrondis

    def _get_compte_cloture(self, type_compte: str) -> CompteComptable:
        """Retourne le compte de clôture pour un type donné"""
        return self.db.query(CompteComptable).filter(
            CompteComptable.code.like("89%"),
            CompteComptable.type == type_compte
        ).first()

    def _get_journal_cloture(self) -> JournalComptable:
        """Retourne le journal de clôture"""
        return self.db.query(JournalComptable).filter(
            JournalComptable.code == "CLOT"
        ).first()