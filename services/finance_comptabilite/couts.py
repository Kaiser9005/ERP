"""
Module de gestion des coûts intégrée finance-comptabilité
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session

from models.comptabilite import (
    CompteComptable, 
    EcritureComptable,
    TypeCompte,
    JournalComptable
)
from models.finance import Transaction, Budget, CategorieTransaction
from models.production import Parcelle

class GestionCouts:
    """Gestion intégrée des coûts finance-comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db

    async def _get_couts_parcelle(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse détaillée des coûts d'une parcelle"""
        # Requête optimisée avec jointures
        couts_query = self.db.query(
            EcritureComptable.categorie,
            func.sum(EcritureComptable.debit).label('total')
        ).filter(
            EcritureComptable.parcelle_id == parcelle_id,
            EcritureComptable.date_ecriture.between(date_debut, date_fin)
        ).group_by(
            EcritureComptable.categorie
        )
        
        couts_details = {}
        total = Decimal('0')
        
        for cout in couts_query.all():
            couts_details[cout.categorie] = float(cout.total)
            total += cout.total
            
        return {
            "details": couts_details,
            "total": float(total),
            "par_hectare": float(total / self.db.query(Parcelle).get(parcelle_id).surface)
        }

    async def _get_compte_charge(
        self,
        transaction: Transaction
    ) -> str:
        """Détermine le compte de charge approprié"""
        # Mapping des catégories vers les comptes
        mapping_comptes = {
            CategorieTransaction.INTRANT: "601",  # Achats stockés - Matières premières
            CategorieTransaction.MATERIEL: "215",  # Installations techniques
            CategorieTransaction.MAIN_OEUVRE: "641",  # Rémunérations du personnel
            CategorieTransaction.TRANSPORT: "624",  # Transports de biens
            CategorieTransaction.MAINTENANCE: "615",  # Entretien et réparations
        }
        
        # Récupération du compte par défaut si catégorie non mappée
        compte_numero = mapping_comptes.get(
            transaction.categorie,
            "627"  # Compte par défaut - Services bancaires
        )
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero.like(f"{compte_numero}%"),
            CompteComptable.type_compte == TypeCompte.CHARGE
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de charge {compte_numero} non trouvé")
            
        return compte.id

    async def _get_compte_produit(
        self,
        transaction: Transaction
    ) -> str:
        """Détermine le compte de produit approprié"""
        # Mapping des catégories vers les comptes
        mapping_comptes = {
            CategorieTransaction.VENTE_RECOLTE: "701",  # Ventes de produits finis
            CategorieTransaction.SUBVENTION: "74",  # Subventions d'exploitation
            CategorieTransaction.PRESTATION: "706",  # Prestations de services
        }
        
        # Récupération du compte par défaut si catégorie non mappée
        compte_numero = mapping_comptes.get(
            transaction.categorie,
            "708"  # Compte par défaut - Produits des activités annexes
        )
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero.like(f"{compte_numero}%"),
            CompteComptable.type_compte == TypeCompte.PRODUIT
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de produit {compte_numero} non trouvé")
            
        return compte.id

    async def get_analyse_couts(
        self,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        parcelle_id: Optional[str] = None,
        categorie: Optional[CategorieTransaction] = None
    ) -> Dict[str, Any]:
        """Analyse détaillée des coûts avec filtres"""
        # Période par défaut: mois en cours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin.replace(day=1)
            
        # Construction de la requête de base
        query = self.db.query(
            EcritureComptable.categorie,
            func.sum(EcritureComptable.debit).label('total'),
            func.count(EcritureComptable.id).label('count')
        )
        
        # Application des filtres
        filters = [
            EcritureComptable.date_ecriture.between(date_debut, date_fin)
        ]
        
        if parcelle_id:
            filters.append(EcritureComptable.parcelle_id == parcelle_id)
            
        if categorie:
            filters.append(EcritureComptable.categorie == categorie)
            
        query = query.filter(*filters).group_by(EcritureComptable.categorie)
        
        # Exécution et formatage des résultats
        resultats = query.all()
        analyse = {
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            },
            "total": 0,
            "categories": {},
            "repartition": [],
            "evolution": await self._get_evolution_couts(
                date_debut,
                date_fin,
                parcelle_id,
                categorie
            )
        }
        
        for resultat in resultats:
            montant = float(resultat.total)
            analyse["total"] += montant
            analyse["categories"][resultat.categorie] = {
                "montant": montant,
                "count": resultat.count
            }
            
        # Calcul des pourcentages
        if analyse["total"] > 0:
            for cat, data in analyse["categories"].items():
                pourcentage = (data["montant"] / analyse["total"]) * 100
                analyse["repartition"].append({
                    "categorie": cat,
                    "pourcentage": round(pourcentage, 2)
                })
                
        return analyse

    async def _get_evolution_couts(
        self,
        date_debut: date,
        date_fin: date,
        parcelle_id: Optional[str] = None,
        categorie: Optional[CategorieTransaction] = None
    ) -> List[Dict[str, Any]]:
        """Analyse l'évolution des coûts sur la période"""
        evolution = []
        current = date_debut
        
        while current <= date_fin:
            # Requête pour la période
            query = self.db.query(
                func.sum(EcritureComptable.debit)
            ).filter(
                func.date_trunc('month', EcritureComptable.date_ecriture) == current
            )
            
            if parcelle_id:
                query = query.filter(EcritureComptable.parcelle_id == parcelle_id)
                
            if categorie:
                query = query.filter(EcritureComptable.categorie == categorie)
                
            total = query.scalar() or 0
            
            evolution.append({
                "periode": current.strftime("%Y-%m"),
                "montant": float(total)
            })
            
            # Passage au mois suivant
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
                
        return evolution
