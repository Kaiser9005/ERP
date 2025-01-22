"""
Service de gestion de l'intégration IoT avec la finance
"""

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

from models.iot_sensor import IoTSensor, SensorReading
from models.production import Parcelle
from models.comptabilite import CompteComptable, EcritureComptable
from services.iot_service import IoTService
from services.cache_service import cache_result

class GestionIoT:
    """Service de gestion de l'intégration IoT"""

    def __init__(self, db: Session):
        self.db = db
        self.iot_service = IoTService(db)
        self._cache_duration = timedelta(minutes=15)

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _get_iot_analysis(self,
                              parcelle_id: int,
                              date_debut: datetime,
                              date_fin: datetime) -> Dict:
        """Analyse des données IoT pour une parcelle"""
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            return {}

        # Récupération des capteurs
        capteurs = self.db.query(IoTSensor).filter(
            IoTSensor.parcelle_id == parcelle_id
        ).all()

        if not capteurs:
            return {
                "status": "no_sensors",
                "alertes": [],
                "tendances": {},
                "recommandations": []
            }

        # Récupération des lectures
        lectures = []
        for capteur in capteurs:
            lectures.extend(
                self.db.query(SensorReading).filter(
                    SensorReading.sensor_id == capteur.id,
                    SensorReading.timestamp >= date_debut,
                    SensorReading.timestamp <= date_fin
                ).all()
            )

        # Analyse des tendances
        tendances = await self._analyser_tendance(lectures)
        
        # Génération des alertes
        alertes = await self._generer_alertes_iot(lectures, tendances)
        
        # Génération des recommandations
        recommandations = self._generer_recommandations(tendances, alertes)

        return {
            "status": "ok",
            "alertes": alertes,
            "tendances": tendances,
            "recommandations": recommandations,
            "date_analyse": datetime.now(datetime.timezone.utc).isoformat()
        }

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _analyser_tendance(self,
                               lectures: List[SensorReading]) -> Dict[str, Dict]:
        """Analyse les tendances des données IoT"""
        if not lectures:
            return {}

        # Conversion en DataFrame pour analyse
        df = pd.DataFrame([{
            'timestamp': l.timestamp,
            'type': l.sensor.type,
            'value': l.value
        } for l in lectures])

        tendances = {}
        for type_capteur in df['type'].unique():
            data_capteur = df[df['type'] == type_capteur]
            
            # Calcul des statistiques
            stats = {
                'moyenne': float(data_capteur['value'].mean()),
                'min': float(data_capteur['value'].min()),
                'max': float(data_capteur['value'].max()),
                'ecart_type': float(data_capteur['value'].std())
            }
            
            # Calcul de la tendance
            if len(data_capteur) > 1:
                x = range(len(data_capteur))
                y = data_capteur['value'].values
                z = np.polyfit(x, y, 1)
                stats['tendance'] = float(z[0])  # Pente de la régression
            else:
                stats['tendance'] = 0.0

            tendances[type_capteur] = stats

        return tendances

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _generer_alertes_iot(self,
                                 lectures: List[SensorReading],
                                 tendances: Dict[str, Dict]) -> List[Dict]:
        """Génère les alertes basées sur les données IoT"""
        alertes = []
        
        for type_capteur, stats in tendances.items():
            # Alerte sur les valeurs extrêmes
            if stats['max'] > self._get_seuil_max(type_capteur):
                alertes.append({
                    'type': 'extreme_high',
                    'capteur': type_capteur,
                    'valeur': stats['max'],
                    'seuil': self._get_seuil_max(type_capteur),
                    'priorite': 'haute'
                })
                
            if stats['min'] < self._get_seuil_min(type_capteur):
                alertes.append({
                    'type': 'extreme_low',
                    'capteur': type_capteur,
                    'valeur': stats['min'],
                    'seuil': self._get_seuil_min(type_capteur),
                    'priorite': 'haute'
                })
                
            # Alerte sur les tendances
            if abs(stats['tendance']) > self._get_seuil_tendance(type_capteur):
                alertes.append({
                    'type': 'trend',
                    'capteur': type_capteur,
                    'tendance': stats['tendance'],
                    'seuil': self._get_seuil_tendance(type_capteur),
                    'priorite': 'moyenne'
                })

        return alertes

    def _generer_recommandations(self,
                               tendances: Dict[str, Dict],
                               alertes: List[Dict]) -> List[str]:
        """Génère des recommandations basées sur l'analyse IoT"""
        recommandations = []
        
        # Recommandations basées sur les alertes
        for alerte in alertes:
            if alerte['type'] == 'extreme_high':
                recommandations.append(
                    f"Réduire les niveaux de {alerte['capteur']}"
                )
            elif alerte['type'] == 'extreme_low':
                recommandations.append(
                    f"Augmenter les niveaux de {alerte['capteur']}"
                )
            elif alerte['type'] == 'trend':
                if alerte['tendance'] > 0:
                    recommandations.append(
                        f"Surveiller l'augmentation de {alerte['capteur']}"
                    )
                else:
                    recommandations.append(
                        f"Surveiller la diminution de {alerte['capteur']}"
                    )

        # Recommandations basées sur les tendances
        for type_capteur, stats in tendances.items():
            if stats['ecart_type'] > self._get_seuil_variation(type_capteur):
                recommandations.append(
                    f"Stabiliser les variations de {type_capteur}"
                )

        return list(set(recommandations))  # Dédoublonnage

    def _get_seuil_max(self, type_capteur: str) -> float:
        """Retourne le seuil maximum pour un type de capteur"""
        seuils = {
            'temperature': 35.0,
            'humidity': 80.0,
            'soil_moisture': 90.0,
            'light': 1000.0,
            'co2': 1000.0
        }
        return seuils.get(type_capteur, float('inf'))

    def _get_seuil_min(self, type_capteur: str) -> float:
        """Retourne le seuil minimum pour un type de capteur"""
        seuils = {
            'temperature': 5.0,
            'humidity': 20.0,
            'soil_moisture': 10.0,
            'light': 0.0,
            'co2': 300.0
        }
        return seuils.get(type_capteur, float('-inf'))

    def _get_seuil_tendance(self, type_capteur: str) -> float:
        """Retourne le seuil de tendance pour un type de capteur"""
        seuils = {
            'temperature': 0.5,
            'humidity': 2.0,
            'soil_moisture': 1.0,
            'light': 50.0,
            'co2': 10.0
        }
        return seuils.get(type_capteur, 1.0)

    def _get_seuil_variation(self, type_capteur: str) -> float:
        """Retourne le seuil de variation pour un type de capteur"""
        seuils = {
            'temperature': 2.0,
            'humidity': 5.0,
            'soil_moisture': 3.0,
            'light': 100.0,
            'co2': 20.0
        }
        return seuils.get(type_capteur, 2.0)