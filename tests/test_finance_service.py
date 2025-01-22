"""
Tests du service finance avec ML et cache
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from services.finance_service import FinanceService
from models.finance import Budget, Transaction, Compte
from schemas.finance import BudgetCreate, TransactionCreate, BudgetUpdate
from decimal import Decimal
from typing import Dict, Any

@pytest.fixture
def db_session():
    """Mock de session DB"""
    return Mock()

@pytest.fixture
def finance_service(db_session):
    """Instance de FinanceService avec DB mockée"""
    return FinanceService(db_session)

@pytest.fixture
def sample_budget_create():
    """Données de test pour la création d'un budget"""
    return BudgetCreate(
        periode="2024-01",
        categorie="ACHAT_INTRANT",
        montant_prevu=1000000.0,
        notes="Budget intrants Q1 2024"
    )

@pytest.fixture
def sample_transaction_create():
    """Données de test pour la création d'une transaction"""
    return TransactionCreate(
        reference="TRX-2024-001",
        date_transaction=datetime.now(datetime.timezone.utc),
        type_transaction="DEPENSE",
        categorie="ACHAT_INTRANT",
        montant=50000.0,
        description="Achat engrais",
        compte_source_id="123e4567-e89b-12d3-a456-426614174000"
    )

class TestFinanceService:
    """Tests du service finance"""

    async def test_get_stats_with_ml(self, finance_service, db_session):
        """Test des statistiques avec ML"""
        # Setup
        db_session.query().filter().scalar.return_value = 1000000.0
        
        # Mock ML
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
            mock_predict.return_value = {
                "predictions": [
                    {
                        "month": "2024-02",
                        "revenue": 3500,
                        "costs": 2000,
                        "margin": 1500
                    }
                ],
                "risk_factors": [
                    {
                        "factor": "Météo",
                        "severity": "HIGH",
                        "mitigation": ["Action 1"]
                    }
                ]
            }
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
                mock_optimize.return_value = {
                    "potential_savings": 1000,
                    "implementation_plan": [
                        {
                            "category": "TRANSPORT",
                            "actions": ["Optimiser routes"]
                        }
                    ]
                }
                
                # Exécution
                stats = await finance_service.get_stats()
                
                # Vérifications
                assert "predictions" in stats
                assert "optimization" in stats
                assert "recommendations" in stats
                assert len(stats["recommendations"]) > 0

    async def test_stats_cache(self, finance_service, db_session):
        """Test du cache des statistiques"""
        # Setup
        mock_cache = Mock()
        mock_cache.get.return_value = None
        finance_service.cache = mock_cache
        
        db_session.query().filter().scalar.return_value = 1000000.0
        
        # Mock ML
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
            mock_predict.return_value = {
                "predictions": [],
                "risk_factors": []
            }
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
                mock_optimize.return_value = {
                    "potential_savings": 0,
                    "implementation_plan": []
                }
                
                # Première exécution
                await finance_service.get_stats()
                
                # Vérifications cache
                assert mock_cache.set.called
                
                # Deuxième exécution avec cache
                mock_cache.get.return_value = {"cached": True}
                stats = await finance_service.get_stats()
                
                assert stats["cached"]

    async def test_create_budget_with_ml(self, finance_service, sample_budget_create, db_session):
        """Test création d'un budget avec ML"""
        # Setup
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock()
        
        # Mock ML
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
            mock_optimize.return_value = {
                "potential_savings": 100000.0,
                "implementation_plan": [
                    {
                        "category": "ACHAT_INTRANT",
                        "actions": ["Optimiser achats"]
                    }
                ]
            }
            
            # Exécution
            budget = await finance_service.create_budget(sample_budget_create)
            
            # Vérifications
            assert db_session.add.called
            assert db_session.commit.called
            assert budget.montant_prevu == sample_budget_create.montant_prevu - 100000.0

    async def test_get_budgets_with_ml(self, finance_service, db_session):
        """Test récupération des budgets avec ML"""
        # Setup
        expected_budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0
            )
        ]
        db_session.query().filter().all.return_value = expected_budgets
        
        # Mock ML
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle') as mock_analyse:
            mock_analyse.return_value = {
                "ml_analysis": {
                    "predictions": {"revenue": 1500000.0},
                    "recommendations": ["Optimisation possible"]
                }
            }
            
            # Exécution
            budgets = await finance_service.get_budgets("2024-01")
            
            # Vérifications
            assert len(budgets) == 1
            assert hasattr(budgets[0], "ml_predictions")
            assert hasattr(budgets[0], "ml_recommendations")

    async def test_budget_cache(self, finance_service, db_session):
        """Test du cache des budgets"""
        # Setup
        mock_cache = Mock()
        mock_cache.get.return_value = None
        finance_service.cache = mock_cache
        
        expected_budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0
            )
        ]
        db_session.query().filter().all.return_value = expected_budgets
        
        # Première exécution
        await finance_service.get_budgets("2024-01")
        
        # Vérifications cache
        assert mock_cache.set.called
        
        # Deuxième exécution avec cache
        mock_cache.get.return_value = [{"cached": True}]
        budgets = await finance_service.get_budgets("2024-01")
        
        assert budgets[0]["cached"]

    async def test_get_budget_analysis_with_ml(self, finance_service, db_session):
        """Test analyse budgétaire avec ML"""
        # Setup
        budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0,
                montant_realise=1200000.0
            )
        ]
        db_session.query().filter().all.return_value = budgets
        
        # Mock services
        with patch.object(finance_service, '_analyze_weather_impact') as mock_weather:
            mock_weather.return_value = {
                "score": 50,
                "factors": ["Fortes précipitations"],
                "projections": {"TRANSPORT": "Augmentation probable"}
            }
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
                mock_optimize.return_value = {
                    "potential_savings": 100000.0,
                    "implementation_plan": [
                        {
                            "category": "ACHAT_INTRANT",
                            "actions": ["Optimiser achats"]
                        }
                    ]
                }
                
                with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
                    mock_predict.return_value = {
                        "predictions": [
                            {
                                "month": "2024-02",
                                "margin": -100000.0
                            }
                        ]
                    }
                    
                    # Exécution
                    analysis = await finance_service.get_budget_analysis("2024-01")
                    
                    # Vérifications
                    assert "optimization" in analysis
                    assert "performance" in analysis
                    assert len(analysis["recommendations"]) > 0

    async def test_get_financial_projections_with_ml(self, finance_service, db_session):
        """Test projections financières avec ML"""
        # Setup
        db_session.query().filter().scalar.return_value = 1000000.0
        
        # Mock services
        with patch.object(finance_service, '_analyze_weather_impact') as mock_weather:
            mock_weather.return_value = {
                "score": 30,
                "factors": ["Températures élevées"],
                "projections": {}
            }
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
                mock_predict.return_value = {
                    "predictions": [
                        {
                            "month": "2024-02",
                            "revenue": 3500,
                            "costs": 2000,
                            "margin": 1500
                        }
                    ]
                }
                
                # Exécution
                projections = await finance_service.get_financial_projections(months_ahead=1)
                
                # Vérifications
                assert "ml_predictions" in projections
                assert len(projections["revenue"]) == 1
                assert "ml_prediction" in projections["revenue"][0]

    async def test_projections_cache(self, finance_service, db_session):
        """Test du cache des projections"""
        # Setup
        mock_cache = Mock()
        mock_cache.get.return_value = None
        finance_service.cache = mock_cache
        
        db_session.query().filter().scalar.return_value = 1000000.0
        
        # Mock services
        with patch.object(finance_service, '_analyze_weather_impact') as mock_weather:
            mock_weather.return_value = {
                "score": 30,
                "factors": [],
                "projections": {}
            }
            
            # Première exécution
            await finance_service.get_financial_projections()
            
            # Vérifications cache
            assert mock_cache.set.called
            
            # Deuxième exécution avec cache
            mock_cache.get.return_value = {"cached": True}
            projections = await finance_service.get_financial_projections()
            
            assert projections["cached"]

    async def test_generate_recommendations(self, finance_service):
        """Test génération des recommandations"""
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
                    "severity": "HIGH",
                    "mitigation": ["Action 1"]
                }
            ]
        }
        
        optimization = {
            "potential_savings": 100000.0,
            "implementation_plan": [
                {
                    "category": "TRANSPORT",
                    "actions": ["Optimiser routes"]
                }
            ]
        }
        
        # Exécution
        recommendations = await finance_service._generate_recommendations(
            stats,
            predictions,
            optimization
        )
        
        # Vérifications
        assert len(recommendations) > 0
        
        # Vérification types
        profit_recs = [r for r in recommendations if r["type"] == "PROFIT"]
        assert len(profit_recs) > 0
        
        risk_recs = [r for r in recommendations if r["type"] == "RISK"]
        assert len(risk_recs) > 0
        
        opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
        assert len(opt_recs) > 0

    async def test_generate_budget_recommendations(self, finance_service):
        """Test génération des recommandations budgétaires"""
        # Données test
        analysis = {
            "categories": {
                "ACHAT_INTRANT": {
                    "ecart_percentage": -15
                },
                "TRANSPORT": {
                    "ecart_percentage": 20
                }
            }
        }
        
        optimization = {
            "potential_savings": 100000.0,
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
                    "margin": -50000.0
                }
            ]
        }
        
        # Exécution
        recommendations = await finance_service._generate_budget_recommendations(
            analysis,
            optimization,
            performance
        )
        
        # Vérifications
        assert len(recommendations) > 0
        
        # Vérification types
        gap_recs = [r for r in recommendations if r["type"] == "BUDGET_GAP"]
        assert len(gap_recs) > 0
        
        opt_recs = [r for r in recommendations if r["type"] == "OPTIMIZATION"]
        assert len(opt_recs) > 0
        
        perf_recs = [r for r in recommendations if r["type"] == "PERFORMANCE"]
        assert len(perf_recs) > 0

    async def test_create_transaction_updates_budget(self, finance_service, sample_transaction_create, db_session):
        """Test que la création d'une transaction met à jour le budget"""
        # Setup
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock()
        
        existing_budget = Budget(
            periode=datetime.utcnow().strftime("%Y-%m"),
            categorie="ACHAT_INTRANT",
            montant_prevu=1000000.0,
            montant_realise=0
        )
        db_session.query().filter().first.side_effect = [
            Mock(solde=100000),  # Pour le compte
            existing_budget  # Pour le budget
        ]
        
        # Mock cache
        mock_cache = Mock()
        finance_service.cache = mock_cache

        # Exécution
        transaction = await finance_service.create_transaction(sample_transaction_create)

        # Vérifications
        assert db_session.commit.called
        assert existing_budget.montant_realise == sample_transaction_create.montant
        assert mock_cache.delete.call_count == 2  # Stats et budget analysis

    async def test_create_transaction_insufficient_balance(self, finance_service, sample_transaction_create, db_session):
        """Test la création d'une transaction avec solde insuffisant"""
        # Setup
        db_session.query().filter().first.return_value = Mock(solde=10000)  # Solde insuffisant

        # Vérification
        with pytest.raises(ValueError, match="Solde insuffisant"):
            await finance_service.create_transaction(sample_transaction_create)

    async def test_create_transaction_account_not_found(self, finance_service, sample_transaction_create, db_session):
        """Test la création d'une transaction avec compte inexistant"""
        # Setup
        db_session.query().filter().first.return_value = None

        # Vérification
        with pytest.raises(ValueError, match="Compte source non trouvé"):
            await finance_service.create_transaction(sample_transaction_create)

    async def test_handle_virement(self, finance_service, db_session):
        """Test d'un virement entre comptes"""
        # Setup
        virement = TransactionCreate(
            reference="VIR-2024-001",
            date_transaction=datetime.now(datetime.timezone.utc),
            type_transaction="VIREMENT",
            categorie="VIREMENT_INTERNE",
            montant=50000.0,
            description="Virement entre comptes",
            compte_source_id="compte1",
            compte_destination_id="compte2"
        )

        compte_source = Mock(solde=100000)
        compte_destination = Mock(solde=20000)
        db_session.query().filter().first.side_effect = [
            compte_source,  # Pour le compte source
            compte_destination,  # Pour le compte destination
            None  # Pour le budget (pas de budget pour les virements)
        ]

        # Exécution
        await finance_service.create_transaction(virement)

        # Vérifications
        assert compte_source.solde == 50000  # 100000 - 50000
        assert compte_destination.solde == 70000  # 20000 + 50000

    async def test_update_budget_not_found(self, finance_service, db_session):
        """Test la mise à jour d'un budget inexistant"""
        # Setup
        db_session.query().filter().first.return_value = None
        budget_update = BudgetUpdate(montant_prevu=1000000.0)

        # Vérification
        with pytest.raises(ValueError, match="Budget non trouvé"):
            await finance_service.update_budget("budget_id", budget_update)

    async def test_handle_recette(self, finance_service, db_session):
        """Test d'une recette"""
        # Setup
        recette = TransactionCreate(
            reference="REC-2024-001",
            date_transaction=datetime.now(datetime.timezone.utc),
            type_transaction="RECETTE",
            categorie="VENTE_PRODUCTION",
            montant=75000.0,
            description="Vente production",
            compte_destination_id="compte1"
        )

        compte = Mock(solde=100000)
        db_session.query().filter().first.side_effect = [
            compte,  # Pour le compte
            None  # Pour le budget
        ]

        # Exécution
        await finance_service.create_transaction(recette)

        # Vérifications
        assert compte.solde == 175000  # 100000 + 75000

    async def test_get_basic_stats(self, finance_service, db_session):
        """Test des statistiques de base"""
        # Setup
        db_session.query().filter().scalar.side_effect = [
            1000000.0,  # revenue actuel
            800000.0,   # revenue précédent
            600000.0,   # dépenses actuelles
            500000.0,   # dépenses précédentes
            2000000.0   # trésorerie
        ]

        # Exécution
        stats = await finance_service._get_basic_stats()

        # Vérifications
        assert stats["revenue"] == 1000000.0
        assert stats["expenses"] == 600000.0
        assert stats["profit"] == 400000.0
        assert stats["cashflow"] == 2000000.0
        assert stats["revenueVariation"]["value"] == 25.0
        assert stats["revenueVariation"]["type"] == "increase"

    async def test_calculate_base_projection(self, finance_service, db_session):
        """Test du calcul de projection de base"""
        # Setup
        db_session.query().filter().scalar.return_value = 50000.0

        # Exécution
        projection = await finance_service._calculate_base_projection(
            "RECETTE",
            "2024-02"
        )

        # Vérifications
        assert projection == 50000.0

    async def test_update_budget_realise_depense(self, finance_service, db_session):
        """Test de mise à jour du budget réalisé pour une dépense"""
        # Setup
        budget = Budget(
            periode="2024-02",
            categorie="ACHAT_INTRANT",
            montant_prevu=100000.0,
            montant_realise=0
        )
        db_session.query().filter().first.return_value = budget

        transaction = TransactionCreate(
            reference="DEP-2024-001",
            date_transaction=datetime.strptime("2024-02-01", "%Y-%m-%d"),
            type_transaction="DEPENSE",
            categorie="ACHAT_INTRANT",
            montant=30000.0,
            description="Test dépense",
            compte_source_id="compte1"
        )

        # Exécution
        await finance_service._update_budget_realise(transaction)

        # Vérifications
        assert budget.montant_realise == 30000.0

    async def test_update_budget_realise_recette(self, finance_service, db_session):
        """Test de mise à jour du budget réalisé pour une recette"""
        # Setup
        budget = Budget(
            periode="2024-02",
            categorie="VENTE_PRODUCTION",
            montant_prevu=200000.0,
            montant_realise=0
        )
        db_session.query().filter().first.return_value = budget

        transaction = TransactionCreate(
            reference="REC-2024-001",
            date_transaction=datetime.strptime("2024-02-01", "%Y-%m-%d"),
            type_transaction="RECETTE",
            categorie="VENTE_PRODUCTION",
            montant=50000.0,
            description="Test recette",
            compte_destination_id="compte1"
        )

        # Exécution
        await finance_service._update_budget_realise(transaction)

        # Vérifications
        assert budget.montant_realise == 50000.0

    async def test_get_budgets_all(self, finance_service, db_session):
        """Test récupération de tous les budgets"""
        # Setup
        expected_budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0
            ),
            Budget(
                periode="2024-02",
                categorie="TRANSPORT",
                montant_prevu=500000.0
            )
        ]
        db_session.query().all.return_value = expected_budgets

        # Exécution
        budgets = await finance_service.get_budgets()

        # Vérifications
        assert len(budgets) == 2
        assert not hasattr(budgets[0], "ml_predictions")

    async def test_update_budget_multiple_fields(self, finance_service, db_session):
        """Test mise à jour de plusieurs champs d'un budget"""
        # Setup
        budget = Budget(
            periode="2024-02",
            categorie="ACHAT_INTRANT",
            montant_prevu=100000.0,
            notes="Initial"
        )
        db_session.query().filter().first.return_value = budget

        update = BudgetUpdate(
            montant_prevu=120000.0,
            notes="Updated"
        )

        # Mock ML
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
            mock_optimize.return_value = {
                "potential_savings": 10000.0,
                "implementation_plan": []
            }

            # Exécution
            updated = await finance_service.update_budget("budget-id", update)

            # Vérifications
            assert updated.montant_prevu == 110000.0  # 120000 - 10000
            assert updated.notes == "Updated"
