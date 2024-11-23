import pytest
from datetime import datetime, timezone, timedelta
from unittest.mock import Mock, patch, AsyncMock
from services.production_report_service import ProductionReportService
from models.production import Parcelle, Recolte, QualiteRecolte, ProductionEvent
import json


@pytest.fixture
def mock_db():
    """Fixture pour simuler la base de données"""
    db = Mock()

    # Création de données de test
    recoltes = [
        Mock(
            id=1,
            parcelle_id=1,
            date_recolte=datetime.now(timezone.utc) - timedelta(days=1),
            quantite_kg=100,
            qualite=QualiteRecolte.A
        ),
        Mock(
            id=2,
            parcelle_id=1,
            date_recolte=datetime.now(timezone.utc) - timedelta(days=2),
            quantite_kg=150,
            qualite=QualiteRecolte.B
        ),
        Mock(
            id=3,
            parcelle_id=2,
            date_recolte=datetime.now(timezone.utc) - timedelta(days=1),
            quantite_kg=120,
            qualite=QualiteRecolte.C
        )
    ]

    parcelles = [
        Mock(id=1, code="P001", culture_type="PALMIER"),
        Mock(id=2, code="P002", culture_type="PAPAYE")
    ]

    # Configuration des mocks
    db.query.return_value.join.return_value.filter.return_value.all.return_value = [
        (recolte, parcelle.code, parcelle.culture_type)
        for recolte, parcelle in zip(recoltes, parcelles)
    ]
    db.query.return_value.get.return_value = parcelles[0]

    return db


@pytest.fixture
def mock_weather_metrics():
    """Fixture pour simuler les données météo"""
    return {
        "current_conditions": {
            "temperature": 32,
            "humidity": 75,
            "precipitation": 15,
            "wind_speed": 20,
            "conditions": "Pluie forte",
            "uv_index": 7,
            "cloud_cover": 90
        },
        "risks": {
            "precipitation": {
                "level": "HIGH",
                "message": "Risque d'inondation - Vérifier le drainage"
            },
            "temperature": {
                "level": "MEDIUM",
                "message": "Températures élevées - Surveillance recommandée"
            },
            "level": "HIGH"
        },
        "recommendations": [
            "Vérifier les systèmes de drainage",
            "Reporter les activités de plantation",
            "Protéger les jeunes plants"
        ]
    }


@pytest.fixture
def mock_redis():
    """Fixture pour simuler Redis"""
    redis_mock = Mock()
    redis_mock.get.return_value = None
    return redis_mock


@pytest.fixture
def mock_notification_service():
    """Fixture pour simuler le service de notifications"""
    return AsyncMock()


@pytest.mark.asyncio
async def test_generate_weekly_report(mock_db, mock_weather_metrics):
    """Test de génération du rapport hebdomadaire"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        service = ProductionReportService(mock_db)
        start_date = datetime.now(timezone.utc)

        report = await service.generate_weekly_report(start_date)

        # Vérification de la structure du rapport
        assert "periode" in report
        assert "meteo" in report
        assert "production" in report
        assert "recommandations" in report

        # Vérification des données de production
        assert report["production"]["total_global"] == 370  # 100 + 150 + 120
        assert len(report["production"]["recoltes"]) == 3

        # Vérification des impacts météo
        assert report["meteo"]["risques"]["level"] == "HIGH"
        assert "inondation" in report["meteo"]["risques"]["precipitation"]["message"]


@pytest.mark.asyncio
async def test_generate_weekly_report_with_cache(mock_db, mock_redis, mock_weather_metrics):
    """Test de génération du rapport avec cache"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        service = ProductionReportService(mock_db)
        service.redis_client = mock_redis

        # Premier appel - pas de cache
        start_date = datetime.now(timezone.utc)
        report1 = await service.generate_weekly_report(start_date)

        # Simuler données en cache
        cached_data = {
            "periode": {
                "debut": start_date.isoformat(),
                "fin": (start_date + timedelta(days=7)).isoformat()
            },
            "meteo": mock_weather_metrics,
            "production": {"total_global": 370}
        }
        mock_redis.get.return_value = json.dumps(cached_data)

        # Deuxième appel - depuis le cache
        report2 = await service.generate_weekly_report(start_date)

        assert report2["production"]["total_global"] == 370
        mock_redis.get.assert_called()
        mock_redis.setex.assert_called()


@pytest.mark.asyncio
async def test_generate_weekly_report_force_refresh(mock_db, mock_redis, mock_weather_metrics):
    """Test de génération du rapport avec force refresh"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        service = ProductionReportService(mock_db)
        service.redis_client = mock_redis

        start_date = datetime.now(timezone.utc)
        report = await service.generate_weekly_report(start_date, force_refresh=True)

        mock_redis.get.assert_not_called()
        mock_redis.setex.assert_called()


@pytest.mark.asyncio
async def test_notifications_for_high_risk(mock_db, mock_notification_service, mock_weather_metrics):
    """Test des notifications pour risque élevé"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        service = ProductionReportService(mock_db)
        service.notification_service = mock_notification_service

        await service.generate_weekly_report(datetime.now(timezone.utc))

        # Vérifier l'envoi de notification pour risque élevé
        service.notification_service.send_notification.assert_called_with(
            "production",
            "Impact Météo Critique",
            pytest.approx(type=str)
        )


