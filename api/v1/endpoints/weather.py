from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any
from db.database import get_db
from models.auth import Utilisateur
from api.v1.endpoints.auth import get_current_user
from services.weather_service import WeatherService

router = APIRouter()

@router.get("/current")
async def get_current_weather(
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
) -> Dict[str, Any]:
    """Récupère les données météorologiques actuelles"""
    weather_service = WeatherService()
    return await weather_service.get_current_weather()