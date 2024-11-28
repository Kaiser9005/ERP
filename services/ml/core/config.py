"""
Configuration et optimisation avancée des performances ML pour l'inventaire
"""

from typing import Dict, Any, Optional
import os
import psutil
import logging
from dataclasses import dataclass
import torch

# Configuration logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ResourceLimits:
    """Limites ressources système"""
    max_memory_mb: int
    max_cpu_percent: float
    max_gpu_memory_mb: Optional[int]
    max_batch_size: int
    max_workers: int

# Configuration générale optimisée
ML_CONFIG = {
    # Paramètres d'entraînement optimisés
    'training': {
        'batch_size': 128,  # Augmenté pour meilleur throughput
        'epochs': 100,
        'learning_rate': 0.001,
        'validation_split': 0.2,
        'early_stopping_patience': 10,
        'gradient_accumulation_steps': 4,  # Ajouté pour optimisation mémoire
        'mixed_precision': True,  # Ajouté pour performance GPU
        'optimizer': {
            'name': 'adam',
            'weight_decay': 0.01,
            'momentum': 0.9,
            'scheduler': 'cosine_with_warmup'
        }
    },
    
    # Optimisation mémoire avancée
    'memory': {
        'max_memory_mb': 2048,
        'gc_threshold': 0.8,
        'tensor_float_precision': 'mixed',  # Changé pour mixed precision
        'gradient_checkpointing': True,  # Ajouté pour grands modèles
        'pin_memory': True,
        'clear_cache_frequency': 100,  # Nettoyage cache périodique
        'memory_efficient_attention': True  # Optimisation attention
    },
    
    # Configuration cache optimisée
    'cache': {
        'predictions_ttl': 3600,
        'features_ttl': 7200,
        'model_ttl': 86400,
        'max_cache_size_mb': 512,
        'eviction_policy': 'lru',
        'compression_level': 3,
        'persistent_cache': True,
        'cache_warming': True,  # Préchauffage cache
        'distributed_cache': False  # Pour futur scaling
    },
    
    # Optimisation calculs avancée
    'compute': {
        'use_gpu': True,
        'num_workers': 4,
        'prefetch_factor': 2,
        'pin_memory': True,
        'cuda_graphs': True,  # Optimisation CUDA
        'torch_compile': True,  # Compilation JIT
        'channels_last': True,  # Format mémoire optimal
        'kernel_fusion': True,  # Fusion opérations
        'async_prefetch': True  # Chargement asynchrone
    },
    
    # Seuils performance optimisés
    'thresholds': {
        'min_accuracy': 0.95,  # Augmenté
        'max_latency_ms': 100,  # Réduit
        'max_memory_usage': 0.8,
        'min_throughput': 200,  # Augmenté
        'max_error_rate': 0.02,
        'max_drift_threshold': 0.1,
        'min_cache_hit_ratio': 0.85
    },
    
    # Optimisation inférence
    'inference': {
        'batch_inference': True,
        'dynamic_batching': True,
        'quantization': {
            'enabled': True,
            'dtype': 'int8',
            'calibration_samples': 1000
        },
        'model_pruning': {
            'enabled': True,
            'target_sparsity': 0.5,
            'pruning_schedule': 'polynomial'
        }
    }
}

# Optimisation modèles spécifiques
MODEL_CONFIGS = {
    'base': {
        'architecture': 'efficient',  # Changé pour version efficiente
        'hidden_layers': [64, 32],
        'dropout_rate': 0.2,
        'activation': 'relu',
        'layer_norm': True,  # Ajouté normalisation
        'skip_connections': True,  # Ajouté connexions résiduelles
        'attention_type': 'linear'  # Attention linéaire efficiente
    },
    
    'optimization': {
        'architecture': 'medium_efficient',
        'hidden_layers': [128, 64, 32],
        'dropout_rate': 0.3,
        'activation': 'leaky_relu',
        'layer_norm': True,
        'skip_connections': True,
        'attention_type': 'linear'
    },
    
    'analysis': {
        'architecture': 'deep_efficient',
        'hidden_layers': [256, 128, 64],
        'dropout_rate': 0.4,
        'activation': 'elu',
        'layer_norm': True,
        'skip_connections': True,
        'attention_type': 'linear'
    },
    
    'quality': {
        'architecture': 'medium_efficient',
        'hidden_layers': [128, 64],
        'dropout_rate': 0.3,
        'activation': 'relu',
        'layer_norm': True,
        'skip_connections': True,
        'attention_type': 'linear'
    }
}

