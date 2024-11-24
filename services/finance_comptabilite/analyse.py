"""
Module d'analyse financière et comptable intégrée
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from models.comptabilite import (
    CompteComptable, 
    EcritureComptable,
    TypeCompte
)
from models.finance import Transaction, Budget
from models.production import Parcelle

class AnalyseFinanceCompta:
    """Analyse intégrée finance-comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db

    async def get_analyse_parcelle(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse financière détaillée d'une parcelle"""
        # Récupération des données de base
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)

        # Analyse intégrée
        transactions = await self._get_transactions_parcelle(
            parcelle_id, 
            date_debut,
            date_fin
        )
        
        ecritures = await self._get_ecritures_parcelle(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Calcul des indicateurs
        indicateurs = await self._calculer_indicateurs(
            transactions,
            ecritures,
            parcelle.surface
        )
        
        return {
            "parcelle": {
                "id": parcelle.id,
                "code": parcelle.code,
                "surface": parcelle.surface,
                "culture": parcelle.culture_actuelle
            },
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            },
            "indicateurs": indicateurs,
            "transactions": {
                "count": len(transactions),
                "total_recettes": sum(t.montant for t in transactions if t.type_transaction == "RECETTE"),
                "total_depenses": sum(t.montant for t in transactions if t.type_transaction == "DEPENSE")
            },
            "comptabilite": {
                "count": len(ecritures),
                "total_debit": sum(e.debit or 0 for e in ecritures),
                "total_credit": sum(e.credit or 0 for e in ecritures)
            }
        }

    async def _get_transactions_parcelle(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> List[Transaction]:
        """Récupère les transactions d'une parcelle"""
        return self.db.query(Transaction).filter(
            Transaction.parcelle_id == parcelle_id,
            Transaction.date_transaction.between(date_debut, date_fin),
            Transaction.statut == "VALIDEE"
        ).all()

    async def _get_ecritures_parcelle(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> List[EcritureComptable]:
        """Récupère les écritures d'une parcelle"""
        return self.db.query(EcritureComptable).filter(
            EcritureComptable.parcelle_id == parcelle_id,
            EcritureComptable.date_ecriture.between(date_debut, date_fin),
            EcritureComptable.statut == "VALIDEE"
        ).all()

    async def _calculer_indicateurs(
        self,
        transactions: List[Transaction],
        ecritures: List[EcritureComptable],
        surface: float
    ) -> Dict[str, Any]:
        """Calcule les indicateurs financiers et comptables"""
        # Calcul des totaux
        total_recettes = sum(t.montant for t in transactions if t.type_transaction == "RECETTE")
        total_depenses = sum(t.montant for t in transactions if t.type_transaction == "DEPENSE")
        
        total_debit = sum(e.debit or 0 for e in ecritures)
        total_credit = sum(e.credit or 0 for e in ecritures)
        
        # Calcul des ratios
        return {
            "marge_brute": total_recettes - total_depenses,
            "marge_hectare": (total_recettes - total_depenses) / surface,
            "ratio_rentabilite": (total_recettes / total_depenses * 100) if total_depenses > 0 else 0,
            "equilibre_comptable": abs(total_debit - total_credit) < Decimal('0.01'),
            "coherence_fin_compta": abs((total_recettes - total_depenses) - (total_debit - total_credit)) < Decimal('0.01')
        }

    async def _calculer_rentabilite_parcelle(
        self,
        parcelle_id: str,
        couts: Dict[str, Any],
        meteo_data: Dict[str, Any],
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Calcul détaillé de la rentabilité d'une parcelle"""
        # Récupération des revenus
        revenus = self.db.query(
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.parcelle_id == parcelle_id,
            EcritureComptable.type_compte == TypeCompte.PRODUIT,
            EcritureComptable.date_ecriture.between(date_debut, date_fin)
        ).scalar() or Decimal('0')
        
        # Calcul des indicateurs
        marge_brute = float(revenus - Decimal(str(couts["total"])))
        
        return {
            "revenus": float(revenus),
            "charges": couts["total"],
            "marge_brute": marge_brute,
            "marge_hectare": marge_brute / self.db.query(Parcelle).get(parcelle_id).surface,
            "impact_meteo": meteo_data["score"],
            "rentabilite": (marge_brute / couts["total"] * 100) if couts["total"] > 0 else 0
        }

    async def _generer_recommendations(
        self,
        parcelle_id: str,
        couts: Dict[str, Any],
        meteo_data: Dict[str, Any],
        iot_data: Dict[str, Any]
    ) -> List[str]:
        """Génère des recommendations basées sur l'analyse complète"""
        recommendations = []
        
        # Recommendations basées sur les coûts
        for categorie, montant in couts["details"].items():
            if montant > couts["total"] * 0.4:  # Si une catégorie > 40% du total
                recommendations.append(
                    f"Optimisation possible des coûts {categorie}: "
                    f"représente {round(montant/couts['total']*100, 1)}% des coûts totaux"
                )
                
        # Recommendations basées sur la météo
        for facteur in meteo_data["facteurs"]:
            if "précipitations" in facteur.lower():
                recommendations.append(
                    f"Ajuster l'irrigation en fonction des {facteur.lower()}"
                )
            elif "températures" in facteur.lower():
                recommendations.append(
                    f"Adapter les traitements aux {facteur.lower()}"
                )
                
        # Recommendations basées sur les données IoT
        for alerte in iot_data.get("alertes", []):
            recommendations.append(
                f"Action requise: {alerte['message']}"
            )
            
        return recommendations
