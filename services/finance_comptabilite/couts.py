"""
Service de gestion des coûts
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

class GestionCouts:
    """Service de gestion des coûts"""

    def __init__(self, db: Session):
        self.db = db
        self._cache_duration = timedelta(minutes=15)

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _get_couts_parcelle(self,
                                parcelle_id: int,
                                date_debut: datetime,
                                date_fin: datetime) -> Dict:
        """Récupère les coûts d'une parcelle"""
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            return {}

        # Récupération des écritures comptables
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.parcelle_id == parcelle.id,
            EcritureComptable.date >= date_debut,
            EcritureComptable.date <= date_fin
        ).all()

        # Calcul des coûts par catégorie
        couts_par_categorie = {}
        for ecriture in ecritures:
            if ecriture.compte.type == "CHARGE":
                categorie = ecriture.compte.categorie
                if categorie not in couts_par_categorie:
                    couts_par_categorie[categorie] = 0
                couts_par_categorie[categorie] += ecriture.montant

        return {
            "couts_par_categorie": couts_par_categorie,
            "total": sum(couts_par_categorie.values()),
            "date_calcul": datetime.now(datetime.timezone.utc).isoformat()
        }

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _get_compte_charge(self, code: str) -> Optional[CompteComptable]:
        """Récupère un compte de charge"""
        return self.db.query(CompteComptable).filter(
            CompteComptable.code == code,
            CompteComptable.type == "CHARGE"
        ).first()

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _get_compte_produit(self, code: str) -> Optional[CompteComptable]:
        """Récupère un compte de produit"""
        return self.db.query(CompteComptable).filter(
            CompteComptable.code == code,
            CompteComptable.type == "PRODUIT"
        ).first()

    async def _calculer_couts_directs(self,
                                    parcelle: Parcelle,
                                    date_debut: datetime,
                                    date_fin: datetime) -> float:
        """Calcule les coûts directs d'une parcelle"""
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.parcelle_id == parcelle.id,
            EcritureComptable.date >= date_debut,
            EcritureComptable.date <= date_fin,
            EcritureComptable.type_imputation == "DIRECT"
        ).all()

        return sum(e.montant for e in ecritures if e.compte.type == "CHARGE")

    async def _calculer_couts_indirects(self,
                                      parcelle: Parcelle,
                                      date_debut: datetime,
                                      date_fin: datetime) -> float:
        """Calcule les coûts indirects d'une parcelle"""
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.parcelle_id == parcelle.id,
            EcritureComptable.date >= date_debut,
            EcritureComptable.date <= date_fin,
            EcritureComptable.type_imputation == "INDIRECT"
        ).all()

        return sum(e.montant for e in ecritures if e.compte.type == "CHARGE")

    async def _calculer_cle_repartition(self,
                                      parcelle: Parcelle,
                                      date: datetime) -> float:
        """Calcule la clé de répartition pour une parcelle"""
        # Par défaut, répartition égale entre toutes les parcelles
        total_parcelles = self.db.query(Parcelle).count()
        if total_parcelles == 0:
            return 0
        return 1 / total_parcelles