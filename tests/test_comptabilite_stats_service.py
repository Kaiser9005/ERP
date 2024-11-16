import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch
from services.comptabilite_stats_service import ComptabiliteStatsService
from models.comptabilite import CompteComptable, EcritureComptable, TypeCompte, StatutEcriture

@pytest.fixture
def db_session():
    return Mock()

@pytest.fixture
def weather_service():
    return Mock()

@pytest.fixture
def stats_service(db_session, weather_service):
    service = ComptabiliteStatsService(db_session)
    service.weather_service = weather_service
    return service

@pytest.fixture
def mock_comptes(db_session):
    compte_produit = Mock(
        id='123',
        type_compte=TypeCompte.PRODUIT,
        solde_credit=Decimal('150000'),
        solde_debit=Decimal('0')
    )
    compte_charge = Mock(
        id='456',
        type_compte=TypeCompte.CHARGE,
        solde_debit=Decimal('120000'),
        solde_credit=Decimal('0')
    )
    compte_actif = Mock(
        id='789',
        type_compte=TypeCompte.ACTIF,
        solde_debit=Decimal('45000'),
        solde_credit=Decimal('0'),
        actif=True
    )
    
    db_session.query.return_value.filter.return_value.all.return_value = [
        compte_produit, compte_charge, compte_actif
    ]
    return compte_produit, compte_charge, compte_actif

@pytest.mark.asyncio
async def test_get_stats(stats_service, db_session, mock_comptes):
    # Configuration des mocks pour les requêtes SQL
    current_month = datetime.now().strftime("%Y-%m")
    last_month = (datetime.now() - timedelta(days=30)).strftime("%Y-%m")
    
    db_session.query.return_value.filter.return_value.scalar.side_effect = [
        Decimal('150000'),  # revenue current
        Decimal('142500'),  # revenue previous
        Decimal('120000'),  # expenses current
        Decimal('123800'),  # expenses previous
        Decimal('45000'),   # cashflow
    ]

    # Exécution du test
    result = await stats_service.get_stats()

    # Vérifications
    assert result['revenue'] == float(150000)
    assert result['revenueVariation']['value'] == 5.3  # (150000-142500)/142500 * 100
    assert result['revenueVariation']['type'] == 'increase'
    
    assert result['expenses'] == float(120000)
    assert result['expensesVariation']['value'] == 3.1  # (120000-123800)/123800 * 100
    assert result['expensesVariation']['type'] == 'decrease'
    
    assert result['profit'] == float(30000)  # 150000 - 120000
    assert result['cashflow'] == float(45000)

@pytest.mark.asyncio
async def test_get_budget_analysis(stats_service, db_session, weather_service):
    # Mock des données météo
    weather_service.get_monthly_stats.return_value = {
        'precipitation': 250,
        'temperature_avg': 32
    }

    # Mock des données comptables
    mock_query_result = [
        Mock(
            numero='601',
            libelle='Achats',
            debit=Decimal('98000'),
            credit=Decimal('0')
        )
    ]
    db_session.query.return_value.join.return_value.filter.return_value.group_by.return_value = mock_query_result

    # Exécution du test
    result = await stats_service.get_budget_analysis('2024-01')

    # Vérifications
    assert 'total_prevu' in result
    assert 'total_realise' in result
    assert 'categories' in result
    assert 'weather_impact' in result
    assert 'recommendations' in result

    # Vérification de l'impact météo
    weather_impact = result['weather_impact']
    assert weather_impact['score'] == 50  # 30 (précipitations) + 20 (température)
    assert 'Fortes précipitations' in weather_impact['factors']
    assert 'Températures élevées' in weather_impact['factors']
    assert 'TRANSPORT' in weather_impact['projections']
    assert 'MAINTENANCE' in weather_impact['projections']

@pytest.mark.asyncio
async def test_get_cashflow(stats_service, db_session, weather_service):
    # Mock des données météo
    weather_service.get_daily_impact.return_value = {
        'impact': 4.0
    }

    # Mock des écritures comptables
    mock_daily_data = Mock(
        entrees=Decimal('25000'),
        sorties=Decimal('20000')
    )
    db_session.query.return_value.filter.return_value.first.return_value = mock_daily_data

    # Mock du solde initial
    db_session.query.return_value.filter.return_value.scalar.return_value = Decimal('40000')

    # Exécution du test
    result = await stats_service.get_cashflow(days=30)

    # Vérifications
    assert len(result) == 30  # Un résultat par jour
    first_day = result[0]
    assert first_day['entrees'] == float(25000)
    assert first_day['sorties'] == float(20000)
    assert first_day['impact_meteo'] == 4.0
    assert 'date' in first_day
    assert 'solde' in first_day
    assert 'prevision' in first_day

@pytest.mark.asyncio
async def test_analyze_weather_impact(stats_service, weather_service):
    # Mock des données météo
    weather_service.get_monthly_stats.return_value = {
        'precipitation': 250,
        'temperature_avg': 32
    }

    # Exécution du test
    result = await stats_service._analyze_weather_impact('2024-01')

    # Vérifications
    assert result['score'] == 50
    assert len(result['factors']) == 2
    assert 'Fortes précipitations' in result['factors']
    assert 'Températures élevées' in result['factors']
    assert len(result['projections']) == 2
    assert 'TRANSPORT' in result['projections']
    assert 'MAINTENANCE' in result['projections']

def test_calculate_variation():
    service = ComptabiliteStatsService(Mock())
    
    # Test augmentation
    result = service._calculate_variation(110, 100)
    assert result['value'] == 10.0
    assert result['type'] == 'increase'
    
    # Test diminution
    result = service._calculate_variation(90, 100)
    assert result['value'] == 10.0
    assert result['type'] == 'decrease'
    
    # Test pas de changement
    result = service._calculate_variation(100, 100)
    assert result['value'] == 0
    assert result['type'] == 'increase'
    
    # Test valeur précédente à zéro
    result = service._calculate_variation(100, 0)
    assert result['value'] == 0
    assert result['type'] == 'increase'

def test_calculate_prevision():
    service = ComptabiliteStatsService(Mock())
    
    # Test impact positif
    result = service._calculate_prevision(1000, 5.0)
    assert result == 1050.0  # 1000 * (1 + 5/100)
    
    # Test impact négatif
    result = service._calculate_prevision(1000, -3.0)
    assert result == 970.0  # 1000 * (1 + (-3)/100)
    
    # Test sans impact
    result = service._calculate_prevision(1000, 0)
    assert result == 1000.0
