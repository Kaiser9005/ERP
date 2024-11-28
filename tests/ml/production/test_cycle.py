"""
Tests pour le module d'optimisation des cycles de culture.
"""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
from sqlalchemy.orm import Session

from models.production import Parcelle, CultureType
from services.weather_service import WeatherService
from services.ml.production.cycle import CycleOptimizer

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def weather_service():
    """Fixture pour le service météo."""
    return AsyncMock(spec=WeatherService)

@pytest.fixture
def optimizer(db_session, weather_service):
    """Fixture pour l'optimiseur."""
    service = CycleOptimizer(db_session)
    service.weather_service = weather_service
    return service

@pytest.fixture
def sample_parcelle():
    """Fixture pour une parcelle exemple."""
    return Mock(
        spec=Parcelle,
        id="P1",
        culture_type=CultureType.CEREALE,
        surface=1000.0,
        conditions_sol={
            "type": "LIMONEUX",
            "ph": 6.5,
            "matiere_organique": 3.0
        }
    )

@pytest.fixture
def sample_historique():
    """Fixture pour l'historique des cycles."""
    return [{
        "date_debut": date.today() - timedelta(days=i*45),
        "date_fin": date.today() - timedelta(days=i*45-44),
        "rendement_prevu": 1000.0 + i*100,
        "rendement_reel": 950.0 + i*90
    } for i in range(5)]

@pytest.fixture
def sample_meteo():
    """Fixture pour les prévisions météo."""
    return [{
        "date": date.today() + timedelta(days=i),
        "temperature": 25.0,
        "humidite": 65.0,
        "precipitation": 10.0,
        "vent": 15.0
    } for i in range(45)]  # 45 jours de prévisions

class TestCycleOptimizer:
    """Tests pour CycleOptimizer."""

    async def test_optimize_cycle_culture_with_date(
        self,
        optimizer,
        sample_parcelle,
        sample_historique,
        sample_meteo
    ):
        """Test de l'optimisation avec date spécifiée."""
        # Configuration
        parcelle_id = "P1"
        date_debut = date.today() + timedelta(days=7)
        
        optimizer.db.query().get.return_value = sample_parcelle
        optimizer._get_historique_cycles = AsyncMock(return_value=sample_historique)
        optimizer.weather_service.get_forecast.return_value = sample_meteo
        optimizer.predict_rendement = AsyncMock(return_value=1200.0)
        
        # Exécution
        result = await optimizer.optimize_cycle_culture(parcelle_id, date_debut)
        
        # Vérifications
        assert isinstance(result, dict)
        assert "date_debut_optimale" in result
        assert result["date_debut_optimale"] == date_debut
        
        assert "date_fin_prevue" in result
        assert isinstance(result["date_fin_prevue"], date)
        assert result["date_fin_prevue"] > date_debut
        
        assert "etapes" in result
        assert isinstance(result["etapes"], list)
        assert len(result["etapes"]) > 0
        
        for etape in result["etapes"]:
            assert "etape" in etape
            assert "date_debut" in etape
            assert "date_fin" in etape
            assert "conditions_optimales" in etape
            assert isinstance(etape["conditions_optimales"], dict)

    async def test_optimize_cycle_culture_without_date(
        self,
        optimizer,
        sample_parcelle,
        sample_historique,
        sample_meteo
    ):
        """Test de l'optimisation sans date spécifiée."""
        # Configuration
        parcelle_id = "P1"
        
        optimizer.db.query().get.return_value = sample_parcelle
        optimizer._get_historique_cycles = AsyncMock(return_value=sample_historique)
        optimizer.weather_service.get_forecast.return_value = sample_meteo
        optimizer.predict_rendement = AsyncMock(return_value=1200.0)
        
        # Exécution
        result = await optimizer.optimize_cycle_culture(parcelle_id)
        
        # Vérifications
        assert isinstance(result, dict)
        assert "date_debut_optimale" in result
        assert isinstance(result["date_debut_optimale"], date)
        assert result["date_debut_optimale"] >= date.today()

    async def test_calculate_optimal_start_date(
        self,
        optimizer,
        sample_meteo
    ):
        """Test du calcul de la date optimale de début."""
        # Configuration
        culture_type = CultureType.CEREALE
        
        # Exécution
        result = await optimizer._calculate_optimal_start_date(
            culture_type,
            sample_meteo
        )
        
        # Vérifications
        assert isinstance(result, date)
        assert result >= date.today()
        # La date optimale ne devrait pas être trop éloignée
        assert result <= date.today() + timedelta(days=30)

    async def test_optimize_cycle_steps(
        self,
        optimizer,
        sample_meteo
    ):
        """Test de l'optimisation des étapes du cycle."""
        # Configuration
        culture_type = CultureType.CEREALE
        date_debut = date.today()
        
        # Exécution
        result = await optimizer._optimize_cycle_steps(
            culture_type,
            date_debut,
            sample_meteo
        )
        
        # Vérifications
        assert isinstance(result, list)
        assert len(result) == 3  # Préparation, Croissance, Récolte
        
        for etape in result:
            assert "etape" in etape
            assert "date_debut" in etape
            assert "date_fin" in etape
            assert "conditions_optimales" in etape
            
            assert etape["date_debut"] >= date_debut
            if etape["etape"] != "Préparation":
                assert etape["date_debut"] > result[0]["date_fin"]
            
            assert isinstance(etape["conditions_optimales"], dict)
            assert "temperature" in etape["conditions_optimales"]
            assert "humidite" in etape["conditions_optimales"]

    async def test_error_handling(self, optimizer):
        """Test de la gestion des erreurs."""
        # Test avec une parcelle invalide
        with pytest.raises(ValueError):
            await optimizer.optimize_cycle_culture("")
        
        # Test avec une date de début dans le passé
        with pytest.raises(ValueError):
            await optimizer.optimize_cycle_culture(
                "P1",
                date.today() - timedelta(days=1)
            )
        
        # Test avec une parcelle inexistante
        optimizer.db.query().get.return_value = None
        with pytest.raises(ValueError):
            await optimizer.optimize_cycle_culture("P1")

    async def test_cycle_duration_constraints(
        self,
        optimizer,
        sample_parcelle,
        sample_meteo
    ):
        """Test des contraintes de durée du cycle."""
        # Configuration
        parcelle_id = "P1"
        optimizer.db.query().get.return_value = sample_parcelle
        optimizer._get_historique_cycles = AsyncMock(return_value=[])
        optimizer.weather_service.get_forecast.return_value = sample_meteo
        optimizer.predict_rendement = AsyncMock(return_value=1200.0)
        
        # Exécution
        result = await optimizer.optimize_cycle_culture(parcelle_id)
        
        # Vérifications
        etapes = result["etapes"]
        duree_totale = (etapes[-1]["date_fin"] - etapes[0]["date_debut"]).days
        
        # La durée totale devrait être cohérente avec le type de culture
        if sample_parcelle.culture_type == CultureType.CEREALE:
            assert 30 <= duree_totale <= 60
        elif sample_parcelle.culture_type == CultureType.LEGUME:
            assert 20 <= duree_totale <= 45
