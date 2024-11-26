"""
Tests de performance pour le service ML inventaire optimisé
"""

import pytest
import torch
import numpy as np
from datetime import datetime
from unittest.mock import Mock, patch

from models.inventory import Stock, MouvementStock
from services.inventory_ml_service import InventoryMLService, MLContext
from services.inventory_ml.config import (
    get_model_config,
    get_cache_config,
    get_monitoring_config,
    get_resource_limits
)

@pytest.fixture
def ml_service():
    """Fixture service ML"""
    return InventoryMLService()

@pytest.fixture
def mock_stock():
    """Fixture stock test"""
    return Mock(spec=Stock, id='test_stock', capteurs_id=['sensor1'])

@pytest.fixture
def mock_mouvements():
    """Fixture mouvements test"""
    return [Mock(spec=MouvementStock) for _ in range(10)]

@pytest.mark.gpu
def test_gpu_optimization(ml_service):
    """Test optimisations GPU"""
    if not torch.cuda.is_available():
        pytest.skip("GPU non disponible")
        
    # Vérification configuration GPU
    assert ml_service.device == 'cuda'
    assert hasattr(ml_service, 'scaler')
    
    # Test mixed precision
    context = ml_service._get_context()
    assert context.precision == 'mixed'
    
    # Test CUDA graphs
    config = get_model_config('base')
    assert config['compute']['cuda_graphs']
    assert config['compute']['channels_last']

def test_resource_management(ml_service):
    """Test gestion ressources"""
    limits = get_resource_limits()
    
    # Vérification limites
    assert limits.max_memory_mb > 0
    assert 0 < limits.max_cpu_percent <= 100
    assert limits.max_batch_size > 0
    assert limits.max_workers > 0
    
    # Test adaptation batch size
    context = ml_service._get_context(batch_size=1000000)
    assert context.batch_size <= limits.max_batch_size

@pytest.mark.asyncio
async def test_prediction_latency(ml_service, mock_stock, mock_mouvements):
    """Test latence prédictions"""
    context = MLContext(
        device=ml_service.device,
        precision='mixed',
        batch_size=32,
        use_cache=True,
        profiling=True,
        resource_limits=get_resource_limits()
    )
    
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    # Test latence
    start = datetime.now()
    result = await ml_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    latency = (datetime.now() - start).total_seconds()
    
    # Vérification performance
    assert latency < 0.2  # Max 200ms
    assert 'metadata' in result
    assert result['metadata']['device'] == context.device
    assert result['metadata']['precision'] == context.precision

@pytest.mark.gpu
@patch('torch.cuda.memory_allocated')
def test_memory_optimization(mock_memory, ml_service):
    """Test optimisation mémoire"""
    if not torch.cuda.is_available():
        pytest.skip("GPU non disponible")
        
    # Simulation utilisation mémoire
    mock_memory.return_value = 1024 * 1024 * 100  # 100MB
    
    # Test limites mémoire
    limits = get_resource_limits()
    assert mock_memory() < limits.max_memory_mb * 1024 * 1024

@pytest.mark.asyncio
async def test_cache_optimization(ml_service, mock_stock, mock_mouvements):
    """Test optimisation cache"""
    context = ml_service._get_context()
    
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    # Premier appel (sans cache)
    start = datetime.now()
    result1 = await ml_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    time1 = (datetime.now() - start).total_seconds()
    
    # Deuxième appel (avec cache)
    start = datetime.now()
    result2 = await ml_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    time2 = (datetime.now() - start).total_seconds()
    
    # Vérification gain performance
    assert time2 < time1 * 0.5  # Au moins 50% plus rapide
    assert result1['niveau_optimal'] == result2['niveau_optimal']

@pytest.mark.asyncio
@pytest.mark.parametrize('batch_size', [16, 32, 64, 128])
async def test_batch_size_impact(ml_service, mock_stock, mock_mouvements, batch_size):
    """Test impact taille batch"""
    context = ml_service._get_context(batch_size=batch_size)
    
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    start = datetime.now()
    await ml_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    latency = (datetime.now() - start).total_seconds()
    
    # Log performance
    print(f"Batch size {batch_size}: {latency:.3f}s")
    
    # Vérification latence acceptable
    assert latency < 0.5  # Max 500ms

