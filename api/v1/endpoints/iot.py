"""Endpoints pour la gestion des capteurs IoT."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.database import get_db
from models.iot_sensor import (
    IoTSensor, SensorReading,
    IoTSensorCreate, IoTSensorUpdate,
    SensorReadingCreate
)
from services.iot_service import IoTService
from services.weather_service import WeatherService

router = APIRouter(
    prefix="/iot",
    tags=["iot"]
)

def get_iot_service(
    db: Session = Depends(get_db),
    weather_service: WeatherService = Depends(WeatherService)
) -> IoTService:
    """Dépendance pour obtenir le service IoT."""
    return IoTService(db, weather_service)

@router.post("/sensors", response_model=IoTSensor)
async def create_sensor(
    sensor_data: IoTSensorCreate,
    service: IoTService = Depends(get_iot_service)
):
    """Crée un nouveau capteur IoT."""
    return await service.create_sensor(sensor_data)

@router.get("/sensors/{sensor_id}", response_model=IoTSensor)
async def get_sensor(
    sensor_id: UUID,
    service: IoTService = Depends(get_iot_service)
):
    """Récupère les détails d'un capteur."""
    sensor = await service.get_sensor(sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return sensor

@router.get("/parcelles/{parcelle_id}/sensors", response_model=List[IoTSensor])
async def get_parcelle_sensors(
    parcelle_id: UUID,
    service: IoTService = Depends(get_iot_service)
):
    """Récupère tous les capteurs d'une parcelle."""
    return await service.get_sensors_by_parcelle(parcelle_id)

@router.patch("/sensors/{sensor_id}", response_model=IoTSensor)
async def update_sensor(
    sensor_id: UUID,
    sensor_data: IoTSensorUpdate,
    service: IoTService = Depends(get_iot_service)
):
    """Met à jour un capteur."""
    sensor = await service.update_sensor(sensor_id, sensor_data)
    if not sensor:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return sensor

@router.delete("/sensors/{sensor_id}")
async def delete_sensor(
    sensor_id: UUID,
    service: IoTService = Depends(get_iot_service)
):
    """Supprime un capteur."""
    success = await service.delete_sensor(sensor_id)
    if not success:
        raise HTTPException(status_code=404, detail="Capteur non trouvé")
    return {"message": "Capteur supprimé avec succès"}

@router.post("/sensors/{sensor_id}/readings", response_model=SensorReading)
async def create_sensor_reading(
    sensor_id: UUID,
    reading_data: SensorReadingCreate,
    service: IoTService = Depends(get_iot_service)
):
    """Crée une nouvelle lecture pour un capteur."""
    return await service.create_reading(sensor_id, reading_data)

@router.get("/sensors/{sensor_id}/readings", response_model=List[SensorReading])
async def get_sensor_readings(
    sensor_id: UUID,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    limit: int = Query(100, gt=0, le=1000),
    service: IoTService = Depends(get_iot_service)
):
    """Récupère les lectures d'un capteur."""
    return await service.get_sensor_readings(
        sensor_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit
    )

@router.get("/sensors/{sensor_id}/stats")
async def get_sensor_stats(
    sensor_id: UUID,
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None),
    service: IoTService = Depends(get_iot_service)
):
    """Récupère les statistiques d'un capteur."""
    return await service.get_sensor_stats(
        sensor_id,
        start_date=start_date,
        end_date=end_date
    )

@router.get("/sensors/{sensor_id}/health")
async def check_sensor_health(
    sensor_id: UUID,
    service: IoTService = Depends(get_iot_service)
):
    """Vérifie l'état de santé d'un capteur."""
    return await service.check_sensor_health(sensor_id)

# Routes pour les données en masse
@router.post("/sensors/batch-readings")
async def create_batch_readings(
    readings: List[SensorReadingCreate],
    sensor_id: UUID,
    service: IoTService = Depends(get_iot_service)
):
    """Crée plusieurs lectures en une seule requête."""
    results = []
    for reading_data in readings:
        try:
            reading = await service.create_reading(sensor_id, reading_data)
            results.append({
                "success": True,
                "reading": reading
            })
        except Exception as e:
            results.append({
                "success": False,
                "error": str(e)
            })
    return results

@router.get("/sensors/health-check")
async def check_all_sensors_health(
    parcelle_id: Optional[UUID] = None,
    service: IoTService = Depends(get_iot_service)
):
    """Vérifie l'état de santé de tous les capteurs ou ceux d'une parcelle."""
    sensors = []
    if parcelle_id:
        sensors = await service.get_sensors_by_parcelle(parcelle_id)
    else:
        # TODO: Implémenter get_all_sensors dans le service
        pass

    results = []
    for sensor in sensors:
        try:
            health = await service.check_sensor_health(sensor.id)
            results.append({
                "sensor_id": sensor.id,
                "code": sensor.code,
                "health": health
            })
        except Exception as e:
            results.append({
                "sensor_id": sensor.id,
                "code": sensor.code,
                "error": str(e)
            })
    return results
