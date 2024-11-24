"""
Tests pour le service ML des projets
"""

import pytest
from datetime import datetime, date, timedelta
from decimal import Decimal
from unittest.mock import Mock, patch

from services.projects_ml_service import ProjectsMLService
from models.task import Task, TaskStatus
from models.resource import Resource, ResourceType

@pytest.fixture
def ml_service(db_session):
    """Fixture du service ML"""
    return ProjectsMLService(db_session)

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

async def test_predict_project_success(ml_service, project, tasks, resources):
    """Test de la prédiction de succès du projet"""
    # Prédiction
    prediction = await ml_service.predict_project_success(
        project_id=project.id,
        current_date=date(2024, 1, 15)
    )
    
    # Vérifications
    assert "success_probability" in prediction
    assert isinstance(prediction["success_probability"], float)
    assert 0 <= prediction["success_probability"] <= 1
    
    assert "risk_factors" in prediction
    assert len(prediction["risk_factors"]) > 0
    for rf in prediction["risk_factors"]:
        assert "factor" in rf
        assert "impact" in rf
        assert "description" in rf
        
    assert "recommendations" in prediction
    assert len(prediction["recommendations"]) > 0
    for rec in prediction["recommendations"]:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_optimize_resource_allocation(ml_service, project, tasks, resources):
    """Test de l'optimisation des ressources"""
    # Optimisation
    allocation = await ml_service.optimize_resource_allocation(
        project_id=project.id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31)
    )
    
    # Vérifications
    assert "optimal_allocation" in allocation
    assert len(allocation["optimal_allocation"]) > 0
    for alloc in allocation["optimal_allocation"]:
        assert "task_id" in alloc
        assert "resources" in alloc
        assert "start_date" in alloc
        assert "end_date" in alloc
        
    assert "efficiency_score" in allocation
    assert isinstance(allocation["efficiency_score"], float)
    assert 0 <= allocation["efficiency_score"] <= 1
    
    assert "bottlenecks" in allocation
    for bottleneck in allocation["bottlenecks"]:
        assert "resource" in bottleneck
        assert "period" in bottleneck
        assert "utilization" in bottleneck
        
    assert "recommendations" in allocation
    assert len(allocation["recommendations"]) > 0

async def test_analyze_project_performance(ml_service, project, tasks, resources):
    """Test de l'analyse de performance"""
    # Analyse
    performance = await ml_service.analyze_project_performance(
        project_id=project.id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31)
    )
    
    # Vérifications
    assert "kpis" in performance
    assert "schedule_performance" in performance["kpis"]
    assert "cost_performance" in performance["kpis"]
    assert "resource_efficiency" in performance["kpis"]
    assert "quality_score" in performance["kpis"]
    assert "risk_score" in performance["kpis"]
    
    assert "trends" in performance
    assert "velocity" in performance["trends"]
    assert "completion_rate" in performance["trends"]
    assert "resource_usage" in performance["trends"]
    
    assert "predictions" in performance
    assert "completion_date" in performance["predictions"]
    assert "final_cost" in performance["predictions"]
    assert "quality_forecast" in performance["predictions"]
    assert "risk_forecast" in performance["predictions"]
    
    assert "recommendations" in performance
    assert len(performance["recommendations"]) > 0

async def test_predict_weather_impact(ml_service, project, tasks):
    """Test de la prédiction d'impact météo"""
    # Prédiction
    impact = await ml_service.predict_weather_impact(
        project_id=project.id,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31)
    )
    
    # Vérifications
    assert "impact_score" in impact
    assert isinstance(impact["impact_score"], float)
    assert 0 <= impact["impact_score"] <= 1
    
    assert "affected_tasks" in impact
    assert len(impact["affected_tasks"]) > 0
    for task in impact["affected_tasks"]:
        assert "task_id" in task
        assert "impact" in task
        assert "conditions" in task
        
    assert "risk_periods" in impact
    for period in impact["risk_periods"]:
        assert "period" in period
        assert "risk" in period
        assert "conditions" in period
        
    assert "alternatives" in impact
    assert len(impact["alternatives"]) > 0
    for alt in impact["alternatives"]:
        assert "task_id" in alt
        assert "original_date" in alt
        assert "alternative_date" in alt
        assert "reason" in alt

