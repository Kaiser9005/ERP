"""
Tests pour le module de clôture finance-comptabilité
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch
import os
import json

from services.finance_comptabilite.cloture import GestionCloture, ValidationResult
from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    TypeCompte,
    StatutEcriture
)

@pytest.fixture
def cloture_service(db_session):
    """Fixture du service de clôture"""
    return GestionCloture(db_session)

@pytest.fixture
def periode():
    """Fixture de la période test"""
    return datetime.now().strftime("%Y-%m")

@pytest.fixture
def comptes(db_session):
    """Fixture des comptes test"""
    comptes = []
    
    # Compte de charges
    compte_charge = CompteComptable(
        numero="6",
        libelle="Charges",
        type_compte=TypeCompte.CHARGE
    )
    comptes.append(compte_charge)
    
    # Compte de produits
    compte_produit = CompteComptable(
        numero="7",
        libelle="Produits",
        type_compte=TypeCompte.PRODUIT
    )
    comptes.append(compte_produit)
    
    # Compte de provisions
    compte_provision = CompteComptable(
        numero="15",
        libelle="Provisions",
        type_compte=TypeCompte.PASSIF
    )
    comptes.append(compte_provision)
    
    for compte in comptes:
        db_session.add(compte)
    db_session.commit()
    
    return comptes

@pytest.fixture
def ecritures(db_session, periode, comptes):
    """Fixture des écritures test"""
    ecritures = []
    
    # Écritures de charges
    ecriture_charge = EcritureComptable(
        compte_id=comptes[0].id,
        periode=periode,
        date=datetime.now(),
        libelle="Charge test",
        montant=Decimal("1000"),
        sens="DEBIT",
        statut=StatutEcriture.BROUILLON
    )
    ecritures.append(ecriture_charge)
    
    # Écritures de produits
    ecriture_produit = EcritureComptable(
        compte_id=comptes[1].id,
        periode=periode,
        date=datetime.now(),
        libelle="Produit test",
        montant=Decimal("1500"),
        sens="CREDIT",
        statut=StatutEcriture.BROUILLON
    )
    ecritures.append(ecriture_produit)
    
    for ecriture in ecritures:
        db_session.add(ecriture)
    db_session.commit()
    
    return ecritures

async def test_executer_cloture_mensuelle_ml(cloture_service, periode, ecritures, mocker):
    """Test de l'exécution de la clôture mensuelle avec ML"""
    # Mock des services ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "charge_adjustments": {
                    "CHARGE": {"factor": 1.1}
                },
                "stock_predictions": {
                    "STOCK": {"variation": 500}
                },
                "provision_recommendations": [
                    {
                        "category": "RISQUE",
                        "amount": 1000,
                        "description": "Provision test",
                        "confidence": 0.85
                    }
                ],
                "amortization_predictions": [
                    {
                        "category": "MATERIEL",
                        "amount": 800,
                        "description": "Amortissement test",
                        "confidence": 0.9
                    }
                ],
                "recommendations": [
                    {
                        "type": "CLOSING",
                        "priority": "HIGH",
                        "description": "Action requise",
                        "actions": ["Action 1"]
                    }
                ]
            }
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "provision_optimizations": {
                "RISQUE": {
                    "optimized_amount": 900
                }
            },
            "closing_optimizations": [
                {
                    "description": "Optimisation test",
                    "actions": ["Action 1"],
                    "savings": 100
                }
            ]
        }
    )
    
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(cloture_service, 'cache', mock_cache)
    
    # Test
    resultat = await cloture_service.executer_cloture_mensuelle(
        periode=periode,
        utilisateur_id="USER001"
    )
    
    # Vérification structure
    assert "periode" in resultat
    assert "statut" in resultat
    assert "date_cloture" in resultat
    assert "totaux" in resultat
    assert "etats" in resultat
    assert "ml_analysis" in resultat
    assert "optimization" in resultat
    assert "recommendations" in resultat
    
    # Vérification ML
    assert "charge_adjustments" in resultat["ml_analysis"]
    assert "stock_predictions" in resultat["ml_analysis"]
    assert "provision_recommendations" in resultat["ml_analysis"]
    assert len(resultat["recommendations"]) > 0
    
    # Vérification cache
    assert mock_cache.set.called

async def test_verifier_conditions_cloture_ml(cloture_service, periode, mocker):
    """Test de la vérification des conditions de clôture avec ML"""
    # Mock des vérifications
    mocker.patch.object(
        cloture_service,
        '_verifier_equilibre_comptes',
        return_value={"equilibre": True, "difference": 0}
    )
    
    mocker.patch.object(
        cloture_service,
        '_compter_ecritures_attente',
        return_value=0
    )
    
    mocker.patch.object(
        cloture_service,
        '_verifier_rapprochements',
        return_value={"complet": True, "manquants": 0}
    )
    
    mocker.patch.object(
        cloture_service,
        '_verifier_provisions_obligatoires_ml',
        return_value={"complet": True, "manquantes": []}
    )
    
    # Test
    validation = await cloture_service._verifier_conditions_cloture(periode)
    
    # Vérification
    assert isinstance(validation, ValidationResult)
    assert validation.is_valid
    assert len(validation.errors) == 0
    assert len(validation.warnings) == 0

