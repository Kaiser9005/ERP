"""
Service de gestion comptable avec ML et cache
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from models.comptabilite import (
    CompteComptable, EcritureComptable, JournalComptable,
    ExerciceComptable, TypeCompte, StatutEcriture
)
from sqlalchemy import func, and_, or_
from decimal import Decimal
from .comptabilite_stats_service import ComptabiliteStatsService
from .cache_service import CacheService
from .finance_comptabilite.analyse import AnalyseFinanceCompta

class ComptabiliteService:
    def __init__(self, db: Session):
        self.db = db
        self.stats_service = ComptabiliteStatsService(db)
        self.cache = CacheService()
        self.analyse = AnalyseFinanceCompta(db)

    async def create_compte(self, compte_data: Dict[str, Any]) -> CompteComptable:
        """Crée un nouveau compte comptable"""
        compte = CompteComptable(**compte_data)
        self.db.add(compte)
        self.db.commit()
        self.db.refresh(compte)
        
        # Invalidation cache
        await self._invalidate_cache()
        
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
        
        # Invalidation cache
        await self._invalidate_cache()
        
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
        ecriture.date_validation = datetime.now(datetime.timezone.utc)
        
        # Invalidation cache
        await self._invalidate_cache()
        
        self.db.commit()
        self.db.refresh(ecriture)
        return ecriture

    async def get_grand_livre(
        self,
        compte_id: Optional[str] = None,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Génère le grand livre avec cache"""
        # Clé de cache
        cache_key = f"grand_livre_{compte_id or 'all'}_{date_debut}_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

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

        # Mise en cache
        await self.cache.set(cache_key, grand_livre, expire=3600)
        
        return grand_livre

    async def get_balance_generale(
        self,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """Génère la balance générale avec cache"""
        # Clé de cache
        cache_key = f"balance_{date_debut}_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

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

        # Mise en cache
        await self.cache.set(cache_key, balance, expire=3600)
        
        return balance

    async def get_journal(
        self,
        journal_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> List[EcritureComptable]:
        """Récupère les écritures d'un journal avec cache"""
        # Clé de cache
        cache_key = f"journal_{journal_id}_{date_debut}_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        query = self.db.query(EcritureComptable).filter(
            EcritureComptable.journal_id == journal_id
        )

        if date_debut:
            query = query.filter(EcritureComptable.date_ecriture >= date_debut)
        if date_fin:
            query = query.filter(EcritureComptable.date_ecriture <= date_fin)

        ecritures = query.order_by(EcritureComptable.date_ecriture).all()
        
        # Mise en cache
        await self.cache.set(cache_key, ecritures, expire=3600)
        
        return ecritures

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
        exercice.date_cloture = datetime.now(datetime.timezone.utc)
        exercice.cloture_par_id = cloture_par_id
        
        # Invalidation cache
        await self._invalidate_cache()
        
        self.db.commit()
        self.db.refresh(exercice)
        return exercice

    async def get_bilan(self, date_fin: date) -> Dict[str, Any]:
        """Génère le bilan comptable avec ML"""
        # Clé de cache
        cache_key = f"bilan_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

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

        # Analyse ML
        ml_analysis = await self.analyse.get_analyse_parcelle(
            parcelle_id=None,
            date_debut=date_fin - timedelta(days=30),
            date_fin=date_fin
        )
        
        # Enrichissement ML
        bilan.update({
            "ml_analysis": ml_analysis["ml_analysis"],
            "recommendations": await self._generate_bilan_recommendations(
                bilan,
                ml_analysis
            )
        })
        
        # Mise en cache
        await self.cache.set(cache_key, bilan, expire=3600)
        
        return bilan

    async def get_compte_resultat(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Génère le compte de résultat avec ML"""
        # Clé de cache
        cache_key = f"resultat_{date_debut}_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

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

        # Analyse ML
        ml_analysis = await self.analyse.get_analyse_parcelle(
            parcelle_id=None,
            date_debut=date_debut,
            date_fin=date_fin
        )
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(target_date=date_fin)
        
        # Performance ML
        performance = await self.analyse.predict_performance(months_ahead=3)
        
        # Enrichissement ML
        resultat.update({
            "ml_analysis": ml_analysis["ml_analysis"],
            "optimization": optimization,
            "performance": performance,
            "recommendations": await self._generate_resultat_recommendations(
                resultat,
                ml_analysis,
                optimization,
                performance
            )
        })
        
        # Mise en cache
        await self.cache.set(cache_key, resultat, expire=3600)
        
        return resultat

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

    async def _invalidate_cache(self):
        """Invalide tous les caches comptables"""
        patterns = [
            "grand_livre_*",
            "balance_*",
            "journal_*",
            "bilan_*",
            "resultat_*"
        ]
        for pattern in patterns:
            await self.cache.delete_pattern(pattern)

    async def _generate_bilan_recommendations(
        self,
        bilan: Dict[str, Any],
        ml_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations pour le bilan"""
        recommendations = []
        
        # Analyse ratios
        ratio_liquidite = bilan["total_actif"] / bilan["total_passif"] if bilan["total_passif"] != 0 else 0
        if ratio_liquidite < 1.5:
            recommendations.append({
                "type": "RATIO",
                "priority": "HIGH",
                "description": "Ratio de liquidité faible",
                "actions": [
                    "Optimiser BFR",
                    "Réduire délais paiement",
                    "Négocier délais fournisseurs"
                ]
            })
            
        # Recommandations ML
        if "recommendations" in ml_analysis["ml_analysis"]:
            for rec in ml_analysis["ml_analysis"]["recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec.get("priority", "MEDIUM"),
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        return recommendations

    async def _generate_resultat_recommendations(
        self,
        resultat: Dict[str, Any],
        ml_analysis: Dict[str, Any],
        optimization: Dict[str, Any],
        performance: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations pour le compte de résultat"""
        recommendations = []
        
        # Analyse rentabilité
        marge = resultat["resultat_net"] / resultat["total_produits"] if resultat["total_produits"] != 0 else 0
        if marge < 0.1:
            recommendations.append({
                "type": "MARGIN",
                "priority": "HIGH",
                "description": "Marge nette faible",
                "actions": [
                    "Optimiser coûts",
                    "Revoir pricing",
                    "Analyser postes charges"
                ]
            })
            
        # Recommandations ML
        if "recommendations" in ml_analysis["ml_analysis"]:
            for rec in ml_analysis["ml_analysis"]["recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec.get("priority", "MEDIUM"),
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        # Recommandations optimisation
        if optimization["potential_savings"]:
            recommendations.append({
                "type": "OPTIMIZATION",
                "priority": "HIGH",
                "description": "Potentiel d'optimisation identifié",
                "actions": optimization["implementation_plan"],
                "expected_savings": optimization["potential_savings"]
            })
            
        # Recommandations performance
        if performance["predictions"][0]["margin"] < 0:
            recommendations.append({
                "type": "PERFORMANCE",
                "priority": "HIGH",
                "description": "Marge négative prévue",
                "actions": [
                    "Revoir structure coûts",
                    "Optimiser revenus",
                    "Ajuster pricing"
                ]
            })
            
        return recommendations

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
