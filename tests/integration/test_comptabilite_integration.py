"""
Tests d'intégration du service comptable avec ML et cache
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from main import app
from services.comptabilite_service import ComptabiliteService
from services.comptabilite_stats_service import ComptabiliteStatsService
from models.comptabilite import (
    CompteComptable, EcritureComptable, JournalComptable,
    TypeCompte, StatutEcriture, TypeJournal
)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db_session():
    return Mock(spec=Session)

@pytest.fixture
def mock_weather_data():
    return {
        'precipitation': 250,
        'temperature_avg': 32,
        'impact': 4.0
    }

@pytest.fixture
def mock_compte_data():
    return {
        'numero': '601000',
        'libelle': 'Achats matières premières',
        'type_compte': TypeCompte.CHARGE,
        'description': 'Compte pour les achats de matières premières'
    }

@pytest.fixture
def mock_ecriture_data():
    return {
        'date_ecriture': date.today().isoformat(),
        'numero_piece': 'FAC2024-001',
        'compte_id': '123e4567-e89b-12d3-a456-426614174000',
        'libelle': 'Achat matières premières',
        'debit': 1000.00,
        'credit': 0.00,
        'journal_id': '123e4567-e89b-12d3-a456-426614174001'
    }

@pytest.fixture
def mock_ml_data():
    return {
        'ml_analysis': {
            'predictions': {
                'revenue': 3500,
                'costs': 2000,
                'margin': 1500
            },
            'recommendations': [
                {
                    'type': 'COST',
                    'priority': 'HIGH',
                    'description': 'Optimisation possible',
                    'actions': ['Action 1']
                }
            ]
        },
        'optimization': {
            'potential_savings': 1000,
            'implementation_plan': [
                {
                    'category': 'TRANSPORT',
                    'actions': ['Optimiser routes']
                }
            ]
        },
        'performance': {
            'predictions': [
                {
                    'month': '2024-02',
                    'margin': -1000
                }
            ]
        }
    }

@pytest.mark.asyncio
async def test_workflow_comptable_complet(
    client,
    db_session,
    mock_weather_data,
    mock_compte_data,
    mock_ecriture_data,
    mock_ml_data
):
    """Test d'intégration du workflow comptable complet"""
    
    # Mock ML
    with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle') as mock_analyse:
        mock_analyse.return_value = mock_ml_data
        
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
            mock_optimize.return_value = mock_ml_data['optimization']
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
                mock_predict.return_value = mock_ml_data['performance']
                
                # 1. Création d'un compte comptable
                response = client.post('/api/v1/comptabilite/comptes', json=mock_compte_data)
                assert response.status_code == 200
                compte_id = response.json()['id']
                
                # 2. Création d'une écriture comptable
                mock_ecriture_data['compte_id'] = compte_id
                response = client.post('/api/v1/comptabilite/ecritures', json=mock_ecriture_data)
                assert response.status_code == 200
                ecriture_id = response.json()['id']
                
                # 3. Validation de l'écriture
                response = client.post(
                    f'/api/v1/comptabilite/ecritures/{ecriture_id}/valider',
                    json={'validee_par_id': '123e4567-e89b-12d3-a456-426614174002'}
                )
                assert response.status_code == 200
                assert response.json()['statut'] == StatutEcriture.VALIDEE
                
                # 4. Vérification des statistiques avec ML
                response = client.get('/api/v1/comptabilite/stats')
                assert response.status_code == 200
                stats = response.json()
                assert 'revenue' in stats
                assert 'expenses' in stats
                assert 'profit' in stats
                assert 'cashflow' in stats
                assert 'ml_analysis' in stats
                assert 'recommendations' in stats
                
                # 5. Vérification de l'analyse budgétaire avec ML
                response = client.get('/api/v1/comptabilite/budget/analysis', params={'periode': '2024-01'})
                assert response.status_code == 200
                budget = response.json()
                assert 'total_prevu' in budget
                assert 'total_realise' in budget
                assert 'weather_impact' in budget
                assert 'ml_analysis' in budget
                assert 'optimization' in budget
                assert 'recommendations' in budget
                
                # 6. Vérification du cashflow avec ML
                response = client.get('/api/v1/comptabilite/cashflow', params={'days': 30})
                assert response.status_code == 200
                cashflow = response.json()
                assert len(cashflow) == 30
                assert all(key in cashflow[0] for key in [
                    'date', 'entrees', 'sorties', 'solde',
                    'ml_predictions', 'ml_risks', 'impact_meteo'
                ])
                
                # 7. Génération des rapports comptables avec ML
                # Grand Livre
                response = client.get('/api/v1/comptabilite/grand-livre', params={'compte_id': compte_id})
                assert response.status_code == 200
                
                # Balance
                response = client.get('/api/v1/comptabilite/balance')
                assert response.status_code == 200
                
                # Bilan avec ML
                response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
                assert response.status_code == 200
                bilan = response.json()
                assert 'ml_analysis' in bilan
                assert 'recommendations' in bilan
                
                # Compte de résultat avec ML
                response = client.get(
                    '/api/v1/comptabilite/compte-resultat',
                    params={
                        'date_debut': (date.today() - timedelta(days=30)).isoformat(),
                        'date_fin': date.today().isoformat()
                    }
                )
                assert response.status_code == 200
                resultat = response.json()
                assert 'ml_analysis' in resultat
                assert 'optimization' in resultat
                assert 'performance' in resultat
                assert 'recommendations' in resultat

