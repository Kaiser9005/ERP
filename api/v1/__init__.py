from fastapi import APIRouter
from .endpoints import (
    employes,
    inventaire,
    production,
    weather,
    activities,
    dashboard,
    auth,
    parametrage,
    iot_monitoring
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentification"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Tableau de bord"])
api_router.include_router(employes.router, prefix="/employes", tags=["Employés"])
api_router.include_router(inventaire.router, prefix="/inventaire", tags=["Inventaire"])
api_router.include_router(production.router, prefix="/production", tags=["Production"])
api_router.include_router(weather.router, prefix="/weather", tags=["Météo"])
api_router.include_router(activities.router, prefix="/activities", tags=["Activités"])
api_router.include_router(parametrage.router, prefix="/parametrage", tags=["Paramétrage"])
api_router.include_router(iot_monitoring.router, prefix="/iot-monitoring", tags=["IoT Monitoring"])