@pytest.mark.asyncio
async def test_notifications_for_low_quality(mock_db, mock_notification_service, mock_weather_metrics):
    """Test des notifications pour qualité basse"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        service = ProductionReportService(mock_db)
        service.notification_service = mock_notification_service

        await service.generate_weekly_report(datetime.now(timezone.utc))

        # Vérifier l'envoi de notification pour qualité basse
        notifications = service.notification_service.send_notification.call_args_list
        quality_notification = next(
            (call for call in notifications if "Qualité" in call[0][1]),
            None
        )
        assert quality_notification is not None


@pytest.mark.asyncio
async def test_record_production_event(mock_db, mock_notification_service):
    """Test d'enregistrement d'événement de production"""
    service = ProductionReportService(mock_db)
    service.notification_service = mock_notification_service

    event_data = {
        "parcelle_id": "1",
        "event_type": "RECOLTE",
        "description": "Récolte palmiers",
        "metadata": {"quantite": 500}
    }

    await service.record_production_event(**event_data)

    # Vérifier l'ajout en base
    mock_db.add.assert_called_once()
    mock_db.commit.assert_called_once()

    # Vérifier la notification
    service.notification_service.send_notification.assert_called_with(
        "production",
        "Nouvel événement - P001",
        "Type: RECOLTE\nDescription: Récolte palmiers"
    )


def test_get_production_data(mock_db):
    """Test de récupération des données de production"""
    service = ProductionReportService(mock_db)
    start_date = datetime.now(timezone.utc) - timedelta(days=7)
    end_date = datetime.now(timezone.utc)

    data = service._get_production_data(start_date, end_date)

    # Vérification des totaux
    assert data["total_global"] == 370
    assert len(data["recoltes"]) == 3
    assert len(data["totaux_parcelles"]) == 2

    # Vérification des moyennes par parcelle
    parcelle_1 = data["totaux_parcelles"][1]
    assert parcelle_1["quantite"] == 250  # 100 + 150
    assert parcelle_1["qualite_moyenne"] == 8.5  # (10 + 7) / 2


def test_analyze_weather_impact(mock_db, mock_weather_metrics):
    """Test d'analyse de l'impact météo"""
    service = ProductionReportService(mock_db)
    recoltes = [
        {
            "id": 1,
            "parcelle_id": 1,
            "parcelle_code": "P001",
            "culture_type": "PALMIER",
            "quantite": 100,
            "qualite": "A"
        }
    ]

    impact = service._analyze_weather_impact(recoltes, mock_weather_metrics)

    # Vérification du niveau d'impact
    assert impact["niveau"] == "ÉLEVÉ"
    assert len(impact["facteurs"]) > 0

    # Vérification des facteurs d'impact
    precipitation_factor = next(
        (f for f in impact["facteurs"] if "Précipitations" in f["facteur"]),
        None
    )
    assert precipitation_factor is not None
    assert "drainage" in precipitation_factor["recommandation"].lower()


def test_generate_recommendations(mock_db, mock_weather_metrics):
    """Test de génération des recommandations"""
    service = ProductionReportService(mock_db)

    production_data = {
        "recoltes": [
            {
                "id": 1,
                "parcelle_id": 1,
                "parcelle_code": "P001",
                "culture_type": "PALMIER",
                "quantite": 100,
                "qualite": "C"
            }
        ],
        "totaux_parcelles": {
            1: {
                "code": "P001",
                "culture_type": "PALMIER",
                "quantite": 100,
                "qualite_moyenne": 4,
                "nombre_recoltes": 1
            }
        },
        "total_global": 100
    }

    weather_impact = {
        "niveau": "ÉLEVÉ",
        "facteurs": [
            {
                "facteur": "Précipitations excessives",
                "impact": "Risque d'inondation",
                "recommandation": "Renforcer le drainage"
            }
        ]
    }

    recommendations = service._generate_recommendations(
        mock_weather_metrics["recommendations"],
        production_data,
        weather_impact
    )

    # Vérification des recommandations
    assert len(recommendations) > 0

    # Vérification de la priorité
    high_priority = [r for r in recommendations if r["priorite"] == "HAUTE"]
    assert len(high_priority) > 0

    # Vérification des types de recommandations
    meteo_recs = [r for r in recommendations if r["type"] == "METEO"]
    production_recs = [r for r in recommendations if r["type"] == "PRODUCTION"]

    assert len(meteo_recs) > 0
    assert len(production_recs) > 0


@pytest.mark.asyncio
async def test_error_handling(mock_db, mock_notification_service):
    """Test de la gestion des erreurs"""
    service = ProductionReportService(mock_db)
    service.notification_service = mock_notification_service

    # Test avec une base de données défaillante
    mock_db.query.side_effect = Exception("Erreur DB")

    with pytest.raises(Exception):
        await service.generate_weekly_report(datetime.now(timezone.utc))
