from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from services.task_service import TaskService
from schemas.task import (
    Task, TaskCreate, TaskUpdate, TaskWithWeather,
    TaskComment, TaskCommentCreate, TaskList
)
from models.task import TaskStatus, TaskCategory

router = APIRouter()

@router.post("/tasks", response_model=Task)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle tâche avec ses ressources et dépendances associées.
    """
    task_service = TaskService(db)
    return await task_service.create_task(task_data)

@router.get("/tasks/{task_id}", response_model=Task)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une tâche par son ID.
    """
    task_service = TaskService(db)
    return task_service.get_task(task_id)

@router.get("/tasks/{task_id}/weather", response_model=TaskWithWeather)
async def get_task_with_weather(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une tâche avec analyse des conditions météo actuelles.
    """
    task_service = TaskService(db)
    return await task_service.get_task_with_weather(task_id)

@router.put("/tasks/{task_id}", response_model=Task)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour une tâche existante.
    """
    task_service = TaskService(db)
    return task_service.update_task(task_id, task_data)

@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime une tâche et libère ses ressources.
    """
    task_service = TaskService(db)
    task_service.delete_task(task_id)
    return {"message": "Tâche supprimée avec succès"}

@router.get("/projects/{project_id}/tasks", response_model=TaskList)
def get_project_tasks(
    project_id: int,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    status: Optional[TaskStatus] = None,
    category: Optional[TaskCategory] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les tâches d'un projet avec pagination et filtres.
    """
    task_service = TaskService(db)
    return task_service.get_tasks_by_project(
        project_id=project_id,
        page=page,
        size=size,
        status=status,
        category=category
    )

@router.post("/tasks/{task_id}/comments", response_model=TaskComment)
def add_task_comment(
    task_id: int,
    comment_data: TaskCommentCreate,
    db: Session = Depends(get_db)
):
    """
    Ajoute un commentaire à une tâche.
    """
    task_service = TaskService(db)
    return task_service.add_task_comment(comment_data)

@router.put("/tasks/{task_id}/resources/{resource_id}")
def update_resource_usage(
    task_id: int,
    resource_id: int,
    quantity_used: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Met à jour l'utilisation d'une ressource pour une tâche.
    """
    task_service = TaskService(db)
    task_service.update_task_resource(task_id, resource_id, quantity_used)
    return {"message": "Utilisation de la ressource mise à jour"}

@router.get("/tasks/{task_id}/dependencies", response_model=List[Task])
def get_task_dependencies(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les tâches qui dépendent de la tâche spécifiée.
    """
    task_service = TaskService(db)
    return task_service.get_dependent_tasks(task_id)

@router.get("/tasks/weather-dependent", response_model=List[TaskWithWeather])
async def get_weather_dependent_tasks(
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les tâches dépendantes de la météo avec leur statut actuel.
    """
    task_service = TaskService(db)
    return await task_service.get_weather_dependent_tasks()
