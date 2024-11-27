"""
Utilitaires pour les tests ML.
"""

import json
import numpy as np
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Union, List

from . import ML_CACHE_DIR, ML_DATA_DIR, ML_MODELS_DIR

def save_test_data(data: Dict[str, Any], filename: str) -> Path:
    """Sauvegarde des données de test au format JSON."""
    filepath = ML_DATA_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return filepath

def load_test_data(filename: str) -> Dict[str, Any]:
    """Chargement des données de test depuis un fichier JSON."""
    filepath = ML_DATA_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def clear_test_cache() -> None:
    """Nettoyage du cache de test."""
    for file in ML_CACHE_DIR.glob('*'):
        if file.name != '.gitkeep':
            file.unlink()

def clear_test_data() -> None:
    """Nettoyage des données de test."""
    for file in ML_DATA_DIR.glob('*'):
        if file.name != '.gitkeep':
            file.unlink()

def clear_test_models() -> None:
    """Nettoyage des modèles de test."""
    for file in ML_MODELS_DIR.glob('*'):
        if file.name != '.gitkeep':
            file.unlink()

def generate_test_predictions() -> Dict[str, Any]:
    """Génération de prédictions de test."""
    return {
        "production": {
            "yield_prediction": np.random.normal(1000, 100),
            "quality_prediction": np.random.uniform(0.8, 1.0),
            "maintenance_prediction": ["Machine A", "Machine B"]
        },
        "finance": {
            "revenue_prediction": np.random.normal(100000, 10000),
            "expense_prediction": np.random.normal(80000, 8000),
            "cash_flow_prediction": np.random.normal(20000, 2000)
        },
        "inventory": {
            "stock_level_predictions": {
                f"item_{i}": np.random.randint(50, 150) 
                for i in range(5)
            },
            "reorder_suggestions": [f"item_{i}" for i in range(2)]
        },
        "hr": {
            "turnover_prediction": np.random.uniform(0.1, 0.2),
            "hiring_needs": ["Developer", "Manager"],
            "training_recommendations": ["Python", "Leadership"]
        }
    }

def generate_test_alerts() -> List[Dict[str, Any]]:
    """Génération d'alertes de test."""
    alert_types = ["production", "finance", "inventory", "hr"]
    alerts = []
    
    for alert_type in alert_types:
        if np.random.random() > 0.5:  # 50% de chance d'avoir une alerte
            alerts.append({
                "type": alert_type,
                "message": f"Test alert for {alert_type}",
                "priority": np.random.randint(1, 4),
                "timestamp": datetime.now().isoformat()
            })
    
    return sorted(alerts, key=lambda x: x["priority"], reverse=True)

def format_test_results(results: Dict[str, Any]) -> str:
    """Formatage des résultats de test pour le rapport."""
    output = []
    for module, data in results.items():
        output.append(f"\n=== {module.upper()} ===")
        for key, value in data.items():
            if isinstance(value, dict):
                output.append(f"\n{key}:")
                for k, v in value.items():
                    output.append(f"  {k}: {v}")
            else:
                output.append(f"{key}: {value}")
    
    return "\n".join(output)

def calculate_metrics(predictions: Dict[str, Any], actuals: Dict[str, Any]) -> Dict[str, float]:
    """Calcul des métriques de performance."""
    metrics = {}
    
    # Métriques de production
    if "production" in predictions and "production" in actuals:
        pred = predictions["production"]["yield_prediction"]
        actual = actuals["production"]["yield_prediction"]
        metrics["production_mape"] = abs((pred - actual) / actual) * 100
    
    # Métriques financières
    if "finance" in predictions and "finance" in actuals:
        pred = predictions["finance"]["revenue_prediction"]
        actual = actuals["finance"]["revenue_prediction"]
        metrics["finance_mape"] = abs((pred - actual) / actual) * 100
    
    # Métriques RH
    if "hr" in predictions and "hr" in actuals:
        pred = predictions["hr"]["turnover_prediction"]
        actual = actuals["hr"]["turnover_prediction"]
        metrics["hr_mae"] = abs(pred - actual)
    
    return metrics
