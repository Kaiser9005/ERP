from pydantic import BaseModel, UUID4
from datetime import date, datetime
from typing import Optional, List, Dict
from models.project import ProjectStatus, TaskPriority, TaskStatus

class ProjectBase(BaseModel):
    code: str
    nom: str
    description: Optional[str]
    date_debut: date
    date_fin_prevue: date
    statut: ProjectStatus
    budget: Optional[float]
    responsable_id: UUID4
    objectifs: Optional[List[str]]
    risques: Optional[List[Dict[str, str]]]

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    code: Optional[str]
    nom: Optional[str]
    date_debut: Optional[date]
    date_fin_prevue: Optional[date]
    date_fin_reelle: Optional[date]
    statut: Optional[ProjectStatus]

class ProjectResponse(ProjectBase):
    id: UUID4
    date_fin_reelle: Optional[date]
    
    class Config:
        orm_mode = True

class TaskBase(BaseModel):
    projet_id: UUID4
    titre: str
    description: Optional[str]
    priorite: TaskPriority
    date_fin_prevue: datetime
    assignee_id: Optional[UUID4]
    temps_estime: Optional[float]
    dependances: Optional[List[UUID4]]

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    titre: Optional[str]
    priorite: Optional[TaskPriority]
    statut: Optional[TaskStatus]
    date_fin_prevue: Optional[datetime]
    date_fin_reelle: Optional[datetime]
    temps_passe: Optional[float]

class TaskResponse(TaskBase):
    id: UUID4
    statut: TaskStatus
    date_debut: Optional[datetime]
    date_fin_reelle: Optional[datetime]
    temps_passe: Optional[float]
    
    class Config:
        orm_mode = True

class TaskCommentBase(BaseModel):
    tache_id: UUID4
    contenu: str

class TaskCommentCreate(TaskCommentBase):
    pass

class TaskCommentResponse(TaskCommentBase):
    id: UUID4
    auteur_id: UUID4
    date_creation: datetime
    
    class Config:
        orm_mode = True

class ProjectDocumentBase(BaseModel):
    projet_id: UUID4
    nom: str
    type: Optional[str]

class ProjectDocumentCreate(ProjectDocumentBase):
    chemin_fichier: str

class ProjectDocumentResponse(ProjectDocumentBase):
    id: UUID4
    chemin_fichier: str
    date_upload: datetime
    uploaded_by_id: UUID4
    
    class Config:
        orm_mode = True