async def test_generer_ecritures_cloture_ml(cloture_service, periode, comptes, mocker):
    """Test de la génération des écritures de clôture avec ML"""
    # Données test
    analyse_ml = {
        "ml_analysis": {
            "charge_adjustments": {
                "CHARGE": {"factor": 1.1}
            },
            "stock_predictions": {
                "STOCK": {"variation": 500}
            },
            "provision_recommendations": [
                {
                    "category": "RISQUE",
                    "amount": 1000,
                    "description": "Provision test",
                    "confidence": 0.85
                }
            ],
            "amortization_predictions": [
                {
                    "category": "MATERIEL",
                    "amount": 800,
                    "description": "Amortissement test",
                    "confidence": 0.9
                }
            ]
        }
    }
    
    optimization = {
        "provision_optimizations": {
            "RISQUE": {
                "optimized_amount": 900
            }
        }
    }
    
    # Mock des fonctions de compte
    mocker.patch.object(
        cloture_service,
        '_get_compte_variation_stock',
        return_value=comptes[0].id
    )
    
    mocker.patch.object(
        cloture_service,
        '_get_compte_provision',
        return_value=comptes[2].id
    )
    
    mocker.patch.object(
        cloture_service,
        '_get_compte_amortissement',
        return_value=comptes[0].id
    )
    
    # Test
    ecritures = await cloture_service._generer_ecritures_cloture_ml(
        periode,
        analyse_ml,
        optimization
    )
    
    # Vérification
    assert len(ecritures) > 0
    for ecriture in ecritures:
        assert isinstance(ecriture, EcritureComptable)
        if "ML" in ecriture.libelle:
            assert hasattr(ecriture, "ml_confidence")

async def test_calculer_provisions_ml(cloture_service, periode, comptes, mocker):
    """Test du calcul des provisions avec ML"""
    # Données test
    analyse_ml = {
        "ml_analysis": {
            "provision_recommendations": [
                {
                    "category": "RISQUE",
                    "amount": 1000,
                    "description": "Provision test",
                    "confidence": 0.85
                }
            ]
        }
    }
    
    optimization = {
        "provision_optimizations": {
            "RISQUE": {
                "optimized_amount": 900
            }
        }
    }
    
    # Mock du compte provision
    mocker.patch.object(
        cloture_service,
        '_get_compte_provision',
        return_value=comptes[2].id
    )
    
    # Test
    provisions = await cloture_service._calculer_provisions_ml(
        periode,
        analyse_ml,
        optimization
    )
    
    # Vérification
    assert len(provisions) > 0
    for provision in provisions:
        assert isinstance(provision, EcritureComptable)
        assert provision.montant == 900  # Montant optimisé
        assert provision.ml_confidence == 0.85

async def test_generate_cloture_recommendations(cloture_service):
    """Test de la génération des recommandations ML"""
    # Données test
    totaux = {
        "resultat": -1000
    }
    
    analyse_ml = {
        "ml_analysis": {
            "recommendations": [
                {
                    "type": "CLOSING",
                    "priority": "HIGH",
                    "description": "Action requise",
                    "actions": ["Action 1"]
                }
            ]
        }
    }
    
    optimization = {
        "closing_optimizations": [
            {
                "description": "Optimisation test",
                "actions": ["Action 1"],
                "savings": 100,
                "timeline": "1M"
            }
        ]
    }
    
    # Test
    recommendations = await cloture_service._generate_cloture_recommendations(
        totaux,
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

async def test_archiver_documents(cloture_service, periode, tmp_path, mocker):
    """Test de l'archivage des documents avec ML"""
    # Mock du chemin d'archive
    archive_path = tmp_path / "archives" / "cloture" / periode
    mocker.patch('os.makedirs')
    
    # Données test
    etats = {
        "grand_livre": {"data": "test"},
        "balance": {"data": "test"},
        "ml_analysis": {
            "predictions": {},
            "risk_factors": []
        }
    }
    
    # Mock des fonctions d'archivage
    mocker.patch.object(
        cloture_service,
        '_archiver_pieces_justificatives',
        return_value=None
    )
    
    mocker.patch.object(
        cloture_service,
        '_generer_rapport_cloture_ml',
        return_value=None
    )
    
    # Test
    await cloture_service._archiver_documents(periode, etats)
    
    # Vérification
    assert os.makedirs.called

async def test_cache_cloture_mensuelle(cloture_service, periode, mocker):
    """Test du cache pour la clôture mensuelle"""
    # Mock du cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    mocker.patch.object(cloture_service, 'cache', mock_cache)
    
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
            "closing_optimizations": []
        }
    )
    
    # Premier appel
    await cloture_service.executer_cloture_mensuelle(
        periode=periode,
        utilisateur_id="USER001"
    )
    
    # Vérification cache
    assert mock_cache.set.called
    
    # Deuxième appel
    mock_cache.get.return_value = {"cached": True}
    result = await cloture_service.executer_cloture_mensuelle(
        periode=periode,
        utilisateur_id="USER001"
    )
    
    # Vérification résultat du cache
    assert result == {"cached": True}
