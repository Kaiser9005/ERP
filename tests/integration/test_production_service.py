"""Tests pour le service de production"""

import pytest
from datetime import datetime, timedelta, date
from decimal import Decimal
from sqlalchemy.orm import Session
from unittest.mock import patch, AsyncMock
from services.production_service import ProductionService
from models.production import (
    Parcelle,
    CycleCulture,
    Recolte,
    CultureType,
    ParcelleStatus,
    QualiteRecolte
)

@pytest.fixture
def mock_weather_service():
    mock = AsyncMock()
    mock.get_current_conditions.return_value = {
        "temperature": 25.5,
        "humidity": 65,
        "precipitation": 0
    }
    return mock

@pytest.fixture
def mock_iot_service():
    return AsyncMock()

@pytest.fixture
def mock_production_ml_service():
    mock = AsyncMock()
    mock.predict_rendement.return_value = {
        "rendement_prevu": 1200,
        "facteurs_impact": ["temperature", "humidite"]
    }
    mock.analyze_meteo_impact.return_value = {
        "impact_score": 0.8,
        "recommandations": ["Augmenter l'irrigation"]
    }
    mock.optimize_cycle_culture.return_value = {
        "date_debut_optimale": date.today(),
        "rendement_prevu": {"rendement_prevu": 1500}
    }
    mock.predict_qualite.return_value = {
        "qualite_prevue": QualiteRecolte.A
    }
    return mock

@pytest.fixture
def parcelle_test(db: Session, test_user):
    parcelle = Parcelle(
        code="P001",
        culture_type=CultureType.PALMIER,
        surface_hectares=Decimal("10.5"),
        date_plantation=date.today() - timedelta(days=365),
        statut=ParcelleStatus.ACTIVE,
        coordonnees_gps={"latitude": 0, "longitude": 0},
        responsable_id=test_user.id
    )
    db.add(parcelle)
    db.commit()
    db.refresh(parcelle)
    return parcelle

@pytest.fixture
def cycle_culture_test(db: Session, parcelle_test):
    cycle = CycleCulture(
        parcelle_id=parcelle_test.id,
        date_debut=date.today() - timedelta(days=30),
        rendement_prevu=Decimal("1200")
    )
    db.add(cycle)
    db.commit()
    db.refresh(cycle)
    return cycle

@pytest.fixture
def production_service(db, mock_weather_service, mock_iot_service, mock_production_ml_service):
    with patch("services.production_service.WeatherService", return_value=mock_weather_service), \
         patch("services.production_service.IoTService", return_value=mock_iot_service), \
         patch("services.production_service.ProductionMLService", return_value=mock_production_ml_service):
        return ProductionService(db)

@pytest.mark.asyncio
async def test_get_parcelle_details(production_service, parcelle_test, cycle_culture_test):
    """Test de récupération des détails d'une parcelle"""
    # Test sans prédictions
    details = await production_service.get_parcelle_details(str(parcelle_test.id))
    assert details["id"] == parcelle_test.id
    assert details["code"] == "P001"
    assert details["culture_type"] == CultureType.PALMIER
    assert float(details["surface_hectares"]) == 10.5
    assert "predictions" not in details

    # Test avec prédictions
    details = await production_service.get_parcelle_details(str(parcelle_test.id), include_predictions=True)
    assert "predictions" in details
    assert "meteo_impact" in details

@pytest.mark.asyncio
async def test_create_cycle_culture(production_service, parcelle_test):
    """Test de création d'un cycle de culture"""
    # Test avec optimisation
    cycle = await production_service.create_cycle_culture(str(parcelle_test.id), optimize=True)
    assert cycle["rendement_prevu"] == 1500
    assert "optimisation" in cycle

    # Test sans optimisation
    cycle = await production_service.create_cycle_culture(str(parcelle_test.id), optimize=False)
    assert cycle["rendement_prevu"] == 0
    assert cycle["optimisation"] is None

@pytest.mark.asyncio
async def test_create_recolte(production_service, parcelle_test):
    """Test de création d'une récolte"""
    # Test avec prédiction de qualité
    recolte = await production_service.create_recolte(
        str(parcelle_test.id),
        date.today(),
        1000,
        predict_quality=True
    )
    assert float(recolte["quantite_kg"]) == 1000
    assert recolte["qualite"] == QualiteRecolte.A
    assert "prediction_qualite" in recolte

    # Test sans prédiction de qualité
    recolte = await production_service.create_recolte(
        str(parcelle_test.id),
        date.today(),
        1000,
        predict_quality=False
    )
    assert recolte["qualite"] == QualiteRecolte.B
    assert recolte["prediction_qualite"] is None

@pytest.mark.asyncio
async def test_get_production_stats(production_service, parcelle_test):
    """Test de récupération des statistiques de production"""
    # Créer des récoltes
    for i in range(3):
        recolte = Recolte(
            parcelle_id=parcelle_test.id,
            date_recolte=datetime.now() - timedelta(days=i),
            quantite_kg=Decimal(str(500 + i * 100)),
            qualite=QualiteRecolte.A,
            equipe_recolte=[str(parcelle_test.responsable_id)]
        )
        production_service.db.add(recolte)
    production_service.db.commit()

    # Test sans prédictions
    stats = await production_service.get_production_stats(
        str(parcelle_test.id),
        date.today() - timedelta(days=30),
        date.today()
    )
    assert stats["recoltes"]["nombre"] == 3
    assert stats["recoltes"]["quantite_totale"] == 1800  # 500 + 600 + 700
    assert stats["recoltes"]["qualite"]["A"] == 3
    assert "predictions" not in stats

    # Test avec prédictions
    stats = await production_service.get_production_stats(
        str(parcelle_test.id),
        date.today() - timedelta(days=30),
        date.today(),
        include_predictions=True
    )
    assert "predictions" in stats
    assert "meteo_impact" in stats

@pytest.mark.asyncio
async def test_get_production_recommendations(production_service, parcelle_test, cycle_culture_test):
    """Test de récupération des recommandations de production"""
    # Test avec cycle actif
    recommendations = await production_service.get_production_recommendations(str(parcelle_test.id))
    assert len(recommendations) > 0
    assert any(r["type"] == "ACTION" for r in recommendations)
    assert any("message" in r for r in recommendations)

    # Test sans cycle actif
    cycle_culture_test.date_fin = date.today()
    production_service.db.commit()

    recommendations = await production_service.get_production_recommendations(str(parcelle_test.id))
    assert len(recommendations) == 0

@pytest.mark.asyncio
async def test_error_handling(production_service, parcelle_test):
    """Test de la gestion des erreurs"""
    # Test parcelle inexistante
    with pytest.raises(ValueError, match="Parcelle non trouvée"):
        await production_service.get_parcelle_details("00000000-0000-0000-0000-000000000000")

    # Test création de cycle sur parcelle inexistante
    with pytest.raises(ValueError, match="Parcelle non trouvée"):
        await production_service.create_cycle_culture("00000000-0000-0000-0000-000000000000")

    # Test création de récolte sur parcelle inexistante
    with pytest.raises(ValueError, match="Parcelle non trouvée"):
        await production_service.create_recolte(
            "00000000-0000-0000-0000-000000000000",
            date.today(),
            1000
        )