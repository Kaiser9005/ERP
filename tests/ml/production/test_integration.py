"""
Tests d'intégration pour les services ML de production.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.production import Parcelle, QualiteRecolte
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.ml.production.service import ProductionMLService

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def weather_service():
    """Fixture pour le service météo."""
    return AsyncMock(spec=WeatherService)

@pytest.fixture
def iot_service():
    """Fixture pour le service IoT."""
    return AsyncMock(spec=IoTService)

@pytest.fixture
def service(db_session, weather_service, iot_service):
    """Fixture pour le service ML de production."""
    service = ProductionMLService(db_session)
    service.rendement_predictor.weather_service = weather_service
    service.rendement_predictor.iot_service = iot_service
    service.cycle_optimizer.weather_service = weather_service
    service.meteo_analyzer.weather_service = weather_service
    service.meteo_analyzer.iot_service = iot_service
    service.qualite_predictor.weather_service = weather_service
    service.qualite_predictor.iot_service = iot_service
    return service

@pytest.fixture
def sample_historique():
    """Fixture pour l'historique des récoltes."""
    return [{
        "date": date.today() - timedelta(days=i*30),
        "rendement": 1000.0 + i*100,
        "qualite": QualiteRecolte.A if i % 3 == 0 else (
            QualiteRecolte.B if i % 3 == 1 else QualiteRecolte.C
        ),
        "conditions_meteo": {
            "temperature": 25.0,
            "humidite": 65.0,
            "precipitation": 10.0
        }
    } for i in range(6)]

@pytest.fixture
def sample_meteo():
    """Fixture pour les données météo."""
    return [{
        "date": date.today() + timedelta(days=i),
        "temperature": 25.0,
        "humidite": 65.0,
        "precipitation": 10.0,
        "vent": 15.0
    } for i in range(10)]

@pytest.fixture
def sample_iot_data():
    """Fixture pour les données IoT."""
    return [{
        "date": date.today() + timedelta(days=i),
        "capteur": "SOIL_TEMP",
        "valeur": 22.0 + i*0.5
    } for i in range(10)]

class TestProductionMLIntegration:
    """Tests d'intégration pour ProductionMLService."""

    async def test_rendement_with_cycle_optimization(
        self,
        service,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la prédiction de rendement avec optimisation du cycle."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=90)
        
        service.rendement_predictor._get_historique_rendements = AsyncMock(
            return_value=sample_historique
        )
        service.cycle_optimizer._get_historique_cycles = AsyncMock(
            return_value=sample_historique
        )
        service.weather_service.get_forecast.return_value = sample_meteo
        service.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        rendement = await service.predict_rendement(
            parcelle_id,
            date_debut,
            date_fin
        )
        cycle = await service.optimize_cycle_culture(
            parcelle_id,
            date_debut
        )
        
        # Vérifications
        assert isinstance(rendement, dict)
        assert "rendement_prevu" in rendement
        assert isinstance(rendement["rendement_prevu"], float)
        
        assert isinstance(cycle, dict)
        assert "date_debut_optimale" in cycle
        assert isinstance(cycle["date_debut_optimale"], date)
        
        # Vérification cohérence
        if rendement["rendement_prevu"] < 1000:
            assert any(
                "cycle" in r.lower()
                for r in rendement.get("recommandations", [])
            )
            assert cycle["date_debut_optimale"] > date_debut

    async def test_qualite_with_meteo_impact(
        self,
        service,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la prédiction de qualité avec impact météo."""
        # Configuration
        parcelle_id = "P1"
        date_recolte = date.today() + timedelta(days=30)
        
        service.qualite_predictor._get_historique_qualite = AsyncMock(
            return_value=sample_historique
        )
        service.meteo_analyzer._get_historique_meteo = AsyncMock(
            return_value=sample_historique
        )
        service.weather_service.get_forecast.return_value = sample_meteo
        service.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        qualite = await service.predict_qualite(
            parcelle_id,
            date_recolte
        )
        meteo = await service.analyze_meteo_impact(
            parcelle_id,
            date.today(),
            date_recolte
        )
        
        # Vérifications
        assert isinstance(qualite, dict)
        assert "qualite_prevue" in qualite
        assert isinstance(qualite["qualite_prevue"], QualiteRecolte)
        
        assert isinstance(meteo, dict)
        assert "impact_global" in meteo
        assert isinstance(meteo["impact_global"], str)
        
        # Vérification cohérence
        if meteo["impact_global"] == "HAUT":
            assert qualite["qualite_prevue"] != QualiteRecolte.A
            assert any(
                "météo" in f["facteur"].lower()
                for f in qualite.get("facteurs_impact", [])
            )

    async def test_cycle_with_meteo_constraints(
        self,
        service,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de l'optimisation du cycle avec contraintes météo."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        
        service.cycle_optimizer._get_historique_cycles = AsyncMock(
            return_value=sample_historique
        )
        service.meteo_analyzer._get_historique_meteo = AsyncMock(
            return_value=sample_historique
        )
        service.weather_service.get_forecast.return_value = sample_meteo
        service.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        meteo = await service.analyze_meteo_impact(
            parcelle_id,
            date_debut,
            date_debut + timedelta(days=90)
        )
        cycle = await service.optimize_cycle_culture(
            parcelle_id,
            date_debut
        )
        
        # Vérifications
        assert isinstance(meteo, dict)
        assert "periodes_risque" in meteo
        assert isinstance(meteo["periodes_risque"], list)
        
        assert isinstance(cycle, dict)
        assert "etapes" in cycle
        assert isinstance(cycle["etapes"], list)
        
        # Vérification cohérence
        if meteo["periodes_risque"]:
            # Les étapes sensibles ne devraient pas être planifiées 
            # pendant les périodes à risque
            periodes_risque = {
                d["date"]
                for d in meteo["periodes_risque"]
            }
            etapes_sensibles = {
                e["date_debut"]
                for e in cycle["etapes"]
                if e.get("sensible_meteo", False)
            }
            assert not periodes_risque.intersection(etapes_sensibles)

    async def test_rendement_impact_on_quality(
        self,
        service,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de l'impact du rendement sur la qualité."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=90)
        
        service.rendement_predictor._get_historique_rendements = AsyncMock(
            return_value=sample_historique
        )
        service.qualite_predictor._get_historique_qualite = AsyncMock(
            return_value=sample_historique
        )
        service.weather_service.get_forecast.return_value = sample_meteo
        service.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        rendement = await service.predict_rendement(
            parcelle_id,
            date_debut,
            date_fin
        )
        qualite = await service.predict_qualite(
            parcelle_id,
            date_fin
        )
        
        # Vérifications
        assert isinstance(rendement, dict)
        assert "rendement_prevu" in rendement
        
        assert isinstance(qualite, dict)
        assert "qualite_prevue" in qualite
        
        # Vérification cohérence
        if rendement["rendement_prevu"] > 1500:
            assert qualite["qualite_prevue"] != QualiteRecolte.A
            assert any(
                "rendement" in f["facteur"].lower()
                for f in qualite.get("facteurs_impact", [])
            )