async def test_get_project_tasks(ml_service, project, tasks):
    """Test de la récupération des tâches"""
    project_tasks = await ml_service._get_project_tasks(project.id)
    
    assert len(project_tasks) == len(tasks)
    for task in project_tasks:
        assert "id" in task
        assert "name" in task
        assert "status" in task
        assert "start_date" in task
        assert "end_date" in task
        assert "progress" in task
        assert "dependencies" in task
        assert "resources" in task
        assert "metrics" in task

async def test_get_project_resources(ml_service, project, resources):
    """Test de la récupération des ressources"""
    project_resources = await ml_service._get_project_resources(project.id)
    
    assert len(project_resources) == len(resources)
    for resource in project_resources:
        assert "id" in resource
        assert "type" in resource
        assert "name" in resource
        assert "availability" in resource
        assert "efficiency" in resource
        assert "cost" in resource

async def test_calculate_success_features(ml_service):
    """Test du calcul des features"""
    # Données test
    tasks = [
        {"progress": 50, "status": TaskStatus.IN_PROGRESS},
        {"progress": 100, "status": TaskStatus.COMPLETED}
    ]
    resources = [
        {"efficiency": 0.8, "cost": 1000},
        {"efficiency": 0.9, "cost": 2000}
    ]
    weather = {
        "impact_score": 0.7,
        "risk_factors": ["RAIN"],
        "affected_tasks": ["T1"]
    }
    
    # Calcul features
    features = ml_service._calculate_success_features(tasks, resources, weather)
    
    # Vérifications
    assert len(features) == 9  # 3 features par source
    assert all(isinstance(f, float) for f in features)

async def test_predict_success(ml_service):
    """Test de la prédiction de succès"""
    # Features test
    features = np.array([1.0, 0.8, 0.5, 0.9, 0.7, 1000.0, 0.7, 1.0, 1.0])
    
    # Prédiction
    prediction = await ml_service._predict_success(features)
    
    # Vérifications
    assert "probability" in prediction
    assert isinstance(prediction["probability"], float)
    assert 0 <= prediction["probability"] <= 1
    
    assert "risk_factors" in prediction
    assert len(prediction["risk_factors"]) > 0
    for rf in prediction["risk_factors"]:
        assert "factor" in rf
        assert "impact" in rf
        assert "description" in rf

async def test_generate_recommendations(ml_service, project):
    """Test de la génération de recommandations"""
    # Données test
    prediction = {
        "probability": 0.7,
        "risk_factors": [
            {
                "factor": "Ressources",
                "impact": 0.3,
                "description": "Allocation sous-optimale"
            }
        ]
    }
    
    # Génération recommandations
    recommendations = await ml_service._generate_recommendations(
        project.id,
        prediction
    )
    
    # Vérifications
    assert len(recommendations) > 0
    for rec in recommendations:
        assert "type" in rec
        assert "priority" in rec
        assert "description" in rec
        assert "actions" in rec

async def test_optimize_allocation(ml_service):
    """Test de l'optimisation d'allocation"""
    # Données test
    tasks = [
        {
            "id": "T1",
            "duration": 7,
            "resources_needed": ["R1"]
        }
    ]
    resources = [
        {
            "id": "R1",
            "availability": 80
        }
    ]
    constraints = {
        "max_parallel": 2
    }
    
    # Optimisation
    allocation = await ml_service._optimize_allocation(
        tasks,
        resources,
        constraints
    )
    
    # Vérifications
    assert "allocation" in allocation
    assert len(allocation["allocation"]) > 0
    assert "efficiency" in allocation
    assert "bottlenecks" in allocation
    assert "recommendations" in allocation

