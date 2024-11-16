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

@pytest.mark.asyncio
async def test_workflow_comptable_complet(
    client,
    db_session,
    mock_weather_data,
    mock_compte_data,
    mock_ecriture_data
):
    """Test d'intégration du workflow comptable complet"""
    
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
    
    # 4. Vérification des statistiques
    response = client.get('/api/v1/comptabilite/stats')
    assert response.status_code == 200
    stats = response.json()
    assert 'revenue' in stats
    assert 'expenses' in stats
    assert 'profit' in stats
    assert 'cashflow' in stats
    
    # 5. Vérification de l'analyse budgétaire
    response = client.get('/api/v1/comptabilite/budget/analysis', params={'periode': '2024-01'})
    assert response.status_code == 200
    budget = response.json()
    assert 'total_prevu' in budget
    assert 'total_realise' in budget
    assert 'weather_impact' in budget
    
    # 6. Vérification du cashflow
    response = client.get('/api/v1/comptabilite/cashflow', params={'days': 30})
    assert response.status_code == 200
    cashflow = response.json()
    assert len(cashflow) == 30
    assert all(key in cashflow[0] for key in ['date', 'entrees', 'sorties', 'solde', 'prevision', 'impact_meteo'])
    
    # 7. Génération des rapports comptables
    # Grand Livre
    response = client.get('/api/v1/comptabilite/grand-livre', params={'compte_id': compte_id})
    assert response.status_code == 200
    
    # Balance
    response = client.get('/api/v1/comptabilite/balance')
    assert response.status_code == 200
    
    # Bilan
    response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
    assert response.status_code == 200
    
    # Compte de résultat
    response = client.get(
        '/api/v1/comptabilite/compte-resultat',
        params={
            'date_debut': (date.today() - timedelta(days=30)).isoformat(),
            'date_fin': date.today().isoformat()
        }
    )
    assert response.status_code == 200

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
    assert cashflow[0]['prevision'] != cashflow[0]['solde']

@pytest.mark.asyncio
async def test_coherence_donnees_comptables(client, db_session):
    """Test de la cohérence des données comptables"""
    
    # 1. Vérification de la balance
    response = client.get('/api/v1/comptabilite/balance')
    assert response.status_code == 200
    balance = response.json()
    
    total_debit = sum(compte['debit'] for compte in balance)
    total_credit = sum(compte['credit'] for compte in balance)
    assert total_debit == total_credit
    
    # 2. Vérification du bilan
    response = client.get('/api/v1/comptabilite/bilan', params={'date_fin': date.today().isoformat()})
    assert response.status_code == 200
    bilan = response.json()
    
    assert bilan['total_actif'] == bilan['total_passif']
    
    # 3. Vérification de la cohérence entre les différents rapports
    # Compte de résultat
    response = client.get(
        '/api/v1/comptabilite/compte-resultat',
        params={
            'date_debut': (date.today() - timedelta(days=30)).isoformat(),
            'date_fin': date.today().isoformat()
        }
    )
    assert response.status_code == 200
    compte_resultat = response.json()
    
    # Vérification que le résultat net correspond à la différence entre produits et charges
    assert compte_resultat['resultat_net'] == compte_resultat['total_produits'] - compte_resultat['total_charges']
    
    # 4. Vérification des statistiques
    response = client.get('/api/v1/comptabilite/stats')
    assert response.status_code == 200
    stats = response.json()
    
    # Le profit doit correspondre à la différence entre revenus et dépenses
    assert stats['profit'] == stats['revenue'] - stats['expenses']
