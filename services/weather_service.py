import aiohttp
from typing import Dict, Any
from core.config import APP_CONFIG

class WeatherService:
    def __init__(self):
        self.api_key = APP_CONFIG.get("weather_api_key", "")
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.coordinates = {
            "lat": 4.0511,  # Coordonnées de FOFAL
            "lon": 9.7679
        }

    async def get_current_weather(self) -> Dict[str, Any]:
        """Récupère les données météo actuelles depuis l'API OpenWeather"""
        async with aiohttp.ClientSession() as session:
            params = {
                "lat": self.coordinates["lat"],
                "lon": self.coordinates["lon"],
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with session.get(f"{self.base_url}/weather", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "temperature": round(data["main"]["temp"], 1),
                        "humidity": data["main"]["humidity"],
                        "windSpeed": round(data["wind"]["speed"] * 3.6, 1),  # Conversion en km/h
                        "uvIndex": await self._get_uv_index(),
                        "forecast": await self._get_forecast()
                    }
                return self._get_fallback_data()

    async def _get_uv_index(self) -> int:
        """Récupère l'index UV"""
        async with aiohttp.ClientSession() as session:
            params = {
                "lat": self.coordinates["lat"],
                "lon": self.coordinates["lon"],
                "appid": self.api_key
            }
            
            async with session.get(f"{self.base_url}/uvi", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return round(data["value"])
                return 0

    async def _get_forecast(self) -> list:
        """Récupère les prévisions météo"""
        async with aiohttp.ClientSession() as session:
            params = {
                "lat": self.coordinates["lat"],
                "lon": self.coordinates["lon"],
                "appid": self.api_key,
                "units": "metric"
            }
            
            async with session.get(f"{self.base_url}/forecast", params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return [
                        {
                            "date": item["dt_txt"],
                            "temperature": round(item["main"]["temp"], 1),
                            "precipitation": item["pop"] * 100  # Probabilité de précipitation en %
                        }
                        for item in data["list"][:5]  # 5 prochaines périodes
                    ]
                return []

    def _get_fallback_data(self) -> Dict[str, Any]:
        """Retourne des données par défaut en cas d'erreur"""
        return {
            "temperature": 25.0,
            "humidity": 80,
            "windSpeed": 5.0,
            "uvIndex": 5,
            "forecast": []
        }