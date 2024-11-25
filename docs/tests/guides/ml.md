# Guide des Tests Machine Learning

## Vue d'ensemble

Ce guide détaille les bonnes pratiques et standards pour les tests des composants Machine Learning de l'ERP FOFAL.

## Types de Tests ML

### 1. Tests Unitaires
- Validation des transformations de données
- Tests des fonctions d'évaluation
- Vérification des prétraitements

### 2. Tests d'Intégration
- Workflow complet d'entraînement
- Pipeline de prédiction
- Intégration avec les services externes

### 3. Tests de Performance
- Temps d'inférence
- Utilisation mémoire
- Scalabilité

### 4. Tests de Qualité
- Métriques de performance
- Validation croisée
- Tests de robustesse

## Structure des Tests ML

### Configuration de Base
```python
import pytest
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

@pytest.fixture
def test_data():
    """Fixture pour les données de test."""
    return {
        "X_train": np.random.rand(100, 10),
        "y_train": np.random.rand(100),
        "X_test": np.random.rand(20, 10),
        "y_test": np.random.rand(20)
    }

@pytest.fixture
def model_config():
    """Configuration du modèle pour les tests."""
    return {
        "learning_rate": 0.01,
        "max_depth": 5,
        "n_estimators": 100
    }
```

### Tests de Modèle
```python
def test_model_training(test_data, model_config):
    """Test l'entraînement du modèle."""
    model = MLModel(model_config)
    model.fit(test_data["X_train"], test_data["y_train"])
    
    # Vérification des prédictions
    predictions = model.predict(test_data["X_test"])
    assert len(predictions) == len(test_data["y_test"])
    
    # Vérification des métriques
    metrics = model.evaluate(test_data["X_test"], test_data["y_test"])
    assert metrics["mae"] < 0.5
    assert metrics["rmse"] < 0.7
    assert metrics["r2"] > 0.6

def test_model_persistence(test_data, model_config, tmp_path):
    """Test la sauvegarde et le chargement du modèle."""
    model = MLModel(model_config)
    model.fit(test_data["X_train"], test_data["y_train"])
    
    # Sauvegarde
    model_path = tmp_path / "model.pkl"
    model.save(model_path)
    
    # Chargement
    loaded_model = MLModel.load(model_path)
    
    # Vérification des prédictions identiques
    orig_preds = model.predict(test_data["X_test"])
    loaded_preds = loaded_model.predict(test_data["X_test"])
    np.testing.assert_array_almost_equal(orig_preds, loaded_preds)
```

### Tests de Pipeline
```python
def test_preprocessing_pipeline():
    """Test du pipeline de prétraitement."""
    pipeline = PreprocessingPipeline()
    
    # Données brutes
    raw_data = pd.DataFrame({
        "numeric": [1, 2, np.nan, 4],
        "categorical": ["A", "B", None, "A"]
    })
    
    # Application du pipeline
    processed = pipeline.transform(raw_data)
    
    # Vérifications
    assert not processed.isnull().any().any()
    assert "numeric_scaled" in processed.columns
    assert set(processed["categorical_encoded"].unique()) == {0, 1}

def test_feature_engineering():
    """Test de la création de features."""
    engineer = FeatureEngineer()
    
    # Données d'entrée
    data = pd.DataFrame({
        "date": pd.date_range("2024-01-01", periods=5),
        "value": [1, 2, 3, 4, 5]
    })
    
    # Création des features
    features = engineer.create_features(data)
    
    # Vérifications
    assert "day_of_week" in features.columns
    assert "month" in features.columns
    assert "value_lag1" in features.columns
```

## Standards de Test ML

### 1. Tests de Données
```python
def test_data_quality():
    """Test de la qualité des données."""
    data = load_training_data()
    
    # Vérification des valeurs manquantes
    assert data.isnull().sum().sum() == 0
    
    # Vérification des types de données
    assert data["numeric_col"].dtype == np.float64
    assert data["categorical_col"].dtype == "category"
    
    # Vérification des valeurs aberrantes
    z_scores = stats.zscore(data["numeric_col"])
    assert np.abs(z_scores).max() < 4

def test_data_splits():
    """Test des splits de données."""
    X, y = prepare_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Vérification des proportions
    assert len(X_train) == 0.8 * len(X)
    assert len(X_test) == 0.2 * len(X)
    
    # Vérification de la distribution
    assert np.mean(y_train) == pytest.approx(np.mean(y), rel=0.1)
    assert np.std(y_train) == pytest.approx(np.std(y), rel=0.1)
```

### 2. Tests de Performance
```python
def test_inference_time():
    """Test du temps d'inférence."""
    model = load_trained_model()
    X = generate_test_data(1000)
    
    # Mesure du temps d'inférence
    start_time = time.time()
    predictions = model.predict(X)
    inference_time = time.time() - start_time
    
    # Vérification du temps d'inférence
    assert inference_time < 0.1  # 100ms max
    
    # Vérification de la mémoire
    memory_usage = get_model_memory_usage(model)
    assert memory_usage < 100  # 100MB max

def test_model_scalability():
    """Test de la scalabilité du modèle."""
    model = MLModel()
    
    # Test avec différentes tailles de données
    for size in [100, 1000, 10000]:
        X = generate_test_data(size)
        
        # Mesure du temps d'entraînement
        start_time = time.time()
        model.fit(X)
        training_time = time.time() - start_time
        
        # Vérification de la scalabilité linéaire
        assert training_time < size * 0.001  # 1ms par exemple
```

### 3. Tests de Robustesse
```python
def test_model_robustness():
    """Test de la robustesse du modèle."""
    model = load_trained_model()
    X = generate_test_data()
    
    # Test avec bruit
    X_noisy = add_noise(X, std=0.1)
    pred_orig = model.predict(X)
    pred_noisy = model.predict(X_noisy)
    
    # Vérification de la stabilité
    assert np.mean(np.abs(pred_orig - pred_noisy)) < 0.2
    
    # Test avec valeurs manquantes
    X_missing = introduce_missing_values(X, ratio=0.1)
    pred_missing = model.predict(X_missing)
    assert not np.any(np.isnan(pred_missing))
```

## Bonnes Pratiques

### 1. Reproductibilité
- Fixer les seeds aléatoires
- Documenter les versions des dépendances
- Sauvegarder les états intermédiaires

### 2. Données de Test
- Utiliser des données synthétiques
- Créer des cas limites
- Tester différentes distributions

### 3. Métriques
- Définir des seuils de performance
- Utiliser plusieurs métriques
- Comparer aux baselines

### 4. Monitoring
- Logging des métriques
- Suivi des temps d'exécution
- Alertes sur dégradation

## Maintenance

### Documentation
- Documenter les choix de modélisation
- Expliquer les métriques utilisées
- Maintenir un journal des expériences

### Mise à Jour
- Réentraînement périodique
- Validation des nouvelles données
- Mise à jour des seuils

### Performance
- Optimisation des hyperparamètres
- Réduction de la complexité
- Amélioration du pipeline
