"""
Service de gestion des alertes critiques pour le tableau de bord.
"""

from typing import Dict, List, Any

from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService

async def get_critical_alerts(
    hr_service: HRAnalyticsService,
    production_service: ProductionService,
    finance_service: FinanceService,
    inventory_service: InventoryService,
    weather_service: WeatherService
) -> List[Dict[str, Any]]:
    """Agrège les alertes critiques de tous les modules."""
    alerts = []
    
    # Alertes RH
    hr_alerts = await hr_service.get_critical_alerts()
    alerts.extend(hr_alerts)
    
    # Alertes Production
    prod_alerts = await production_service.get_critical_alerts()
    alerts.extend(prod_alerts)
    
    # Alertes Finance
    finance_alerts = await finance_service.get_critical_alerts()
    alerts.extend(finance_alerts)
    
    # Alertes Inventaire
    inventory_alerts = await inventory_service.get_critical_alerts()
    alerts.extend(inventory_alerts)
    
    # Alertes Météo
    weather_alerts = await weather_service.get_critical_alerts()
    alerts.extend(weather_alerts)
    
    return sorted(alerts, key=lambda x: x.get('priority', 0), reverse=True)
