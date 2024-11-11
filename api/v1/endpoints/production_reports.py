from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from services.production_report_service import ProductionReportService
from db.database import get_db

router = APIRouter()

@router.get("/weekly")
async def get_weekly_report(
    date: str = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Génère un rapport hebdomadaire de production intégrant les données météo.
    
    Args:
        date: Date de début au format YYYY-MM-DD (défaut: date actuelle)
        db: Session de base de données
    
    Returns:
        Dict contenant le rapport hebdomadaire avec :
        - Période couverte
        - Données météo et impacts
        - Données de production
        - Recommandations
    """
    try:
        # Utilisation de la date fournie ou date actuelle
        start_date = datetime.strptime(date, "%Y-%m-%d") if date else datetime.now()
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        # Génération du rapport
        report_service = ProductionReportService(db)
        report = await report_service.generate_weekly_report(start_date)

        return report

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Format de date invalide. Utilisez YYYY-MM-DD. Erreur: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du rapport: {str(e)}"
        )

@router.get("/impact-meteo")
async def get_weather_impact(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyse l'impact des conditions météo sur la production pour une période donnée.
    
    Args:
        start_date: Date de début au format YYYY-MM-DD
        end_date: Date de fin au format YYYY-MM-DD
        db: Session de base de données
    
    Returns:
        Dict contenant l'analyse d'impact avec :
        - Niveau d'impact global
        - Facteurs d'impact détaillés
        - Recommandations spécifiques
    """
    try:
        # Conversion des dates
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")

        if end < start:
            raise ValueError("La date de fin doit être postérieure à la date de début")

        # Génération de l'analyse
        report_service = ProductionReportService(db)
        
        # Récupération des données de production
        production_data = report_service._get_production_data(start, end)
        
        # Récupération des métriques météo
        weather_metrics = await report_service.weather_service.get_agricultural_metrics()
        
        # Analyse de l'impact
        impact_analysis = report_service._analyze_weather_impact(
            production_data["recoltes"],
            weather_metrics
        )

        # Génération des recommandations
        recommendations = report_service._generate_recommendations(
            weather_metrics["recommendations"],
            production_data,
            impact_analysis
        )

        return {
            "periode": {
                "debut": start_date,
                "fin": end_date
            },
            "analyse_impact": impact_analysis,
            "recommandations": recommendations,
            "statistiques_production": {
                "total_recoltes": len(production_data["recoltes"]),
                "total_quantite": production_data["total_global"],
                "parcelles_impactees": len(production_data["totaux_parcelles"])
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Erreur de validation des dates: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse d'impact: {str(e)}"
        )
