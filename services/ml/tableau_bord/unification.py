"""
Service d'unification du tableau de bord avec intégration ML.
Regroupe les données de tous les modules pour présentation unifiée.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.ml.projets.service import ProjetsMLService
from services.cache_service import CacheService

from .alertes import get_critical_alerts, AlertPriority
from .predictions import get_ml_predictions

class TableauBordUnifieService:
    def __init__(
        self,
        hr_service: HRAnalyticsService,
        production_service: ProductionService,
        finance_service: FinanceService,
        inventory_service: InventoryService,
        weather_service: WeatherService,
        projets_ml: ProjetsMLService,
        cache_service: CacheService
    ):
        self.hr_service = hr_service
        self.production_service = production_service
        self.finance_service = finance_service
        self.inventory_service = inventory_service
        self.weather_service = weather_service
        self.projets_ml = projets_ml
        self.cache_service = cache_service
        self.cache_ttl = 900  # 15 minutes

    async def get_unified_dashboard_data(self) -> Dict[str, Any]:
        """
        Récupère et agrège les données de tous les modules pour le tableau de bord unifié.
        Utilise le cache pour optimiser les performances.
        """
        try:
            cache_key = "unified_dashboard_data"
            cached_data = await self.cache_service.get(cache_key)
            
            if cached_data:
                return cached_data

            data = {
                "timestamp": datetime.now().isoformat(),
                "modules": {
                    "hr": await self._get_module_data(self._get_hr_summary, "hr"),
                    "production": await self._get_module_data(self._get_production_summary, "production"),
                    "finance": await self._get_module_data(self._get_finance_summary, "finance"),
                    "inventory": await self._get_module_data(self._get_inventory_summary, "inventory"),
                    "weather": await self._get_module_data(self._get_weather_summary, "weather"),
                    "projets": await self._get_module_data(self._get_projets_summary, "projets")
                },
                "alerts": await get_critical_alerts(
                    hr_service=self.hr_service,
                    production_service=self.production_service,
                    finance_service=self.finance_service,
                    inventory_service=self.inventory_service,
                    weather_service=self.weather_service
                ),
                "predictions": await get_ml_predictions(
                    projets_ml=self.projets_ml,
                    finance_service=self.finance_service,
                    inventory_service=self.inventory_service,
                    hr_analytics=self.hr_service,
                    cache_service=self.cache_service
                )
            }

            await self.cache_service.set(cache_key, data, self.cache_ttl)
            return data
            
        except Exception as e:
            # En cas d'erreur, on retourne une structure minimale avec une alerte
            return {
                "timestamp": datetime.now().isoformat(),
                "modules": {},
                "alerts": [{
                    "type": "SYSTEM",
                    "priority": AlertPriority.CRITIQUE,
                    "message": f"Erreur lors de la récupération des données: {str(e)}",
                    "source": "tableau_bord"
                }],
                "predictions": {}
            }

    async def _get_module_data(self, func: callable, module_name: str) -> Dict[str, Any]:
        """
        Récupère les données d'un module avec gestion des erreurs.
        
        Args:
            func: Fonction à exécuter pour obtenir les données
            module_name: Nom du module pour les messages d'erreur
            
        Returns:
            Données du module ou message d'erreur
        """
        try:
            return await func()
        except Exception as e:
            return {
                "error": True,
                "message": f"Erreur {module_name}: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }

    async def _get_hr_summary(self) -> Dict[str, Any]:
        """Résumé des indicateurs RH clés."""
        return {
            "total_employees": await self.hr_service.get_total_employees(),
            "active_contracts": await self.hr_service.get_active_contracts_count(),
            "completed_trainings": await self.hr_service.get_completed_trainings_count(),
            "training_completion_rate": await self.hr_service.get_training_completion_rate(),
            "recent_activities": await self.hr_service.get_recent_activities(limit=5)
        }

    async def _get_production_summary(self) -> Dict[str, Any]:
        """Résumé des indicateurs de production clés."""
        return {
            "daily_production": await self.production_service.get_daily_production(),
            "efficiency_rate": await self.production_service.get_efficiency_rate(),
            "active_sensors": await self.production_service.get_active_sensors_count(),
            "quality_metrics": await self.production_service.get_quality_metrics(),
            "recent_activities": await self.production_service.get_recent_activities(limit=5)
        }

    async def _get_finance_summary(self) -> Dict[str, Any]:
        """Résumé des indicateurs financiers clés."""
        return {
            "daily_revenue": await self.finance_service.get_daily_revenue(),
            "monthly_expenses": await self.finance_service.get_monthly_expenses(),
            "cash_flow": await self.finance_service.get_cash_flow(),
            "budget_status": await self.finance_service.get_budget_status(),
            "recent_transactions": await self.finance_service.get_recent_transactions(limit=5)
        }

    async def _get_inventory_summary(self) -> Dict[str, Any]:
        """Résumé des indicateurs d'inventaire clés."""
        return {
            "total_items": await self.inventory_service.get_total_items(),
            "low_stock_items": await self.inventory_service.get_low_stock_items(),
            "stock_value": await self.inventory_service.get_total_stock_value(),
            "recent_movements": await self.inventory_service.get_recent_movements(limit=5)
        }

    async def _get_weather_summary(self) -> Dict[str, Any]:
        """Résumé des conditions météorologiques et impacts."""
        return {
            "current_conditions": await self.weather_service.get_current_conditions(),
            "daily_forecast": await self.weather_service.get_daily_forecast(),
            "alerts": await self.weather_service.get_active_alerts(),
            "production_impact": await self.weather_service.get_production_impact()
        }

    async def _get_projets_summary(self) -> Dict[str, Any]:
        """Résumé des projets et prédictions ML."""
        return {
            "active_projects": await self.projets_ml.get_active_projects_count(),
            "completion_predictions": await self.projets_ml.get_completion_predictions(),
            "resource_optimization": await self.projets_ml.get_resource_optimization(),
            "recent_activities": await self.projets_ml.get_recent_activities(limit=5)
        }

    async def get_module_details(self, module: str) -> Dict[str, Any]:
        """
        Récupère les détails complets d'un module spécifique.
        Utilisé pour l'expansion des widgets du dashboard.
        """
        try:
            if module == "hr":
                return await self.hr_service.get_detailed_analytics()
            elif module == "production":
                return await self.production_service.get_detailed_analytics()
            elif module == "finance":
                return await self.finance_service.get_detailed_analytics()
            elif module == "inventory":
                return await self.inventory_service.get_detailed_analytics()
            elif module == "weather":
                return await self.weather_service.get_detailed_analytics()
            elif module == "projets":
                return await self.projets_ml.get_detailed_analytics()
            else:
                raise ValueError(f"Module inconnu: {module}")
        except Exception as e:
            return {
                "error": True,
                "message": f"Erreur lors de la récupération des détails du module {module}: {str(e)}",
                "timestamp": datetime.now().isoformat()
            }
