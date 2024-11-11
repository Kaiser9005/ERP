from typing import Dict, Any, List
from datetime import datetime, timedelta
from services.weather_service import WeatherService
from models.production import Parcelle, Recolte
from sqlalchemy.orm import Session
from sqlalchemy import func
import json

class ProductionReportService:
    """Service de génération de rapports de production intégrés"""

    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()

    async def generate_weekly_report(self, start_date: datetime) -> Dict[str, Any]:
        """Génère un rapport hebdomadaire intégrant données de production et météo"""
        end_date = start_date + timedelta(days=7)
        
        # Récupération des données météo
        weather_metrics = await self.weather_service.get_agricultural_metrics()
        
        # Données de production de la semaine
        production_data = self._get_production_data(start_date, end_date)
        
        # Analyse de l'impact météo sur la production
        weather_impact = self._analyze_weather_impact(
            production_data["recoltes"],
            weather_metrics
        )

        return {
            "periode": {
                "debut": start_date.isoformat(),
                "fin": end_date.isoformat()
            },
            "meteo": {
                "conditions": weather_metrics["current_conditions"],
                "risques": weather_metrics["risks"],
                "impact": weather_impact
            },
            "production": production_data,
            "recommandations": self._generate_recommendations(
                weather_metrics["recommendations"],
                production_data,
                weather_impact
            )
        }

    def _get_production_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Récupère les données de production pour la période"""
        
        # Récupération des récoltes
        recoltes = self.db.query(Recolte).filter(
            Recolte.date.between(start_date, end_date)
        ).all()

        # Calcul des totaux par parcelle
        totaux_parcelles = {}
        for recolte in recoltes:
            if recolte.parcelle_id not in totaux_parcelles:
                totaux_parcelles[recolte.parcelle_id] = {
                    "quantite": 0,
                    "qualite_moyenne": 0,
                    "nombre_recoltes": 0
                }
            
            totaux_parcelles[recolte.parcelle_id]["quantite"] += recolte.quantite
            totaux_parcelles[recolte.parcelle_id]["qualite_moyenne"] += recolte.qualite
            totaux_parcelles[recolte.parcelle_id]["nombre_recoltes"] += 1

        # Calcul des moyennes
        for parcelle_id in totaux_parcelles:
            totaux_parcelles[parcelle_id]["qualite_moyenne"] /= \
                totaux_parcelles[parcelle_id]["nombre_recoltes"]

        return {
            "recoltes": [
                {
                    "id": recolte.id,
                    "parcelle_id": recolte.parcelle_id,
                    "date": recolte.date.isoformat(),
                    "quantite": recolte.quantite,
                    "qualite": recolte.qualite
                }
                for recolte in recoltes
            ],
            "totaux_parcelles": totaux_parcelles,
            "total_global": sum(
                total["quantite"] 
                for total in totaux_parcelles.values()
            )
        }

    def _analyze_weather_impact(
        self,
        recoltes: List[Dict[str, Any]],
        weather_metrics: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyse l'impact des conditions météo sur la production"""
        
        impact_level = "FAIBLE"
        impact_factors = []

        # Analyse des précipitations
        if weather_metrics["risks"]["precipitation"]["level"] == "HIGH":
            impact_level = "ÉLEVÉ"
            impact_factors.append({
                "facteur": "Précipitations excessives",
                "impact": "Risque d'inondation et de perte de récoltes",
                "recommandation": "Renforcer le drainage des parcelles"
            })
        elif weather_metrics["risks"]["precipitation"]["level"] == "MEDIUM":
            impact_level = "MOYEN"
            impact_factors.append({
                "facteur": "Précipitations modérées",
                "impact": "Possible ralentissement des activités",
                "recommandation": "Adapter le calendrier des récoltes"
            })

        # Analyse des températures
        if weather_metrics["risks"]["temperature"]["level"] == "HIGH":
            impact_level = "ÉLEVÉ"
            impact_factors.append({
                "facteur": "Températures élevées",
                "impact": "Stress thermique des cultures",
                "recommandation": "Augmenter l'irrigation et la protection"
            })
        elif weather_metrics["risks"]["temperature"]["level"] == "MEDIUM":
            if impact_level != "ÉLEVÉ":
                impact_level = "MOYEN"
            impact_factors.append({
                "facteur": "Températures modérées",
                "impact": "Possible stress des cultures sensibles",
                "recommandation": "Surveiller l'hydratation"
            })

        return {
            "niveau": impact_level,
            "facteurs": impact_factors
        }

    def _generate_recommendations(
        self,
        weather_recommendations: List[str],
        production_data: Dict[str, Any],
        weather_impact: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Génère des recommandations basées sur la météo et la production"""
        
        recommendations = []

        # Recommandations basées sur l'impact météo
        for factor in weather_impact["facteurs"]:
            recommendations.append({
                "type": "METEO",
                "priorite": "HAUTE" if weather_impact["niveau"] == "ÉLEVÉ" else "MOYENNE",
                "description": factor["recommandation"],
                "details": f"En raison de : {factor['facteur']} - {factor['impact']}"
            })

        # Recommandations générales météo
        for rec in weather_recommendations:
            if not any(r["description"] == rec for r in recommendations):
                recommendations.append({
                    "type": "METEO",
                    "priorite": "NORMALE",
                    "description": rec,
                    "details": "Recommandation générale basée sur les conditions météo"
                })

        # Recommandations basées sur la production
        if production_data["total_global"] > 0:
            for parcelle_id, totaux in production_data["totaux_parcelles"].items():
                if totaux["qualite_moyenne"] < 7:
                    recommendations.append({
                        "type": "PRODUCTION",
                        "priorite": "HAUTE",
                        "description": f"Améliorer la qualité des récoltes - Parcelle {parcelle_id}",
                        "details": f"Qualité moyenne: {totaux['qualite_moyenne']:.1f}/10"
                    })

        return sorted(
            recommendations,
            key=lambda x: 0 if x["priorite"] == "HAUTE" else 1 if x["priorite"] == "MOYENNE" else 2
        )
