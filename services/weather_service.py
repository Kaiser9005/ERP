import httpx
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
import json
from redis import Redis
from fastapi import HTTPException
from core.config import settings
from services.notification_service import NotificationService
from models.notification import TypeNotification, ModuleNotification

class WeatherService:
    def __init__(self, db=None):
        self.api_key = settings.WEATHER_API_KEY
        self.base_url = settings.WEATHER_API_URL
        self.location = "Ebondi,Cameroon"  # Localisation des plantations FOFAL
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        self.notification_service = NotificationService()
        self.cache_ttl = 1800  # 30 minutes en secondes
        self.max_retries = 3
        self.timeout = 10.0  # timeout en secondes

    async def get_current_weather(self) -> Dict[str, Any]:
        """Récupère les conditions météorologiques actuelles pour Ebondi"""
        cache_key = f"weather:current:{self.location}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data

        url = f"{self.base_url}/{self.location}/today"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "include": "current",
            "contentType": "json"
        }

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    current = data.get("currentConditions", {})
                    result = {
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "temperature": current.get("temp", 0),
                        "humidity": current.get("humidity", 0),
                        "precipitation": current.get("precip", 0),
                        "wind_speed": current.get("windspeed", 0),
                        "conditions": current.get("conditions", ""),
                        "uv_index": current.get("uvindex", 0),
                        "cloud_cover": current.get("cloudcover", 0)
                    }
                    
                    self._save_to_cache(cache_key, result)
                    return result
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    await self._handle_error("Erreur lors de la récupération des données météo actuelles", str(e))
                    return self._get_fallback_data()
                continue

    async def get_forecast(self, days: int = 7) -> Dict[str, Any]:
        """Récupère les prévisions météo pour les prochains jours"""
        cache_key = f"weather:forecast:{self.location}:{days}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data

        url = f"{self.base_url}/{self.location}/next/{days}days"
        params = {
            "key": self.api_key,
            "unitGroup": "metric",
            "contentType": "json"
        }

        for attempt in range(self.max_retries):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.get(url, params=params)
                    response.raise_for_status()
                    data = response.json()

                    result = {
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
                    
                    self._save_to_cache(cache_key, result)
                    return result
            except httpx.HTTPError as e:
                if attempt == self.max_retries - 1:
                    await self._handle_error("Erreur lors de la récupération des prévisions météo", str(e))
                    return {"location": self.location, "days": []}
                continue

    async def get_agricultural_metrics(self) -> Dict[str, Any]:
        """Calcule les métriques agricoles basées sur les données météo"""
        cache_key = f"weather:metrics:{self.location}"
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data

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

        result = {
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

        # Envoyer des notifications si risque élevé
        if result["risks"]["level"] == "HIGH":
            await self._send_risk_notification(result["risks"])

        self._save_to_cache(cache_key, result)
        return result

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

    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Récupère les données du cache Redis"""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def _save_to_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Sauvegarde les données dans le cache Redis"""
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(data)
        )

    async def _handle_error(self, message: str, error_details: str) -> None:
        """Gère les erreurs du service météo"""
        error_data = {
            "service": "WeatherService",
            "message": message,
            "details": error_details,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.notification_service.create_notification(
            titre="Erreur Service Météo",
            message=json.dumps(error_data),
            type=TypeNotification.ERROR,
            module=ModuleNotification.WEATHER,
            destinataire_id="admin"
        )

    async def _send_risk_notification(self, risks: Dict[str, Any]) -> None:
        """Envoie une notification en cas de risque élevé"""
        message = f"ALERTE MÉTÉO: Risque {risks['level']}\n"
        if risks["precipitation"]["level"] == "HIGH":
            message += f"- Précipitations: {risks['precipitation']['message']}\n"
        if risks["temperature"]["level"] == "HIGH":
            message += f"- Température: {risks['temperature']['message']}"
        
        await self.notification_service.create_notification(
            titre="Alerte Risque Météo",
            message=message,
            type=TypeNotification.WARNING,
            module=ModuleNotification.WEATHER,
            destinataire_id="production"
        )
