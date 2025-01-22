"""
Service de gestion des alertes critiques pour le tableau de bord.
"""

from typing import Dict, List, Any
from enum import IntEnum

from services.hr_analytics_service import HRAnalyticsService
from services.production_service import ProductionService
from services.finance_service import FinanceService
from services.inventory_service import InventoryService
from services.weather_service import WeatherService

class AlertPriority(IntEnum):
    """Niveaux de priorité des alertes"""
    FAIBLE = 1
    MOYENNE = 2
    ELEVEE = 3
    CRITIQUE = 4

def _normalize_priority(priority: Any) -> int:
    """
    Normalise la priorité en entier.
    
    Args:
        priority: Priorité sous forme de str, int ou autre
        
    Returns:
        Priorité normalisée en entier
    """
    if isinstance(priority, int):
        return priority
    
    if isinstance(priority, str):
        priority = priority.upper()
        if priority in ["HIGH", "ELEVEE", "CRITIQUE", "CRITICAL"]:
            return AlertPriority.CRITIQUE
        elif priority in ["MEDIUM", "MOYENNE", "ELEVEE", "HIGH"]:
            return AlertPriority.ELEVEE
        elif priority in ["MEDIUM", "MOYENNE"]:
            return AlertPriority.MOYENNE
        elif priority in ["LOW", "FAIBLE", "LOW_PRIORITY"]:
            return AlertPriority.FAIBLE
    
    return AlertPriority.FAIBLE

async def get_critical_alerts(
    hr_service: HRAnalyticsService,
    production_service: ProductionService,
    finance_service: FinanceService,
    inventory_service: InventoryService,
    weather_service: WeatherService
) -> List[Dict[str, Any]]:
    """
    Agrège les alertes critiques de tous les modules.
    
    Args:
        hr_service: Service RH
        production_service: Service Production
        finance_service: Service Finance
        inventory_service: Service Inventaire
        weather_service: Service Météo
        
    Returns:
        Liste des alertes triées par priorité
    """
    alerts = []
    
    try:
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
        
        # Normalisation des priorités et tri
        for alert in alerts:
            if 'priority' in alert:
                alert['priority'] = _normalize_priority(alert['priority'])
            else:
                alert['priority'] = AlertPriority.FAIBLE
        
        return sorted(alerts, key=lambda x: x['priority'], reverse=True)
        
    except Exception as e:
        # En cas d'erreur, on retourne une alerte système
        return [{
            'type': 'SYSTEM',
            'priority': AlertPriority.CRITIQUE,
            'message': f'Erreur lors de la récupération des alertes: {str(e)}',
            'source': 'tableau_bord'
        }]
