from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from models.comptabilite import (
    CompteComptable, EcritureComptable, JournalComptable,
    ExerciceComptable, TypeCompte, StatutEcriture
)
from sqlalchemy import func, and_, or_
from decimal import Decimal
from .comptabilite_stats_service import ComptabiliteStatsService

class ComptabiliteService:
    def __init__(self, db: Session):
        self.db = db
        self.stats_service = ComptabiliteStatsService(db)

    async def create_compte(self, compte_data: Dict[str, Any]) -> CompteComptable:
        """Crée un nouveau compte comptable"""
        compte = CompteComptable(**compte_data)
        self.db.add(compte)
        self.db.commit()
        self.db.refresh(compte)
        return compte

    async def create_ecriture(self, ecriture_data: Dict[str, Any]) -> EcritureComptable:
        """Crée une nouvelle écriture comptable"""
        # Vérification de l'exercice
        exercice = await self._get_exercice_for_date(ecriture_data["date_ecriture"])
        if not exercice or exercice.cloture:
            raise ValueError("Exercice comptable non disponible ou clôturé")

        ecriture = EcritureComptable(**ecriture_data)
        ecriture.periode = ecriture_data["date_ecriture"].strftime("%Y-%m")
        
        self.db.add(ecriture)
        await self._update_compte_soldes(ecriture)
        self.db.commit()
        self.db.refresh(ecriture)
        return ecriture

    async def valider_ecriture(self, ecriture_id: str, validee_par_id: str) -> EcritureComptable:
        """Valide une écriture comptable"""
        ecriture = self.db.query(EcritureComptable).filter(
            EcritureComptable.id == ecriture_id
        ).first()
        
        if not ecriture:
            raise ValueError("Écriture non trouvée")
        
        if ecriture.statut != StatutEcriture.BROUILLON:
            raise ValueError("Seules les écritures en brouillon peuvent être validées")

        ecriture.statut = StatutEcriture.VALIDEE
        ecriture.validee_par_id = validee_par_id
        ecriture.date_validation = datetime.utcnow()
        
        self.db.commit()
        self.db.refresh(ecriture)
        return ecriture

    async def get_grand_livre(
        self,
        compte_id: Optional[str] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Génère le grand livre pour un compte ou tous les comptes"""
        query = self.db.query(EcritureComptable)

        if compte_id:
            query = query.filter(EcritureComptable.compte_id == compte_id)
        if date_debut:
            query = query.filter(EcritureComptable.date_ecriture >= date_debut)
        if date_fin:
            query = query.filter(EcritureComptable.date_ecriture <= date_fin)

        query = query.order_by(
            EcritureComptable.compte_id,
            EcritureComptable.date_ecriture,
            EcritureComptable.id
        )

        ecritures = query.all()
        grand_livre = []
        solde = Decimal('0')

        for ecriture in ecritures:
            solde += (ecriture.debit or 0) - (ecriture.credit or 0)
            grand_livre.append({
                "date": ecriture.date_ecriture,
                "piece": ecriture.numero_piece,
                "libelle": ecriture.libelle,
                "debit": float(ecriture.debit or 0),
                "credit": float(ecriture.credit or 0),
                "solde": float(solde)
            })

        return grand_livre

    async def get_balance_generale(
        self,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Génère la balance générale des comptes"""
        query = self.db.query(
            EcritureComptable.compte_id,
            func.sum(EcritureComptable.debit).label('total_debit'),
            func.sum(EcritureComptable.credit).label('total_credit')
        )

        if date_debut:
            query = query.filter(EcritureComptable.date_ecriture >= date_debut)
        if date_fin:
            query = query.filter(EcritureComptable.date_ecriture <= date_fin)

        query = query.group_by(EcritureComptable.compte_id)
        
        resultats = query.all()
        balance = []

        for resultat in resultats:
            compte = self.db.query(CompteComptable).get(resultat.compte_id)
            balance.append({
                "compte": {
                    "numero": compte.numero,
                    "libelle": compte.libelle,
                    "type": compte.type_compte
                },
                "debit": float(resultat.total_debit or 0),
                "credit": float(resultat.total_credit or 0),
                "solde": float((resultat.total_debit or 0) - (resultat.total_credit or 0))
            })

        return balance

    async def get_journal(
        self,
        journal_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[EcritureComptable]:
        """Récupère les écritures d'un journal comptable"""
        query = self.db.query(EcritureComptable).filter(
            EcritureComptable.journal_id == journal_id
        )

        if date_debut:
            query = query.filter(EcritureComptable.date_ecriture >= date_debut)
        if date_fin:
            query = query.filter(EcritureComptable.date_ecriture <= date_fin)

        return query.order_by(EcritureComptable.date_ecriture).all()

    async def cloturer_exercice(self, annee: str, cloture_par_id: str) -> ExerciceComptable:
        """Clôture un exercice comptable"""
        exercice = self.db.query(ExerciceComptable).filter(
            ExerciceComptable.annee == annee
        ).first()

        if not exercice:
            raise ValueError("Exercice non trouvé")
        
        if exercice.cloture:
            raise ValueError("Exercice déjà clôturé")

        # Vérification de l'équilibre des comptes
        balance = await self.get_balance_generale(
            date_debut=exercice.date_debut,
            date_fin=exercice.date_fin
        )
        
        total_debit = sum(compte["debit"] for compte in balance)
        total_credit = sum(compte["credit"] for compte in balance)
        
        if total_debit != total_credit:
            raise ValueError("Les comptes ne sont pas équilibrés")

        exercice.cloture = True
        exercice.date_cloture = datetime.utcnow()
        exercice.cloture_par_id = cloture_par_id
        
        self.db.commit()
        self.db.refresh(exercice)
        return exercice

    async def _get_exercice_for_date(self, date_ecriture: date) -> Optional[ExerciceComptable]:
        """Récupère l'exercice comptable correspondant à une date"""
        return self.db.query(ExerciceComptable).filter(
            and_(
                ExerciceComptable.date_debut <= date_ecriture,
                ExerciceComptable.date_fin >= date_ecriture
            )
        ).first()

    async def _update_compte_soldes(self, ecriture: EcritureComptable):
        """Met à jour les soldes du compte après une écriture"""
        compte = self.db.query(CompteComptable).get(ecriture.compte_id)
        if not compte:
            raise ValueError("Compte non trouvé")

        compte.solde_debit += ecriture.debit or 0
        compte.solde_credit += ecriture.credit or 0

    async def get_bilan(self, date_fin: date) -> Dict[str, Any]:
        """Génère le bilan comptable"""
        bilan = {
            "actif": {},
            "passif": {},
            "total_actif": 0,
            "total_passif": 0
        }

        # Calcul de l'actif
        comptes_actif = self.db.query(CompteComptable).filter(
            CompteComptable.type_compte == TypeCompte.ACTIF
        ).all()

        for compte in comptes_actif:
            solde = float(compte.solde_debit - compte.solde_credit)
            if solde != 0:
                bilan["actif"][compte.numero] = {
                    "libelle": compte.libelle,
                    "montant": solde
                }
                bilan["total_actif"] += solde

        # Calcul du passif
        comptes_passif = self.db.query(CompteComptable).filter(
            CompteComptable.type_compte == TypeCompte.PASSIF
        ).all()

        for compte in comptes_passif:
            solde = float(compte.solde_credit - compte.solde_debit)
            if solde != 0:
                bilan["passif"][compte.numero] = {
                    "libelle": compte.libelle,
                    "montant": solde
                }
                bilan["total_passif"] += solde

        return bilan

    async def get_compte_resultat(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Génère le compte de résultat"""
        resultat = {
            "produits": {},
            "charges": {},
            "total_produits": 0,
            "total_charges": 0,
            "resultat_net": 0
        }

        # Calcul des produits
        comptes_produits = self.db.query(CompteComptable).filter(
            CompteComptable.type_compte == TypeCompte.PRODUIT
        ).all()

        for compte in comptes_produits:
            solde = float(compte.solde_credit - compte.solde_debit)
            if solde != 0:
                resultat["produits"][compte.numero] = {
                    "libelle": compte.libelle,
                    "montant": solde
                }
                resultat["total_produits"] += solde

        # Calcul des charges
        comptes_charges = self.db.query(CompteComptable).filter(
            CompteComptable.type_compte == TypeCompte.CHARGE
        ).all()

        for compte in comptes_charges:
            solde = float(compte.solde_debit - compte.solde_credit)
            if solde != 0:
                resultat["charges"][compte.numero] = {
                    "libelle": compte.libelle,
                    "montant": solde
                }
                resultat["total_charges"] += solde

        resultat["resultat_net"] = resultat["total_produits"] - resultat["total_charges"]
        return resultat

    # Méthodes déléguées au service de statistiques
    async def get_stats(self) -> Dict[str, Any]:
        """Délègue au service de statistiques"""
        return await self.stats_service.get_stats()

    async def get_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Délègue au service de statistiques"""
        return await self.stats_service.get_budget_analysis(periode)

    async def get_cashflow(self, days: int = 30) -> List[Dict[str, Any]]:
        """Délègue au service de statistiques"""
        return await self.stats_service.get_cashflow(days)
