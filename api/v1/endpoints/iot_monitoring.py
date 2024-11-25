"""Endpoints pour le monitoring IoT."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.orm import Session

from db.database import get_db
from schemas.iot_monitoring import (
    MonitoringRequestSchema,
    MonitoringDataSchema,
    MonitoringDashboardSchema,
    MaintenanceRequestSchema,
    MaintenanceRecommendationSchema,
    MonitoringConfigSchema,
    MonitoringErrorSchema,
    SensorAlertWebhookSchema
)
from services.iot_monitoring_service import IoTMonitoringService
from services.iot_service import IoTService
from services.weather_service import WeatherService
from services.production_ml_service import ProductionMLService

router = APIRouter(prefix="/api/v1/iot-monitoring", tags=["IoT Monitoring"])

async def get_monitoring_service(
    db: Session = Depends(get_db),
    iot_service: IoTService = Depends(),
    weather_service: WeatherService = Depends(),
    ml_service: ProductionMLService = Depends()
) -> IoTMonitoringService:
    """Injection de dépendances pour le service de monitoring."""
    return IoTMonitoringService(db, iot_service, weather_service, ml_service)

@router.get(
    "/parcelles/{parcelle_id}",
    response_model=MonitoringDataSchema,
    responses={404: {"model": MonitoringErrorSchema}}
)
async def get_parcelle_monitoring(
    parcelle_id: UUID,
    request: MonitoringRequestSchema = Depends(),
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Récupère les données de monitoring pour une parcelle."""
    try:
        return await monitoring_service.get_parcelle_monitoring(
            parcelle_id=parcelle_id,
            start_date=request.start_date,
            end_date=request.end_date
        )
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=MonitoringErrorSchema(
                code="MONITORING_ERROR",
                message=str(e)
            ).dict()
        )

@router.get(
    "/parcelles/{parcelle_id}/dashboard",
    response_model=MonitoringDashboardSchema,
    responses={404: {"model": MonitoringErrorSchema}}
)
async def get_monitoring_dashboard(
    parcelle_id: UUID,
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Récupère les données du dashboard de monitoring."""
    try:
        return await monitoring_service.get_monitoring_dashboard(parcelle_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=MonitoringErrorSchema(
                code="DASHBOARD_ERROR",
                message=str(e)
            ).dict()
        )

@router.get(
    "/parcelles/{parcelle_id}/maintenance",
    response_model=List[MaintenanceRecommendationSchema],
    responses={404: {"model": MonitoringErrorSchema}}
)
async def get_maintenance_recommendations(
    parcelle_id: UUID,
    request: MaintenanceRequestSchema = Depends(),
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Récupère les recommandations de maintenance."""
    try:
        return await monitoring_service._get_maintenance_recommendations(parcelle_id)
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=MonitoringErrorSchema(
                code="MAINTENANCE_ERROR",
                message=str(e)
            ).dict()
        )

@router.post(
    "/webhooks/alerts",
    status_code=201,
    responses={400: {"model": MonitoringErrorSchema}}
)
async def register_alert_webhook(
    webhook: SensorAlertWebhookSchema,
    background_tasks: BackgroundTasks,
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Enregistre un webhook pour les alertes."""
    try:
        # Traitement asynchrone de l'alerte
        background_tasks.add_task(
            monitoring_service._process_alert_webhook,
            webhook
        )
        return {"status": "Alerte enregistrée"}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=MonitoringErrorSchema(
                code="WEBHOOK_ERROR",
                message=str(e)
            ).dict()
        )

@router.get(
    "/config",
    response_model=MonitoringConfigSchema,
    responses={404: {"model": MonitoringErrorSchema}}
)
async def get_monitoring_config(
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Récupère la configuration du monitoring."""
    try:
        # TODO: Implémenter la récupération de config depuis la base
        return MonitoringConfigSchema()
    except Exception as e:
        raise HTTPException(
            status_code=404,
            detail=MonitoringErrorSchema(
                code="CONFIG_ERROR",
                message=str(e)
            ).dict()
        )

@router.put(
    "/config",
    response_model=MonitoringConfigSchema,
    responses={400: {"model": MonitoringErrorSchema}}
)
async def update_monitoring_config(
    config: MonitoringConfigSchema,
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Met à jour la configuration du monitoring."""
    try:
        # TODO: Implémenter la mise à jour de config dans la base
        return config
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=MonitoringErrorSchema(
                code="CONFIG_UPDATE_ERROR",
                message=str(e)
            ).dict()
        )

@router.get(
    "/health",
    responses={500: {"model": MonitoringErrorSchema}}
)
async def check_monitoring_health(
    monitoring_service: IoTMonitoringService = Depends(get_monitoring_service)
):
    """Vérifie l'état de santé du système de monitoring."""
    try:
        # TODO: Implémenter la vérification complète du système
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow(),
            "components": {
                "database": "ok",
                "cache": "ok",
                "services": {
                    "iot": "ok",
                    "weather": "ok",
                    "ml": "ok"
                }
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=MonitoringErrorSchema(
                code="HEALTH_CHECK_ERROR",
                message=str(e)
            ).dict()
        )
