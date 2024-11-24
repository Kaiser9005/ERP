"""
Tests pour le service de statistiques comptables
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.comptabilite_stats_service import ComptabiliteStatsService
from models.comptabilite import (
    CompteComptable,
    EcritureComptable,
    TypeCompte,
    StatutEcriture
)

@pytest.fixture
def stats_service(db_session):
    """Fixture du service de stats"""
    return ComptabiliteStatsService(db_session)

@pytest.fixture
def comptes(db_session):
    """Fixture des comptes test"""
    comptes = []
    
    # Compte produit
    compte_produit = CompteComptable(
        numero="701",
        libelle="Ventes produits",
        type_compte=TypeCompte.PRODUIT,
        actif=True,
        solde_debit=Decimal("0"),
        solde_credit=Decimal("5000")
    )
    comptes.append(compte_produit)
    
    # Compte charge
    compte_charge = CompteComptable(
        numero="601",
        libelle="Achats",
        type_compte=TypeCompte.CHARGE,
        actif=True,
        solde_debit=Decimal("3000"),
        solde_credit=Decimal("0")
    )
    comptes.append(compte_charge)
    
    # Compte trésorerie
    compte_tresorerie = CompteComptable(
        numero="512",
        libelle="Banque",
        type_compte=TypeCompte.ACTIF,
        actif=True,
        solde_debit=Decimal("10000"),
        solde_credit=Decimal("0")
    )
    comptes.append(compte_tresorerie)
    
    for compte in comptes:
        db_session.add(compte)
    db_session.commit()
    
    return comptes

@pytest.fixture
def ecritures(db_session, comptes):
    """Fixture des écritures test"""
    ecritures = []
    now = datetime.now(datetime.timezone.utc)
    
    # Écritures du mois
    for i in range(3):
        # Vente
        ecriture = EcritureComptable(
            compte_id=comptes[0].id,  # Compte produit
            date_ecriture=now - timedelta(days=i),
            periode=now.strftime("%Y-%m"),
            credit=Decimal("1000"),
            statut=StatutEcriture.VALIDEE
        )
        ecritures.append(ecriture)
        
        # Achat
        ecriture = EcritureComptable(
            compte_id=comptes[1].id,  # Compte charge
            date_ecriture=now - timedelta(days=i),
            periode=now.strftime("%Y-%m"),
            debit=Decimal("600"),
            statut=StatutEcriture.VALIDEE
        )
        ecritures.append(ecriture)
    
    # Écritures du mois précédent
    last_month = now - timedelta(days=30)
    for i in range(2):
        # Vente
        ecriture = EcritureComptable(
            compte_id=comptes[0].id,
            date_ecriture=last_month - timedelta(days=i),
            periode=last_month.strftime("%Y-%m"),
            credit=Decimal("800"),
            statut=StatutEcriture.VALIDEE
        )
        ecritures.append(ecriture)
        
        # Achat
        ecriture = EcritureComptable(
            compte_id=comptes[1].id,
            date_ecriture=last_month - timedelta(days=i),
            periode=last_month.strftime("%Y-%m"),
            debit=Decimal("500"),
            statut=StatutEcriture.VALIDEE
        )
        ecritures.append(ecriture)
    
    for ecriture in ecritures:
        db_session.add(ecriture)
    db_session.commit()
    
    return ecritures

async def test_get_stats_basic(stats_service, comptes, ecritures):
    """Test des statistiques de base"""
    stats = await stats_service.get_stats()
    
    # Vérification structure
    assert "revenue" in stats
    assert "revenueVariation" in stats
    assert "expenses" in stats
    assert "expensesVariation" in stats
    assert "profit" in stats
    assert "profitVariation" in stats
    assert "cashflow" in stats
    assert "cashflowVariation" in stats
    
    # Vérification montants
    assert stats["revenue"] == 3000  # 3 x 1000
    assert stats["expenses"] == 1800  # 3 x 600
    assert stats["profit"] == 1200  # 3000 - 1800
    assert stats["cashflow"] == 10000  # Solde compte trésorerie

async def test_get_stats_with_ml(stats_service, comptes, ecritures, mocker):
    """Test des statistiques avec ML"""
    # Mock des prédictions ML
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance',
        return_value={
            "predictions": [
                {
                    "month": "2024-02",
                    "revenue": 3500,
                    "costs": 2000,
                    "margin": 1500,
                    "confidence": 0.85
                }
            ],
            "risk_factors": [
                {
                    "factor": "Météo",
                    "severity": "MEDIUM",
                    "mitigation": ["Adapter planning"]
                }
            ]
        }
    )
    
    stats = await stats_service.get_stats()
    
    # Vérification ML
    assert "predictions" in stats
    assert "next_3_months" in stats["predictions"]
    assert "trends" in stats["predictions"]
    assert "risk_factors" in stats["predictions"]
    
    # Vérification recommandations
    assert "recommendations" in stats
    assert len(stats["recommendations"]) > 0
    for rec in stats["recommendations"]:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_get_budget_analysis(stats_service, comptes, ecritures, mocker):
    """Test de l'analyse budgétaire"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_monthly_stats',
        return_value={
            "precipitation": 250,
            "temperature_avg": 32
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs',
        return_value={
            "current_costs": {"TRANSPORT": 1000},
            "optimized_costs": {"TRANSPORT": 900},
            "potential_savings": 100,
            "implementation_plan": [
                {
                    "category": "TRANSPORT",
                    "actions": ["Optimiser routes"]
                }
            ]
        }
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance',
        return_value={
            "predictions": [
                {
                    "month": "2024-02",
                    "revenue": 3500,
                    "costs": 2000,
                    "margin": 1500
                }
            ]
        }
    )
    
    # Analyse
    analysis = await stats_service.get_budget_analysis("2024-01")
    
    # Vérification structure
    assert "total_prevu" in analysis
    assert "total_realise" in analysis
    assert "categories" in analysis
    assert "weather_impact" in analysis
    assert "optimization" in analysis
    assert "performance" in analysis
    assert "recommendations" in analysis
    
    # Vérification optimisation
    assert "potential_savings" in analysis["optimization"]
    assert "implementation_plan" in analysis["optimization"]
    
    # Vérification recommandations
    assert len(analysis["recommendations"]) > 0
    for rec in analysis["recommendations"]:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_get_cashflow(stats_service, comptes, ecritures, mocker):
    """Test des données de trésorerie"""
    # Mock des services externes
    mocker.patch(
        'services.weather_service.WeatherService.get_daily_impact',
        return_value={"impact": 5}
    )
    
    mocker.patch(
        'services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle',
        return_value={
            "ml_analysis": {
                "predictions": {
                    "revenue": 3500,
                    "costs": 2000
                },
                "risks": [
                    {
                        "type": "WEATHER",
                        "severity": "MEDIUM",
                        "description": "Impact météo"
                    }
                ]
            }
        }
    )
    
    # Données trésorerie
    cashflow = await stats_service.get_cashflow(days=7)
    
    # Vérification structure
    assert len(cashflow) == 7
    for entry in cashflow:
        assert "date" in entry
        assert "entrees" in entry
        assert "sorties" in entry
        assert "solde" in entry
        assert "impact_meteo" in entry
        assert "ml_predictions" in entry
        assert "ml_risks" in entry
        
    # Vérification ML
    for entry in cashflow:
        assert "revenue" in entry["ml_predictions"]
        assert "costs" in entry["ml_predictions"]
        assert len(entry["ml_risks"]) > 0

