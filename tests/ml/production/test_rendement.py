"""
Tests pour le module de prédiction des rendements.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.production import Parcelle, Recolte
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.ml.production.rendement import RendementPredictor

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
def predictor(db_session, weather_service, iot_service):
    """Fixture pour le prédicteur."""
    service = RendementPredictor(db_session)
    service.weather_service = weather_service
    service.iot_service = iot_service
    return service

@pytest.fixture
def sample_historique():
    """Fixture pour l'historique des rendements."""
    return [{
        "date": date.today() - timedelta(days=i*30),
        "quantite": 1000.0 + i*100,
        "qualite": "A",
        "conditions_meteo": {
            "temperature": 25.0,
            "humidite": 65.0,
            "precipitation": 10.0
        }
    } for i in range(5)]

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

class TestRendementPredictor:
    """Tests pour RendementPredictor."""

    async def test_predict_rendement(
        self,
        predictor,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la prédiction de rendement."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=30)
        
        predictor._get_historique_rendements = AsyncMock(
            return_value=sample_historique
        )
        predictor.weather_service.get_historical_data.return_value = sample_meteo
        predictor.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        result = await predictor.predict_rendement(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Vérifications
        assert isinstance(result, dict)
        assert "rendement_prevu" in result
        assert isinstance(result["rendement_prevu"], float)
        assert result["rendement_prevu"] > 0
        
        assert "intervalle_confiance" in result
        assert isinstance(result["intervalle_confiance"], dict)
        assert "min" in result["intervalle_confiance"]
        assert "max" in result["intervalle_confiance"]
        assert result["intervalle_confiance"]["min"] < result["intervalle_confiance"]["max"]
        
        assert "facteurs_impact" in result
        assert isinstance(result["facteurs_impact"], list)
        assert len(result["facteurs_impact"]) > 0

    async def test_predict_rendement_without_history(
        self,
        predictor,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la prédiction sans historique."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=30)
        
        predictor._get_historique_rendements = AsyncMock(return_value=[])
        predictor.weather_service.get_historical_data.return_value = sample_meteo
        predictor.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        result = await predictor.predict_rendement(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Vérifications
        assert isinstance(result, dict)
        assert "rendement_prevu" in result
        assert isinstance(result["rendement_prevu"], float)
        assert result["rendement_prevu"] >= 0
        
        # L'intervalle de confiance devrait être plus large sans historique
        assert result["intervalle_confiance"]["max"] - result["intervalle_confiance"]["min"] > 100

    def test_predict_with_model(self, predictor):
        """Test de la prédiction avec le modèle."""
        # Configuration
        features = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        
        # Exécution
        result = predictor._predict_with_model(features)
        
        # Vérifications
        assert isinstance(result, float)
        assert result > 0
        
        # Test avec des features nulles
        result_zero = predictor._predict_with_model(np.zeros(9))
        assert result_zero == 0.0

    def test_calculate_confidence(self, predictor, sample_historique):
        """Test du calcul de l'intervalle de confiance."""
        # Test avec historique
        prediction = 1000.0
        confidence = predictor._calculate_confidence(prediction, sample_historique)
        
        assert isinstance(confidence, dict)
        assert "min" in confidence
        assert "max" in confidence
        assert confidence["min"] < prediction < confidence["max"]
        
        # Test sans historique
        confidence_no_history = predictor._calculate_confidence(prediction, [])
        assert confidence_no_history["min"] == prediction * 0.8
        assert confidence_no_history["max"] == prediction * 1.2

    async def test_analyze_impact_factors(self, predictor):
        """Test de l'analyse des facteurs d'impact."""
        # Configuration
        features = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0])
        
        # Exécution
        factors = await predictor._analyze_impact_factors(features)
        
        # Vérifications
        assert isinstance(factors, list)
        assert len(factors) == 3  # Historique, Météo, IoT
        
        for factor in factors:
            assert "facteur" in factor
            assert "impact" in factor
            assert "description" in factor
            assert 0 <= factor["impact"] <= 1

    async def test_error_handling(self, predictor):
        """Test de la gestion des erreurs."""
        # Test avec une parcelle invalide
        with pytest.raises(ValueError):
            await predictor.predict_rendement(
                "",
                date.today(),
                date.today() + timedelta(days=30)
            )
        
        # Test avec des dates invalides
        with pytest.raises(ValueError):
            await predictor.predict_rendement(
                "P1",
                date.today() + timedelta(days=30),
                date.today()
            )
