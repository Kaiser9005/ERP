from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from fastapi import HTTPException

from models.tache import Tache, RessourceTache, CommentaireTache, DependanceTache, StatutTache
from models.resource import Resource, ResourceStatus
from schemas.tache import (
    TacheCreate, TacheUpdate, RessourceTacheCreate,
    CommentaireTacheCreate, TacheAvecMeteo
)
from services.weather_service import WeatherService

class TacheService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()

    async def create_task(self, task_data: TacheCreate) -> Tache:
        """Crée une nouvelle tâche avec ses ressources et dépendances"""
        # Création de la tâche
        task = Tache(**task_data.model_dump(exclude={'ressources', 'dependances'}))
        self.db.add(task)
        self.db.flush()  # Pour obtenir l'ID de la tâche

        # Ajout des ressources
        if task_data.ressources:
            for resource_data in task_data.ressources:
                # Vérification de la disponibilité des ressources
                resource = self.db.query(Resource).get(resource_data.ressource_id)
                if not resource:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Ressource {resource_data.ressource_id} non trouvée"
                    )
                if resource.quantity_available < resource_data.quantite_requise:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Quantité insuffisante pour la ressource {resource.name}"
                    )
                
                # Mise à jour des quantités de ressources
                resource.quantity_available -= resource_data.quantite_requise
                resource.quantity_reserved += resource_data.quantite_requise
                if resource.quantity_available == 0:
                    resource.status = ResourceStatus.EN_UTILISATION
                
                task_resource = RessourceTache(
                    tache_id=task.id,
                    ressource_id=resource_data.ressource_id,
                    quantite_requise=resource_data.quantite_requise
                )
                self.db.add(task_resource)

        # Ajout des dépendances
        if task_data.dependances:
            for dep_data in task_data.dependances:
                # Vérification de l'existence de la tâche dépendante
                dependent_task = self.db.query(Tache).get(dep_data.dependance_id)
                if not dependent_task:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Tâche dépendante {dep_data.dependance_id} non trouvée"
                    )
                
                # Vérification des dépendances circulaires
                if self.check_circular_dependency(task.id, dep_data.dependance_id):
                    raise HTTPException(
                        status_code=400,
                        detail="Dépendance circulaire détectée"
                    )
                
                dependency = DependanceTache(
                    tache_id=task.id,
                    dependance_id=dep_data.dependance_id,
                    type_dependance=dep_data.type_dependance
                )
                self.db.add(dependency)

        self.db.commit()
        self.db.refresh(task)
        return task

    def get_task(self, task_id: int) -> Tache:
        """Récupère une tâche par son ID"""
        task = self.db.query(Tache).get(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tâche non trouvée")
        return task

    async def get_task_with_weather(self, task_id: int) -> TacheAvecMeteo:
        """Récupère une tâche avec analyse des conditions météo"""
        task = self.get_task(task_id)
        
        if not task.dependant_meteo:
            return TacheAvecMeteo(
                **task.__dict__,
                conditions_favorables=True,
                conditions_meteo={},
                alertes_meteo=[]
            )

        # Récupération des conditions météo
        weather_data = await self.weather_service.get_agricultural_metrics()
        current_conditions = weather_data["current_conditions"]
        
        # Analyse des conditions
        warnings = []
        suitable = True

        if task.min_temperature is not None and current_conditions["temperature"] < task.min_temperature:
            warnings.append(f"Température trop basse ({current_conditions['temperature']}°C)")
            suitable = False

        if task.max_temperature is not None and current_conditions["temperature"] > task.max_temperature:
            warnings.append(f"Température trop élevée ({current_conditions['temperature']}°C)")
            suitable = False

        if task.max_wind_speed is not None and current_conditions["wind_speed"] > task.max_wind_speed:
            warnings.append(f"Vent trop fort ({current_conditions['wind_speed']} km/h)")
            suitable = False

        if task.max_precipitation is not None and current_conditions["precipitation"] > task.max_precipitation:
            warnings.append(f"Précipitations trop importantes ({current_conditions['precipitation']} mm)")
            suitable = False

        return TacheAvecMeteo(
            **task.__dict__,
            conditions_favorables=suitable,
            conditions_meteo=current_conditions,
            alertes_meteo=warnings
        )

    def update_task(self, task_id: int, task_data: TacheUpdate) -> Tache:
        """Met à jour une tâche"""
        task = self.get_task(task_id)
        
        # Mise à jour des champs
        for field, value in task_data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)

        # Si la tâche est marquée comme terminée
        if task_data.statut == StatutTache.TERMINEE and task.statut != StatutTache.TERMINEE:
            task.date_fin_reelle = datetime.now()
            task.pourcentage_completion = 100
            
            # Libération des ressources
            task_resources = self.db.query(RessourceTache).filter(
                RessourceTache.tache_id == task.id
            ).all()
            
            for task_resource in task_resources:
                resource = self.db.query(Resource).get(task_resource.ressource_id)
                if resource:
                    resource.quantity_available += task_resource.quantite_requise
                    resource.quantity_reserved -= task_resource.quantite_requise
                    if resource.quantity_available > 0:
                        resource.status = ResourceStatus.DISPONIBLE

        self.db.commit()
        self.db.refresh(task)
        return task

    def delete_task(self, task_id: int) -> None:
        """Supprime une tâche"""
        task = self.get_task(task_id)
        
        # Libération des ressources avant suppression
        task_resources = self.db.query(RessourceTache).filter(
            RessourceTache.tache_id == task.id
        ).all()
        
        for task_resource in task_resources:
            resource = self.db.query(Resource).get(task_resource.ressource_id)
            if resource:
                resource.quantity_available += task_resource.quantite_requise
                resource.quantity_reserved -= task_resource.quantite_requise
                if resource.quantity_available > 0:
                    resource.status = ResourceStatus.DISPONIBLE

        self.db.delete(task)
        self.db.commit()

    def get_tasks_by_project(
        self,
        project_id: int,
        page: int = 1,
        size: int = 20,
        status: Optional[StatutTache] = None,
        category: Optional[str] = None
    ) -> Dict[str, Any]:
        """Récupère les tâches d'un projet avec pagination et filtres"""
        query = self.db.query(Tache).filter(Tache.projet_id == project_id)
        
        if status:
            query = query.filter(Tache.statut == status)
        if category:
            query = query.filter(Tache.categorie == category)

        total = query.count()
        tasks = query.offset((page - 1) * size).limit(size).all()

        return {
            "taches": tasks,
            "total": total,
            "page": page,
            "taille": size,
            "total_pages": (total + size - 1) // size
        }

    def add_task_comment(self, comment_data: CommentaireTacheCreate) -> CommentaireTache:
        """Ajoute un commentaire à une tâche"""
        task = self.get_task(comment_data.tache_id)
        
        comment = CommentaireTache(**comment_data.model_dump())
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        
        return comment

    def update_task_resource(
        self,
        task_id: int,
        resource_id: int,
        quantity_used: float
    ) -> RessourceTache:
        """Met à jour l'utilisation des ressources d'une tâche"""
        task_resource = self.db.query(RessourceTache).filter(
            and_(
                RessourceTache.tache_id == task_id,
                RessourceTache.ressource_id == resource_id
            )
        ).first()

        if not task_resource:
            raise HTTPException(
                status_code=404,
                detail="Association tâche-ressource non trouvée"
            )

        if quantity_used > task_resource.quantite_requise:
            raise HTTPException(
                status_code=400,
                detail="La quantité utilisée ne peut pas dépasser la quantité requise"
            )

        task_resource.quantite_utilisee = quantity_used
        self.db.commit()
        self.db.refresh(task_resource)
        
        return task_resource

    def get_dependent_tasks(self, task_id: int) -> List[Tache]:
        """Récupère toutes les tâches qui dépendent de la tâche spécifiée"""
        dependencies = self.db.query(DependanceTache).filter(
            DependanceTache.dependance_id == task_id
        ).all()
        
        return [dep.tache for dep in dependencies]

    def check_circular_dependency(self, task_id: int, dependent_on_id: int) -> bool:
        """Vérifie s'il y a une dépendance circulaire"""
        def check_dependencies(current_id: int, target_id: int, visited: set) -> bool:
            if current_id in visited:
                return False
            
            visited.add(current_id)
            dependencies = self.db.query(DependanceTache).filter(
                DependanceTache.tache_id == current_id
            ).all()
            
            for dep in dependencies:
                if dep.dependance_id == target_id:
                    return True
                if check_dependencies(dep.dependance_id, target_id, visited):
                    return True
            
            return False

        return check_dependencies(dependent_on_id, task_id, set())

    async def get_weather_dependent_tasks(self) -> List[TacheAvecMeteo]:
        """Récupère toutes les tâches dépendantes de la météo avec leur statut"""
        tasks = self.db.query(Tache).filter(
            and_(
                Tache.dependant_meteo == True,
                Tache.statut.in_([StatutTache.A_FAIRE, StatutTache.EN_COURS])
            )
        ).all()

        result = []
        for task in tasks:
            task_with_weather = await self.get_task_with_weather(task.id)
            result.append(task_with_weather)

        return result