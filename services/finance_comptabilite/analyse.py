"""
Service d'analyse financière et comptable
"""

from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    JournalComptable,
    ExerciceComptable
)
from models.finance import Transaction, Budget, CategorieTransaction
from models.production import Parcelle, CycleCulture
from services.cache_service import cache_result

class AnalyseFinanceCompta:
    """Service d'analyse financière et comptable"""

    def __init__(self, db: Session):
        self.db = db
        self._cache_duration = timedelta(minutes=15)

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def get_analyse_parcelle(self, 
                                 parcelle_id: int,
                                 date_debut: datetime,
                                 date_fin: datetime) -> Dict:
        """Analyse financière d'une parcelle"""
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            return {}

        rentabilite = await self._calculer_rentabilite_parcelle(
            parcelle,
            date_debut,
            date_fin
        )

        return {
            "rentabilite": rentabilite,
            "recommendations": await self._generer_recommendations(
                parcelle,
                rentabilite
            ),
            "date_analyse": datetime.now(datetime.timezone.utc).isoformat()
        }

    async def _calculer_rentabilite_parcelle(self,
                                           parcelle: Parcelle,
                                           date_debut: datetime,
                                           date_fin: datetime) -> Dict:
        """Calcule la rentabilité d'une parcelle"""
        # Récupération des cycles de culture
        cycles = self.db.query(CycleCulture).filter(
            CycleCulture.parcelle_id == parcelle.id,
            CycleCulture.date_debut >= date_debut,
            CycleCulture.date_fin <= date_fin
        ).all()

        if not cycles:
            return {
                "produits": 0,
                "charges": 0,
                "marge": 0,
                "rentabilite": 0
            }

        # Calcul des produits et charges
        produits = sum(c.produits_totaux or 0 for c in cycles)
        charges = sum(c.charges_totales or 0 for c in cycles)
        marge = produits - charges

        # Calcul de la rentabilité
        rentabilite = (marge / charges * 100) if charges > 0 else 0

        return {
            "produits": float(produits),
            "charges": float(charges),
            "marge": float(marge),
            "rentabilite": float(rentabilite)
        }

    async def _generer_recommendations(self,
                                     parcelle: Parcelle,
                                     rentabilite: Dict) -> List[str]:
        """Génère des recommandations basées sur l'analyse"""
        recommendations = []

        # Analyse de la rentabilité
        if rentabilite["rentabilite"] < 0:
            recommendations.append(
                "Rentabilité négative : revoir la structure des coûts"
            )
        elif rentabilite["rentabilite"] < 10:
            recommendations.append(
                "Rentabilité faible : optimiser les charges ou augmenter les produits"
            )

        # Analyse des charges
        if rentabilite["charges"] > rentabilite["produits"] * 0.8:
            recommendations.append(
                "Charges élevées par rapport aux produits : identifier les postes à optimiser"
            )

        return recommendations