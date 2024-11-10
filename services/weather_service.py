import httpx
from typing import Dict, Any
from datetime import datetime, timezone
from fastapi import HTTPException

class WeatherService:
    def __init__(self):
        self.api_key = "L6JNFAY48CA9P9G5NCGBYCNDA"
        self.base_url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        self.location = "Ebondi,Cameroon"  # Localisation des plantations FOFAL

    async def get_current_weather(self) -> Dict[str, Any]:
        """Récupère les conditions météorologiques actuelles pour Ebondi"""
        url = f"{self.base_url}/{self.location}/today"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "include": "current",
            "contentType": "json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                current = data.get("currentConditions", {})
                return {
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "temperature": current.get("temp", 0),
                    "humidity": current.get("humidity", 0),
                    "precipitation": current.get("precip", 0),
                    "wind_speed": current.get("windspeed", 0),
                    "conditions": current.get("conditions", ""),
                    "uv_index": current.get("uvindex", 0),
                    "cloud_cover": current.get("cloudcover", 0)
                }
        except httpx.HTTPError as e:
            return self._get_fallback_data()

    async def get_forecast(self, days: int = 7) -> Dict[str, Any]:
        """Récupère les prévisions météo pour les prochains jours"""
        url = f"{self.base_url}/{self.location}/next/{days}days"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "contentType": "json"
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params)
                response.raise_for_status()
                data = response.json()

                return {
                    "location": data.get("resolvedAddress", ""),
                    "days": [
                        {
                            "date": day.get("datetime", ""),
                            "temp_max": day.get("tempmax", 0),
                            "temp_min": day.get("tempmin", 0),
                            "precipitation": day.get("precip", 0),
                            "humidity": day.get("humidity", 0),
                            "conditions": day.get("conditions", ""),
                            "description": day.get("description", "")
                        }
                        for day in data.get("days", [])
                    ]
                }
        except httpx.HTTPError as e:
            return {"location": self.location, "days": []}

    async def get_agricultural_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques agricoles basées sur les données météo"""
        current = await self.get_current_weather()
        forecast = await self.get_forecast(3)  # Prévisions sur 3 jours

        # Analyse des conditions pour l'agriculture
        precipitation_risk = self._analyze_precipitation(
            current["precipitation"],
            [day["precipitation"] for day in forecast["days"]]
        )
        
        temperature_risk = self._analyze_temperature(
            current["temperature"],
            [day["temp_max"] for day in forecast["days"]]
        )

        return {
            "current_conditions": current,
            "risks": {
                "precipitation": precipitation_risk,
                "temperature": temperature_risk,
                "level": max(precipitation_risk["level"], temperature_risk["level"])
            },
            "recommendations": self._generate_recommendations(
                precipitation_risk,
                temperature_risk
            )
        }

    def _analyze_precipitation(self, current: float, forecast: list) -> Dict[str, Any]:
        """Analyse les risques liés aux précipitations"""
        avg_forecast = sum(forecast) / len(forecast) if forecast else current
        
        if current > 20 or avg_forecast > 20:
            return {
                "level": "HIGH",
                "message": "Risque d'inondation - Vérifier le drainage"
            }
        elif current > 10 or avg_forecast > 10:
            return {
                "level": "MEDIUM",
                "message": "Précipitations modérées - Surveillance recommandée"
            }
        return {
            "level": "LOW",
            "message": "Conditions de précipitation normales"
        }

    def _analyze_temperature(self, current: float, forecast: list) -> Dict[str, Any]:
        """Analyse les risques liés à la température"""
        max_temp = max([current] + forecast) if forecast else current
        
        if max_temp > 35:
            return {
                "level": "HIGH",
                "message": "Risque de stress thermique pour les cultures"
            }
        elif max_temp > 30:
            return {
                "level": "MEDIUM",
                "message": "Températures élevées - Surveillance recommandée"
            }
        return {
            "level": "LOW",
            "message": "Températures dans la normale"
        }

    def _generate_recommendations(
        self,
        precip_risk: Dict[str, Any],
        temp_risk: Dict[str, Any]
    ) -> list:
        """Génère des recommandations basées sur les risques"""
        recommendations = []

        if precip_risk["level"] == "HIGH":
            recommendations.extend([
                "Vérifier les systèmes de drainage",
                "Reporter les activités de plantation",
                "Protéger les jeunes plants"
            ])
        elif precip_risk["level"] == "MEDIUM":
            recommendations.append(
                "Surveiller l'accumulation d'eau dans les parcelles"
            )

        if temp_risk["level"] == "HIGH":
            recommendations.extend([
                "Augmenter l'irrigation",
                "Protéger les plants sensibles",
                "Éviter les travaux aux heures les plus chaudes"
            ])
        elif temp_risk["level"] == "MEDIUM":
            recommendations.append(
                "Maintenir une surveillance de l'hydratation des plants"
            )

        return recommendations if recommendations else [
            "Conditions favorables pour les activités agricoles normales"
        ]

    def _get_fallback_data(self) -> Dict[str, Any]:
        """Retourne des données par défaut en cas d'erreur"""
        return {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "temperature": 25.0,
            "humidity": 80,
            "precipitation": 0,
            "wind_speed": 5.0,
            "conditions": "Partiellement nuageux",
            "uv_index": 5,
            "cloud_cover": 50
        }
