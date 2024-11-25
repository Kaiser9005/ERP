"""Service d'optimisation des ressources des projets."""

from typing import Dict, Any, List
from datetime import date, timedelta
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus
from sqlalchemy.orm import Session

from models.task import Task
from models.resource import Resource
from services.cache_service import CacheService

class ResourceOptimizer:
    """Optimiseur de ressources pour les projets."""
    
    def __init__(self, db: Session):
        """Initialisation de l'optimiseur."""
        self.db = db
        self.cache = CacheService()

    async def optimize_allocation(
        self,
        project_id: str,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Optimise l'allocation des ressources du projet."""
        # Vérification du cache
        cache_key = f"resource_allocation_{project_id}_{start_date}_{end_date}"
        cached = await self.cache.get(cache_key)
        if cached:
            return cached

        # Récupération données
        tasks = await self._get_tasks(project_id)
        resources = await self._get_resources(project_id)
        
        # Création du problème d'optimisation
        prob = LpProblem("resource_allocation", LpMinimize)
        
        # Variables de décision
        x = {}  # x[t,r,d] = 1 si ressource r est allouée à tâche t le jour d
        for task in tasks:
            task_days = (task["end_date"] - task["start_date"]).days + 1
            for resource in resources:
                for day in range(task_days):
                    x[task["id"], resource["id"], day] = LpVariable(
                        f'x_{task["id"]}_{resource["id"]}_{day}',
                        0, 1, 'Binary'
                    )

        # Fonction objectif: minimiser le coût total
        prob += lpSum(
            x[t["id"], r["id"], d] * r["cost"]
            for t in tasks
            for r in resources
            for d in range((t["end_date"] - t["start_date"]).days + 1)
        )

        # Contraintes
        for task in tasks:
            task_days = (task["end_date"] - task["start_date"]).days + 1
            
            # Ressources nécessaires
            prob += lpSum(
                x[task["id"], r["id"], d]
                for r in resources
                for d in range(task_days)
            ) >= task.get("resources_needed", 1)
            
            # Dépendances
            if task.get("dependencies"):
                for dep_id in task["dependencies"]:
                    dep_task = next(t for t in tasks if t["id"] == dep_id)
                    prob += task["start_date"] >= dep_task["end_date"]

        # Disponibilité des ressources
        for resource in resources:
            for day in range((end_date - start_date).days + 1):
                prob += lpSum(
                    x[t["id"], resource["id"], d]
                    for t in tasks
                    for d in range((t["end_date"] - t["start_date"]).days + 1)
                    if d == day
                ) <= resource["availability"]

        # Résolution
        prob.solve()
        
        # Analyse des résultats
        if LpStatus[prob.status] == 'Optimal':
            result = self._analyze_solution(x, tasks, resources, prob)
            await self.cache.set(cache_key, result, expire=3600)
            return result
        
        return {
            "optimal_allocation": [],
            "efficiency_score": 0.0,
            "bottlenecks": [],
            "recommendations": ["Impossible de trouver une allocation optimale"]
        }

    async def _get_tasks(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les tâches du projet."""
        tasks = self.db.query(Task).filter(Task.project_id == project_id).all()
        return [{
            "id": task.id,
            "name": task.name,
            "start_date": task.start_date,
            "end_date": task.end_date,
            "dependencies": task.dependencies,
            "resources_needed": task.resources_needed
        } for task in tasks]

    async def _get_resources(self, project_id: str) -> List[Dict[str, Any]]:
        """Récupère les ressources disponibles."""
        resources = self.db.query(Resource).filter(
            Resource.project_id == project_id,
            Resource.availability > 0
        ).all()
        return [{
            "id": resource.id,
            "name": resource.name,
            "availability": resource.availability / 100.0,
            "cost": float(resource.cost)
        } for resource in resources]

    def _analyze_solution(
        self,
        x: Dict[Any, LpVariable],
        tasks: List[Dict[str, Any]],
        resources: List[Dict[str, Any]],
        prob: LpProblem
    ) -> Dict[str, Any]:
        """Analyse la solution d'optimisation."""
        # Extraction allocation
        allocation = []
        for task in tasks:
            task_resources = []
            task_days = (task["end_date"] - task["start_date"]).days + 1
            
            for resource in resources:
                days = []
                for day in range(task_days):
                    if x[task["id"], resource["id"], day].value() > 0.5:
                        days.append(day)
                
                if days:
                    task_resources.append({
                        "resource_id": resource["id"],
                        "days": days
                    })
            
            if task_resources:
                allocation.append({
                    "task_id": task["id"],
                    "resources": task_resources,
                    "start_date": task["start_date"],
                    "end_date": task["end_date"]
                })

        # Calcul efficacité
        total_days = sum(
            (t["end_date"] - t["start_date"]).days + 1
            for t in tasks
        )
        total_allocations = sum(
            x[t["id"], r["id"], d].value()
            for t in tasks
            for r in resources
            for d in range((t["end_date"] - t["start_date"]).days + 1)
        )
        efficiency = total_allocations / (len(resources) * total_days)

        # Identification goulots
        bottlenecks = []
        for resource in resources:
            utilization = {}
            for task in tasks:
                task_days = (task["end_date"] - task["start_date"]).days + 1
                for day in range(task_days):
                    month = (task["start_date"] + timedelta(days=day)).strftime("%Y-%m")
                    if month not in utilization:
                        utilization[month] = 0
                    if x[task["id"], resource["id"], day].value() > 0.5:
                        utilization[month] += 1
            
            for month, days in utilization.items():
                if days / 30 > 0.8:  # Seuil critique d'utilisation
                    bottlenecks.append({
                        "resource": resource["id"],
                        "period": month,
                        "utilization": days / 30
                    })

        # Génération recommandations
        recommendations = []
        if efficiency < 0.5:
            recommendations.append(
                "L'utilisation des ressources est sous-optimale. "
                "Considérer la réduction du nombre de ressources."
            )
        elif efficiency > 0.9:
            recommendations.append(
                "Les ressources sont très sollicitées. "
                "Considérer l'ajout de ressources supplémentaires."
            )
        
        for bottleneck in bottlenecks:
            recommendations.append(
                f"Surcharge de la ressource {bottleneck['resource']} "
                f"en {bottleneck['period']}. "
                f"Prévoir des alternatives."
            )
        
        if len(allocation) < len(tasks):
            recommendations.append(
                "Certaines tâches n'ont pas de ressources allouées. "
                "Revoir la planification."
            )

        return {
            "optimal_allocation": allocation,
            "efficiency_score": efficiency,
            "bottlenecks": bottlenecks,
            "recommendations": recommendations
        }
