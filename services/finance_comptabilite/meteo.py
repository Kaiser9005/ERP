"""
Service de gestion de l'impact météorologique sur les finances
"""

from sqlalchemy.orm import Session
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np

from models.production import Parcelle, CycleCulture
from models.comptabilite import CompteComptable, EcritureComptable
from services.weather_service import WeatherService
from services.cache_service import cache_result

class GestionMeteo:
    """Service de gestion de l'impact météorologique"""

    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self._cache_duration = timedelta(minutes=15)

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _get_meteo_impact(self,
                              parcelle_id: int,
                              date_debut: datetime,
                              date_fin: datetime) -> Dict:
        """Calcule l'impact météorologique sur une parcelle"""
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            return {}

        # Récupération des données météo
        meteo_data = await self.weather_service.get_historical_data(
            parcelle.latitude,
            parcelle.longitude,
            date_debut,
            date_fin
        )

        if not meteo_data:
            return {
                "score": 0,
                "facteurs": [],
                "couts_additionnels": {},
                "risques": [],
                "opportunites": []
            }

        # Analyse des facteurs météo
        facteurs = self._analyser_facteurs_meteo(meteo_data)
        
        # Calcul des coûts additionnels
        couts = self._calculer_couts_meteo(parcelle, facteurs)
        
        # Évaluation des risques et opportunités
        risques, opportunites = self._evaluer_risques_opportunites(facteurs)

        # Calcul du score d'impact global
        score = self._calculer_score_impact(facteurs)

        return {
            "score": score,
            "facteurs": facteurs,
            "couts_additionnels": couts,
            "risques": risques,
            "opportunites": opportunites,
            "date_analyse": datetime.now(datetime.timezone.utc).isoformat()
        }

    @cache_result(ttl_seconds=900)  # 15 minutes
    async def _calculer_provision_meteo(self,
                                      parcelle_id: int,
                                      date_debut: datetime,
                                      date_fin: datetime) -> float:
        """Calcule la provision pour risques météorologiques"""
        impact = await self._get_meteo_impact(parcelle_id, date_debut, date_fin)
        if not impact:
            return 0.0

        # Base de calcul : somme des coûts additionnels
        base = sum(impact["couts_additionnels"].values())
        
        # Facteur de risque : basé sur le score d'impact
        facteur_risque = impact["score"] / 100  # Score normalisé entre 0 et 1
        
        # Calcul de la provision
        provision = base * (1 + facteur_risque)
        
        return float(provision)

    def _analyser_facteurs_meteo(self, meteo_data: Dict) -> List[Dict]:
        """Analyse les facteurs météorologiques"""
        facteurs = []
        
        # Analyse des précipitations
        if "precipitation" in meteo_data:
            facteurs.append({
                "type": "precipitation",
                "valeur": meteo_data["precipitation"],
                "impact": self._evaluer_impact_precipitation(
                    meteo_data["precipitation"]
                )
            })
            
        # Analyse des températures
        if "temperature" in meteo_data:
            facteurs.append({
                "type": "temperature",
                "valeur": meteo_data["temperature"],
                "impact": self._evaluer_impact_temperature(
                    meteo_data["temperature"]
                )
            })
            
        # Analyse de l'humidité
        if "humidity" in meteo_data:
            facteurs.append({
                "type": "humidity",
                "valeur": meteo_data["humidity"],
                "impact": self._evaluer_impact_humidite(
                    meteo_data["humidity"]
                )
            })

        return facteurs

    def _calculer_couts_meteo(self,
                             parcelle: Parcelle,
                             facteurs: List[Dict]) -> Dict[str, float]:
        """Calcule les coûts additionnels liés à la météo"""
        couts = {}
        
        for facteur in facteurs:
            if facteur["impact"] > 0:  # Impact négatif nécessitant des coûts
                if facteur["type"] == "precipitation":
                    couts["drainage"] = self._cout_drainage(
                        parcelle,
                        facteur["valeur"]
                    )
                elif facteur["type"] == "temperature":
                    couts["protection"] = self._cout_protection_temperature(
                        parcelle,
                        facteur["valeur"]
                    )
                elif facteur["type"] == "humidity":
                    couts["ventilation"] = self._cout_ventilation(
                        parcelle,
                        facteur["valeur"]
                    )

        return couts

    def _evaluer_risques_opportunites(self,
                                    facteurs: List[Dict]) -> Tuple[List[str], List[str]]:
        """Évalue les risques et opportunités météorologiques"""
        risques = []
        opportunites = []
        
        for facteur in facteurs:
            if facteur["impact"] > 0.7:  # Impact très négatif
                risques.append(
                    f"Risque élevé lié à {facteur['type']}"
                )
            elif facteur["impact"] < -0.3:  # Impact positif
                opportunites.append(
                    f"Conditions favorables : {facteur['type']}"
                )

        return risques, opportunites

    def _calculer_score_impact(self, facteurs: List[Dict]) -> float:
        """Calcule le score d'impact global"""
        if not facteurs:
            return 0.0
            
        # Moyenne pondérée des impacts
        impacts = [f["impact"] for f in facteurs]
        return float(np.mean(impacts) * 100)  # Score sur 100

    def _evaluer_impact_precipitation(self, valeur: float) -> float:
        """Évalue l'impact des précipitations"""
        # Impact normalisé entre -1 et 1
        if valeur < 10:  # Trop sec
            return 0.8
        elif valeur > 50:  # Trop humide
            return 0.6
        else:  # Optimal
            return -0.5

    def _evaluer_impact_temperature(self, valeur: float) -> float:
        """Évalue l'impact de la température"""
        if valeur < 5 or valeur > 35:  # Extrêmes
            return 0.9
        elif 15 <= valeur <= 25:  # Optimal
            return -0.4
        else:  # Modéré
            return 0.3

    def _evaluer_impact_humidite(self, valeur: float) -> float:
        """Évalue l'impact de l'humidité"""
        if valeur < 30:  # Trop sec
            return 0.7
        elif valeur > 80:  # Trop humide
            return 0.5
        else:  # Optimal
            return -0.3

    def _cout_drainage(self, parcelle: Parcelle, precipitation: float) -> float:
        """Calcule le coût du drainage"""
        # Coût de base par m²
        cout_base = 0.5
        return cout_base * parcelle.surface * (precipitation / 50)

    def _cout_protection_temperature(self,
                                   parcelle: Parcelle,
                                   temperature: float) -> float:
        """Calcule le coût de protection contre la température"""
        # Coût de base par m²
        cout_base = 0.3
        return cout_base * parcelle.surface * (abs(temperature - 20) / 10)

    def _cout_ventilation(self, parcelle: Parcelle, humidite: float) -> float:
        """Calcule le coût de la ventilation"""
        # Coût de base par m²
        cout_base = 0.2
        return cout_base * parcelle.surface * (humidite / 100)