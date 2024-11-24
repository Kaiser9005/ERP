"""
Module d'intégration IoT avec la finance et la comptabilité
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

class GestionIoT:
    """Gestion de l'intégration IoT avec la finance et la comptabilité"""
    
    def __init__(self, db: Session):
        self.db = db
        self.iot_service = IoTService(db)

    async def _get_iot_analysis(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse des données IoT pour la parcelle"""
        # Récupération des capteurs de la parcelle
        sensors = self.db.query(IoTSensor).filter(
            IoTSensor.parcelle_id == parcelle_id
        ).all()
        
        if not sensors:
            return {"status": "Aucun capteur installé"}
            
        analysis = {
            "alertes": [],
            "mesures": {},
            "tendances": {},
            "recommendations": [],
            "impact_financier": {},
            "provisions_suggeres": {}
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
                
                # Détection des tendances
                analysis["tendances"][sensor.type] = self._analyser_tendance(data)
                
                # Génération d'alertes si nécessaire
                alertes = self._generer_alertes_iot(sensor.type, data)
                if alertes:
                    analysis["alertes"].extend(alertes)
                    
                # Analyse de l'impact financier
                impact = self._analyser_impact_financier(
                    sensor.type,
                    data,
                    analysis["tendances"][sensor.type]
                )
                analysis["impact_financier"][sensor.type] = impact
                
                # Calcul des provisions suggérées
                if impact["score"] > 50:  # Seuil d'impact significatif
                    provision = self._calculer_provision_iot(
                        sensor.type,
                        impact,
                        analysis["tendances"][sensor.type]
                    )
                    if provision:
                        analysis["provisions_suggeres"][sensor.type] = provision
                    
        return analysis

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
