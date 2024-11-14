from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from services.production_report_service import ProductionReportService
from db.database import get_db
from pydantic import BaseModel

router = APIRouter()

class ProductionEventCreate(BaseModel):
    """Modèle pour la création d'un événement de production"""
    parcelle_id: str
    event_type: str
    description: str
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        schema_extra = {
            "example": {
                "parcelle_id": "123e4567-e89b-12d3-a456-426614174000",
                "event_type": "RECOLTE",
                "description": "Récolte des palmiers - Zone Nord",
                "metadata": {
                    "quantite_kg": 500,
                    "qualite": "A",
                    "equipe": ["emp001", "emp002"]
                }
            }
        }

@router.get("/weekly", response_model=Dict[str, Any])
async def get_weekly_report(
    date: Optional[str] = Query(
        None,
        description="Date de début au format YYYY-MM-DD (défaut: date actuelle)"
    ),
    force_refresh: bool = Query(
        False,
        description="Force le rafraîchissement du cache"
    ),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Génère un rapport hebdomadaire de production intégrant les données météo.
    
    Le rapport inclut :
    - Période couverte
    - Données météo et impacts
    - Données de production
    - Recommandations
    
    Les données sont mises en cache pendant 1 heure pour optimiser les performances.
    Utilisez force_refresh=true pour forcer une mise à jour des données.
    """
    try:
        # Utilisation de la date fournie ou date actuelle
        start_date = (
            datetime.strptime(date, "%Y-%m-%d") if date 
            else datetime.now(timezone.utc)
        )
        start_date = start_date.replace(
            hour=0, minute=0, second=0, microsecond=0, tzinfo=timezone.utc
        )

        # Génération du rapport
        report_service = ProductionReportService(db)
        report = await report_service.generate_weekly_report(
            start_date,
            force_refresh=force_refresh
        )

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

@router.get("/impact-meteo", response_model=Dict[str, Any])
async def get_weather_impact(
    start_date: str = Query(..., description="Date de début au format YYYY-MM-DD"),
    end_date: str = Query(..., description="Date de fin au format YYYY-MM-DD"),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Analyse l'impact des conditions météo sur la production pour une période donnée.
    
    L'analyse inclut :
    - Niveau d'impact global
    - Facteurs d'impact détaillés
    - Recommandations spécifiques
    - Statistiques de production
    """
    try:
        # Conversion des dates
        start = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        end = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

        if end < start:
            raise ValueError("La date de fin doit être postérieure à la date de début")

        # Génération de l'analyse
        report_service = ProductionReportService(db)
        
        # Récupération des données de production
        production_data = await report_service._get_production_data(start, end)
        
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

@router.post("/events", status_code=201)
async def create_production_event(
    event: ProductionEventCreate,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Crée un nouvel événement de production.
    
    L'événement sera enregistré et une notification sera envoyée aux utilisateurs concernés.
    Les types d'événements possibles sont :
    - RECOLTE : Enregistrement d'une récolte
    - PLANTATION : Nouvelle plantation
    - MAINTENANCE : Opération de maintenance
    - TRAITEMENT : Application de traitements
    - IRRIGATION : Opération d'irrigation
    """
    try:
        report_service = ProductionReportService(db)
        await report_service.record_production_event(
            parcelle_id=event.parcelle_id,
            event_type=event.event_type,
            description=event.description,
            metadata=event.metadata
        )

        return {
            "status": "success",
            "message": "Événement de production enregistré avec succès",
            "event": {
                "type": event.event_type,
                "parcelle_id": event.parcelle_id,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=f"Données d'événement invalides: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'enregistrement de l'événement: {str(e)}"
        )