@pytest.mark.asyncio
async def test_integration_ml_comptabilite(client, db_session, mock_ml_data):
    """Test de l'intégration ML dans la comptabilité"""
    
    # Mock ML
    with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle') as mock_analyse:
        mock_analyse.return_value = mock_ml_data
        
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
            mock_optimize.return_value = mock_ml_data['optimization']
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
                mock_predict.return_value = mock_ml_data['performance']
                
                # 1. Vérification ML dans le bilan
                response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
                assert response.status_code == 200
                bilan = response.json()
                
                assert 'ml_analysis' in bilan
                assert len(bilan['recommendations']) > 0
                assert any(rec['type'] == 'ML' for rec in bilan['recommendations'])
                
                # 2. Vérification ML dans le compte de résultat
                response = client.get(
                    '/api/v1/comptabilite/compte-resultat',
                    params={
                        'date_debut': (date.today() - timedelta(days=30)).isoformat(),
                        'date_fin': date.today().isoformat()
                    }
                )
                assert response.status_code == 200
                resultat = response.json()
                
                assert 'ml_analysis' in resultat
                assert 'optimization' in resultat
                assert 'performance' in resultat
                assert len(resultat['recommendations']) > 0
                assert any(rec['type'] == 'ML' for rec in resultat['recommendations'])
                assert any(rec['type'] == 'OPTIMIZATION' for rec in resultat['recommendations'])
                assert any(rec['type'] == 'PERFORMANCE' for rec in resultat['recommendations'])

@pytest.mark.asyncio
async def test_cache_comptabilite(client, db_session):
    """Test du cache dans la comptabilité"""
    
    # Mock cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    
    with patch('services.cache_service.CacheService', return_value=mock_cache):
        # 1. Premier appel - pas de cache
        response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
        assert response.status_code == 200
        assert mock_cache.set.called
        
        # Reset mock
        mock_cache.set.reset_mock()
        
        # 2. Deuxième appel - avec cache
        mock_cache.get.return_value = {"cached": True}
        response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
        assert response.status_code == 200
        assert not mock_cache.set.called
        assert response.json()["cached"]

