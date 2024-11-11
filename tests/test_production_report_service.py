import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from services.production_report_service import ProductionReportService
from models.production import Parcelle, Recolte

@pytest.fixture
def mock_db():
    """Fixture pour simuler la base de données"""
    db = Mock()
    
    # Création de données de test
    recoltes = [
        Mock(
            id=1,
            parcelle_id=1,
            date=datetime.now() - timedelta(days=1),
            quantite=100,
            qualite=8
        ),
        Mock(
            id=2,
            parcelle_id=1,
            date=datetime.now() - timedelta(days=2),
            quantite=150,
            qualite=7
        ),
        Mock(
            id=3,
            parcelle_id=2,
            date=datetime.now() - timedelta(days=1),
            quantite=120,
            qualite=6
        )
    ]
    
    # Configuration du mock pour la requête des récoltes
    db.query.return_value.filter.return_value.all.return_value = recoltes
    
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

@pytest.mark.asyncio
async def test_generate_weekly_report(mock_db, mock_weather_metrics):
    """Test de génération du rapport hebdomadaire"""
    with patch('services.weather_service.WeatherService.get_agricultural_metrics',
              return_value=mock_weather_metrics):
        
        service = ProductionReportService(mock_db)
        start_date = datetime.now()
        
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

def test_get_production_data(mock_db):
    """Test de récupération des données de production"""
    service = ProductionReportService(mock_db)
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
    
    data = service._get_production_data(start_date, end_date)
    
    # Vérification des totaux
    assert data["total_global"] == 370
    assert len(data["recoltes"]) == 3
    assert len(data["totaux_parcelles"]) == 2
    
    # Vérification des moyennes par parcelle
    parcelle_1 = data["totaux_parcelles"][1]
    assert parcelle_1["quantite"] == 250  # 100 + 150
    assert parcelle_1["qualite_moyenne"] == 7.5  # (8 + 7) / 2

def test_analyze_weather_impact(mock_db, mock_weather_metrics):
    """Test d'analyse de l'impact météo"""
    service = ProductionReportService(mock_db)
    recoltes = [
        {"id": 1, "parcelle_id": 1, "quantite": 100, "qualite": 8},
        {"id": 2, "parcelle_id": 1, "quantite": 150, "qualite": 7}
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
            {"id": 1, "parcelle_id": 1, "quantite": 100, "qualite": 6}
        ],
        "totaux_parcelles": {
            1: {"quantite": 100, "qualite_moyenne": 6, "nombre_recoltes": 1}
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
    assert len(production_recs) > 0  # Pour la faible qualité (6/10)

@pytest.mark.asyncio
async def test_error_handling(mock_db):
    """Test de la gestion des erreurs"""
    service = ProductionReportService(mock_db)
    
    # Test avec une base de données défaillante
    mock_db.query.side_effect = Exception("Erreur DB")
    
    with pytest.raises(Exception):
        await service.generate_weekly_report(datetime.now())
