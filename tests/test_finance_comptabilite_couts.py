"""
Tests pour le module de gestion des coûts finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.finance_comptabilite.couts import GestionCouts
from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    TypeCompte
)
from models.finance import Transaction, CategorieTransaction
from models.production import Parcelle

@pytest.fixture
def couts_service(db_session):
    """Fixture du service de coûts"""
    return GestionCouts(db_session)

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
def ecritures(db_session, parcelle):
    """Fixture des écritures test"""
    ecritures = []
    
    # Écritures de charges
    categories = ["INTRANT", "MATERIEL", "MAIN_OEUVRE"]
    for i, cat in enumerate(categories):
        ecriture = EcritureComptable(
            parcelle_id=parcelle.id,
            categorie=cat,
            debit=Decimal(str((i + 1) * 1000)),
            date_ecriture=date.today()
        )
        ecritures.append(ecriture)
        db_session.add(ecriture)
        
    db_session.commit()
    return ecritures

@pytest.fixture
def comptes(db_session):
    """Fixture des comptes test"""
    comptes = []
    
    # Compte de charges
    compte_charge = CompteComptable(
        numero="601",
        libelle="Achats",
        type_compte=TypeCompte.CHARGE
    )
    comptes.append(compte_charge)
    
    # Compte de produits
    compte_produit = CompteComptable(
        numero="701",
        libelle="Ventes",
        type_compte=TypeCompte.PRODUIT
    )
    comptes.append(compte_produit)
    
    for compte in comptes:
        db_session.add(compte)
    db_session.commit()
    
    return comptes

async def test_get_couts_parcelle_ml(couts_service, parcelle, ecritures, mocker):
    """Test de l'analyse ML des coûts d'une parcelle"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "predictions": {
                    "costs": 5000,
                    "margin": 2000
                },
                "recommendations": [
                    {
                        "type": "COST",
                        "priority": "HIGH",
                        "description": "Optimisation possible",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "current_costs": {"INTRANT": 1000},
            "optimized_costs": {"INTRANT": 900},
            "potential_savings": 100,
            "implementation_plan": [
                {
                    "category": "INTRANT",
                    "actions": ["Optimiser achats"]
                }
            ]
        }
    )
    
    # Test
    couts = await couts_service._get_couts_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification structure
    assert "details" in couts
    assert "total" in couts
    assert "par_hectare" in couts
    assert "ml_analysis" in couts
    assert "optimization" in couts
    assert "recommendations" in couts
    
    # Vérification ML
    assert "predictions" in couts["ml_analysis"]
    assert "recommendations" in couts["ml_analysis"]
    assert len(couts["recommendations"]) > 0
    
    # Vérification optimisation
    assert "potential_savings" in couts["optimization"]
    assert "implementation_plan" in couts["optimization"]

async def test_get_analyse_couts_ml(couts_service, parcelle, ecritures, mocker):
    """Test de l'analyse ML des coûts globaux"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance',
        return_value={
            "predictions": [
                {
                    "month": "2024-02",
                    "costs": 5000,
                    "margin": 2000
                }
            ],
            "risk_factors": [
                {
                    "factor": "Coûts",
                    "severity": "MEDIUM"
                }
            ]
        }
    )
    
    # Test
    analyse = await couts_service.get_analyse_couts(
        parcelle_id=parcelle.id
    )
    
    # Vérification structure
    assert "periode" in analyse
    assert "total" in analyse
    assert "categories" in analyse
    assert "repartition" in analyse
    assert "evolution" in analyse
    assert "ml_analysis" in analyse
    assert "optimization" in analyse
    assert "recommendations" in analyse
    
    # Vérification ML
    assert len(analyse["recommendations"]) > 0
    for rec in analyse["recommendations"]:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_get_evolution_couts_ml(couts_service, parcelle, ecritures, mocker):
    """Test de l'évolution des coûts avec ML"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_monthly_stats',
        return_value={
            "impact": 0.2,
            "temperature_avg": 25,
            "precipitation": 50
        }
    )
    
    mocker.patch(
        'services.iot_service.IoTService.get_monthly_stats',
        return_value={
            "temperature": 24,
            "humidity": 65,
            "alerts": []
        }
    )
    
    # Test
    evolution = await couts_service._get_evolution_couts(
        date_debut=date.today() - timedelta(days=30),
        date_fin=date.today(),
        parcelle_id=parcelle.id
    )
    
    # Vérification
    assert len(evolution) > 0
    for entry in evolution:
        assert "periode" in entry
        assert "montant" in entry
        assert "weather_impact" in entry
        assert "iot_data" in entry

async def test_generate_cost_recommendations(couts_service):
    """Test de la génération des recommandations ML"""
    # Données test
    couts = {
        "INTRANT": {"montant": 3000, "count": 5},
        "MATERIEL": {"montant": 1000, "count": 2}
    }
    
    analyse_ml = {
        "recommendations": [
            {
                "type": "COST",
                "priority": "HIGH",
                "description": "Optimisation possible",
                "actions": ["Action 1"]
            }
        ]
    }
    
    optimization = {
        "implementation_plan": [
            {
                "category": "INTRANT",
                "actions": ["Optimiser achats"],
                "savings": 500
            }
        ]
    }
    
    # Test
    recommendations = await couts_service._generate_cost_recommendations(
        couts,
        analyse_ml,
        optimization
    )
    
    # Vérification
    assert len(recommendations) > 0
    
    # Vérification recommandations ML
    ml_recs = [r for r in recommendations if r["type"] == "ML"]
    assert len(ml_recs) > 0
    
    # Vérification recommandations optimisation
    opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
    assert len(opt_recs) > 0
    
    # Vérification recommandations analyse
    analysis_recs = [r for r in recommendations if r["type"] == "ANALYSIS"]
    assert len(analysis_recs) > 0

async def test_get_compte_charge(couts_service, comptes):
    """Test de la détermination du compte de charge"""
    # Transaction test
    transaction = Mock(
        categorie=CategorieTransaction.INTRANT
    )
    
    # Test
    compte_id = await couts_service._get_compte_charge(transaction)
    assert compte_id is not None
    
    # Vérification compte inconnu
    transaction.categorie = "UNKNOWN"
    compte_id = await couts_service._get_compte_charge(transaction)
    assert compte_id is not None  # Compte par défaut

async def test_get_compte_produit(couts_service, comptes):
    """Test de la détermination du compte de produit"""
    # Transaction test
    transaction = Mock(
        categorie=CategorieTransaction.VENTE_RECOLTE
    )
    
    # Test
    compte_id = await couts_service._get_compte_produit(transaction)
    assert compte_id is not None
    
    # Vérification compte inconnu
    transaction.categorie = "UNKNOWN"
    compte_id = await couts_service._get_compte_produit(transaction)
    assert compte_id is not None  # Compte par défaut

async def test_cache_couts_parcelle(couts_service, parcelle, mocker):
    """Test du cache pour l'analyse des coûts"""
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(couts_service, 'cache', mock_cache)
    
    # Mock des services ML
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
            "potential_savings": 100
        }
    )
    
    # Premier appel
    await couts_service._get_couts_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification cache
    assert mock_cache.set.called
    
    # Deuxième appel
    mock_cache.get.return_value = {"cached": True}
    result = await couts_service._get_couts_parcelle(
        parcelle_id=parcelle.id,
        date_debut=date.today(),
        date_fin=date.today()
    )
    
    # Vérification résultat du cache
    assert result == {"cached": True}
