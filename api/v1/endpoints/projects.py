from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.auth import Utilisateur
from models.project import Project, Task, TaskComment, ProjectDocument
from schemas.project import (
    ProjectCreate, ProjectUpdate, ProjectResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    TaskCommentCreate, TaskCommentResponse,
    ProjectDocumentCreate, ProjectDocumentResponse
)
from api.v1.endpoints.auth import get_current_user
from services.storage_service import StorageService

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    statut: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère la liste des projets"""
    query = db.query(Project)
    if statut:
        query = query.filter(Project.statut == statut)
    return query.offset(skip).limit(limit).all()

@router.post("/", response_model=ProjectResponse)
async def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée un nouveau projet"""
    db_project = Project(**project.dict())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les détails d'un projet"""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    return project

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: str,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Met à jour un projet"""
    db_project = db.query(Project).filter(Project.id == project_id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Projet non trouvé")
    
    for key, value in project.dict(exclude_unset=True).items():
        setattr(db_project, key, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project

# Endpoints pour les tâches
@router.get("/{project_id}/tasks", response_model=List[TaskResponse])
async def get_project_tasks(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les tâches d'un projet"""
    return db.query(Task).filter(Task.projet_id == project_id).all()

@router.post("/tasks", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Crée une nouvelle tâche"""
    db_task = Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: str,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Met à jour une tâche"""
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    
    for key, value in task.dict(exclude_unset=True).items():
        setattr(db_task, key, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task

# Endpoints pour les commentaires
@router.post("/tasks/{task_id}/comments", response_model=TaskCommentResponse)
async def create_task_comment(
    task_id: str,
    comment: TaskCommentCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Ajoute un commentaire à une tâche"""
    db_comment = TaskComment(
        **comment.dict(),
        auteur_id=current_user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# Endpoints pour les documents
@router.post("/{project_id}/documents", response_model=ProjectDocumentResponse)
async def upload_project_document(
    project_id: str,
    file: UploadFile = File(...),
    type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Upload un document pour un projet"""
    storage = StorageService()
    file_path = await storage.save_file(file, f"projects/{project_id}/documents")
    
    document = ProjectDocument(
        projet_id=project_id,
        nom=file.filename,
        type=type,
        chemin_fichier=file_path,
        uploaded_by_id=current_user.id
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    return document