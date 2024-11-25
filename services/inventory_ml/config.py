"""
Configuration et optimisation des performances ML pour l'inventaire
"""

from typing import Dict, Any
import os

# Configuration générale
ML_CONFIG = {
    # Paramètres d'entraînement
    'training': {
        'batch_size': 64,
        'epochs': 100,
        'learning_rate': 0.001,
        'validation_split': 0.2,
        'early_stopping_patience': 10,
    },
    
    # Optimisation mémoire
    'memory': {
        'max_memory_mb': 2048,
        'gc_threshold': 0.8,
        'tensor_float_precision': 32,
    },
    
    # Configuration cache
    'cache': {
        'predictions_ttl': 3600,  # 1 heure
        'features_ttl': 7200,    # 2 heures
        'model_ttl': 86400,      # 24 heures
        'max_cache_size_mb': 512,
    },
    
    # Optimisation calculs
    'compute': {
        'use_gpu': True,
        'num_workers': 4,
        'prefetch_factor': 2,
        'pin_memory': True,
    },
    
    # Seuils performance
    'thresholds': {
        'min_accuracy': 0.90,
        'max_latency_ms': 200,
        'max_memory_usage': 0.8,
        'min_throughput': 100,  # prédictions/seconde
    }
}

# Optimisation modèles spécifiques
MODEL_CONFIGS = {
    'base': {
        'architecture': 'lightweight',
        'hidden_layers': [64, 32],
        'dropout_rate': 0.2,
        'activation': 'relu',
    },
    
    'optimization': {
        'architecture': 'medium',
        'hidden_layers': [128, 64, 32],
        'dropout_rate': 0.3,
        'activation': 'leaky_relu',
    },
    
    'analysis': {
        'architecture': 'deep',
        'hidden_layers': [256, 128, 64],
        'dropout_rate': 0.4,
        'activation': 'elu',
    },
    
    'quality': {
        'architecture': 'medium',
        'hidden_layers': [128, 64],
        'dropout_rate': 0.3,
        'activation': 'relu',
    }
}

# Configuration monitoring
MONITORING_CONFIG = {
    'metrics': [
        'latency',
        'memory_usage',
        'prediction_accuracy',
        'cache_hit_ratio',
        'throughput',
        'error_rate',
    ],
    'logging_interval': 60,  # secondes
    'alert_thresholds': {
        'latency_ms': 500,
        'memory_usage': 0.9,
        'error_rate': 0.05,
    }
}

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Récupère la configuration optimisée pour un modèle spécifique
    
    Args:
        model_name: Nom du modèle ('base', 'optimization', etc.)
        
    Returns:
        Configuration optimisée du modèle
    """
    base_config = ML_CONFIG.copy()
    model_specific = MODEL_CONFIGS.get(model_name, {})
    
    # Fusion configurations
    for key, value in model_specific.items():
        if key in base_config:
            if isinstance(value, dict):
                base_config[key].update(value)
            else:
                base_config[key] = value
        else:
            base_config[key] = value
            
    return base_config

def optimize_for_environment() -> None:
    """
    Optimise la configuration selon l'environnement d'exécution
    """
    # Détection ressources disponibles
    import psutil
    total_memory = psutil.virtual_memory().total / (1024 * 1024)  # MB
    cpu_count = psutil.cpu_count()
    
    # Ajustement configuration
    ML_CONFIG['memory']['max_memory_mb'] = min(
        ML_CONFIG['memory']['max_memory_mb'],
        int(total_memory * 0.8)
    )
    
    ML_CONFIG['compute']['num_workers'] = min(
        ML_CONFIG['compute']['num_workers'],
        cpu_count - 1
    )
    
    # Détection GPU
    try:
        import torch
        ML_CONFIG['compute']['use_gpu'] = torch.cuda.is_available()
    except ImportError:
        ML_CONFIG['compute']['use_gpu'] = False

def get_cache_config() -> Dict[str, Any]:
    """
    Récupère la configuration optimisée du cache
    
    Returns:
        Configuration du cache
    """
    return {
        'redis': {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'db': int(os.getenv('REDIS_DB', 0)),
        },
        'ttl': ML_CONFIG['cache'],
        'compression': True,
        'serializer': 'msgpack',
    }

def get_monitoring_config() -> Dict[str, Any]:
    """
    Récupère la configuration du monitoring
    
    Returns:
        Configuration monitoring
    """
    return MONITORING_CONFIG

# Optimisation automatique au chargement
optimize_for_environment()
