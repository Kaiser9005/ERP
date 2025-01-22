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
from services.finance_comptabilite.analyse import AnalyseFinanceCompta

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

class TestAnalyseFinanceComptaService:
    """Tests d'intégration du service d'analyse financière"""

    async def test_calculer_rentabilite_parcelle(self, db_session):
        """Test du calcul de rentabilité d'une parcelle"""
        # Setup
        service = AnalyseFinanceCompta(db_session)
        parcelle = Mock(id=1)
        
        cycles = [
            Mock(
                produits_totaux=150000.0,
                charges_totales=100000.0
            ),
            Mock(
                produits_totaux=120000.0,
                charges_totales=90000.0
            )
        ]
        db_session.query().filter().all.return_value = cycles

        # Exécution
        result = await service._calculer_rentabilite_parcelle(
            parcelle=parcelle,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=180),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result["produits"] == 270000.0  # 150000 + 120000
        assert result["charges"] == 190000.0  # 100000 + 90000
        assert result["marge"] == 80000.0  # 270000 - 190000
        assert result["rentabilite"] == pytest.approx(42.11, 0.01)  # (80000 / 190000) * 100

    async def test_generer_recommendations_rentabilite_negative(self, db_session):
        """Test des recommandations avec rentabilité négative"""
        # Setup
        service = AnalyseFinanceCompta(db_session)
        parcelle = Mock(id=1)
        rentabilite = {
            "produits": 100000.0,
            "charges": 150000.0,
            "marge": -50000.0,
            "rentabilite": -33.33
        }

        # Exécution
        recommendations = await service._generer_recommendations(
            parcelle=parcelle,
            rentabilite=rentabilite
        )

        # Vérifications
        assert len(recommendations) == 2
        assert any("Rentabilité négative" in r for r in recommendations)
        assert any("Charges élevées" in r for r in recommendations)

    async def test_generer_recommendations_rentabilite_faible(self, db_session):
        """Test des recommandations avec rentabilité faible"""
        # Setup
        service = AnalyseFinanceCompta(db_session)
        parcelle = Mock(id=1)
        rentabilite = {
            "produits": 100000.0,
            "charges": 95000.0,
            "marge": 5000.0,
            "rentabilite": 5.26
        }

        # Exécution
        recommendations = await service._generer_recommendations(
            parcelle=parcelle,
            rentabilite=rentabilite
        )

        # Vérifications
        assert len(recommendations) == 2
        assert any("Rentabilité faible" in r for r in recommendations)
        assert any("Charges élevées" in r for r in recommendations)

    async def test_get_analyse_parcelle_not_found(self, db_session):
        """Test de l'analyse d'une parcelle inexistante"""
        # Setup
        service = AnalyseFinanceCompta(db_session)
        db_session.query().get.return_value = None

        # Exécution
        result = await service.get_analyse_parcelle(
            parcelle_id=999,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == {}

    async def test_get_analyse_parcelle_cache(self, db_session):
        """Test du cache pour l'analyse de parcelle"""
        # Setup
        service = AnalyseFinanceCompta(db_session)
        mock_cache = Mock()
        mock_cache.get.return_value = {"cached": True}
        service.cache = mock_cache

        # Exécution
        result = await service.get_analyse_parcelle(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result["cached"]

class TestGestionCoutsService:
    """Tests d'intégration du service de gestion des coûts"""

    async def test_get_couts_parcelle(self, db_session):
        """Test de récupération des coûts d'une parcelle"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        
        parcelle = Mock(id=1)
        db_session.query().get.return_value = parcelle
        
        ecritures = [
            Mock(
                compte=Mock(type="CHARGE", categorie="INTRANT"),
                montant=1000.0
            ),
            Mock(
                compte=Mock(type="CHARGE", categorie="INTRANT"),
                montant=500.0
            ),
            Mock(
                compte=Mock(type="CHARGE", categorie="TRANSPORT"),
                montant=300.0
            ),
            Mock(
                compte=Mock(type="PRODUIT", categorie="VENTE"),
                montant=2000.0  # Ne devrait pas être compté
            )
        ]
        db_session.query().filter().all.return_value = ecritures

        # Exécution
        result = await service._get_couts_parcelle(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=30),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert "couts_par_categorie" in result
        assert "total" in result
        assert "date_calcul" in result
        assert result["couts_par_categorie"]["INTRANT"] == 1500.0
        assert result["couts_par_categorie"]["TRANSPORT"] == 300.0
        assert result["total"] == 1800.0

    async def test_get_couts_parcelle_not_found(self, db_session):
        """Test avec parcelle inexistante"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        db_session.query().get.return_value = None

        # Exécution
        result = await service._get_couts_parcelle(
            parcelle_id=999,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == {}

    async def test_get_compte_charge(self, db_session):
        """Test de récupération d'un compte de charge"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        
        compte = Mock(code="601000", type="CHARGE")
        db_session.query().filter().first.return_value = compte

        # Exécution
        result = await service._get_compte_charge("601000")

        # Vérifications
        assert result == compte

    async def test_calculer_couts_directs(self, db_session):
        """Test du calcul des coûts directs"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        
        parcelle = Mock(id=1)
        ecritures = [
            Mock(
                compte=Mock(type="CHARGE"),
                montant=1000.0
            ),
            Mock(
                compte=Mock(type="CHARGE"),
                montant=500.0
            ),
            Mock(
                compte=Mock(type="PRODUIT"),
                montant=2000.0  # Ne devrait pas être compté
            )
        ]
        db_session.query().filter().all.return_value = ecritures

        # Exécution
        result = await service._calculer_couts_directs(
            parcelle=parcelle,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=30),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == 1500.0

    async def test_calculer_cle_repartition(self, db_session):
        """Test du calcul de la clé de répartition"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        
        # Simuler 4 parcelles
        db_session.query().count.return_value = 4

        # Exécution
        result = await service._calculer_cle_repartition(
            parcelle=Mock(id=1),
            date=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == 0.25  # 1/4

    async def test_calculer_cle_repartition_no_parcelles(self, db_session):
        """Test du calcul de la clé de répartition sans parcelles"""
        # Setup
        from services.finance_comptabilite.couts import GestionCouts
        service = GestionCouts(db_session)
        
        db_session.query().count.return_value = 0

        # Exécution
        result = await service._calculer_cle_repartition(
            parcelle=Mock(id=1),
            date=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == 0

class TestGestionMeteoService:
    """Tests d'intégration du service de gestion météorologique"""

    async def test_get_meteo_impact(self, db_session):
        """Test du calcul de l'impact météorologique"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        parcelle = Mock(
            id=1,
            latitude=48.8566,
            longitude=2.3522,
            surface=10000.0  # 1 hectare
        )
        db_session.query().get.return_value = parcelle
        
        # Mock WeatherService
        service.weather_service.get_historical_data = Mock(
            return_value={
                "precipitation": 45.0,
                "temperature": 28.0,
                "humidity": 75.0
            }
        )

        # Exécution
        result = await service._get_meteo_impact(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=30),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert "score" in result
        assert "facteurs" in result
        assert "couts_additionnels" in result
        assert "risques" in result
        assert "opportunites" in result
        assert len(result["facteurs"]) == 3  # precipitation, temperature, humidity

    async def test_calculer_provision_meteo(self, db_session):
        """Test du calcul de la provision météorologique"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        parcelle = Mock(
            id=1,
            surface=10000.0,
            latitude=48.8566,
            longitude=2.3522
        )
        db_session.query().get.return_value = parcelle
        
        # Mock WeatherService
        service.weather_service.get_historical_data = Mock(
            return_value={
                "precipitation": 60.0,  # Conditions défavorables
                "temperature": 32.0,
                "humidity": 85.0
            }
        )

        # Exécution
        provision = await service._calculer_provision_meteo(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=30),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert provision > 0  # Provision nécessaire vu les conditions
        assert isinstance(provision, float)

    async def test_analyser_facteurs_meteo(self, db_session):
        """Test de l'analyse des facteurs météorologiques"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        meteo_data = {
            "precipitation": 5.0,  # Trop sec
            "temperature": 38.0,   # Trop chaud
            "humidity": 25.0       # Trop sec
        }

        # Exécution
        facteurs = service._analyser_facteurs_meteo(meteo_data)

        # Vérifications
        assert len(facteurs) == 3
        assert all("impact" in f for f in facteurs)
        assert all("type" in f for f in facteurs)
        assert all("valeur" in f for f in facteurs)
        
        # Vérification des impacts négatifs
        assert all(f["impact"] > 0 for f in facteurs)  # Conditions défavorables

    async def test_evaluer_risques_opportunites(self, db_session):
        """Test de l'évaluation des risques et opportunités"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        facteurs = [
            {"type": "precipitation", "impact": 0.8},  # Risque élevé
            {"type": "temperature", "impact": -0.4},   # Opportunité
            {"type": "humidity", "impact": 0.5}        # Neutre
        ]

        # Exécution
        risques, opportunites = service._evaluer_risques_opportunites(facteurs)

        # Vérifications
        assert len(risques) == 1
        assert len(opportunites) == 1
        assert "precipitation" in risques[0]
        assert "temperature" in opportunites[0]

    async def test_calculer_couts_meteo(self, db_session):
        """Test du calcul des coûts météorologiques"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        parcelle = Mock(surface=10000.0)  # 1 hectare
        facteurs = [
            {"type": "precipitation", "impact": 0.8, "valeur": 60.0},
            {"type": "temperature", "impact": 0.9, "valeur": 35.0},
            {"type": "humidity", "impact": 0.7, "valeur": 85.0}
        ]

        # Exécution
        couts = service._calculer_couts_meteo(parcelle, facteurs)

        # Vérifications
        assert "drainage" in couts
        assert "protection" in couts
        assert "ventilation" in couts
        assert all(cout > 0 for cout in couts.values())

    async def test_get_meteo_impact_not_found(self, db_session):
        """Test avec parcelle inexistante"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        db_session.query().get.return_value = None

        # Exécution
        result = await service._get_meteo_impact(
            parcelle_id=999,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result == {}

    async def test_get_meteo_impact_no_weather_data(self, db_session):
        """Test sans données météo"""
        # Setup
        from services.finance_comptabilite.meteo import GestionMeteo
        service = GestionMeteo(db_session)
        
        parcelle = Mock(id=1, latitude=48.8566, longitude=2.3522)
        db_session.query().get.return_value = parcelle
        
        # Mock WeatherService sans données
        service.weather_service.get_historical_data = Mock(return_value=None)

        # Exécution
        result = await service._get_meteo_impact(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result["score"] == 0
        assert len(result["facteurs"]) == 0
        assert len(result["couts_additionnels"]) == 0
        assert len(result["risques"]) == 0
        assert len(result["opportunites"]) == 0

class TestGestionClotureService:
    """Tests d'intégration du service de clôture comptable"""

    async def test_executer_cloture_mensuelle_success(self, db_session):
        """Test d'une clôture mensuelle réussie"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(
            id=1,
            annee=2024,
            statut="OUVERT",
            periodes_status={}
        )
        db_session.query().get.return_value = exercice
        
        # Mock des conditions de clôture
        service._verifier_conditions_cloture = Mock(
            return_value={"peut_cloturer": True, "message": "OK"}
        )
        service._valider_ecritures_attente = Mock(
            return_value={"success": True, "message": "OK"}
        )
        service._calculer_totaux_mensuels = Mock(
            return_value={"CHARGE": 1000.0, "PRODUIT": -1000.0}
        )
        service._generer_ecritures_cloture = Mock(
            return_value=[
                {"type": "CHARGE", "montant": -1000.0},
                {"type": "PRODUIT", "montant": 1000.0}
            ]
        )

        # Exécution
        result = await service.executer_cloture_mensuelle(1, 1)  # Janvier

        # Vérifications
        assert result["status"] == "success"
        assert "totaux" in result
        assert "ecritures_cloture" in result
        assert "date_cloture" in result

    async def test_verifier_conditions_cloture(self, db_session):
        """Test de vérification des conditions de clôture"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(
            id=1,
            statut="OUVERT"
        )
        
        # Pas d'écritures en attente
        db_session.query().filter().count.return_value = 0
        
        # Mock de l'équilibre des comptes
        service._verifier_equilibre_comptes = Mock(return_value=True)

        # Exécution
        result = await service._verifier_conditions_cloture(exercice, 1)

        # Vérifications
        assert result["peut_cloturer"] is True
        assert result["message"] == "OK"

    async def test_verifier_conditions_cloture_exercice_cloture(self, db_session):
        """Test avec exercice déjà clôturé"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(
            id=1,
            statut="CLOTURE"
        )

        # Exécution
        result = await service._verifier_conditions_cloture(exercice, 1)

        # Vérifications
        assert result["peut_cloturer"] is False
        assert "déjà clôturé" in result["message"]

    async def test_valider_ecritures_attente(self, db_session):
        """Test de validation des écritures en attente"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(id=1)
        ecritures = [
            Mock(statut="ATTENTE"),
            Mock(statut="ATTENTE")
        ]
        db_session.query().filter().all.return_value = ecritures

        # Exécution
        result = await service._valider_ecritures_attente(exercice, 1)

        # Vérifications
        assert result["success"] is True
        assert "2 écritures validées" in result["message"]
        assert all(e.statut == "VALIDE" for e in ecritures)
        assert db_session.commit.called

    async def test_calculer_totaux_mensuels(self, db_session):
        """Test du calcul des totaux mensuels"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(id=1)
        ecritures = [
            Mock(compte=Mock(type="CHARGE"), montant=1000.0),
            Mock(compte=Mock(type="CHARGE"), montant=500.0),
            Mock(compte=Mock(type="PRODUIT"), montant=-2000.0)
        ]
        db_session.query().filter().all.return_value = ecritures

        # Exécution
        totaux = await service._calculer_totaux_mensuels(exercice, 1)

        # Vérifications
        assert totaux["CHARGE"] == 1500.0
        assert totaux["PRODUIT"] == -2000.0

    async def test_generer_ecritures_cloture(self, db_session):
        """Test de génération des écritures de clôture"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(id=1, annee=2024)
        totaux = {
            "CHARGE": 1000.0,
            "PRODUIT": -1000.0
        }
        
        # Mock des comptes et journal de clôture
        compte_cloture = Mock(id=1)
        journal_cloture = Mock(id=1)
        service._get_compte_cloture = Mock(return_value=compte_cloture)
        service._get_journal_cloture = Mock(return_value=journal_cloture)

        # Exécution
        ecritures = await service._generer_ecritures_cloture(exercice, 1, totaux)

        # Vérifications
        assert len(ecritures) == 2
        assert any(e["type"] == "CHARGE" and e["montant"] == -1000.0 for e in ecritures)
        assert any(e["type"] == "PRODUIT" and e["montant"] == 1000.0 for e in ecritures)
        assert db_session.commit.called

    async def test_verifier_equilibre_comptes(self, db_session):
        """Test de vérification de l'équilibre des comptes"""
        # Setup
        from services.finance_comptabilite.cloture import GestionCloture
        service = GestionCloture(db_session)
        
        exercice = Mock(id=1)
        service._calculer_totaux_mensuels = Mock(
            return_value={
                "CHARGE": 1000.0,
                "PRODUIT": -1000.0
            }
        )

        # Exécution
        equilibre = await service._verifier_equilibre_comptes(exercice, 1)

        # Vérifications
        assert equilibre is True

class TestGestionIoTService:
    """Tests d'intégration du service de gestion IoT"""

    async def test_get_iot_analysis(self, db_session):
        """Test de l'analyse IoT complète"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)
        
        parcelle = Mock(id=1)
        db_session.query().get.return_value = parcelle
        
        capteurs = [
            Mock(
                id=1,
                type="temperature",
                parcelle_id=1
            ),
            Mock(
                id=2,
                type="humidity",
                parcelle_id=1
            )
        ]
        db_session.query().filter().all.return_value = capteurs

        lectures = [
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc),
                value=25.0
            ),
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc) + timedelta(hours=1),
                value=26.0
            ),
            Mock(
                sensor=Mock(type="humidity"),
                timestamp=datetime.now(datetime.timezone.utc),
                value=60.0
            )
        ]
        db_session.query().filter().all.side_effect = [capteurs, lectures]

        # Exécution
        result = await service._get_iot_analysis(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc) - timedelta(days=1),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result["status"] == "ok"
        assert "alertes" in result
        assert "tendances" in result
        assert "recommandations" in result
        assert "date_analyse" in result

    async def test_get_iot_analysis_no_sensors(self, db_session):
        """Test sans capteurs IoT"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)
        
        parcelle = Mock(id=1)
        db_session.query().get.return_value = parcelle
        db_session.query().filter().all.return_value = []

        # Exécution
        result = await service._get_iot_analysis(
            parcelle_id=1,
            date_debut=datetime.now(datetime.timezone.utc),
            date_fin=datetime.now(datetime.timezone.utc)
        )

        # Vérifications
        assert result["status"] == "no_sensors"
        assert len(result["alertes"]) == 0
        assert len(result["tendances"]) == 0
        assert len(result["recommandations"]) == 0

    async def test_analyser_tendance(self, db_session):
        """Test de l'analyse des tendances"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)
        
        lectures = [
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc),
                value=25.0
            ),
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc) + timedelta(hours=1),
                value=26.0
            ),
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc) + timedelta(hours=2),
                value=27.0
            )
        ]

        # Exécution
        tendances = await service._analyser_tendance(lectures)

        # Vérifications
        assert "temperature" in tendances
        assert "moyenne" in tendances["temperature"]
        assert "min" in tendances["temperature"]
        assert "max" in tendances["temperature"]
        assert "ecart_type" in tendances["temperature"]
        assert "tendance" in tendances["temperature"]
        assert tendances["temperature"]["tendance"] > 0  # Tendance à la hausse

    async def test_generer_alertes_iot(self, db_session):
        """Test de la génération des alertes"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)
        
        lectures = [
            Mock(
                sensor=Mock(type="temperature"),
                timestamp=datetime.now(datetime.timezone.utc),
                value=40.0  # Au-dessus du seuil max (35.0)
            )
        ]
        
        tendances = {
            "temperature": {
                "max": 40.0,
                "min": 40.0,
                "moyenne": 40.0,
                "ecart_type": 0.0,
                "tendance": 0.0
            }
        }

        # Exécution
        alertes = await service._generer_alertes_iot(lectures, tendances)

        # Vérifications
        assert len(alertes) == 1
        assert alertes[0]["type"] == "extreme_high"
        assert alertes[0]["capteur"] == "temperature"
        assert alertes[0]["priorite"] == "haute"

    def test_generer_recommandations(self, db_session):
        """Test de la génération des recommandations"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)
        
        tendances = {
            "temperature": {
                "ecart_type": 3.0  # Au-dessus du seuil de variation (2.0)
            }
        }
        
        alertes = [
            {
                "type": "extreme_high",
                "capteur": "temperature",
                "valeur": 40.0,
                "seuil": 35.0,
                "priorite": "haute"
            }
        ]

        # Exécution
        recommandations = service._generer_recommandations(tendances, alertes)

        # Vérifications
        assert len(recommandations) == 2
        assert any("Réduire les niveaux de temperature" in r for r in recommandations)
        assert any("Stabiliser les variations de temperature" in r for r in recommandations)

    def test_get_seuils(self, db_session):
        """Test des méthodes de seuils"""
        # Setup
        from services.finance_comptabilite.iot import GestionIoT
        service = GestionIoT(db_session)

        # Exécution & Vérifications
        assert service._get_seuil_max("temperature") == 35.0
        assert service._get_seuil_min("temperature") == 5.0
        assert service._get_seuil_tendance("temperature") == 0.5
        assert service._get_seuil_variation("temperature") == 2.0

        # Test avec type de capteur inconnu
        assert service._get_seuil_max("unknown") == float('inf')
        assert service._get_seuil_min("unknown") == float('-inf')
        assert service._get_seuil_tendance("unknown") == 1.0
        assert service._get_seuil_variation("unknown") == 2.0
