# Guide de Maintenance des Tests

## Vue d'ensemble

Ce guide détaille les procédures et bonnes pratiques pour maintenir la suite de tests FOFAL ERP en bon état.

## Maintenance Régulière

### 1. Vérification de la Couverture
```bash
# Génération du rapport de couverture
pytest --cov=app --cov-report=html

# Vérification des seuils minimaux
pytest --cov=app --cov-fail-under=80
```

### 2. Optimisation des Tests
```python
# ✅ Bon : Utilisation efficace des fixtures
@pytest.fixture(scope="session")
def db_engine():
    """Crée une seule instance de l'engine pour la session."""
    return create_test_engine()

# ❌ Mauvais : Création répétée de ressources
def test_something():
    engine = create_test_engine()  # Création inutile à chaque test
```

### 3. Nettoyage des Tests
```python
# ✅ Bon : Nettoyage explicite
def test_with_cleanup(db_session):
    try:
        # Test logic
        pass
    finally:
        db_session.rollback()
        cleanup_test_data()

# ❌ Mauvais : Pas de nettoyage
def test_without_cleanup(db_session):
    # Test logic
    pass  # Risque de pollution des données
```

## Mise à Jour des Tests

### 1. Lors des Changements de Code
```python
# Avant le changement
def test_original_feature():
    result = calculate_total(10, 20)
    assert result == 30

# Après l'ajout d'un paramètre optionnel
def test_feature_with_new_param():
    # Test du cas original
    result = calculate_total(10, 20)
    assert result == 30
    
    # Test avec le nouveau paramètre
    result_with_tax = calculate_total(10, 20, tax_rate=0.2)
    assert result_with_tax == 36
```

### 2. Lors des Changements d'API
```python
# Mise à jour des mocks
@pytest.fixture
def updated_api_response():
    """Mock de la nouvelle structure de réponse API."""
    return {
        "data": {
            "value": 100,
            "metadata": {  # Nouveau champ
                "timestamp": "2024-01-01T00:00:00Z"
            }
        }
    }

# Mise à jour des tests
def test_api_integration(client, updated_api_response):
    response = client.get("/api/data")
    assert response.status_code == 200
    assert "metadata" in response.json()["data"]
```

## Monitoring des Tests

### 1. Performance
```python
# pytest.ini
[pytest]
junit_family = xunit2
junit_duration_report = call

# Exécution avec mesure du temps
pytest --durations=10 --durations-min=1.0
```

### 2. Logs et Rapports
```python
# conftest.py
import logging

@pytest.fixture(autouse=True)
def setup_logging():
    """Configure les logs pour les tests."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename='test.log'
    )

# Usage dans les tests
def test_with_logging(caplog):
    with caplog.at_level(logging.INFO):
        # Test logic
        assert "Expected log message" in caplog.text
```

## Gestion des Tests Flaky

### 1. Identification
```python
# Marquage des tests instables
@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_unstable_feature():
    """Test qui peut échouer de manière aléatoire."""
    result = unstable_operation()
    assert result.status == "success"
```

### 2. Stabilisation
```python
# ✅ Bon : Attentes explicites
@pytest.mark.asyncio
async def test_with_proper_wait():
    await asyncio.sleep(0.1)  # Attente explicite
    result = await async_operation()
    assert result.is_ready

# ❌ Mauvais : Timing arbitraire
time.sleep(1)  # Attente arbitraire
```

## Documentation des Tests

### 1. Documentation des Fixtures
```python
@pytest.fixture
def complex_fixture():
    """
    Fixture pour les tests de fonctionnalités complexes.
    
    Crée:
    - Une base de données de test
    - Des données de test
    - Des mocks des services externes
    
    Nettoie:
    - Les données de test
    - Les connexions de base de données
    - Les mocks
    """
    # Setup
    db = setup_test_db()
    data = create_test_data()
    mocks = setup_mocks()
    
    yield db, data, mocks
    
    # Cleanup
    cleanup_test_data()
    cleanup_db(db)
    cleanup_mocks(mocks)
```

### 2. Documentation des Tests Complexes
```python
def test_complex_workflow():
    """
    Test du workflow complet de traitement des commandes.
    
    Étapes:
    1. Création des données initiales
       - Produits
       - Client
       - Stock
    
    2. Exécution du workflow
       - Création de la commande
       - Validation du stock
       - Traitement du paiement
       - Mise à jour du stock
    
    3. Vérifications
       - État de la commande
       - Niveau de stock
       - Transactions financières
       - Notifications client
    
    Dépendances:
    - Base de données de test
    - Service de paiement mock
    - Service de notification mock
    """
```

## Maintenance Préventive

### 1. Revue de Code
- Vérifier la couverture des nouveaux tests
- Valider les assertions
- Vérifier le nettoyage des ressources
- Examiner la documentation

### 2. Automatisation
```yaml
# .github/workflows/tests.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: |
          pytest --cov=app
          pytest --dead-fixtures
          pytest --durations=10
```

### 3. Monitoring Continu
- Surveiller les temps d'exécution
- Identifier les tests flaky
- Vérifier l'utilisation des ressources
- Analyser les tendances d'échec

## Bonnes Pratiques

### 1. Organisation
- Maintenir une structure claire
- Documenter les changements
- Nettoyer les tests obsolètes
- Mettre à jour les fixtures

### 2. Performance
- Optimiser les fixtures lourdes
- Paralléliser quand possible
- Minimiser les E/S
- Gérer efficacement les ressources

### 3. Qualité
- Maintenir les standards de code
- Revoir régulièrement les tests
- Mettre à jour la documentation
- Former l'équipe aux bonnes pratiques
