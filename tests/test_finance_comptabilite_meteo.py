"""
Tests pour le module d'impact météorologique finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.finance_comptabilite.meteo import GestionMeteo
from models.comptabilite import (
    CompteComptable,
    TypeCompte
)
from models.production import Parcelle

@pytest.fixture
def meteo_service(db_session):
    """Fixture du service météo"""
    return GestionMeteo(db_session)

@pytest.fixture
def parcelle(db_session):
    """Fixture d'une parcelle test"""
    parcelle = Parcelle(
        code="P001",
        surface=10.5,
        culture_actuelle="BLE"
    )
    db_session.add(parcelle)
    db_session.commit()
    return parcelle

@pytest.fixture
def comptes(db_session):
    """Fixture des comptes test"""
    comptes = []
    
    # Comptes de provision
    numeros_provision = ["1511", "1512", "1513", "1514", "1515"]
    for numero in numeros_provision:
        compte = CompteComptable(
            numero=numero,
            libelle=f"Provision {numero}",
            type_compte=TypeCompte.PASSIF
        )
        comptes.append(compte)
        
    # Comptes de charge
    numeros_charge = ["6815", "6816", "6817", "6818", "6819"]
    for numero in numeros_charge:
        compte = CompteComptable(
            numero=numero,
            libelle=f"Dotation {numero}",
            type_compte=TypeCompte.CHARGE
        )
        comptes.append(compte)
        
    for compte in comptes:
        db_session.add(compte)
    db_session.commit()
    
    return comptes

async def test_get_meteo_impact_ml(meteo_service, parcelle, mocker):
    """Test de l'analyse ML de l'impact météo"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_period_stats',
        return_value={
            "precipitation": 250,
            "temperature_avg": 32,
            "humidity_avg": 85
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "erosion_history": {
                    "impact_factor": 1.2
                },
                "predictions": {
                    "erosion_risk": 1.3
                },
                "recommendations": [
                    {
                        "type": "WEATHER",
                        "priority": "HIGH",
                        "description": "Risque élevé",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "implementation_plan": [
                {
                    "category": "EROSION",
                    "actions": ["Optimiser protection"],
                    "savings": 500
                }
            ]
        }
    )
    
    # Test
    impact = await meteo_service._get_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "score" in impact
    assert "facteurs" in impact
    assert "couts_additionnels" in impact
    assert "risques" in impact
    assert "opportunites" in impact
    assert "provisions_suggeres" in impact
    assert "ml_analysis" in impact
    assert "optimization" in impact
    assert "recommendations" in impact
    
    # Vérification ML
    assert "erosion_history" in impact["ml_analysis"]
    assert "predictions" in impact["ml_analysis"]
    assert len(impact["recommendations"]) > 0

async def test_calculer_provision_meteo_ml(meteo_service, comptes, mocker):
    """Test du calcul ML des provisions météo"""
    # Mock du service ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "optimized_costs": {
                "EROSION": 4500,
                "IRRIGATION": 3000
            }
        }
    )
    
    # Données test
    impact_meteo = {
        "score": 75,
        "provisions_suggeres": {
            "EROSION": 5000,
            "IRRIGATION": 3500
        }
    }
    
    # Test
    provisions = await meteo_service._calculer_provision_meteo(impact_meteo)
    
    # Vérification
    assert "EROSION" in provisions
    assert "IRRIGATION" in provisions
    
    # Vérification optimisation ML
    assert provisions["EROSION"]["montant"] == 4500
    assert provisions["EROSION"]["montant_base"] == 5000
    assert provisions["EROSION"]["ml_adjustment"] == -500

async def test_calculer_provisions_specifiques_ml(meteo_service, mocker):
    """Test des calculs ML spécifiques de provisions"""
    # Mock analyse ML
    analyse_ml = {
        "ml_analysis": {
            "erosion_history": {"impact_factor": 1.2},
            "irrigation_predictions": {"cost_factor": 1.3},
            "maintenance_analysis": {"cost_multiplier": 1.1},
            "protection_forecast": {"severity_factor": 1.4},
            "treatment_analysis": {"risk_factor": 1.2}
        }
    }
    
    # Test érosion
    provision = await meteo_service._calculer_provision_erosion_ml(250, analyse_ml)
    assert provision > meteo_service._calculer_provision_erosion(250)
    
    # Test irrigation
    provision = await meteo_service._calculer_provision_irrigation_ml(30, analyse_ml)
    assert provision > meteo_service._calculer_provision_irrigation(30)
    
    # Test maintenance
    provision = await meteo_service._calculer_provision_maintenance_ml(35, analyse_ml)
    assert provision > meteo_service._calculer_provision_maintenance(35)
    
    # Test protection
    provision = await meteo_service._calculer_provision_protection_ml(10, analyse_ml)
    assert provision > meteo_service._calculer_provision_protection(10)
    
    # Test traitements
    provision = await meteo_service._calculer_provision_traitements_ml(85, analyse_ml)
    assert provision > meteo_service._calculer_provision_traitements(85)

async def test_generate_meteo_recommendations(meteo_service):
    """Test de la génération des recommandations ML"""
    # Données test
    impact = {
        "score": 75,
        "couts_additionnels": {
            "EROSION": "Augmentation nécessaire"
        }
    }
    
    analyse_ml = {
        "ml_analysis": {
            "recommendations": [
                {
                    "type": "WEATHER",
                    "priority": "HIGH",
                    "description": "Risque élevé",
                    "actions": ["Action 1"]
                }
            ]
        }
    }
    
    optimization = {
        "implementation_plan": [
            {
                "category": "EROSION",
                "actions": ["Optimiser protection"],
                "savings": 500
            }
        ]
    }
    
    # Test
    recommendations = await meteo_service._generate_meteo_recommendations(
        impact,
        analyse_ml,
        optimization
    )
    
    # Vérification
    assert len(recommendations) > 0
    
    # Vérification types
    ml_recs = [r for r in recommendations if r["type"] == "ML"]
    assert len(ml_recs) > 0
    
    opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
    assert len(opt_recs) > 0
    
    alert_recs = [r for r in recommendations if r["type"] == "ALERT"]
    assert len(alert_recs) > 0

async def test_get_comptes_meteo(meteo_service, comptes):
    """Test de la récupération des comptes météo"""
    # Test compte provision
    compte_id = await meteo_service._get_compte_provision_meteo("EROSION")
    assert compte_id is not None
    
    # Test compte charge
    compte_id = await meteo_service._get_compte_charge_meteo("EROSION")
    assert compte_id is not None
    
    # Test compte inconnu
    compte_id = await meteo_service._get_compte_provision_meteo("UNKNOWN")
    assert compte_id is not None  # Compte par défaut
    
    compte_id = await meteo_service._get_compte_charge_meteo("UNKNOWN")
    assert compte_id is not None  # Compte par défaut

async def test_cache_meteo_impact(meteo_service, parcelle, mocker):
    """Test du cache pour l'impact météo"""
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(meteo_service, 'cache', mock_cache)
    
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_period_stats',
        return_value={
            "precipitation": 250,
            "temperature_avg": 32
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "predictions": {}
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "implementation_plan": []
        }
    )
    
    # Premier appel
    await meteo_service._get_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification cache
    assert mock_cache.set.called
    
    # Deuxième appel
    mock_cache.get.return_value = {"cached": True}
    result = await meteo_service._get_meteo_impact(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification résultat du cache
    assert result == {"cached": True}
