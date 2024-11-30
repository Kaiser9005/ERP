"""Service de gestion des capteurs IoT et de leurs données."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, func

from models.iot_sensor import IoTSensor, SensorReading, SensorStatus
from schemas.iot_monitoring import (
    IoTSensorCreate, IoTSensorUpdate,
    SensorReadingCreate
)
from services.weather_service import WeatherService
from core.config import settings

class IoTService:
    """Service gérant les capteurs IoT et leurs données."""

    def __init__(self, db: Session, weather_service: WeatherService):
        self.db = db
        self.weather_service = weather_service

    async def create_sensor(self, sensor_data: IoTSensorCreate) -> IoTSensor:
        """Crée un nouveau capteur."""
        sensor = IoTSensor(**sensor_data.dict())
        self.db.add(sensor)
        try:
            self.db.commit()
            self.db.refresh(sensor)
            return sensor
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_sensor(self, sensor_id: UUID) -> Optional[IoTSensor]:
        """Récupère un capteur par son ID."""
        return self.db.query(IoTSensor).filter(IoTSensor.id == sensor_id).first()

    async def get_sensors_by_parcelle(self, parcelle_id: UUID) -> List[IoTSensor]:
        """Récupère tous les capteurs d'une parcelle."""
        return self.db.query(IoTSensor).filter(IoTSensor.parcelle_id == parcelle_id).all()

    async def update_sensor(self, sensor_id: UUID, sensor_data: IoTSensorUpdate) -> Optional[IoTSensor]:
        """Met à jour un capteur."""
        sensor = await self.get_sensor(sensor_id)
        if not sensor:
            return None

        for field, value in sensor_data.dict(exclude_unset=True).items():
            setattr(sensor, field, value)

        try:
            self.db.commit()
            self.db.refresh(sensor)
            return sensor
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def delete_sensor(self, sensor_id: UUID) -> bool:
        """Supprime un capteur."""
        sensor = await self.get_sensor(sensor_id)
        if not sensor:
            return False

        try:
            self.db.delete(sensor)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def create_reading(self, sensor_id: UUID, reading_data: SensorReadingCreate) -> SensorReading:
        """Crée une nouvelle lecture de capteur."""
        sensor = await self.get_sensor(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur non trouvé")

        reading = SensorReading(
            capteur_id=sensor_id,
            **reading_data.dict()
        )
        self.db.add(reading)

        try:
            self.db.commit()
            self.db.refresh(reading)
            
            # Vérification des seuils et création d'alertes si nécessaire
            await self._check_thresholds(sensor, reading)
            
            return reading
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    async def get_sensor_readings(
        self, 
        sensor_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[SensorReading]:
        """Récupère les lectures d'un capteur avec filtres optionnels."""
        query = self.db.query(SensorReading).filter(SensorReading.capteur_id == sensor_id)

        if start_date:
            query = query.filter(SensorReading.timestamp >= start_date)
        if end_date:
            query = query.filter(SensorReading.timestamp <= end_date)

        return query.order_by(SensorReading.timestamp.desc()).limit(limit).all()

    async def get_sensor_stats(
        self,
        sensor_id: UUID,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Calcule les statistiques pour un capteur."""
        query = self.db.query(
            func.avg(SensorReading.valeur).label('moyenne'),
            func.min(SensorReading.valeur).label('minimum'),
            func.max(SensorReading.valeur).label('maximum'),
            func.count(SensorReading.id).label('nombre_lectures')
        ).filter(SensorReading.capteur_id == sensor_id)

        if start_date:
            query = query.filter(SensorReading.timestamp >= start_date)
        if end_date:
            query = query.filter(SensorReading.timestamp <= end_date)

        result = query.first()
        return {
            'moyenne': float(result.moyenne) if result.moyenne else 0,
            'minimum': float(result.minimum) if result.minimum else 0,
            'maximum': float(result.maximum) if result.maximum else 0,
            'nombre_lectures': result.nombre_lectures
        }

    async def _check_thresholds(self, sensor: IoTSensor, reading: SensorReading) -> None:
        """Vérifie si une lecture dépasse les seuils configurés."""
        if not sensor.seuils_alerte:
            return

        seuils = sensor.seuils_alerte
        valeur = reading.valeur

        if 'min' in seuils and valeur < seuils['min']:
            await self._create_alert(
                sensor,
                f"Valeur {valeur} inférieure au seuil minimum {seuils['min']}",
                "warning"
            )
        
        if 'max' in seuils and valeur > seuils['max']:
            await self._create_alert(
                sensor,
                f"Valeur {valeur} supérieure au seuil maximum {seuils['max']}",
                "warning"
            )

        if 'critique_min' in seuils and valeur < seuils['critique_min']:
            await self._create_alert(
                sensor,
                f"Valeur {valeur} inférieure au seuil critique minimum {seuils['critique_min']}",
                "critical"
            )
            
        if 'critique_max' in seuils and valeur > seuils['critique_max']:
            await self._create_alert(
                sensor,
                f"Valeur {valeur} supérieure au seuil critique maximum {seuils['critique_max']}",
                "critical"
            )

    async def _create_alert(self, sensor: IoTSensor, message: str, level: str) -> None:
        """Crée une alerte pour un capteur."""
        # TODO: Implémenter la création d'alertes une fois le système d'alertes développé
        print(f"ALERTE {level} - Capteur {sensor.code}: {message}")

    async def check_sensor_health(self, sensor_id: UUID) -> Dict[str, Any]:
        """Vérifie l'état de santé d'un capteur."""
        sensor = await self.get_sensor(sensor_id)
        if not sensor:
            raise HTTPException(status_code=404, detail="Capteur non trouvé")

        # Récupère la dernière lecture
        last_reading = self.db.query(SensorReading)\
            .filter(SensorReading.capteur_id == sensor_id)\
            .order_by(SensorReading.timestamp.desc())\
            .first()

        if not last_reading:
            return {
                "status": SensorStatus.ERREUR,
                "message": "Aucune lecture disponible",
                "last_reading": None,
                "battery_level": None,
                "signal_quality": None
            }

        # Vérifie si le capteur est actif et envoie des données récentes
        time_since_last_reading = datetime.utcnow() - last_reading.timestamp
        max_silence_duration = sensor.intervalle_lecture * 3  # 3 fois l'intervalle normal

        status = SensorStatus.ACTIF
        message = "Capteur fonctionnel"

        if time_since_last_reading.total_seconds() > max_silence_duration:
            status = SensorStatus.ERREUR
            message = f"Pas de lecture depuis {time_since_last_reading.total_seconds()/60:.1f} minutes"

        if last_reading.niveau_batterie and last_reading.niveau_batterie < 20:
            status = SensorStatus.MAINTENANCE
            message = f"Niveau de batterie faible ({last_reading.niveau_batterie}%)"

        if last_reading.qualite_signal and last_reading.qualite_signal < 30:
            status = SensorStatus.MAINTENANCE
            message = f"Qualité du signal faible ({last_reading.qualite_signal}%)"

        return {
            "status": status,
            "message": message,
            "last_reading": last_reading,
            "battery_level": last_reading.niveau_batterie,
            "signal_quality": last_reading.qualite_signal
        }
