from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class TaskPriority(str, Enum):
    BASSE = "BASSE"
    MOYENNE = "MOYENNE"
    HAUTE = "HAUTE"
    CRITIQUE = "CRITIQUE"

class TaskStatus(str, Enum):
    A_FAIRE = "A_FAIRE"
    EN_COURS = "EN_COURS"
    EN_ATTENTE = "EN_ATTENTE"
    TERMINEE = "TERMINEE"
    ANNULEE = "ANNULEE"

class TaskCategory(str, Enum):
    PRODUCTION = "PRODUCTION"
    MAINTENANCE = "MAINTENANCE"
    RECOLTE = "RECOLTE"
    PLANTATION = "PLANTATION"
    IRRIGATION = "IRRIGATION"
    TRAITEMENT = "TRAITEMENT"
    AUTRE = "AUTRE"

class TaskResourceBase(BaseModel):
    resource_id: int
    quantity_required: float
    quantity_used: Optional[float] = 0

    class Config:
        from_attributes = True

class TaskCommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

    class Config:
        from_attributes = True

class TaskDependencyBase(BaseModel):
    dependent_on_id: int
    dependency_type: str = "finish_to_start"

    class Config:
        from_attributes = True

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: TaskStatus = TaskStatus.A_FAIRE
    priority: TaskPriority = TaskPriority.MOYENNE
    category: TaskCategory = TaskCategory.AUTRE
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    project_id: int
    assigned_to: Optional[int]
    parcelle_id: Optional[int]
    weather_dependent: bool = False
    min_temperature: Optional[float]
    max_temperature: Optional[float]
    max_wind_speed: Optional[float]
    max_precipitation: Optional[float]
    estimated_hours: Optional[float]

class TaskCreate(TaskBase):
    resources: Optional[List[TaskResourceBase]] = []
    dependencies: Optional[List[TaskDependencyBase]] = []

    @field_validator('due_date')
    @classmethod
    def due_date_after_start_date(cls, v: Optional[datetime], info) -> Optional[datetime]:
        start_date = info.data.get('start_date')
        if start_date and v and v < start_date:
            raise ValueError("La date d'échéance doit être postérieure à la date de début")
        return v

    @field_validator('max_temperature')
    @classmethod
    def validate_temperature_range(cls, v: Optional[float], info) -> Optional[float]:
        min_temp = info.data.get('min_temperature')
        if v is not None and min_temp is not None and v < min_temp:
            raise ValueError("La température maximale doit être supérieure à la température minimale")
        return v

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[TaskStatus]
    priority: Optional[TaskPriority]
    category: Optional[TaskCategory]
    start_date: Optional[datetime]
    due_date: Optional[datetime]
    assigned_to: Optional[int]
    weather_dependent: Optional[bool]
    min_temperature: Optional[float]
    max_temperature: Optional[float]
    max_wind_speed: Optional[float]
    max_precipitation: Optional[float]
    estimated_hours: Optional[float]
    actual_hours: Optional[float]
    completion_percentage: Optional[int] = Field(None, ge=0, le=100)

class TaskResourceCreate(TaskResourceBase):
    task_id: int

class TaskResourceUpdate(BaseModel):
    quantity_required: Optional[float]
    quantity_used: Optional[float]

class TaskCommentCreate(TaskCommentBase):
    task_id: int
    user_id: int

class TaskDependencyCreate(TaskDependencyBase):
    task_id: int

class TaskResource(TaskResourceBase):
    id: int
    task_id: int
    created_at: datetime
    updated_at: datetime

class TaskComment(TaskCommentBase):
    id: int
    task_id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TaskDependency(TaskDependencyBase):
    id: int
    task_id: int
    created_at: datetime
    updated_at: datetime

class Task(TaskBase):
    id: int
    completed_date: Optional[datetime]
    actual_hours: Optional[float]
    completion_percentage: int
    created_at: datetime
    updated_at: datetime
    resources: List[TaskResource] = []
    comments: List[TaskComment] = []
    dependencies: List[TaskDependency] = []

    class Config:
        from_attributes = True

class TaskWithWeather(Task):
    weather_suitable: bool
    weather_conditions: dict
    weather_warnings: List[str]

class TaskList(BaseModel):
    tasks: List[Task]
    total: int
    page: int
    size: int
    total_pages: int

    class Config:
        from_attributes = True