@pytest.mark.asyncio
async def test_model_save_load(ml_service, mock_stock, mock_mouvements, tmp_path):
    """Test sauvegarde/chargement optimisé"""
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    # Sauvegarde
    save_path = tmp_path / "models"
    save_path.mkdir()
    await ml_service.save_models(str(save_path))
    
    # Vérification fichiers
    model_files = list(save_path.glob("*_model.pt"))
    assert len(model_files) == 4  # base, optimizer, analyzer, quality
    
    # Chargement
    new_service = InventoryMLService()
    await new_service.load_models(str(save_path))
    
    # Vérification état
    assert new_service.is_trained
    assert new_service.device == ml_service.device
    
    # Test prédictions identiques
    context = ml_service._get_context()
    result1 = await ml_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    result2 = await new_service.get_stock_insights(
        mock_stock,
        mock_mouvements,
        context
    )
    assert result1['niveau_optimal'] == result2['niveau_optimal']

@pytest.mark.gpu
@pytest.mark.asyncio
async def test_profiling(ml_service, mock_stock, mock_mouvements):
    """Test profiling performance"""
    if not torch.cuda.is_available():
        pytest.skip("GPU non disponible")
        
    context = MLContext(
        device='cuda',
        precision='mixed',
        batch_size=32,
        use_cache=False,
        profiling=True,
        resource_limits=get_resource_limits()
    )
    
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    with torch.autograd.profiler.profile(use_cuda=True) as prof:
        await ml_service.get_stock_insights(
            mock_stock,
            mock_mouvements,
            context
        )
        
    # Analyse profiling
    stats = prof.key_averages()
    print("\nProfiling results:")
    print(stats.table(sort_by="cuda_time_total", row_limit=10))
    
    # Vérification métriques clés
    for event in stats:
        if 'cuda' in event.key:
            assert event.cuda_time_total < 1e6  # Max 1ms

@pytest.mark.asyncio
async def test_parallel_inference(ml_service):
    """Test inférence parallèle"""
    # Configuration
    n_workers = 4
    batch_size = 32
    n_batches = 10
    
    # Données test
    mock_stocks = [Mock(spec=Stock, id=f'stock_{i}') for i in range(n_batches)]
    mock_mouvs = [[Mock(spec=MouvementStock) for _ in range(10)] 
                  for _ in range(n_batches)]
    
    # Entraînement initial
    await ml_service.train(
        stocks=mock_stocks,
        mouvements={f'test_{i}': mouvs for i, mouvs in enumerate(mock_mouvs)}
    )
    
    context = MLContext(
        device=ml_service.device,
        precision='mixed',
        batch_size=batch_size,
        use_cache=False,
        profiling=False,
        resource_limits=get_resource_limits()
    )
    
    # Test parallèle
    import asyncio
    tasks = []
    for stock, mouvs in zip(mock_stocks, mock_mouvs):
        task = asyncio.create_task(
            ml_service.get_stock_insights(stock, mouvs, context)
        )
        tasks.append(task)
            
    # Vérification résultats
    results = await asyncio.gather(*tasks)
    assert len(results) == n_batches
    
    # Vérification pas d'erreurs
    for result in results:
        assert 'error' not in result
        assert result['niveau_optimal'] is not None

@pytest.mark.asyncio
async def test_error_handling(ml_service, mock_stock, mock_mouvements):
    """Test gestion erreurs"""
    # Test modèle non entraîné
    with pytest.raises(ValueError, match="doit être entraîné"):
        await ml_service.get_stock_insights(mock_stock, mock_mouvements)
        
    # Test paramètres invalides
    with pytest.raises(Exception):
        await ml_service.get_stock_insights(None, None)
        
    # Test erreur GPU
    if torch.cuda.is_available():
        with patch('torch.cuda.is_available', return_value=False):
            context = ml_service._get_context()
            assert context.device == 'cpu'
            
@pytest.mark.asyncio
async def test_monitoring_integration(ml_service, mock_stock, mock_mouvements):
    """Test intégration monitoring"""
    context = MLContext(
        device=ml_service.device,
        precision='mixed',
        batch_size=32,
        use_cache=True,
        profiling=True,
        resource_limits=get_resource_limits()
    )
    
    # Entraînement initial
    await ml_service.train(
        stocks=[mock_stock],
        mouvements={'test': mock_mouvements}
    )
    
    # Vérification métriques
    with patch('logging.Logger.debug') as mock_debug:
        await ml_service.get_stock_insights(
            mock_stock,
            mock_mouvements,
            context
        )
        assert mock_debug.called
        
        # Analyse logs
        calls = mock_debug.call_args_list
        for call in calls:
            msg = call.args[0]
            if 'Profile' in msg:
                assert 'cuda' in msg or 'cpu' in msg
