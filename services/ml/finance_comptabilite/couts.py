"""
Module de gestion des coûts intégrée finance-comptabilité avec ML
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
from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService

class GestionCouts:
    """Gestion intégrée des coûts finance-comptabilité avec ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.analyse = AnalyseFinanceCompta(db)
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        self.cache = CacheService()

    async def _get_couts_parcelle(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse détaillée des coûts d'une parcelle avec ML"""
        # Cache key
        cache_key = f"couts_ml_parcelle_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Analyse ML
        analyse_ml = await self.analyse.get_analyse_parcelle(
            parcelle_id=parcelle_id,
            date_debut=date_debut,
            date_fin=date_fin,
            include_predictions=True
        )
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(
            parcelle_id=parcelle_id,
            target_date=date_fin
        )
        
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
            
        resultat = {
            "details": couts_details,
            "total": float(total),
            "par_hectare": float(total / self.db.query(Parcelle).get(parcelle_id).surface),
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_cost_recommendations(
                couts_details,
                analyse_ml,
                optimization
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, resultat, expire=3600)
        return resultat

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
        """Analyse détaillée des coûts avec ML"""
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
                
        # Ajout ML
        if parcelle_id:
            # Analyse ML par parcelle
            analyse_ml = await self.analyse.get_analyse_parcelle(
                parcelle_id=parcelle_id,
                date_debut=date_debut,
                date_fin=date_fin,
                include_predictions=True
            )
            
            # Optimisation ML
            optimization = await self.analyse.optimize_costs(
                parcelle_id=parcelle_id,
                target_date=date_fin
            )
            
            analyse["ml_analysis"] = analyse_ml["ml_analysis"]
            analyse["optimization"] = optimization
            
        else:
            # Analyse ML globale
            performance = await self.analyse.predict_performance(months_ahead=3)
            analyse["predictions"] = performance["predictions"]
            analyse["risk_factors"] = performance["risk_factors"]
            
        # Recommandations ML
        analyse["recommendations"] = await self._generate_cost_recommendations(
            analyse["categories"],
            analyse.get("ml_analysis"),
            analyse.get("optimization")
        )
                
        return analyse

    async def _get_evolution_couts(
        self,
        date_debut: date,
        date_fin: date,
        parcelle_id: Optional[str] = None,
        categorie: Optional[CategorieTransaction] = None
    ) -> List[Dict[str, Any]]:
        """Analyse l'évolution des coûts avec ML"""
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
            
            # Données météo
            weather_data = await self.weather_service.get_monthly_stats(
                current.strftime("%Y-%m")
            )
            
            # Données IoT si parcelle spécifique
            iot_data = None
            if parcelle_id:
                iot_data = await self.iot_service.get_monthly_stats(
                    parcelle_id,
                    current
                )
            
            evolution.append({
                "periode": current.strftime("%Y-%m"),
                "montant": float(total),
                "weather_impact": weather_data.get("impact", 0),
                "iot_data": iot_data
            })
            
            # Passage au mois suivant
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)
                
        return evolution

    async def _generate_cost_recommendations(
        self,
        couts: Dict[str, Any],
        analyse_ml: Optional[Dict[str, Any]] = None,
        optimization: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations ML pour les coûts"""
        recommendations = []
        
        # Recommandations basées sur l'analyse ML
        if analyse_ml:
            for rec in analyse_ml.get("recommendations", []):
                if rec["type"] == "COST":
                    recommendations.append({
                        "type": "ML",
                        "priority": rec["priority"],
                        "description": rec["description"],
                        "actions": rec["actions"],
                        "expected_impact": rec.get("expected_impact")
                    })
                    
        # Recommandations basées sur l'optimisation
        if optimization:
            for step in optimization.get("implementation_plan", []):
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": f"Optimisation {step['category']}",
                    "actions": step["actions"],
                    "expected_impact": {
                        "savings": step.get("savings", 0),
                        "timeline": step.get("timeline", "N/A")
                    }
                })
                
        # Recommandations basées sur l'analyse des coûts
        total = sum(cout["montant"] for cout in couts.values())
        if total > 0:
            for categorie, data in couts.items():
                pourcentage = (data["montant"] / total) * 100
                if pourcentage > 30:  # Seuil à ajuster
                    recommendations.append({
                        "type": "ANALYSIS",
                        "priority": "MEDIUM",
                        "description": f"Coût {categorie} élevé ({pourcentage:.1f}%)",
                        "actions": [
                            "Analyser détail des coûts",
                            "Identifier optimisations possibles",
                            "Comparer avec moyennes secteur"
                        ]
                    })
                    
        return recommendations
