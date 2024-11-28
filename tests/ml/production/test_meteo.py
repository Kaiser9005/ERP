"""
Tests pour le module d'analyse de l'impact météo.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
from sqlalchemy.orm import Session

from models.production import Recolte
from services.weather_service import WeatherService
from services.ml.production.meteo import MeteoAnalyzer

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def weather_service():
    """Fixture pour le service météo."""
    return AsyncMock(spec=WeatherService)

@pytest.fixture
def analyzer(db_session, weather_service):
    """Fixture pour l'analyseur."""
    service = MeteoAnalyzer(db_session)
    service.weather_service = weather_service
    return service

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
def sample_recoltes():
    """Fixture pour les récoltes."""
    return [Mock(
        spec=Recolte,
        id=f"R{i}",
        parcelle_id="P1",
        date_recolte=date.today() - timedelta(days=i*7),
        quantite_kg=1000.0 + i*100,
        qualite="A",
        conditions_meteo={
            "temperature": 25.0,
            "humidite": 65.0,
            "precipitation": 10.0
        }
    ) for i in range(5)]

class TestMeteoAnalyzer:
    """Tests pour MeteoAnalyzer."""

    async def test_analyze_meteo_impact(
        self,
        analyzer,
        sample_meteo,
        sample_recoltes
    ):
        """Test de l'analyse de l'impact météo."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today()
        date_fin = date.today() + timedelta(days=10)
        
        analyzer.weather_service.get_historical_data.return_value = sample_meteo
        analyzer.db.query().filter().all.return_value = sample_recoltes
        
        # Exécution
        result = await analyzer.analyze_meteo_impact(
            parcelle_id,
            date_debut,
            date_fin
        )
        
        # Vérifications
        assert isinstance(result, dict)
        assert "impact_score" in result
        assert isinstance(result["impact_score"], float)
        assert 0 <= result["impact_score"] <= 1
        
        assert "correlations" in result
        assert isinstance(result["correlations"], dict)
        assert all(0 <= v <= 1 for v in result["correlations"].values())
        
        assert "conditions_critiques" in result
        assert isinstance(result["conditions_critiques"], list)
        assert len(result["conditions_critiques"]) > 0
        
        assert "recommandations" in result
        assert isinstance(result["recommandations"], list)
        assert len(result["recommandations"]) > 0

    def test_analyze_meteo_correlations(
        self,
        analyzer,
        sample_meteo,
        sample_recoltes
    ):
        """Test de l'analyse des corrélations météo."""
        # Exécution
        correlations = analyzer._analyze_meteo_correlations(
            sample_meteo,
            sample_recoltes
        )
        
        # Vérifications
        assert isinstance(correlations, dict)
        assert "temperature" in correlations
        assert "humidite" in correlations
        assert "precipitation" in correlations
        
        assert all(0 <= v <= 1 for v in correlations.values())
        assert sum(correlations.values()) > 0

    def test_identify_critical_conditions(
        self,
        analyzer,
        sample_meteo,
        sample_recoltes
    ):
        """Test de l'identification des conditions critiques."""
        # Exécution
        conditions = analyzer._identify_critical_conditions(
            sample_meteo,
            sample_recoltes
        )
        
        # Vérifications
        assert isinstance(conditions, list)
        assert len(conditions) > 0
        
        for condition in conditions:
            assert "condition" in condition
            assert "seuil" in condition
            assert "impact" in condition
            assert "frequence" in condition
            assert -1 <= condition["impact"] <= 0
            assert 0 <= condition["frequence"] <= 1

    def test_calculate_impact_score(self, analyzer):
        """Test du calcul du score d'impact."""
        # Test avec corrélations normales
        correlations = {
            "temperature": 0.7,
            "humidite": 0.5,
            "precipitation": 0.3
        }
        score = analyzer._calculate_impact_score(correlations)
        assert isinstance(score, float)
        assert 0 <= score <= 1
        assert score == sum(correlations.values()) / len(correlations)
        
        # Test avec corrélations nulles
        correlations = {
            "temperature": 0.0,
            "humidite": 0.0,
            "precipitation": 0.0
        }
        score = analyzer._calculate_impact_score(correlations)
        assert score == 0.0
        
        # Test avec corrélations maximales
        correlations = {
            "temperature": 1.0,
            "humidite": 1.0,
            "precipitation": 1.0
        }
        score = analyzer._calculate_impact_score(correlations)
        assert score == 1.0

    async def test_generate_meteo_recommendations(
        self,
        analyzer,
        sample_meteo
    ):
        """Test de la génération des recommandations."""
        # Configuration
        parcelle_id = "P1"
        conditions_critiques = [
            {
                "condition": "Température élevée",
                "seuil": 30,
                "impact": -0.2,
                "frequence": 0.1
            },
            {
                "condition": "Précipitations faibles",
                "seuil": 10,
                "impact": -0.15,
                "frequence": 0.2
            }
        ]
        
        # Exécution
        recommendations = await analyzer._generate_meteo_recommendations(
            parcelle_id,
            conditions_critiques
        )
        
        # Vérifications
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(r, str) for r in recommendations)
        assert any("température" in r.lower() for r in recommendations)
        assert any("précipitation" in r.lower() for r in recommendations)

    async def test_error_handling(self, analyzer):
        """Test de la gestion des erreurs."""
        # Test avec une parcelle invalide
        with pytest.raises(ValueError):
            await analyzer.analyze_meteo_impact(
                "",
                date.today(),
                date.today() + timedelta(days=10)
            )
        
        # Test avec des dates invalides
        with pytest.raises(ValueError):
            await analyzer.analyze_meteo_impact(
                "P1",
                date.today() + timedelta(days=10),
                date.today()
            )
        
        # Test avec une période trop longue
        with pytest.raises(ValueError):
            await analyzer.analyze_meteo_impact(
                "P1",
                date.today(),
                date.today() + timedelta(days=366)
            )

    def test_correlation_edge_cases(
        self,
        analyzer,
        sample_recoltes
    ):
        """Test des cas limites pour les corrélations."""
        # Test avec données météo extrêmes
        meteo_extreme = [{
            "date": date.today(),
            "temperature": 40.0,  # Très chaud
            "humidite": 10.0,    # Très sec
            "precipitation": 0.0  # Pas de pluie
        }]
        
        correlations = analyzer._analyze_meteo_correlations(
            meteo_extreme,
            sample_recoltes
        )
        
        assert correlations["temperature"] > 0.7  # Forte corrélation négative
        assert correlations["humidite"] > 0.5    # Corrélation moyenne
        assert correlations["precipitation"] > 0.3  # Faible corrélation
        
        # Test avec données météo normales
        meteo_normal = [{
            "date": date.today(),
            "temperature": 25.0,
            "humidite": 65.0,
            "precipitation": 10.0
        }]
        
        correlations = analyzer._analyze_meteo_correlations(
            meteo_normal,
            sample_recoltes
        )
        
        assert all(0.3 <= v <= 0.7 for v in correlations.values())