async def test_calculate_variation(stats_service):
    """Test du calcul des variations"""
    # Augmentation
    variation = stats_service._calculate_variation(110, 100)
    assert variation["value"] == 10.0
    assert variation["type"] == "increase"
    
    # Diminution
    variation = stats_service._calculate_variation(90, 100)
    assert variation["value"] == 10.0
    assert variation["type"] == "decrease"
    
    # Valeur précédente nulle
    variation = stats_service._calculate_variation(100, 0)
    assert variation["value"] == 0
    assert variation["type"] == "increase"

async def test_calculate_trend(stats_service):
    """Test du calcul des tendances"""
    # Tendance à la hausse
    trend = stats_service._calculate_trend([100, 110, 120])
    assert trend == "increasing"
    
    # Tendance à la baisse
    trend = stats_service._calculate_trend([120, 110, 100])
    assert trend == "decreasing"
    
    # Tendance stable
    trend = stats_service._calculate_trend([100, 101, 102])
    assert trend == "stable"
    
    # Liste vide
    trend = stats_service._calculate_trend([])
    assert trend == "stable"

async def test_generate_recommendations(stats_service):
    """Test de la génération des recommandations"""
    # Données test
    stats = {
        "profitVariation": {
            "value": 15,
            "type": "decrease"
        }
    }
    
    predictions = {
        "risk_factors": [
            {
                "factor": "Météo",
                "mitigation": ["Adapter planning"]
            }
        ]
    }
    
    # Génération recommandations
    recommendations = await stats_service._generate_recommendations(
        stats,
        predictions
    )
    
    # Vérification
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec
        
    # Vérification recommandation profit
    profit_recs = [r for r in recommendations if r["type"] == "PROFIT"]
    assert len(profit_recs) > 0
    
    # Vérification recommandation risque
    risk_recs = [r for r in recommendations if r["type"] == "RISK"]
    assert len(risk_recs) > 0

async def test_generate_budget_recommendations(stats_service):
    """Test de la génération des recommandations budgétaires"""
    # Données test
    analysis = {
        "total_prevu": 1000,
        "total_realise": 1200
    }
    
    optimization = {
        "potential_savings": 100,
        "implementation_plan": [
            {
                "category": "TRANSPORT",
                "actions": ["Optimiser routes"]
            }
        ]
    }
    
    performance = {
        "predictions": [
            {
                "month": "2024-02",
                "revenue": 1000,
                "costs": 1200,
                "margin": -200
            }
        ]
    }
    
    # Génération recommandations
    recommendations = await stats_service._generate_budget_recommendations(
        analysis,
        optimization,
        performance
    )
    
    # Vérification
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec
        
    # Vérification recommandation optimisation
    opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
    assert len(opt_recs) > 0
    
    # Vérification recommandation performance
    perf_recs = [r for r in recommendations if r["type"] == "PERFORMANCE"]
    assert len(perf_recs) > 0

async def test_get_prediction_for_date(stats_service):
    """Test de la récupération des prédictions par date"""
    # Données test
    predictions = {
        "revenue": 1000,
        "costs": 800
    }
    
    target_date = date.today()
    
    # Récupération prédiction
    revenue = stats_service._get_prediction_for_date(
        predictions,
        target_date,
        "revenue"
    )
    
    costs = stats_service._get_prediction_for_date(
        predictions,
        target_date,
        "costs"
    )
    
    # Vérification
    assert revenue == 1000
    assert costs == 800
    
    # Métrique inexistante
    unknown = stats_service._get_prediction_for_date(
        predictions,
        target_date,
        "unknown"
    )
    assert unknown == 0

async def test_risk_applies_to_date(stats_service):
    """Test de l'application des risques par date"""
    # Données test
    risk = {
        "type": "WEATHER",
        "severity": "HIGH",
        "description": "Impact météo"
    }
    
    target_date = date.today()
    
    # Vérification
    assert stats_service._risk_applies_to_date(risk, target_date) == True
