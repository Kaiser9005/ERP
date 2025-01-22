"""
Service d'intégration Finance-Comptabilité avec ML
Basé sur les analyses des ERP Odoo et Dolibarr et enrichi des meilleures pratiques
"""

from sqlalchemy.orm import Session
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy import and_, or_, func, update
from models.comptabilite import (
    CompteComptable, 
    EcritureComptable, 
    TypeCompte,
    JournalComptable,
    StatutEcriture,
    TypeJournal
)
from models.production import Parcelle, CycleCulture
from models.iot_sensor import IoTSensor, SensorData
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.cache_service import CacheService
from services.storage_service import StorageService
from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from core.security import Permission, require_permissions
import asyncio
from functools import lru_cache

class ValidationResult:
    """Résultat de validation"""
    def __init__(
        self,
        is_valid: bool,
        errors: List[str] = None,
        warnings: List[str] = None
    ):
        self.is_valid = is_valid
        self.errors = errors or []
        self.warnings = warnings or []

class MeteoImpact:
    """Impact météorologique"""
    def __init__(
        self,
        score: float,
        facteurs: List[str],
        couts_additionnels: Dict[str, float],
        risques: List[str],
        opportunites: List[str]
    ):
        self.score = score
        self.facteurs = facteurs
        self.couts_additionnels = couts_additionnels
        self.risques = risques
        self.opportunites = opportunites

class AnalyticData:
    """Données analytiques"""
    def __init__(
        self,
        charges_directes: float,
        charges_indirectes: float,
        produits: float,
        marge: float,
        axes: Dict[str, Any]
    ):
        self.charges_directes = charges_directes
        self.charges_indirectes = charges_indirectes
        self.produits = produits
        self.marge = marge
        self.axes = axes

class CloturePeriode:
    """Données de clôture"""
    def __init__(
        self,
        periode: str,
        statut: str,
        totaux: Dict[str, float],
        etats: Dict[str, str]
    ):
        self.periode = periode
        self.statut = statut
        self.totaux = totaux
        self.etats = etats

