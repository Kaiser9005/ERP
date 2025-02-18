"""
Service de prédictions ML pour le tableau de bord.
Utilise les services ML spécialisés de chaque module.
"""

from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from services.ml.production.service import ProductionMLService
from services.inventory_ml_service import InventoryMLService
from services.finance_service import FinanceService
from services.comptabilite_service import ComptabiliteService
from services.ml.projets.service import ProjetsMLService
from services.hr_analytics_service import HRAnalyticsService
from services.cache_service import CacheService
from services.finance_comptabilite_integration_service import FinanceComptabiliteIntegrationService

class TableauBordPredictionsService:
    """Service de prédictions ML pour le tableau de bord unifié"""
    
    def __init__(
        self,
        db: Session,
        production_ml: ProductionMLService,
        inventory_ml: InventoryMLService,
        finance_service: FinanceService,
        comptabilite_service: ComptabiliteService,
        projets_ml: ProjetsMLService,
        hr_analytics: HRAnalyticsService,
        finance_comptabilite: FinanceComptabiliteIntegrationService,
        cache_service: CacheService
    ):
        self.db = db
        self.production_ml = production_ml
        self.inventory_ml = inventory_ml
        self.finance_service = finance_service
        self.comptabilite_service = comptabilite_service
        self.projets_ml = projets_ml
        self.hr_analytics = hr_analytics
        self.finance_comptabilite = finance_comptabilite
        self.cache_service = cache_service
        self.cache_ttl = 900  # 15 minutes

    async def get_ml_predictions(self) -> Dict[str, Any]:
        """Agrège les prédictions ML de tous les modules."""
        cache_key = "ml_predictions"
        cached_data = await self.cache_service.get(cache_key)
        
        if cached_data:
            return cached_data

        predictions = {
            "production": await self._get_production_predictions(),
            "finance": await self._get_finance_predictions(),
            "inventory": await self._get_inventory_predictions(),
            "projets": await self._get_projets_predictions(),
            "hr": await self._get_hr_predictions()
        }

        await self.cache_service.set(cache_key, predictions, self.cache_ttl)
        return predictions

    async def _get_production_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML pour la production."""
        return {
            "rendement": await self.production_ml.predict_rendement(
                parcelle_id="all",
                date_debut=None,
                date_fin=None
            ),
            "qualite": await self.production_ml.predict_qualite(
                parcelle_id="all",
                date_recolte=None
            ),
            "meteo_impact": await self.production_ml.analyze_meteo_impact(
                parcelle_id="all",
                date_debut=None,
                date_fin=None
            ),
            "cycle_optimal": await self.production_ml.optimize_cycle_culture(
                parcelle_id="all"
            )
        }

    async def _get_finance_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML pour les finances."""
        return {
            "revenue": await self.finance_service.predict_revenue(),
            "costs": await self.finance_service.predict_costs(),
            "cash_flow": await self.finance_service.predict_cash_flow(),
            "budget_variance": await self.comptabilite_service.predict_budget_variance(),
            "meteo_impact": await self.finance_comptabilite.analyze_meteo_impact()
        }

    async def _get_inventory_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML pour l'inventaire."""
        return {
            "stock_levels": await self.inventory_ml.predict_stock_levels(),
            "demand": await self.inventory_ml.predict_demand(),
            "quality": await self.inventory_ml.predict_quality(),
            "storage_conditions": await self.inventory_ml.analyze_storage_conditions(),
            "optimization": await self.inventory_ml.get_optimization_recommendations()
        }

    async def _get_projets_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML pour les projets."""
        return {
            "success": await self.projets_ml.predict_project_success(),
            "resources": await self.projets_ml.optimize_resources(),
            "trends": await self.projets_ml.analyze_trends(),
            "weather_impact": await self.projets_ml.analyze_weather_impact(),
            "recommendations": await self.projets_ml.get_recommendations()
        }

    async def _get_hr_predictions(self) -> Dict[str, Any]:
        """Récupère les prédictions ML pour les RH."""
        return {
            "performance": await self.hr_analytics.predict_performance(),
            "training_needs": await self.hr_analytics.predict_training_needs(),
            "turnover_risk": await self.hr_analytics.predict_turnover_risk(),
            "skill_gaps": await self.hr_analytics.analyze_skill_gaps(),
            "weather_impact": await self.hr_analytics.analyze_weather_impact()
        }

# Export de la fonction au niveau du module
async def get_ml_predictions(
    projets_ml: ProjetsMLService,
    db: Optional[Session] = None,
    production_ml: Optional[ProductionMLService] = None,
    inventory_ml: Optional[InventoryMLService] = None,
    finance_service: Optional[FinanceService] = None,
    comptabilite_service: Optional[ComptabiliteService] = None,
    hr_analytics: Optional[HRAnalyticsService] = None,
    finance_comptabilite: Optional[FinanceComptabiliteIntegrationService] = None,
    cache_service: Optional[CacheService] = None
) -> Dict[str, Any]:
    """
    Fonction de niveau module pour obtenir les prédictions ML.
    Crée une instance du service et retourne les prédictions.
    
    Args:
        projets_ml: Service ML des projets (requis)
        db: Session de base de données (optionnel)
        production_ml: Service ML de production (optionnel)
        inventory_ml: Service ML d'inventaire (optionnel)
        finance_service: Service financier (optionnel)
        comptabilite_service: Service comptable (optionnel)
        hr_analytics: Service RH (optionnel)
        finance_comptabilite: Service d'intégration finance-compta (optionnel)
        cache_service: Service de cache (optionnel)
        
    Returns:
        Dict contenant les prédictions ML
    """
    # Création des services manquants avec des mocks si nécessaire
    if not db:
        from unittest.mock import AsyncMock, MagicMock
        db = MagicMock()
    if not production_ml:
        production_ml = AsyncMock()
    if not inventory_ml:
        inventory_ml = AsyncMock()
    if not finance_service:
        finance_service = AsyncMock()
    if not comptabilite_service:
        comptabilite_service = AsyncMock()
    if not hr_analytics:
        hr_analytics = AsyncMock()
    if not finance_comptabilite:
        finance_comptabilite = AsyncMock()
    if not cache_service:
        cache_service = AsyncMock()

    service = TableauBordPredictionsService(
        db=db,
        production_ml=production_ml,
        inventory_ml=inventory_ml,
        finance_service=finance_service,
        comptabilite_service=comptabilite_service,
        projets_ml=projets_ml,
        hr_analytics=hr_analytics,
        finance_comptabilite=finance_comptabilite,
        cache_service=cache_service
    )
    return await service.get_ml_predictions()
