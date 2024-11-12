import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch
from services.finance_service import FinanceService
from models.finance import Budget, Transaction, Compte
from schemas.finance import BudgetCreate, TransactionCreate
from decimal import Decimal

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
        date_transaction=datetime.utcnow(),
        type_transaction="DEPENSE",
        categorie="ACHAT_INTRANT",
        montant=50000.0,
        description="Achat engrais",
        compte_source_id="123e4567-e89b-12d3-a456-426614174000"
    )

class TestFinanceService:
    """Tests du service finance"""

    async def test_create_budget(self, finance_service, sample_budget_create, db_session):
        """Test création d'un budget"""
        # Setup
        db_session.add = Mock()
        db_session.commit = Mock()
        db_session.refresh = Mock()

        # Exécution
        budget = await finance_service.create_budget(sample_budget_create)

        # Vérifications
        assert db_session.add.called
        assert db_session.commit.called
        assert budget.periode == sample_budget_create.periode
        assert budget.montant_prevu == sample_budget_create.montant_prevu

    async def test_get_budgets(self, finance_service, db_session):
        """Test récupération des budgets"""
        # Setup
        expected_budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0
            )
        ]
        db_session.query().filter().all.return_value = expected_budgets

        # Exécution
        budgets = await finance_service.get_budgets("2024-01")

        # Vérifications
        assert len(budgets) == 1
        assert budgets[0].periode == "2024-01"

    async def test_update_budget_realise(self, finance_service, sample_transaction_create, db_session):
        """Test mise à jour automatique du budget réalisé"""
        # Setup
        existing_budget = Budget(
            periode="2024-01",
            categorie="ACHAT_INTRANT",
            montant_prevu=1000000.0,
            montant_realise=0
        )
        db_session.query().filter().first.return_value = existing_budget

        # Exécution
        await finance_service._update_budget_realise(sample_transaction_create)

        # Vérifications
        assert existing_budget.montant_realise == sample_transaction_create.montant

    @patch('services.weather_service.WeatherService.get_monthly_stats')
    async def test_analyze_weather_impact(self, mock_weather_stats, finance_service):
        """Test analyse de l'impact météo"""
        # Setup
        mock_weather_stats.return_value = {
            "precipitation": 250,  # Fortes pluies
            "temperature_avg": 32  # Température élevée
        }

        # Exécution
        impact = await finance_service._analyze_weather_impact("2024-01")

        # Vérifications
        assert impact["score"] > 0
        assert len(impact["factors"]) > 0
        assert "TRANSPORT" in impact["projections"]
        assert "MAINTENANCE" in impact["projections"]

    async def test_get_budget_analysis(self, finance_service, db_session):
        """Test analyse budgétaire"""
        # Setup
        budgets = [
            Budget(
                periode="2024-01",
                categorie="ACHAT_INTRANT",
                montant_prevu=1000000.0,
                montant_realise=1200000.0
            ),
            Budget(
                periode="2024-01",
                categorie="TRANSPORT",
                montant_prevu=500000.0,
                montant_realise=400000.0
            )
        ]
        db_session.query().filter().all.return_value = budgets

        with patch.object(finance_service, '_analyze_weather_impact') as mock_weather:
            mock_weather.return_value = {
                "score": 50,
                "factors": ["Fortes précipitations"],
                "projections": {"TRANSPORT": "Augmentation probable"}
            }

            # Exécution
            analysis = await finance_service.get_budget_analysis("2024-01")

            # Vérifications
            assert "total_prevu" in analysis
            assert "total_realise" in analysis
            assert "categories" in analysis
            assert len(analysis["recommendations"]) > 0
            assert "weather_impact" in analysis

    async def test_get_financial_projections(self, finance_service, db_session):
        """Test projections financières"""
        # Setup
        db_session.query().filter().scalar.return_value = 1000000.0

        with patch.object(finance_service, '_analyze_weather_impact') as mock_weather:
            mock_weather.return_value = {
                "score": 30,
                "factors": ["Températures élevées"],
                "projections": {}
            }

            # Exécution
            projections = await finance_service.get_financial_projections(months_ahead=2)

            # Vérifications
            assert "revenue" in projections
            assert "expenses" in projections
            assert "weather_factors" in projections
            assert len(projections["revenue"]) == 2
            assert len(projections["expenses"]) == 2

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

        # Exécution
        transaction = await finance_service.create_transaction(sample_transaction_create)

        # Vérifications
        assert db_session.commit.called
        assert existing_budget.montant_realise == sample_transaction_create.montant
