from typing import Dict, List, Any
from datetime import datetime, timedelta

from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.projects_ml_service import ProjectsMLService
from services.cache_service import CacheService

class DashboardUnifiedService:
    def __init__(
        self,
        hr_service: HRAnalyticsService,
        production_service: ProductionService,
        finance_service: FinanceService,
        inventory_service: InventoryService,
        weather_service: WeatherService,
        projects_ml_service: ProjectsMLService,
        cache_service: CacheService
    ):
        self.hr_service = hr_service
        self.production_service = production_service
        self.finance_service = finance_service
        self.inventory_service = inventory_service
        self.weather_service = weather_service
        self.projects_ml_service = projects_ml_service
        self.cache_service = cache_service
        self.cache_ttl = 900  # 15 minutes

    async def get_unified_dashboard_data(self) -> Dict[str, Any]:
        """
        Récupère et agrège les données de tous les modules pour le dashboard unifié.
        Utilise le cache pour optimiser les performances.
        """
        cache_key = "unified_dashboard_data"
        cached_data = await self.cache_service.get(cache_key)
        
        if cached_data:
            return cached_data

        data = {
            "timestamp": datetime.now().isoformat(),
            "modules": {
                "hr": await self._get_hr_summary(),
                "production": await self._get_production_summary(),
                "finance": await self._get_finance_summary(),
                "inventory": await self._get_inventory_summary(),
                "weather": await self._get_weather_summary(),
                "projects": await self._get_projects_summary()
            },
            "alerts": await self._get_critical_alerts(),
            "predictions": await self._get_ml_predictions()
        }

        await self.cache_service.set(cache_key, data, self.cache_ttl)
        return data

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

    async def _get_projects_summary(self) -> Dict[str, Any]:
        """Résumé des projets et prédictions ML."""
        return {
            "active_projects": await self.projects_ml_service.get_active_projects_count(),
            "completion_predictions": await self.projects_ml_service.get_completion_predictions(),
            "resource_optimization": await self.projects_ml_service.get_resource_optimization(),
            "recent_activities": await self.projects_ml_service.get_recent_activities(limit=5)
        }

    async def _get_critical_alerts(self) -> List[Dict[str, Any]]:
        """Agrège les alertes critiques de tous les modules."""
        alerts = []
        
        # Alertes RH
        hr_alerts = await self.hr_service.get_critical_alerts()
        alerts.extend(hr_alerts)
        
        # Alertes Production
        prod_alerts = await self.production_service.get_critical_alerts()
        alerts.extend(prod_alerts)
        
        # Alertes Finance
        finance_alerts = await self.finance_service.get_critical_alerts()
        alerts.extend(finance_alerts)
        
        # Alertes Inventaire
        inventory_alerts = await self.inventory_service.get_critical_alerts()
        alerts.extend(inventory_alerts)
        
        # Alertes Météo
        weather_alerts = await self.weather_service.get_critical_alerts()
        alerts.extend(weather_alerts)
        
        return sorted(alerts, key=lambda x: x.get('priority', 0), reverse=True)

    async def _get_ml_predictions(self) -> Dict[str, Any]:
        """Agrège les prédictions ML de tous les modules."""
        return {
            "production": await self.projects_ml_service.get_production_predictions(),
            "finance": await self.projects_ml_service.get_finance_predictions(),
            "inventory": await self.projects_ml_service.get_inventory_predictions(),
            "hr": await self.projects_ml_service.get_hr_predictions()
        }

    async def get_module_details(self, module: str) -> Dict[str, Any]:
        """
        Récupère les détails complets d'un module spécifique.
        Utilisé pour l'expansion des widgets du dashboard.
        """
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
        elif module == "projects":
            return await self.projects_ml_service.get_detailed_analytics()
        else:
            raise ValueError(f"Module inconnu: {module}")