# Configuration monitoring avancée
MONITORING_CONFIG = {
    'metrics': [
        'latency',
        'memory_usage',
        'prediction_accuracy',
        'cache_hit_ratio',
        'throughput',
        'error_rate',
        'gpu_utilization',
        'model_drift',
        'data_drift',
        'feature_importance',
        'prediction_confidence'
    ],
    'logging_interval': 60,
    'profiling': {
        'enabled': True,
        'trace_functions': True,
        'memory_profiling': True
    },
    'alert_thresholds': {
        'latency_ms': 200,
        'memory_usage': 0.9,
        'error_rate': 0.05,
        'drift_threshold': 0.2,
        'gpu_memory_usage': 0.9
    },
    'monitoring_hooks': {
        'pre_prediction': True,
        'post_prediction': True,
        'performance_tracking': True
    }
}

def get_resource_limits() -> ResourceLimits:
    """
    Détermine limites ressources optimales
    
    Returns:
        ResourceLimits configurés
    """
    total_memory = psutil.virtual_memory().total / (1024 * 1024)
    cpu_count = psutil.cpu_count()
    
    # Détection GPU
    gpu_memory = None
    if torch.cuda.is_available():
        gpu_memory = torch.cuda.get_device_properties(0).total_memory / (1024 * 1024)
    
    return ResourceLimits(
        max_memory_mb=int(total_memory * 0.8),
        max_cpu_percent=80.0,
        max_gpu_memory_mb=int(gpu_memory * 0.9) if gpu_memory else None,
        max_batch_size=256 if gpu_memory else 128,
        max_workers=max(1, cpu_count - 1)
    )

def get_model_config(model_name: str) -> Dict[str, Any]:
    """
    Récupère configuration optimisée pour un modèle
    
    Args:
        model_name: Nom du modèle
        
    Returns:
        Configuration optimisée
    """
    base_config = ML_CONFIG.copy()
    model_specific = MODEL_CONFIGS.get(model_name, {})
    
    # Fusion configurations avec optimisations
    for key, value in model_specific.items():
        if key in base_config:
            if isinstance(value, dict):
                base_config[key].update(value)
            else:
                base_config[key] = value
        else:
            base_config[key] = value
    
    # Ajustements selon ressources
    limits = get_resource_limits()
    base_config['training']['batch_size'] = min(
        base_config['training']['batch_size'],
        limits.max_batch_size
    )
    base_config['compute']['num_workers'] = limits.max_workers
    
    return base_config

def optimize_for_environment() -> None:
    """
    Optimise configuration selon environnement
    """
    limits = get_resource_limits()
    
    # Ajustement configuration
    ML_CONFIG['memory']['max_memory_mb'] = limits.max_memory_mb
    ML_CONFIG['compute']['num_workers'] = limits.max_workers
    
    # Optimisations GPU si disponible
    if torch.cuda.is_available():
        ML_CONFIG['compute'].update({
            'use_gpu': True,
            'cuda_graphs': True,
            'channels_last': True,
            'mixed_precision': True
        })
        logger.info("Configuration GPU optimisée activée")
    else:
        ML_CONFIG['compute']['use_gpu'] = False
        logger.info("Mode CPU optimisé activé")
    
    # Ajustements selon charge système
    cpu_percent = psutil.cpu_percent()
    if cpu_percent > 70:
        ML_CONFIG['compute']['num_workers'] = max(1, limits.max_workers // 2)
        logger.warning(f"Charge CPU élevée ({cpu_percent}%), workers réduits")

def get_cache_config() -> Dict[str, Any]:
    """
    Configuration cache optimisée
    
    Returns:
        Configuration cache
    """
    return {
        'redis': {
            'host': os.getenv('REDIS_HOST', 'localhost'),
            'port': int(os.getenv('REDIS_PORT', 6379)),
            'db': int(os.getenv('REDIS_DB', 0)),
            'password': os.getenv('REDIS_PASSWORD'),
            'ssl': bool(os.getenv('REDIS_SSL', False))
        },
        'ttl': ML_CONFIG['cache'],
        'compression': True,
        'serializer': 'msgpack',
        'distributed': ML_CONFIG['cache']['distributed_cache'],
        'persistent': ML_CONFIG['cache']['persistent_cache']
    }

def get_monitoring_config() -> Dict[str, Any]:
    """
    Configuration monitoring optimisée
    
    Returns:
        Configuration monitoring
    """
    return MONITORING_CONFIG

# Optimisation automatique au chargement
optimize_for_environment()
