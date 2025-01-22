from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from db.database import get_db
from services.tache_service import TacheService
from schemas.tache import (
    Tache, TacheCreate, TacheUpdate, TacheAvecMeteo,
    CommentaireTache, CommentaireTacheCreate, ListeTaches
)
from models.tache import StatutTache, CategorieTache

router = APIRouter()

@router.post("/taches", response_model=Tache)
async def creer_tache(
    tache_data: TacheCreate,
    db: Session = Depends(get_db)
):
    """
    Crée une nouvelle tâche avec ses ressources et dépendances associées.
    """
    tache_service = TacheService(db)
    return await tache_service.create_task(tache_data)

@router.get("/taches/{tache_id}", response_model=Tache)
def obtenir_tache(
    tache_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une tâche par son ID.
    """
    tache_service = TacheService(db)
    return tache_service.get_task(tache_id)

@router.get("/taches/{tache_id}/meteo", response_model=TacheAvecMeteo)
async def obtenir_tache_avec_meteo(
    tache_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère une tâche avec analyse des conditions météo actuelles.
    """
    tache_service = TacheService(db)
    return await tache_service.get_task_with_weather(tache_id)

@router.put("/taches/{tache_id}", response_model=Tache)
def mettre_a_jour_tache(
    tache_id: int,
    tache_data: TacheUpdate,
    db: Session = Depends(get_db)
):
    """
    Met à jour une tâche existante.
    """
    tache_service = TacheService(db)
    return tache_service.update_task(tache_id, tache_data)

@router.delete("/taches/{tache_id}")
def supprimer_tache(
    tache_id: int,
    db: Session = Depends(get_db)
):
    """
    Supprime une tâche et libère ses ressources.
    """
    tache_service = TacheService(db)
    tache_service.delete_task(tache_id)
    return {"message": "Tâche supprimée avec succès"}

@router.get("/projets/{projet_id}/taches", response_model=ListeTaches)
def obtenir_taches_projet(
    projet_id: int,
    page: int = Query(1, ge=1),
    taille: int = Query(20, ge=1, le=100),
    statut: Optional[StatutTache] = None,
    categorie: Optional[CategorieTache] = None,
    db: Session = Depends(get_db)
):
    """
    Récupère les tâches d'un projet avec pagination et filtres.
    """
    tache_service = TacheService(db)
    return tache_service.get_tasks_by_project(
        project_id=projet_id,
        page=page,
        size=taille,
        status=statut,
        category=categorie
    )

@router.post("/taches/{tache_id}/commentaires", response_model=CommentaireTache)
def ajouter_commentaire_tache(
    tache_id: int,
    commentaire_data: CommentaireTacheCreate,
    db: Session = Depends(get_db)
):
    """
    Ajoute un commentaire à une tâche.
    """
    tache_service = TacheService(db)
    return tache_service.add_task_comment(commentaire_data)

@router.put("/taches/{tache_id}/ressources/{ressource_id}")
def mettre_a_jour_utilisation_ressource(
    tache_id: int,
    ressource_id: int,
    quantite_utilisee: float = Query(..., gt=0),
    db: Session = Depends(get_db)
):
    """
    Met à jour l'utilisation d'une ressource pour une tâche.
    """
    tache_service = TacheService(db)
    tache_service.update_task_resource(tache_id, ressource_id, quantite_utilisee)
    return {"message": "Utilisation de la ressource mise à jour"}

@router.get("/taches/{tache_id}/dependances", response_model=List[Tache])
def obtenir_dependances_tache(
    tache_id: int,
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les tâches qui dépendent de la tâche spécifiée.
    """
    tache_service = TacheService(db)
    return tache_service.get_dependent_tasks(tache_id)

@router.get("/taches/dependantes-meteo", response_model=List[TacheAvecMeteo])
async def obtenir_taches_dependantes_meteo(
    db: Session = Depends(get_db)
):
    """
    Récupère toutes les tâches dépendantes de la météo avec leur statut actuel.
    """
    tache_service = TacheService(db)
    return await tache_service.get_weather_dependent_tasks()