@pytest.mark.asyncio
async def test_invalidation_cache(client, db_session, mock_compte_data):
    """Test de l'invalidation du cache"""
    
    # Mock cache
    mock_cache = Mock()
    mock_cache.get.return_value = None
    
    with patch('services.cache_service.CacheService', return_value=mock_cache):
        # 1. Création compte - doit invalider le cache
        response = client.post('/api/v1/comptabilite/comptes', json=mock_compte_data)
        assert response.status_code == 200
        assert mock_cache.delete_pattern.called
        
        patterns_invalides = [pattern[0][0] for pattern in mock_cache.delete_pattern.call_args_list]
        assert "grand_livre_*" in patterns_invalides
        assert "balance_*" in patterns_invalides
        assert "bilan_*" in patterns_invalides
        assert "resultat_*" in patterns_invalides

@pytest.mark.asyncio
async def test_integration_meteo_comptabilite(client, db_session, mock_weather_data):
    """Test de l'intégration entre la météo et la comptabilité"""
    
    # 1. Vérification de l'impact météo sur le budget
    response = client.get('/api/v1/comptabilite/budget/analysis', params={'periode': '2024-01'})
    assert response.status_code == 200
    budget = response.json()
    
    weather_impact = budget['weather_impact']
    assert weather_impact['score'] > 0
    assert len(weather_impact['factors']) > 0
    assert len(weather_impact['projections']) > 0
    
    # 2. Vérification de l'impact météo sur le cashflow
    response = client.get('/api/v1/comptabilite/cashflow', params={'days': 1})
    assert response.status_code == 200
    cashflow = response.json()
    
    assert len(cashflow) == 1
    assert cashflow[0]['impact_meteo'] > 0
    assert 'ml_predictions' in cashflow[0]
    assert 'ml_risks' in cashflow[0]

@pytest.mark.asyncio
async def test_coherence_donnees_comptables(client, db_session, mock_ml_data):
    """Test de la cohérence des données comptables avec ML"""
    
    # Mock ML
    with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.get_analyse_parcelle') as mock_analyse:
        mock_analyse.return_value = mock_ml_data
        
        with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.optimize_costs') as mock_optimize:
            mock_optimize.return_value = mock_ml_data['optimization']
            
            with patch('services.finance_comptabilite.analyse.AnalyseFinanceCompta.predict_performance') as mock_predict:
                mock_predict.return_value = mock_ml_data['performance']
                
                # 1. Vérification de la balance
                response = client.get('/api/v1/comptabilite/balance')
                assert response.status_code == 200
                balance = response.json()
                
                total_debit = sum(compte['debit'] for compte in balance)
                total_credit = sum(compte['credit'] for compte in balance)
                assert total_debit == total_credit
                
                # 2. Vérification du bilan avec ML
                response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
                assert response.status_code == 200
                bilan = response.json()
                
                assert bilan['total_actif'] == bilan['total_passif']
                assert 'ml_analysis' in bilan
                assert len(bilan['recommendations']) > 0
                
                # 3. Vérification du compte de résultat avec ML
                response = client.get(
                    '/api/v1/comptabilite/compte-resultat',
                    params={
                        'date_debut': (date.today() - timedelta(days=30)).isoformat(),
                        'date_fin': date.today().isoformat()
                    }
                )
                assert response.status_code == 200
                compte_resultat = response.json()
                
                # Vérification résultat net
                assert compte_resultat['resultat_net'] == compte_resultat['total_produits'] - compte_resultat['total_charges']
                
                # Vérification ML
                assert 'ml_analysis' in compte_resultat
                assert 'optimization' in compte_resultat
                assert 'performance' in compte_resultat
                assert len(compte_resultat['recommendations']) > 0
                
                # 4. Vérification des statistiques avec ML
                response = client.get('/api/v1/comptabilite/stats')
                assert response.status_code == 200
                stats = response.json()
                
                # Vérification profit
                assert stats['profit'] == stats['revenue'] - stats['expenses']
                
                # Vérification ML
                assert 'ml_analysis' in stats
                assert 'recommendations' in stats
                assert len(stats['recommendations']) > 0
