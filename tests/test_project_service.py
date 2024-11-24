"""
Tests pour le service unifié des projets
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.project_service import ProjectService
from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType

@pytest.fixture
def project_service(db_session):
    """Fixture du service projets"""
    return ProjectService(db_session)

@pytest.fixture
def project(db_session):
    """Fixture d'un projet test"""
    # TODO: Créer un projet test
    return None

@pytest.fixture
def tasks(db_session, project):
    """Fixture des tâches test"""
    tasks = []
    for i in range(3):
        task = Task(
            project_id=project.id,
            name=f"Task {i}",
            status=TaskStatus.IN_PROGRESS,
            start_date=date(2024, 1, 1) + timedelta(days=i*7),
            end_date=date(2024, 1, 1) + timedelta(days=(i+1)*7),
            progress=50,
            weather_sensitive=(i == 0)
        )
        tasks.append(task)
        db_session.add(task)
    db_session.commit()
    return tasks

@pytest.fixture
def resources(db_session, project):
    """Fixture des ressources test"""
    resources = []
    for i in range(2):
        resource = Resource(
            project_id=project.id,
            name=f"Resource {i}",
            type=ResourceType.HUMAN if i == 0 else ResourceType.MATERIAL,
            availability=80,
            efficiency=0.85,
            cost=Decimal("1000.00")
        )
        resources.append(resource)
        db_session.add(resource)
    db_session.commit()
    return resources

async def test_get_project_details_basic(project_service, project):
    """Test de la récupération des détails basiques"""
    details = await project_service.get_project_details(
        project_id=project.id,
        include_analytics=False
    )
    
    assert "id" in details
    assert "name" in details
    assert "start_date" in details
    assert "end_date" in details

async def test_get_project_details_with_analytics(project_service, project):
    """Test de la récupération des détails avec analytics"""
    details = await project_service.get_project_details(
        project_id=project.id,
        include_analytics=True
    )
    
    # Détails de base
    assert "id" in details
    assert "name" in details
    assert "start_date" in details
    assert "end_date" in details
    
    # Analytics
    assert "success_prediction" in details
    assert "performance_analytics" in details
    assert "weather_impact" in details
    
    # Prédiction succès
    assert "success_probability" in details["success_prediction"]
    assert "risk_factors" in details["success_prediction"]
    
    # Performance
    assert "kpis" in details["performance_analytics"]
    assert "trends" in details["performance_analytics"]
    assert "predictions" in details["performance_analytics"]
    
    # Impact météo
    assert "impact_score" in details["weather_impact"]
    assert "affected_tasks" in details["weather_impact"]
    assert "alternatives" in details["weather_impact"]

async def test_create_project_basic(project_service):
    """Test de la création basique d'un projet"""
    project_data = {
        "name": "Test Project",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    
    created = await project_service.create_project(
        project_data=project_data,
        optimize_resources=False
    )
    
    assert "id" in created
    assert created["name"] == project_data["name"]
    assert created["start_date"] == project_data["start_date"]
    assert created["end_date"] == project_data["end_date"]

async def test_create_project_with_optimization(project_service):
    """Test de la création d'un projet avec optimisation"""
    project_data = {
        "name": "Test Project",
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 12, 31)
    }
    
    created = await project_service.create_project(
        project_data=project_data,
        optimize_resources=True
    )
    
    assert "id" in created
    assert "resource_optimization" in created
    assert "optimal_allocation" in created["resource_optimization"]
    assert "efficiency_score" in created["resource_optimization"]

async def test_update_project_basic(project_service, project):
    """Test de la mise à jour basique d'un projet"""
    project_data = {
        "name": "Updated Project"
    }
    
    updated = await project_service.update_project(
        project_id=project.id,
        project_data=project_data,
        reoptimize=False
    )
    
    assert updated["name"] == project_data["name"]

async def test_update_project_with_reoptimization(project_service, project):
    """Test de la mise à jour d'un projet avec ré-optimisation"""
    project_data = {
        "name": "Updated Project"
    }
    
    updated = await project_service.update_project(
        project_id=project.id,
        project_data=project_data,
        reoptimize=True
    )
    
    assert "resource_optimization" in updated
    assert "optimal_allocation" in updated["resource_optimization"]
    assert "efficiency_score" in updated["resource_optimization"]

async def test_get_project_analytics(project_service, project):
    """Test de la récupération des analytics"""
    analytics = await project_service.get_project_analytics(
        project_id=project.id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31)
    )
    
    # Performance
    assert "performance" in analytics
    assert "kpis" in analytics["performance"]
    assert "trends" in analytics["performance"]
    assert "predictions" in analytics["performance"]
    
    # Prédiction succès
    assert "success_prediction" in analytics
    assert "success_probability" in analytics["success_prediction"]
    assert "risk_factors" in analytics["success_prediction"]
    
    # Impact météo
    assert "weather_impact" in analytics
    assert "impact_score" in analytics["weather_impact"]
    assert "affected_tasks" in analytics["weather_impact"]
    
    # Recommandations
    assert "recommendations" in analytics
    assert len(analytics["recommendations"]) > 0

async def test_optimize_project_resources(project_service, project):
    """Test de l'optimisation des ressources"""
    allocation = await project_service.optimize_project_resources(
        project_id=project.id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 12, 31)
    )
    
    assert "optimal_allocation" in allocation
    assert "efficiency_score" in allocation
    assert "bottlenecks" in allocation
    assert "recommendations" in allocation

async def test_get_project_recommendations(project_service, project):
    """Test de la récupération des recommandations"""
    recommendations = await project_service.get_project_recommendations(
        project_id=project.id
    )
    
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_generate_global_recommendations(project_service, project):
    """Test de la génération des recommandations globales"""
    # Données test
    performance = {
        "kpis": {
            "schedule_performance": 0.85,
            "resource_efficiency": 0.75
        },
        "recommendations": [
            "Optimiser planning"
        ]
    }
    
    success_prediction = {
        "success_probability": 0.75,
        "risk_factors": [
            {
                "factor": "Ressources",
                "impact": 0.3
            }
        ]
    }
    
    weather_impact = {
        "impact_score": 0.8,
        "affected_tasks": [
            {
                "task_id": "T1",
                "impact": "HIGH"
            }
        ],
        "alternatives": [
            {
                "task_id": "T1",
                "alternative_date": date(2024, 2, 1)
            }
        ]
    }
    
    # Génération recommandations
    recommendations = await project_service._generate_global_recommendations(
        project.id,
        performance,
        success_prediction,
        weather_impact
    )
    
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_apply_resource_allocation(project_service, project):
    """Test de l'application d'une allocation"""
    # Données test
    allocation = {
        "optimal_allocation": [
            {
                "task_id": "T1",
                "resources": ["R1"],
                "start_date": date(2024, 1, 1),
                "end_date": date(2024, 1, 7)
            }
        ]
    }
    
    # Application
    await project_service._apply_resource_allocation(project.id, allocation)
    
    # TODO: Vérifier l'application
    pass
