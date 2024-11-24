"""
Module d'intégration des impacts météorologiques sur la finance et la comptabilité avec ML
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
from models.finance import Transaction, Budget
from models.production import Parcelle
from services.weather_service import WeatherService
from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from services.cache_service import CacheService

class GestionMeteo:
    """Gestion des impacts météorologiques sur la finance et la comptabilité avec ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.analyse = AnalyseFinanceCompta(db)
        self.cache = CacheService()

    async def _get_meteo_impact(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse détaillée de l'impact météo avec ML"""
        # Cache key
        cache_key = f"meteo_impact_ml_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Récupération données météo
        meteo_data = await self.weather_service.get_period_stats(date_debut, date_fin)
        
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
        
        impact = {
            "score": 0,
            "facteurs": [],
            "couts_additionnels": {},
            "risques": [],
            "opportunites": [],
            "provisions_suggeres": {},
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization
        }
        
        # Analyse précipitations
        if meteo_data.get("precipitation", 0) > 200:
            impact["score"] += 30
            impact["facteurs"].append("Fortes précipitations")
            impact["couts_additionnels"]["IRRIGATION"] = "Réduction possible"
            impact["risques"].append("Risque d'érosion accru")
            impact["provisions_suggeres"]["EROSION"] = await self._calculer_provision_erosion_ml(
                meteo_data["precipitation"],
                analyse_ml
            )
            
        elif meteo_data.get("precipitation", 0) < 50:
            impact["score"] += 25
            impact["facteurs"].append("Faibles précipitations")
            impact["couts_additionnels"]["IRRIGATION"] = "Augmentation nécessaire"
            impact["provisions_suggeres"]["IRRIGATION"] = await self._calculer_provision_irrigation_ml(
                meteo_data["precipitation"],
                analyse_ml
            )
            
        # Analyse température
        temp_moy = meteo_data.get("temperature_avg", 25)
        if temp_moy > 30:
            impact["score"] += 20
            impact["facteurs"].append("Températures élevées")
            impact["couts_additionnels"]["MAINTENANCE"] = "Augmentation probable"
            impact["risques"].append("Stress thermique des cultures")
            impact["provisions_suggeres"]["MAINTENANCE"] = await self._calculer_provision_maintenance_ml(
                temp_moy,
                analyse_ml
            )
            
        elif temp_moy < 15:
            impact["score"] += 15
            impact["facteurs"].append("Températures basses")
            impact["risques"].append("Ralentissement de la croissance")
            impact["provisions_suggeres"]["PROTECTION"] = await self._calculer_provision_protection_ml(
                temp_moy,
                analyse_ml
            )
            
        # Analyse humidité
        if meteo_data.get("humidity_avg", 60) > 80:
            impact["score"] += 15
            impact["facteurs"].append("Forte humidité")
            impact["risques"].append("Risque accru de maladies")
            impact["couts_additionnels"]["TRAITEMENTS"] = "Augmentation probable"
            impact["provisions_suggeres"]["TRAITEMENTS"] = await self._calculer_provision_traitements_ml(
                meteo_data["humidity_avg"],
                analyse_ml
            )
            
        # Recommandations ML
        impact["recommendations"] = await self._generate_meteo_recommendations(
            impact,
            analyse_ml,
            optimization
        )
        
        # Cache result
        await self.cache.set(cache_key, impact, expire=3600)
        return impact

    async def _calculer_provision_meteo(
        self,
        impact_meteo: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Calcule les provisions nécessaires basées sur l'impact météo avec ML"""
        provisions = {}
        
        # Optimisation ML des provisions
        optimization = await self.analyse.optimize_costs(
            target_date=date.today(),
            cost_categories=list(impact_meteo["provisions_suggeres"].keys())
        )
        
        for categorie, montant_base in impact_meteo["provisions_suggeres"].items():
            # Ajustement ML du montant
            montant_optimise = montant_base
            if categorie in optimization["optimized_costs"]:
                montant_optimise = optimization["optimized_costs"][categorie]
            
            compte = await self._get_compte_provision_meteo(categorie)
            compte_charge = await self._get_compte_charge_meteo(categorie)
            
            provisions[categorie] = {
                "montant": montant_optimise,
                "montant_base": montant_base,
                "compte_provision": compte,
                "compte_charge": compte_charge,
                "justification": f"Provision pour risques météo - {categorie}",
                "impact_score": impact_meteo["score"],
                "ml_adjustment": montant_optimise - montant_base
            }
            
        return provisions

    async def _calculer_provision_erosion_ml(
        self,
        precipitation: float,
        analyse_ml: Dict[str, Any]
    ) -> float:
        """Calcule la provision pour risque d'érosion avec ML"""
        # Base de calcul
        base = self._calculer_provision_erosion(precipitation)
        
        # Ajustement ML basé sur l'historique
        if "erosion_history" in analyse_ml["ml_analysis"]:
            history_factor = analyse_ml["ml_analysis"]["erosion_history"].get(
                "impact_factor",
                1.0
            )
            base *= history_factor
            
        # Ajustement basé sur les prédictions
        if "predictions" in analyse_ml["ml_analysis"]:
            risk_factor = analyse_ml["ml_analysis"]["predictions"].get(
                "erosion_risk",
                1.0
            )
            base *= risk_factor
            
        return base

    async def _calculer_provision_irrigation_ml(
        self,
        precipitation: float,
        analyse_ml: Dict[str, Any]
    ) -> float:
        """Calcule la provision pour besoins d'irrigation avec ML"""
        base = self._calculer_provision_irrigation(precipitation)
        
        # Ajustement ML
        if "irrigation_predictions" in analyse_ml["ml_analysis"]:
            pred = analyse_ml["ml_analysis"]["irrigation_predictions"]
            if "cost_factor" in pred:
                base *= pred["cost_factor"]
                
        return base

    async def _calculer_provision_maintenance_ml(
        self,
        temperature: float,
        analyse_ml: Dict[str, Any]
    ) -> float:
        """Calcule la provision pour maintenance avec ML"""
        base = self._calculer_provision_maintenance(temperature)
        
        # Ajustement ML
        if "maintenance_analysis" in analyse_ml["ml_analysis"]:
            analysis = analyse_ml["ml_analysis"]["maintenance_analysis"]
            if "cost_multiplier" in analysis:
                base *= analysis["cost_multiplier"]
                
        return base

    async def _calculer_provision_protection_ml(
        self,
        temperature: float,
        analyse_ml: Dict[str, Any]
    ) -> float:
        """Calcule la provision pour protection avec ML"""
        base = self._calculer_provision_protection(temperature)
        
        # Ajustement ML
        if "protection_forecast" in analyse_ml["ml_analysis"]:
            forecast = analyse_ml["ml_analysis"]["protection_forecast"]
            if "severity_factor" in forecast:
                base *= forecast["severity_factor"]
                
        return base

    async def _calculer_provision_traitements_ml(
        self,
        humidity: float,
        analyse_ml: Dict[str, Any]
    ) -> float:
        """Calcule la provision pour traitements avec ML"""
        base = self._calculer_provision_traitements(humidity)
        
        # Ajustement ML
        if "treatment_analysis" in analyse_ml["ml_analysis"]:
            analysis = analyse_ml["ml_analysis"]["treatment_analysis"]
            if "risk_factor" in analysis:
                base *= analysis["risk_factor"]
                
        return base

    def _calculer_provision_erosion(self, precipitation: float) -> float:
        """Calcule la provision de base pour risque d'érosion"""
        if precipitation <= 200:
            return 0
        return (precipitation - 200) * 100

    def _calculer_provision_irrigation(self, precipitation: float) -> float:
        """Calcule la provision de base pour besoins d'irrigation"""
        if precipitation >= 50:
            return 0
        return (50 - precipitation) * 150

    def _calculer_provision_maintenance(self, temperature: float) -> float:
        """Calcule la provision de base pour maintenance"""
        if temperature <= 30:
            return 0
        return (temperature - 30) * 200

    def _calculer_provision_protection(self, temperature: float) -> float:
        """Calcule la provision de base pour protection"""
        if temperature >= 15:
            return 0
        return (15 - temperature) * 250

    def _calculer_provision_traitements(self, humidity: float) -> float:
        """Calcule la provision de base pour traitements"""
        if humidity <= 80:
            return 0
        return (humidity - 80) * 180

    async def _get_compte_provision_meteo(self, categorie: str) -> str:
        """Récupère le compte de provision météo approprié"""
        # Mapping des catégories vers les comptes de provision
        mapping_comptes = {
            "EROSION": "1511",      # Provisions pour risques climatiques
            "IRRIGATION": "1512",    # Provisions pour risques d'irrigation
            "MAINTENANCE": "1513",   # Provisions pour risques de maintenance
            "PROTECTION": "1514",    # Provisions pour risques de protection
            "TRAITEMENTS": "1515"    # Provisions pour risques de traitements
        }
        
        compte_numero = mapping_comptes.get(categorie, "1518")  # Compte par défaut
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero == compte_numero
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de provision {compte_numero} non trouvé")
            
        return compte.id

    async def _get_compte_charge_meteo(self, categorie: str) -> str:
        """Récupère le compte de charge météo approprié"""
        # Mapping des catégories vers les comptes de charge
        mapping_comptes = {
            "EROSION": "6815",      # Dotations aux provisions pour risques climatiques
            "IRRIGATION": "6816",    # Dotations aux provisions pour risques d'irrigation
            "MAINTENANCE": "6817",   # Dotations aux provisions pour risques de maintenance
            "PROTECTION": "6818",    # Dotations aux provisions pour risques de protection
            "TRAITEMENTS": "6819"    # Dotations aux provisions pour risques de traitements
        }
        
        compte_numero = mapping_comptes.get(categorie, "6815")  # Compte par défaut
        
        compte = self.db.query(CompteComptable).filter(
            CompteComptable.numero == compte_numero
        ).first()
        
        if not compte:
            raise ValueError(f"Compte de charge {compte_numero} non trouvé")
            
        return compte.id

    async def _generate_meteo_recommendations(
        self,
        impact: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations ML basées sur l'impact météo"""
        recommendations = []
        
        # Recommandations basées sur l'analyse ML
        if "recommendations" in analyse_ml["ml_analysis"]:
            for rec in analyse_ml["ml_analysis"]["recommendations"]:
                if rec["type"] == "WEATHER":
                    recommendations.append({
                        "type": "ML",
                        "priority": rec["priority"],
                        "description": rec["description"],
                        "actions": rec["actions"],
                        "expected_impact": rec.get("expected_impact")
                    })
                    
        # Recommandations basées sur l'optimisation
        if "implementation_plan" in optimization:
            for step in optimization["implementation_plan"]:
                if step["category"] in impact["couts_additionnels"]:
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
                    
        # Recommandations basées sur l'impact
        if impact["score"] > 50:  # Score critique
            recommendations.append({
                "type": "ALERT",
                "priority": "HIGH",
                "description": "Impact météo critique",
                "actions": [
                    "Réviser provisions",
                    "Mettre en place mesures urgentes",
                    "Consulter experts"
                ]
            })
            
        return recommendations
