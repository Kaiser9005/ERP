"""
Service d'analytics cross-module avec ML
Basé sur l'intégration finance-comptabilité et enrichi pour tous les modules
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session

from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService
from services.projects_ml_service import ProjectsMLService
from services.cache_service import CacheService
from services.storage_service import StorageService

class CrossModuleAnalytics:
    """Service d'analytics cross-module"""
    
    def __init__(self, db: Session):
        """Initialisation du service."""
        self.db = db
        self.hr_service = HRAnalyticsService(db)
        self.production_service = ProductionService(db)
        self.finance_service = FinanceService(db)
        self.inventory_service = InventoryService(db)
        self.weather_service = WeatherService(db)
        self.projects_ml_service = ProjectsMLService(db)
        self.cache = CacheService()
        self.storage = StorageService()
        self.cache_ttl = 900  # 15 minutes

    async def get_unified_analytics(
        self,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Récupère et agrège les analytics de tous les modules.
        Utilise le cache pour optimiser les performances.
        """
        # Cache key
        cache_key = f"unified_analytics_{date_debut}_{date_fin}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)

        data = {
            "timestamp": datetime.now().isoformat(),
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            },
            "modules": {
                "hr": await self._get_hr_analytics(date_debut, date_fin),
                "production": await self._get_production_analytics(date_debut, date_fin),
                "finance": await self._get_finance_analytics(date_debut, date_fin),
                "inventory": await self._get_inventory_analytics(date_debut, date_fin),
                "weather": await self._get_weather_analytics(date_debut, date_fin),
                "projects": await self._get_projects_analytics(date_debut, date_fin)
            },
            "correlations": await self._analyze_correlations(date_debut, date_fin),
            "predictions": await self._get_ml_predictions(date_debut, date_fin),
            "recommendations": await self._generate_cross_module_recommendations(date_debut, date_fin)
        }

        await self.cache.set(cache_key, data, self.cache_ttl)
        return data

    async def _get_hr_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics RH avec impact sur autres modules."""
        analytics = await self.hr_service.get_detailed_analytics()
        
        # Impact sur production
        production_impact = {
            "productivity": await self._analyze_hr_productivity_impact(),
            "skills_coverage": await self._analyze_skills_coverage(),
            "training_impact": await self._analyze_training_impact()
        }
        
        # Impact sur finance
        finance_impact = {
            "labor_costs": await self._analyze_labor_costs(),
            "training_roi": await self._analyze_training_roi(),
            "productivity_value": await self._analyze_productivity_value()
        }
        
        return {
            "analytics": analytics,
            "production_impact": production_impact,
            "finance_impact": finance_impact,
            "weather_impact": await self._analyze_weather_hr_impact()
        }

    async def _get_production_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics production avec impact sur autres modules."""
        analytics = await self.production_service.get_detailed_analytics()
        
        # Impact sur RH
        hr_impact = {
            "workload": await self._analyze_production_workload(),
            "skills_required": await self._analyze_skills_requirements(),
            "schedule_impact": await self._analyze_schedule_impact()
        }
        
        # Impact sur finance
        finance_impact = {
            "production_costs": await self._analyze_production_costs(),
            "revenue_impact": await self._analyze_revenue_impact(),
            "efficiency_savings": await self._analyze_efficiency_savings()
        }
        
        return {
            "analytics": analytics,
            "hr_impact": hr_impact,
            "finance_impact": finance_impact,
            "weather_impact": await self._analyze_weather_production_impact()
        }

    async def _get_finance_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics finance avec impact sur autres modules."""
        analytics = await self.finance_service.get_detailed_analytics()
        
        # Impact sur RH
        hr_impact = {
            "budget_constraints": await self._analyze_budget_impact_hr(),
            "hiring_capacity": await self._analyze_hiring_capacity(),
            "training_budget": await self._analyze_training_budget()
        }
        
        # Impact sur production
        production_impact = {
            "investment_capacity": await self._analyze_investment_capacity(),
            "maintenance_budget": await self._analyze_maintenance_budget(),
            "expansion_potential": await self._analyze_expansion_potential()
        }
        
        return {
            "analytics": analytics,
            "hr_impact": hr_impact,
            "production_impact": production_impact,
            "weather_impact": await self._analyze_weather_finance_impact()
        }

    async def _get_inventory_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics inventaire avec impact sur autres modules."""
        analytics = await self.inventory_service.get_detailed_analytics()
        
        # Impact sur production
        production_impact = {
            "stock_availability": await self._analyze_stock_availability(),
            "production_constraints": await self._analyze_production_constraints(),
            "quality_impact": await self._analyze_quality_impact()
        }
        
        # Impact sur finance
        finance_impact = {
            "storage_costs": await self._analyze_storage_costs(),
            "stock_value": await self._analyze_stock_value(),
            "turnover_rate": await self._analyze_turnover_rate()
        }
        
        return {
            "analytics": analytics,
            "production_impact": production_impact,
            "finance_impact": finance_impact,
            "weather_impact": await self._analyze_weather_inventory_impact()
        }

    async def _get_weather_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics météo avec impact sur tous les modules."""
        return {
            "current": await self.weather_service.get_current_conditions(),
            "forecast": await self.weather_service.get_daily_forecast(),
            "alerts": await self.weather_service.get_active_alerts(),
            "impact": {
                "production": await self._analyze_weather_production_impact(),
                "hr": await self._analyze_weather_hr_impact(),
                "finance": await self._analyze_weather_finance_impact(),
                "inventory": await self._analyze_weather_inventory_impact()
            }
        }

    async def _get_projects_analytics(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analytics projets avec ML et impact sur autres modules."""
        return {
            "active_projects": await self.projects_ml_service.get_active_projects_count(),
            "completion_predictions": await self.projects_ml_service.get_completion_predictions(),
            "resource_optimization": await self.projects_ml_service.get_resource_optimization(),
            "impact": {
                "hr": await self._analyze_projects_hr_impact(),
                "production": await self._analyze_projects_production_impact(),
                "finance": await self._analyze_projects_finance_impact()
            }
        }

    async def _analyze_correlations(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse des corrélations entre modules."""
        return {
            "hr_production": await self._analyze_hr_production_correlation(),
            "production_finance": await self._analyze_production_finance_correlation(),
            "weather_global": await self._analyze_weather_global_correlation(),
            "inventory_finance": await self._analyze_inventory_finance_correlation()
        }

    async def _get_ml_predictions(
        self,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Prédictions ML cross-module."""
        return {
            "hr": await self.projects_ml_service.get_hr_predictions(),
            "production": await self.projects_ml_service.get_production_predictions(),
            "finance": await self.projects_ml_service.get_finance_predictions(),
            "inventory": await self.projects_ml_service.get_inventory_predictions(),
            "cross_module": await self._generate_cross_module_predictions()
        }

    async def _generate_cross_module_recommendations(
        self,
        date_debut: date,
        date_fin: date
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations cross-module basées sur ML."""
        recommendations = []
        
        # Analyse des corrélations
        correlations = await self._analyze_correlations(date_debut, date_fin)
        
        # Recommandations basées sur les corrélations fortes
        for correlation, value in correlations.items():
            if value > 0.8:  # Corrélation forte
                recommendations.append({
                    "type": "CORRELATION",
                    "priority": "HIGH",
                    "modules": correlation.split("_"),
                    "description": f"Forte corrélation {correlation}",
                    "actions": await self._generate_correlation_actions(correlation)
                })
                
        # Recommandations ML
        predictions = await self._get_ml_predictions(date_debut, date_fin)
        for module, prediction in predictions.items():
            if prediction.get("risk_level", 0) > 0.7:  # Risque élevé
                recommendations.append({
                    "type": "ML_PREDICTION",
                    "priority": "HIGH",
                    "module": module,
                    "description": f"Risque élevé détecté pour {module}",
                    "actions": prediction.get("recommended_actions", [])
                })
                
        # Recommandations d'optimisation
        optimizations = await self._analyze_optimization_opportunities()
        for opt in optimizations:
            if opt["potential_savings"] > 1000:  # Seuil significatif
                recommendations.append({
                    "type": "OPTIMIZATION",
                    "priority": "MEDIUM",
                    "modules": opt["modules"],
                    "description": opt["description"],
                    "actions": opt["actions"],
                    "savings": opt["potential_savings"]
                })
                
        return sorted(recommendations, key=lambda x: x["priority"])

    # Méthodes d'analyse spécifiques
    async def _analyze_hr_productivity_impact(self) -> Dict[str, Any]:
        """Analyse l'impact de la productivité RH."""
        return await self.hr_service.analyze_productivity_impact()

    async def _analyze_skills_coverage(self) -> Dict[str, Any]:
        """Analyse la couverture des compétences."""
        return await self.hr_service.analyze_skills_coverage()

    async def _analyze_training_impact(self) -> Dict[str, Any]:
        """Analyse l'impact des formations."""
        return await self.hr_service.analyze_training_impact()

    async def _analyze_labor_costs(self) -> Dict[str, Any]:
        """Analyse les coûts de main d'œuvre."""
        return await self.finance_service.analyze_labor_costs()

    async def _analyze_training_roi(self) -> Dict[str, Any]:
        """Analyse le ROI des formations."""
        return await self.finance_service.analyze_training_roi()

    async def _analyze_productivity_value(self) -> Dict[str, Any]:
        """Analyse la valeur de la productivité."""
        return await self.finance_service.analyze_productivity_value()

    async def _analyze_weather_hr_impact(self) -> Dict[str, Any]:
        """Analyse l'impact météo sur les RH."""
        return await self.weather_service.analyze_hr_impact()

    async def _analyze_production_workload(self) -> Dict[str, Any]:
        """Analyse la charge de travail production."""
        return await self.production_service.analyze_workload()

    async def _analyze_skills_requirements(self) -> Dict[str, Any]:
        """Analyse les besoins en compétences."""
        return await self.production_service.analyze_skills_requirements()

    async def _analyze_schedule_impact(self) -> Dict[str, Any]:
        """Analyse l'impact sur les plannings."""
        return await self.production_service.analyze_schedule_impact()

    async def _analyze_production_costs(self) -> Dict[str, Any]:
        """Analyse les coûts de production."""
        return await self.finance_service.analyze_production_costs()

    async def _analyze_revenue_impact(self) -> Dict[str, Any]:
        """Analyse l'impact sur les revenus."""
        return await self.finance_service.analyze_revenue_impact()

    async def _analyze_efficiency_savings(self) -> Dict[str, Any]:
        """Analyse les économies d'efficacité."""
        return await self.finance_service.analyze_efficiency_savings()

    async def _analyze_weather_production_impact(self) -> Dict[str, Any]:
        """Analyse l'impact météo sur la production."""
        return await self.weather_service.analyze_production_impact()

    async def _analyze_budget_impact_hr(self) -> Dict[str, Any]:
        """Analyse l'impact budgétaire sur les RH."""
        return await self.finance_service.analyze_budget_impact_hr()

    async def _analyze_hiring_capacity(self) -> Dict[str, Any]:
        """Analyse la capacité de recrutement."""
        return await self.finance_service.analyze_hiring_capacity()

    async def _analyze_training_budget(self) -> Dict[str, Any]:
        """Analyse le budget formation."""
        return await self.finance_service.analyze_training_budget()

    async def _analyze_investment_capacity(self) -> Dict[str, Any]:
        """Analyse la capacité d'investissement."""
        return await self.finance_service.analyze_investment_capacity()

    async def _analyze_maintenance_budget(self) -> Dict[str, Any]:
        """Analyse le budget maintenance."""
        return await self.finance_service.analyze_maintenance_budget()

    async def _analyze_expansion_potential(self) -> Dict[str, Any]:
        """Analyse le potentiel d'expansion."""
        return await self.finance_service.analyze_expansion_potential()

    async def _analyze_weather_finance_impact(self) -> Dict[str, Any]:
        """Analyse l'impact météo sur les finances."""
        return await self.weather_service.analyze_finance_impact()

    async def _analyze_stock_availability(self) -> Dict[str, Any]:
        """Analyse la disponibilité des stocks."""
        return await self.inventory_service.analyze_stock_availability()

    async def _analyze_production_constraints(self) -> Dict[str, Any]:
        """Analyse les contraintes de production."""
        return await self.inventory_service.analyze_production_constraints()

    async def _analyze_quality_impact(self) -> Dict[str, Any]:
        """Analyse l'impact sur la qualité."""
        return await self.inventory_service.analyze_quality_impact()

    async def _analyze_storage_costs(self) -> Dict[str, Any]:
        """Analyse les coûts de stockage."""
        return await self.inventory_service.analyze_storage_costs()

    async def _analyze_stock_value(self) -> Dict[str, Any]:
        """Analyse la valeur des stocks."""
        return await self.inventory_service.analyze_stock_value()

    async def _analyze_turnover_rate(self) -> Dict[str, Any]:
        """Analyse le taux de rotation."""
        return await self.inventory_service.analyze_turnover_rate()

    async def _analyze_weather_inventory_impact(self) -> Dict[str, Any]:
        """Analyse l'impact météo sur l'inventaire."""
        return await self.weather_service.analyze_inventory_impact()

    async def _analyze_projects_hr_impact(self) -> Dict[str, Any]:
        """Analyse l'impact des projets sur les RH."""
        return await self.projects_ml_service.analyze_hr_impact()

    async def _analyze_projects_production_impact(self) -> Dict[str, Any]:
        """Analyse l'impact des projets sur la production."""
        return await self.projects_ml_service.analyze_production_impact()

    async def _analyze_projects_finance_impact(self) -> Dict[str, Any]:
        """Analyse l'impact des projets sur les finances."""
        return await self.projects_ml_service.analyze_finance_impact()

    async def _analyze_hr_production_correlation(self) -> float:
        """Analyse la corrélation RH-Production."""
        return await self.projects_ml_service.analyze_hr_production_correlation()

    async def _analyze_production_finance_correlation(self) -> float:
        """Analyse la corrélation Production-Finance."""
        return await self.projects_ml_service.analyze_production_finance_correlation()

    async def _analyze_weather_global_correlation(self) -> float:
        """Analyse la corrélation météo globale."""
        return await self.projects_ml_service.analyze_weather_global_correlation()

    async def _analyze_inventory_finance_correlation(self) -> float:
        """Analyse la corrélation Inventaire-Finance."""
        return await self.projects_ml_service.analyze_inventory_finance_correlation()

    async def _generate_cross_module_predictions(self) -> Dict[str, Any]:
        """Génère des prédictions cross-module."""
        return await self.projects_ml_service.generate_cross_module_predictions()

    async def _analyze_optimization_opportunities(self) -> List[Dict[str, Any]]:
        """Analyse les opportunités d'optimisation."""
        return await self.projects_ml_service.analyze_optimization_opportunities()

    async def _generate_correlation_actions(self, correlation: str) -> List[str]:
        """Génère des actions basées sur les corrélations."""
        return await self.projects_ml_service.generate_correlation_actions(correlation)
