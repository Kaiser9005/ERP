"""
Module d'intégration IoT avec la finance et la comptabilité avec ML
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
from models.finance import Transaction
from models.production import Parcelle
from models.iot_sensor import IoTSensor, SensorData
from services.iot_service import IoTService
from services.finance_comptabilite.analyse import AnalyseFinanceCompta
from services.cache_service import CacheService

class GestionIoT:
    """Gestion de l'intégration IoT avec la finance et la comptabilité avec ML"""
    
    def __init__(self, db: Session):
        self.db = db
        self.iot_service = IoTService(db)
        self.analyse = AnalyseFinanceCompta(db)
        self.cache = CacheService()

    async def _get_iot_analysis(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse des données IoT pour la parcelle avec ML"""
        # Cache key
        cache_key = f"iot_analysis_ml_{parcelle_id}_{date_debut}_{date_fin}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached
            
        # Récupération des capteurs de la parcelle
        sensors = self.db.query(IoTSensor).filter(
            IoTSensor.parcelle_id == parcelle_id
        ).all()
        
        if not sensors:
            return {"status": "Aucun capteur installé"}
            
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
            
        analysis = {
            "alertes": [],
            "mesures": {},
            "tendances": {},
            "recommendations": [],
            "impact_financier": {},
            "provisions_suggeres": {},
            "ml_analysis": analyse_ml["ml_analysis"],
            "optimization": optimization
        }
        
        for sensor in sensors:
            # Données du capteur sur la période
            data = await self.iot_service.get_sensor_data(
                sensor.id,
                date_debut,
                date_fin
            )
            
            # Analyse des mesures
            if data:
                analysis["mesures"][sensor.type] = {
                    "min": min(d.value for d in data),
                    "max": max(d.value for d in data),
                    "avg": sum(d.value for d in data) / len(data)
                }
                
                # Détection des tendances avec ML
                analysis["tendances"][sensor.type] = await self._analyser_tendance_ml(
                    data,
                    analyse_ml
                )
                
                # Génération d'alertes si nécessaire
                alertes = await self._generer_alertes_iot_ml(
                    sensor.type,
                    data,
                    analyse_ml
                )
                if alertes:
                    analysis["alertes"].extend(alertes)
                    
                # Analyse de l'impact financier avec ML
                impact = await self._analyser_impact_financier_ml(
                    sensor.type,
                    data,
                    analysis["tendances"][sensor.type],
                    analyse_ml
                )
                analysis["impact_financier"][sensor.type] = impact
                
                # Calcul des provisions suggérées avec ML
                if impact["score"] > 50:  # Seuil d'impact significatif
                    provision = await self._calculer_provision_iot_ml(
                        sensor.type,
                        impact,
                        analysis["tendances"][sensor.type],
                        optimization
                    )
                    if provision:
                        analysis["provisions_suggeres"][sensor.type] = provision
                        
        # Recommandations ML
        analysis["recommendations"] = await self._generate_iot_recommendations(
            analysis,
            analyse_ml,
            optimization
        )
        
        # Cache result
        await self.cache.set(cache_key, analysis, expire=3600)
        return analysis

    async def _analyser_tendance_ml(
        self,
        data: List[SensorData],
        analyse_ml: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse la tendance des données IoT avec ML"""
        if not data or len(data) < 2:
            return {"status": "Données insuffisantes"}
            
        # Analyse de base
        tendance = self._analyser_tendance(data)
        
        # Enrichissement ML
        if "sensor_trends" in analyse_ml:
            ml_trends = analyse_ml["sensor_trends"]
            tendance["ml_confidence"] = ml_trends.get("confidence", 0.8)
            tendance["ml_forecast"] = ml_trends.get("forecast", {})
            tendance["ml_patterns"] = ml_trends.get("patterns", [])
            
        return tendance

    async def _generer_alertes_iot_ml(
        self,
        sensor_type: str,
        data: List[SensorData],
        analyse_ml: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des alertes basées sur les données IoT avec ML"""
        # Alertes de base
        alertes = self._generer_alertes_iot(sensor_type, data)
        
        # Enrichissement ML
        if "sensor_alerts" in analyse_ml:
            ml_alerts = analyse_ml["sensor_alerts"]
            for alerte in alertes:
                if alerte["sensor"] in ml_alerts:
                    ml_data = ml_alerts[alerte["sensor"]]
                    alerte["ml_probability"] = ml_data.get("probability", 0.8)
                    alerte["ml_severity"] = ml_data.get("severity", "MEDIUM")
                    alerte["ml_impact"] = ml_data.get("impact", {})
                    
        return alertes

    async def _analyser_impact_financier_ml(
        self,
        sensor_type: str,
        data: List[SensorData],
        tendance: Dict[str, Any],
        analyse_ml: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse l'impact financier des données IoT avec ML"""
        # Impact de base
        impact = self._analyser_impact_financier(sensor_type, data, tendance)
        
        # Enrichissement ML
        if "financial_impact" in analyse_ml:
            ml_impact = analyse_ml["financial_impact"]
            if sensor_type in ml_impact:
                ml_data = ml_impact[sensor_type]
                
                # Ajustement score
                impact["score"] = (impact["score"] + ml_data.get("score", 0)) / 2
                
                # Ajout prédictions ML
                impact["ml_predictions"] = ml_data.get("predictions", {})
                impact["ml_confidence"] = ml_data.get("confidence", 0.8)
                
                # Ajustement coûts
                for category, cost in ml_data.get("adjusted_costs", {}).items():
                    if category in impact["couts_potentiels"]:
                        impact["couts_potentiels"][category] = (
                            impact["couts_potentiels"][category] + cost
                        ) / 2
                        
        return impact

    async def _calculer_provision_iot_ml(
        self,
        sensor_type: str,
        impact: Dict[str, Any],
        tendance: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Calcule la provision suggérée basée sur l'impact IoT avec ML"""
        # Provision de base
        provision = self._calculer_provision_iot(sensor_type, impact, tendance)
        if not provision:
            return None
            
        # Optimisation ML
        if "sensor_provisions" in optimization:
            opt_data = optimization["sensor_provisions"]
            if sensor_type in opt_data:
                opt_provision = opt_data[sensor_type]
                
                # Ajustement montant
                provision["montant"] = (
                    provision["montant"] + opt_provision.get("amount", 0)
                ) / 2
                
                # Ajout données ML
                provision["ml_confidence"] = opt_provision.get("confidence", 0.8)
                provision["ml_factors"] = opt_provision.get("factors", [])
                provision["ml_timeline"] = opt_provision.get("timeline", "3M")
                
        return provision

    def _analyser_tendance(self, data: List[SensorData]) -> Dict[str, Any]:
        """Analyse la tendance des données IoT"""
        if not data or len(data) < 2:
            return {"status": "Données insuffisantes"}
            
        values = [d.value for d in data]
        dates = [d.timestamp for d in data]
        
        # Calcul tendance linéaire
        n = len(values)
        sum_x = sum(range(n))
        sum_y = sum(values)
        sum_xy = sum(i * v for i, v in enumerate(values))
        sum_xx = sum(i * i for i in range(n))
        
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
        
        # Calcul de la volatilité
        mean = sum(values) / n
        variance = sum((v - mean) ** 2 for v in values) / n
        volatility = (variance ** 0.5) / mean if mean != 0 else 0
        
        return {
            "direction": "hausse" if slope > 0 else "baisse",
            "intensite": abs(slope),
            "volatility": volatility,
            "fiabilite": "haute" if n > 10 else "moyenne",
            "stabilite": "stable" if volatility < 0.1 else "instable"
        }

    def _generer_alertes_iot(
        self,
        sensor_type: str,
        data: List[SensorData]
    ) -> List[Dict[str, Any]]:
        """Génère des alertes basées sur les données IoT"""
        alertes = []
        
        if not data:
            return alertes
            
        latest = data[-1]
        
        # Seuils par type de capteur
        seuils = {
            "HUMIDITE": {"min": 30, "max": 70},
            "TEMPERATURE": {"min": 15, "max": 35},
            "PH": {"min": 6, "max": 7.5},
            "NUTRIMENTS": {"min": 50, "max": 200}
        }
        
        if sensor_type in seuils:
            if latest.value < seuils[sensor_type]["min"]:
                alertes.append({
                    "type": "warning",
                    "sensor": sensor_type,
                    "message": f"{sensor_type} trop bas: {latest.value}",
                    "timestamp": latest.timestamp,
                    "impact_financier": self._estimer_impact_financier(
                        sensor_type,
                        "bas",
                        seuils[sensor_type]["min"] - latest.value
                    )
                })
            elif latest.value > seuils[sensor_type]["max"]:
                alertes.append({
                    "type": "warning",
                    "sensor": sensor_type,
                    "message": f"{sensor_type} trop élevé: {latest.value}",
                    "timestamp": latest.timestamp,
                    "impact_financier": self._estimer_impact_financier(
                        sensor_type,
                        "haut",
                        latest.value - seuils[sensor_type]["max"]
                    )
                })
                
        return alertes

    def _analyser_impact_financier(
        self,
        sensor_type: str,
        data: List[SensorData],
        tendance: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse l'impact financier des données IoT"""
        impact = {
            "score": 0,
            "couts_potentiels": {},
            "economies_potentielles": {},
            "risques": [],
            "opportunites": []
        }
        
        # Analyse basée sur le type de capteur
        if sensor_type == "HUMIDITE":
            self._analyser_impact_humidite(data, tendance, impact)
        elif sensor_type == "TEMPERATURE":
            self._analyser_impact_temperature(data, tendance, impact)
        elif sensor_type == "PH":
            self._analyser_impact_ph(data, tendance, impact)
        elif sensor_type == "NUTRIMENTS":
            self._analyser_impact_nutriments(data, tendance, impact)
            
        return impact

    def _analyser_impact_humidite(
        self,
        data: List[SensorData],
        tendance: Dict[str, Any],
        impact: Dict[str, Any]
    ):
        """Analyse l'impact financier des données d'humidité"""
        avg = sum(d.value for d in data) / len(data)
        
        if avg > 70:
            impact["score"] += 30
            impact["couts_potentiels"]["TRAITEMENTS"] = (avg - 70) * 100
            impact["risques"].append("Augmentation des coûts de traitement")
        elif avg < 30:
            impact["score"] += 25
            impact["couts_potentiels"]["IRRIGATION"] = (30 - avg) * 150
            impact["risques"].append("Augmentation des coûts d'irrigation")
            
        if tendance["direction"] == "hausse" and tendance["intensite"] > 0.1:
            impact["score"] += 10
            impact["risques"].append("Tendance à la hausse de l'humidité")
        elif tendance["direction"] == "baisse" and tendance["intensite"] > 0.1:
            impact["score"] += 10
            impact["risques"].append("Tendance à la baisse de l'humidité")

    def _analyser_impact_temperature(
        self,
        data: List[SensorData],
        tendance: Dict[str, Any],
        impact: Dict[str, Any]
    ):
        """Analyse l'impact financier des données de température"""
        avg = sum(d.value for d in data) / len(data)
        
        if avg > 35:
            impact["score"] += 35
            impact["couts_potentiels"]["CLIMATISATION"] = (avg - 35) * 200
            impact["risques"].append("Augmentation des coûts de climatisation")
        elif avg < 15:
            impact["score"] += 30
            impact["couts_potentiels"]["CHAUFFAGE"] = (15 - avg) * 180
            impact["risques"].append("Augmentation des coûts de chauffage")
            
        if tendance["volatility"] > 0.2:
            impact["score"] += 15
            impact["risques"].append("Forte volatilité de la température")

    def _analyser_impact_ph(
        self,
        data: List[SensorData],
        tendance: Dict[str, Any],
        impact: Dict[str, Any]
    ):
        """Analyse l'impact financier des données de pH"""
        avg = sum(d.value for d in data) / len(data)
        
        if avg > 7.5:
            impact["score"] += 20
            impact["couts_potentiels"]["TRAITEMENT_PH"] = (avg - 7.5) * 300
            impact["risques"].append("Nécessité de traitement pH")
        elif avg < 6:
            impact["score"] += 20
            impact["couts_potentiels"]["TRAITEMENT_PH"] = (6 - avg) * 300
            impact["risques"].append("Nécessité de traitement pH")

    def _analyser_impact_nutriments(
        self,
        data: List[SensorData],
        tendance: Dict[str, Any],
        impact: Dict[str, Any]
    ):
        """Analyse l'impact financier des données de nutriments"""
        avg = sum(d.value for d in data) / len(data)
        
        if avg < 50:
            impact["score"] += 25
            impact["couts_potentiels"]["FERTILISATION"] = (50 - avg) * 50
            impact["risques"].append("Nécessité de fertilisation")
        elif avg > 200:
            impact["score"] += 15
            impact["economies_potentielles"]["FERTILISATION"] = (avg - 200) * 30
            impact["opportunites"].append("Réduction possible de la fertilisation")

    def _estimer_impact_financier(
        self,
        sensor_type: str,
        niveau: str,
        ecart: float
    ) -> float:
        """Estime l'impact financier d'une alerte"""
        # Coûts unitaires par type de capteur et niveau
        couts = {
            "HUMIDITE": {
                "bas": 150,  # €/point d'écart
                "haut": 100
            },
            "TEMPERATURE": {
                "bas": 180,
                "haut": 200
            },
            "PH": {
                "bas": 300,
                "haut": 300
            },
            "NUTRIMENTS": {
                "bas": 50,
                "haut": 30
            }
        }
        
        if sensor_type in couts and niveau in couts[sensor_type]:
            return couts[sensor_type][niveau] * ecart
        return 0

    def _calculer_provision_iot(
        self,
        sensor_type: str,
        impact: Dict[str, Any],
        tendance: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Calcule la provision suggérée basée sur l'impact IoT"""
        if impact["score"] < 50:  # Seuil minimal pour provision
            return None
            
        # Calcul du montant de base
        montant_base = sum(impact["couts_potentiels"].values())
        
        # Ajustement selon la tendance
        if tendance["direction"] == "hausse":
            montant_base *= (1 + tendance["intensite"])
        elif tendance["direction"] == "baisse":
            montant_base *= (1 - tendance["intensite"] * 0.5)
            
        # Ajustement selon la volatilité
        if tendance["volatility"] > 0.2:
            montant_base *= (1 + tendance["volatility"])
            
        return {
            "montant": round(montant_base, 2),
            "justification": f"Provision pour risques IoT - {sensor_type}",
            "score_impact": impact["score"],
            "tendance": tendance["direction"],
            "fiabilite": tendance["fiabilite"]
        }

    async def _generate_iot_recommendations(
        self,
        analysis: Dict[str, Any],
        analyse_ml: Dict[str, Any],
        optimization: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations ML basées sur l'analyse IoT"""
        recommendations = []
        
        # Recommandations ML
        if "recommendations" in analyse_ml:
            for rec in analyse_ml["recommendations"]:
                if rec["type"] == "IOT":
                    recommendations.append({
                        "type": "ML",
                        "priority": rec["priority"],
                        "description": rec["description"],
                        "actions": rec["actions"],
                        "expected_impact": rec.get("expected_impact")
                    })
                    
        # Recommandations optimisation
        if "sensor_optimizations" in optimization:
            for sensor_type, opt in optimization["sensor_optimizations"].items():
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "HIGH",
                    "description": f"Optimisation {sensor_type}",
                    "actions": opt["actions"],
                    "expected_impact": {
                        "savings": opt.get("savings", 0),
                        "timeline": opt.get("timeline", "N/A")
                    }
                })
                
        # Recommandations alertes
        for alerte in analysis["alertes"]:
            if alerte.get("ml_severity", "LOW") in ["HIGH", "CRITICAL"]:
                recommendations.append({
                    "type": "ALERT",
                    "priority": "HIGH",
                    "description": alerte["message"],
                    "actions": [
                        "Vérifier capteur",
                        "Appliquer corrections",
                        "Suivre évolution"
                    ]
                })
                
        return recommendations
