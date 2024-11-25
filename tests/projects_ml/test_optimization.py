"""Tests pour l'optimisation des ressources."""

import pytest
from datetime import date, timedelta
from unittest.mock import Mock, AsyncMock
import numpy as np
from sqlalchemy.orm import Session

from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType
from services.cache_service import CacheService
from services.projects_ml.optimization import ResourceOptimizer

@pytest.fixture
def db_session():
    """Fixture pour la session de base de données."""
    return Mock(spec=Session)

@pytest.fixture
def cache_service():
    """Fixture pour le service de cache."""
    return AsyncMock(spec=CacheService)

@pytest.fixture
def optimizer(db_session, cache_service):
    """Fixture pour l'optimiseur."""
    service = ResourceOptimizer(db_session)
    service.cache = cache_service
    return service

@pytest.fixture
def sample_tasks():
    """Fixture pour les tâches exemple."""
    today = date.today()
    return [{
        "id": "T1",
        "name": "Tâche 1",
        "start_date": today,
        "end_date": today + timedelta(days=5),
        "dependencies": [],
        "resources_needed": 2
    }, {
        "id": "T2",
        "name": "Tâche 2",
        "start_date": today + timedelta(days=3),
        "end_date": today + timedelta(days=8),
        "dependencies": ["T1"],
        "resources_needed": 1
    }]

@pytest.fixture
def sample_resources():
    """Fixture pour les ressources exemple."""
    return [{
        "id": "R1",
        "name": "Resource 1",
        "availability": 0.8,
        "cost": 1000.0
    }, {
        "id": "R2",
        "name": "Resource 2",
        "availability": 1.0,
        "cost": 800.0
    }, {
        "id": "R3",
        "name": "Resource 3",
        "availability": 0.5,
        "cost": 1200.0
    }]

class TestResourceOptimizer:
    """Tests pour ResourceOptimizer."""

    async def test_optimize_allocation_with_cache(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'optimisation avec cache."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        cached_result = {
            "optimal_allocation": [{
                "task_id": "T1",
                "resources": [{"resource_id": "R1", "days": [0, 1, 2]}]
            }],
            "efficiency_score": 0.85,
            "bottlenecks": [],
            "recommendations": []
        }
        optimizer.cache.get.return_value = cached_result
        
        # Exécution
        result = await optimizer.optimize_allocation(project_id, start_date, end_date)
        
        # Vérifications
        assert result == cached_result
        optimizer.cache.get.assert_called_once()

    async def test_optimize_allocation_without_cache(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'optimisation sans cache."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        optimizer.cache.get.return_value = None
        optimizer._get_tasks = AsyncMock(return_value=sample_tasks)
        optimizer._get_resources = AsyncMock(return_value=sample_resources)
        
        # Exécution
        result = await optimizer.optimize_allocation(project_id, start_date, end_date)
        
        # Vérifications
        assert "optimal_allocation" in result
        assert isinstance(result["optimal_allocation"], list)
        assert all(
            {"task_id", "resources", "start_date", "end_date"}.issubset(a.keys())
            for a in result["optimal_allocation"]
        )
        
        assert "efficiency_score" in result
        assert isinstance(result["efficiency_score"], float)
        assert 0 <= result["efficiency_score"] <= 1
        
        assert "bottlenecks" in result
        assert isinstance(result["bottlenecks"], list)
        assert all(
            {"resource", "period", "utilization"}.issubset(b.keys())
            for b in result["bottlenecks"]
        )
        
        assert "recommendations" in result
        assert isinstance(result["recommendations"], list)

    async def test_optimize_allocation_with_dependencies(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'optimisation avec dépendances."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        optimizer.cache.get.return_value = None
        optimizer._get_tasks = AsyncMock(return_value=sample_tasks)
        optimizer._get_resources = AsyncMock(return_value=sample_resources)
        
        # Exécution
        result = await optimizer.optimize_allocation(project_id, start_date, end_date)
        
        # Vérifications
        allocations = result["optimal_allocation"]
        task_dates = {a["task_id"]: (a["start_date"], a["end_date"]) for a in allocations}
        
        # Vérifie que T2 commence après T1
        if "T1" in task_dates and "T2" in task_dates:
            assert task_dates["T2"][0] >= task_dates["T1"][1]

    async def test_optimize_allocation_with_resource_constraints(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'optimisation avec contraintes de ressources."""
        # Configuration
        project_id = "P1"
        start_date = date.today()
        end_date = start_date + timedelta(days=10)
        
        optimizer.cache.get.return_value = None
        optimizer._get_tasks = AsyncMock(return_value=sample_tasks)
        optimizer._get_resources = AsyncMock(return_value=sample_resources)
        
        # Exécution
        result = await optimizer.optimize_allocation(project_id, start_date, end_date)
        
        # Vérifications
        allocations = result["optimal_allocation"]
        
        # Vérifie les contraintes de ressources
        resource_usage = {}
        for alloc in allocations:
            for resource in alloc["resources"]:
                resource_id = resource["resource_id"]
                if resource_id not in resource_usage:
                    resource_usage[resource_id] = set()
                resource_usage[resource_id].update(resource["days"])
        
        # Vérifie que chaque ressource n'est pas surexploitée
        for resource_id, days_used in resource_usage.items():
            resource = next(r for r in sample_resources if r["id"] == resource_id)
            max_days = int((end_date - start_date).days * resource["availability"])
            assert len(days_used) <= max_days

    def test_analyze_solution_with_bottlenecks(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'analyse de solution avec goulots d'étranglement."""
        # Configuration
        x = {}  # Variables de décision simulées
        today = date.today()
        
        # Simule une utilisation intensive de R1
        for task in sample_tasks:
            task_days = (task["end_date"] - task["start_date"]).days + 1
            for day in range(task_days):
                x[task["id"], "R1", day] = Mock(value=lambda: 1)  # Utilisation maximale
        
        # Exécution
        result = optimizer._analyze_solution(x, sample_tasks, sample_resources, Mock())
        
        # Vérifications
        assert any(
            b["resource"] == "R1" and b["utilization"] > 0.8
            for b in result["bottlenecks"]
        )
        assert any(
            "ressources supplémentaires" in r.lower()
            for r in result["recommendations"]
        )

    def test_analyze_solution_with_low_efficiency(
        self,
        optimizer,
        sample_tasks,
        sample_resources
    ):
        """Test de l'analyse de solution avec faible efficacité."""
        # Configuration
        x = {}  # Variables de décision simulées
        today = date.today()
        
        # Simule une faible utilisation des ressources
        for task in sample_tasks:
            task_days = (task["end_date"] - task["start_date"]).days + 1
            for day in range(task_days):
                x[task["id"], "R1", day] = Mock(value=lambda: 0.2)  # Utilisation faible
        
        # Exécution
        result = optimizer._analyze_solution(x, sample_tasks, sample_resources, Mock())
        
        # Vérifications
        assert result["efficiency_score"] < 0.5
        assert any(
            "sous-optimale" in r.lower()
            for r in result["recommendations"]
        )