class FinanceComptabiliteIntegrationService:
    """Service d'intégration entre les modules Finance et Comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        self.cache = CacheService()
        self.storage = StorageService()
        self.analyse = AnalyseFinanceCompta(db)

    async def get_analyse_parcelle(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Analyse financière détaillée d'une parcelle avec ML"""
        # Cache key
        cache_key = f"analyse_parcelle_ml_{parcelle_id}_{date_debut}_{date_fin}"
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
        
        # Optimisation coûts
        optimization = await self.analyse.optimize_costs(
            parcelle_id=parcelle_id,
            target_date=date_fin or date.today()
        )
        
        # Prédictions performance
        performance = await self.analyse.predict_performance(months_ahead=3)
        
        # Analyse de base
        base_analysis = await self._get_base_analysis(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        result = {
            **base_analysis,
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "performance": performance,
            "recommendations": await self._generer_recommendations_ml(
                base_analysis,
                analyse_ml,
                optimization,
                performance
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def _get_base_analysis(
        self,
        parcelle_id: str,
        date_debut: Optional[date],
        date_fin: Optional[date]
    ) -> Dict[str, Any]:
        """Analyse de base d'une parcelle"""
        # Récupération des données de base
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)
            
        # Analyse des coûts
        couts = await self._get_couts_parcelle(parcelle_id, date_debut, date_fin)
        
        # Données météo et IoT
        meteo_data = await self.get_meteo_impact(parcelle_id, date_debut, date_fin)
        iot_data = await self.get_iot_analysis(parcelle_id, date_debut, date_fin)
        
        # Calcul rentabilité
        rentabilite = await self._calculer_rentabilite_parcelle(
            parcelle_id, 
            couts,
            meteo_data,
            date_debut,
            date_fin
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
            "couts": couts,
            "meteo_impact": meteo_data,
            "iot_analysis": iot_data,
            "rentabilite": rentabilite
        }

    async def _get_couts_parcelle(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Récupère les coûts d'une parcelle avec ML"""
        # Cache key
        cache_key = f"couts_parcelle_ml_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Récupération des écritures
        ecritures = self.db.query(EcritureComptable).filter(
            EcritureComptable.parcelle_id == parcelle_id,
            EcritureComptable.date.between(date_debut, date_fin)
        ).all()
        
        # Calcul des coûts par catégorie
        couts = {}
        for ecriture in ecritures:
            if ecriture.categorie not in couts:
                couts[ecriture.categorie] = {
                    "montant": 0,
                    "count": 0
                }
            couts[ecriture.categorie]["montant"] += float(ecriture.montant)
            couts[ecriture.categorie]["count"] += 1
            
        # Analyse ML
        analyse_ml = await self.analyse.get_analyse_parcelle(
            parcelle_id=parcelle_id,
            date_debut=date_debut,
            date_fin=date_fin
        )
        
        # Optimisation ML
        optimization = await self.analyse.optimize_costs(
            parcelle_id=parcelle_id,
            target_date=date_fin
        )
        
        result = {
            "details": couts,
            "total": sum(c["montant"] for c in couts.values()),
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_cost_recommendations(
                couts,
                analyse_ml,
                optimization
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def get_meteo_impact(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse l'impact météo avec ML"""
        # Cache key
        cache_key = f"meteo_impact_ml_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Données météo
        meteo_data = await self.weather_service.get_period_stats(
            date_debut,
            date_fin
        )
        
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
        
        result = {
            "data": meteo_data,
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_meteo_recommendations(
                meteo_data,
                analyse_ml,
                optimization
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def get_iot_analysis(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse les données IoT avec ML"""
        # Cache key
        cache_key = f"iot_analysis_ml_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Données IoT
        iot_data = await self.iot_service.get_period_data(
            parcelle_id,
            date_debut,
            date_fin
        )
        
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
        
        result = {
            "data": iot_data,
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_iot_recommendations(
                iot_data,
                analyse_ml,
                optimization
            )
        }
        
        # Cache result
        await self.cache.set(cache_key, result, expire=3600)
        return result

    async def _calculer_rentabilite_parcelle(
        self,
        parcelle_id: str,
        couts: Dict[str, Any],
        meteo_impact: Dict[str, Any],
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Calcule la rentabilité d'une parcelle avec ML"""
        # Récupération des produits
        produits = self.db.query(
            func.sum(EcritureComptable.montant)
        ).filter(
            EcritureComptable.parcelle_id == parcelle_id,
            EcritureComptable.type_compte == TypeCompte.PRODUIT,
            EcritureComptable.date.between(date_debut, date_fin)
        ).scalar() or 0
        
        # Calcul marge
        marge = float(produits) - couts["total"]
        
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
        
        return {
            "produits": float(produits),
            "charges": couts["total"],
            "marge": marge,
            "roi": marge / couts["total"] if couts["total"] > 0 else 0,
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization,
            "recommendations": await self._generate_profitability_recommendations(
                marge,
                analyse_ml,
                optimization
            )
        }

    async def _generer_recommendations_ml(
        self,
        base_analysis: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any],
        performance: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur ML"""
        recommendations = []
        
        # Recommandations ML
        for rec in analyse_ml["ml_analysis"]["recommendations"]:
            recommendations.append({
                "type": "ML",
                "priority": rec["priority"],
                "description": rec["description"],
                "actions": rec["actions"],
                "expected_impact": rec.get("expected_impact")
            })
            
        # Recommandations optimisation
        if optimization["potential_savings"] > 1000:  # Seuil significatif
            for step in optimization["implementation_plan"]:
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
                
        # Recommandations performance
        if performance["predictions"]:
            next_month = performance["predictions"][0]
            if next_month["margin"] < 0:
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

    async def _generate_cost_recommendations(
        self,
        couts: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations sur les coûts"""
        recommendations = []
        
        # Recommandations ML
        if "cost_recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["cost_recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec["priority"],
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        # Recommandations optimisation
        if "cost_optimizations" in optimization:
            for opt in optimization["cost_optimizations"]:
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "savings": opt.get("savings", 0)
                })
                
        # Recommandations analytiques
        for categorie, data in couts.items():
            if data["montant"] > 10000:  # Seuil d'alerte
                recommendations.append({
                    "type": "ALERT",
                    "priority": "HIGH",
                    "description": f"Coûts élevés - {categorie}",
                    "actions": [
                        "Analyser détail",
                        "Identifier optimisations",
                        "Revoir fournisseurs"
                    ]
                })
                
        return recommendations

    async def _generate_meteo_recommendations(
        self,
        meteo_data: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations météo"""
        recommendations = []
        
        # Recommandations ML
        if "weather_recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["weather_recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec["priority"],
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        # Recommandations optimisation
        if "weather_optimizations" in optimization:
            for opt in optimization["weather_optimizations"]:
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "impact": opt.get("impact", {})
                })
                
        # Recommandations basées sur les données
        if meteo_data.get("precipitation", 0) > 200:
            recommendations.append({
                "type": "ALERT",
                "priority": "HIGH",
                "description": "Fortes précipitations",
                "actions": [
                    "Vérifier drainage",
                    "Adapter irrigation",
                    "Surveiller érosion"
                ]
            })
            
        return recommendations

    async def _generate_iot_recommendations(
        self,
        iot_data: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations IoT"""
        recommendations = []
        
        # Recommandations ML
        if "iot_recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["iot_recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec["priority"],
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        # Recommandations optimisation
        if "iot_optimizations" in optimization:
            for opt in optimization["iot_optimizations"]:
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "savings": opt.get("savings", 0)
                })
                
        # Recommandations alertes
        for sensor_type, data in iot_data.items():
            if data.get("alerts", []):
                recommendations.append({
                    "type": "ALERT",
                    "priority": "HIGH",
                    "description": f"Alertes {sensor_type}",
                    "actions": [
                        "Vérifier capteurs",
                        "Analyser données",
                        "Appliquer corrections"
                    ]
                })
                
        return recommendations

    async def _generate_profitability_recommendations(
        self,
        marge: float,
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations de rentabilité"""
        recommendations = []
        
        # Recommandations ML
        if "profitability_recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["profitability_recommendations"]:
                recommendations.append({
                    "type": "ML",
                    "priority": rec["priority"],
                    "description": rec["description"],
                    "actions": rec["actions"]
                })
                
        # Recommandations optimisation
        if "profitability_optimizations" in optimization:
            for opt in optimization["profitability_optimizations"]:
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "impact": opt.get("impact", {})
                })
                
        # Recommandations marge
        if marge < 0:
            recommendations.append({
                "type": "ALERT",
                "priority": "HIGH",
                "description": "Marge négative",
                "actions": [
                    "Analyser structure coûts",
                    "Optimiser revenus",
                    "Revoir pricing"
                ]
            })
            
        return recommendations
