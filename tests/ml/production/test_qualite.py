"""
Tests pour le module de prédiction de la qualité des récoltes.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.production import QualiteRecolte
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.ml.production.qualite import QualitePredictor

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
    service = QualitePredictor(db_session)
    service.weather_service = weather_service
    service.iot_service = iot_service
    return service

@pytest.fixture
def sample_historique():
    """Fixture pour l'historique des qualités."""
    return [{
        "date": date.today() - timedelta(days=i*30),
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

class TestQualitePredictor:
    """Tests pour QualitePredictor."""

    async def test_predict_qualite(
        self,
        predictor,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la prédiction de qualité."""
        # Configuration
        parcelle_id = "P1"
        date_recolte = date.today() + timedelta(days=30)
        
        predictor._get_historique_qualite = AsyncMock(
            return_value=sample_historique
        )
        predictor.weather_service.get_forecast.return_value = sample_meteo
        predictor.iot_service.get_sensor_data.return_value = sample_iot_data
        
        # Exécution
        result = await predictor.predict_qualite(parcelle_id, date_recolte)
        
        # Vérifications
        assert isinstance(result, dict)
        assert "qualite_prevue" in result
        assert isinstance(result["qualite_prevue"], QualiteRecolte)
        
        assert "probabilites" in result
        assert isinstance(result["probabilites"], dict)
        assert all(q in result["probabilites"] for q in QualiteRecolte)
        assert sum(result["probabilites"].values()) == pytest.approx(1.0)
        
        assert "facteurs_impact" in result
        assert isinstance(result["facteurs_impact"], list)
        assert len(result["facteurs_impact"]) > 0

    def test_calculate_quality_features(
        self,
        predictor,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test du calcul des features."""
        # Exécution
        features = predictor._calculate_quality_features(
            sample_historique,
            sample_meteo,
            sample_iot_data
        )
        
        # Vérifications
        assert isinstance(features, np.ndarray)
        assert len(features) == 9  # 3 features par source de données
        assert all(isinstance(f, (int, float)) for f in features)
        
        # Test des proportions de qualité
        quality_proportions = features[:3]
        assert sum(quality_proportions) == pytest.approx(1.0)
        
        # Test des features météo
        meteo_features = features[3:6]
        assert all(f >= 0 for f in meteo_features)
        
        # Test des features IoT
        iot_features = features[6:]
        assert all(f >= 0 for f in iot_features)

    def test_calculate_quality_features_without_data(self, predictor):
        """Test du calcul des features sans données."""
        # Exécution
        features = predictor._calculate_quality_features([], [], [])
        
        # Vérifications
        assert isinstance(features, np.ndarray)
        assert len(features) == 9
        assert all(f == 0 for f in features)

    async def test_predict_quality(self, predictor):
        """Test de la prédiction avec le modèle."""
        # Configuration
        features = np.array([0.5, 0.3, 0.2, 25.0, 65.0, 10.0, 22.0, 2.0, 10.0])
        
        # Exécution
        result = await predictor._predict_quality(features)
        
        # Vérifications
        assert isinstance(result, dict)
        assert "classe" in result
        assert isinstance(result["classe"], QualiteRecolte)
        
        assert "probabilites" in result
        assert isinstance(result["probabilites"], dict)
        assert all(q in result["probabilites"] for q in QualiteRecolte)
        assert sum(result["probabilites"].values()) == pytest.approx(1.0)

    async def test_analyze_quality_factors(self, predictor):
        """Test de l'analyse des facteurs de qualité."""
        # Configuration
        features = np.array([0.5, 0.3, 0.2, 25.0, 65.0, 10.0, 22.0, 2.0, 10.0])
        
        # Exécution
        factors = await predictor._analyze_quality_factors(features)
        
        # Vérifications
        assert isinstance(factors, list)
        assert len(factors) > 0
        
        for factor in factors:
            assert "facteur" in factor
            assert "impact" in factor
            assert "optimal" in factor
            assert "actuel" in factor
            assert isinstance(factor["impact"], float)
            assert 0 <= factor["impact"] <= 1

    async def test_error_handling(self, predictor):
        """Test de la gestion des erreurs."""
        # Test avec une parcelle invalide
        with pytest.raises(ValueError):
            await predictor.predict_qualite("", date.today())
        
        # Test avec une date dans le passé
        with pytest.raises(ValueError):
            await predictor.predict_qualite(
                "P1",
                date.today() - timedelta(days=1)
            )
        
        # Test avec une date trop éloignée
        with pytest.raises(ValueError):
            await predictor.predict_qualite(
                "P1",
                date.today() + timedelta(days=366)
            )

    def test_quality_distribution(
        self,
        predictor,
        sample_historique,
        sample_meteo,
        sample_iot_data
    ):
        """Test de la distribution des qualités."""
        # Test avec historique parfait
        perfect_historique = [{
            "date": date.today() - timedelta(days=i*30),
            "qualite": QualiteRecolte.A,
            "conditions_meteo": {
                "temperature": 25.0,
                "humidite": 65.0,
                "precipitation": 10.0
            }
        } for i in range(10)]
        
        features = predictor._calculate_quality_features(
            perfect_historique,
            sample_meteo,
            sample_iot_data
        )
        
        assert features[0] == 1.0  # Proportion de qualité A
        assert features[1] == 0.0  # Proportion de qualité B
        assert features[2] == 0.0  # Proportion de qualité C
        
        # Test avec historique mixte
        mixed_historique = [{
            "date": date.today() - timedelta(days=i*30),
            "qualite": QualiteRecolte.A if i % 2 == 0 else QualiteRecolte.B,
            "conditions_meteo": {
                "temperature": 25.0,
                "humidite": 65.0,
                "precipitation": 10.0
            }
        } for i in range(10)]
        
        features = predictor._calculate_quality_features(
            mixed_historique,
            sample_meteo,
            sample_iot_data
        )
        
        assert features[0] == 0.5  # Proportion de qualité A
        assert features[1] == 0.5  # Proportion de qualité B
        assert features[2] == 0.0  # Proportion de qualité C
