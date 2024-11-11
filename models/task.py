from datetime import datetime
from typing import Optional, List
from sqlalchemy import Boolean, Column, String, Integer, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from models.base import BaseModel

class TaskPriority(str, PyEnum):
    """Énumération des niveaux de priorité des tâches"""
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class TaskStatus(str, PyEnum):
    """Énumération des statuts des tâches"""
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_ATTENTE = "EN_ATTENTE"
    TERMINEE = "TERMINEE"
    ANNULEE = "ANNULEE"

class TaskCategory(str, PyEnum):
    """Énumération des catégories de tâches"""
    PRODUCTION = "PRODUCTION"
    MAINTENANCE = "MAINTENANCE"
    RECOLTE = "RECOLTE"
    PLANTATION = "PLANTATION"
    IRRIGATION = "IRRIGATION"
    TRAITEMENT = "TRAITEMENT"
    AUTRE = "AUTRE"

class Task(BaseModel):
    """Modèle pour les tâches du projet"""
    __tablename__ = "tasks"

    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    status = Column(Enum(TaskStatus), default=TaskStatus.A_FAIRE, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MOYENNE, nullable=False)
    category = Column(Enum(TaskCategory), default=TaskCategory.AUTRE, nullable=False)
    
    # Dates
    start_date = Column(DateTime(timezone=True))
    due_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    
    # Relations
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    assigned_to = Column(Integer, ForeignKey("users.id"))
    parcelle_id = Column(Integer, ForeignKey("parcelles.id"))
    
    # Météo
    weather_dependent = Column(Boolean, default=False)
    min_temperature = Column(Float)  # Température minimale requise
    max_temperature = Column(Float)  # Température maximale acceptable
    max_wind_speed = Column(Float)   # Vitesse du vent maximale acceptable
    max_precipitation = Column(Float) # Précipitations maximales acceptables
    
    # Progression
    estimated_hours = Column(Float)
    actual_hours = Column(Float)
    completion_percentage = Column(Integer, default=0)
    
    # Relations bidirectionnelles
    project = relationship("Project", back_populates="tasks")
    assignee = relationship("User", back_populates="assigned_tasks")
    parcelle = relationship("Parcelle", back_populates="tasks")
    resources = relationship("TaskResource", back_populates="task")
    comments = relationship("TaskComment", back_populates="task")
    dependencies = relationship(
        "TaskDependency",
        primaryjoin="or_(Task.id==TaskDependency.task_id, Task.id==TaskDependency.dependent_on_id)"
    )

class TaskResource(BaseModel):
    """Modèle pour les ressources assignées aux tâches"""
    __tablename__ = "task_resources"

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    quantity_required = Column(Float, nullable=False)
    quantity_used = Column(Float, default=0)
    
    task = relationship("Task", back_populates="resources")
    resource = relationship("Resource", back_populates="task_assignments")

class TaskComment(BaseModel):
    """Modèle pour les commentaires sur les tâches"""
    __tablename__ = "task_comments"

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    content = Column(String(1000), nullable=False)
    
    task = relationship("Task", back_populates="comments")
    user = relationship("User", back_populates="task_comments")

class TaskDependency(BaseModel):
    """Modèle pour les dépendances entre tâches"""
    __tablename__ = "task_dependencies"

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    dependent_on_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    dependency_type = Column(String(50), default="finish_to_start")  # finish_to_start, start_to_start, etc.
    
    task = relationship("Task", foreign_keys=[task_id])
    dependent_on = relationship("Task", foreign_keys=[dependent_on_id])