async def test_calculate_project_kpis(ml_service):
    """Test du calcul des KPIs"""
    # Données test
    tasks = [
        {
            "progress": 50,
            "planned_hours": 100,
            "actual_hours": 90
        }
    ]
    resources = [
        {
            "utilization": 0.8,
            "planned_cost": 1000,
            "actual_cost": 950
        }
    ]
    timeline = {
        "planned_end": date(2024, 3, 31),
        "forecast_end": date(2024, 4, 15)
    }
    
    # Calcul KPIs
    kpis = ml_service._calculate_project_kpis(tasks, resources, timeline)
    
    # Vérifications
    assert "schedule_performance" in kpis
    assert "cost_performance" in kpis
    assert "resource_efficiency" in kpis
    assert "quality_score" in kpis
    assert "risk_score" in kpis
    assert all(0 <= kpi <= 1 for kpi in kpis.values())

async def test_analyze_performance_trends(ml_service):
    """Test de l'analyse des tendances"""
    # Données test
    tasks = [
        {
            "completion_date": date(2024, 1, 15),
            "progress": 100
        },
        {
            "completion_date": date(2024, 1, 30),
            "progress": 50
        }
    ]
    timeline = {
        "start_date": date(2024, 1, 1),
        "end_date": date(2024, 3, 31)
    }
    
    # Analyse tendances
    trends = ml_service._analyze_performance_trends(tasks, timeline)
    
    # Vérifications
    assert "velocity" in trends
    assert "completion_rate" in trends
    assert "resource_usage" in trends
    for metric in trends.values():
        assert "current" in metric
        assert "trend" in metric
        assert "forecast" in metric

async def test_predict_future_performance(ml_service, project):
    """Test de la prédiction de performance future"""
    # Données test
    kpis = {
        "schedule_performance": 0.85,
        "cost_performance": 0.92
    }
    trends = {
        "velocity": {
            "current": 8.5,
            "trend": "increasing"
        }
    }
    
    # Prédiction
    predictions = await ml_service._predict_future_performance(
        project.id,
        kpis,
        trends
    )
    
    # Vérifications
    assert "completion_date" in predictions
    assert "final_cost" in predictions
    assert "quality_forecast" in predictions
    assert "risk_forecast" in predictions

async def test_get_weather_sensitive_tasks(ml_service, project, tasks):
    """Test de la récupération des tâches sensibles à la météo"""
    sensitive_tasks = await ml_service._get_weather_sensitive_tasks(project.id)
    
    assert len(sensitive_tasks) > 0
    for task in sensitive_tasks:
        assert "id" in task
        assert "name" in task
        assert "weather_conditions" in task
        assert "flexibility" in task

async def test_analyze_weather_impact(ml_service):
    """Test de l'analyse d'impact météo"""
    # Données test
    weather = [
        {
            "date": date(2024, 2, 1),
            "temperature": 0,
            "precipitation": 10
        }
    ]
    tasks = [
        {
            "id": "T1",
            "weather_conditions": ["FROST"],
            "flexibility": 0.5
        }
    ]
    
    # Analyse impact
    impact = ml_service._analyze_weather_impact(weather, tasks)
    
    # Vérifications
    assert "score" in impact
    assert "tasks" in impact
    assert "risks" in impact
    assert len(impact["tasks"]) > 0
    assert len(impact["risks"]) > 0

async def test_generate_weather_alternatives(ml_service, project):
    """Test de la génération d'alternatives météo"""
    # Données test
    impact = {
        "tasks": [
            {
                "task_id": "T1",
                "impact": "HIGH",
                "conditions": ["FROST"]
            }
        ],
        "risks": [
            {
                "period": "2024-02",
                "risk": "HIGH",
                "conditions": ["FROST"]
            }
        ]
    }
    
    # Génération alternatives
    alternatives = await ml_service._generate_weather_alternatives(
        project.id,
        impact
    )
    
    # Vérifications
    assert len(alternatives) > 0
    for alt in alternatives:
        assert "task_id" in alt
        assert "original_date" in alt
        assert "alternative_date" in alt
        assert "reason" in alt
