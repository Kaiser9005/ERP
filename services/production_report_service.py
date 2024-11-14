from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from services.weather_service import WeatherService
from services.notification_service import NotificationService
from models.production import Parcelle, Recolte, ProductionEvent
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
from redis import Redis
from core.config import settings

class ProductionReportService:
    """Service de génération de rapports de production intégrés"""

    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService()
        self.notification_service = NotificationService()
        self.redis_client = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=0,
            decode_responses=True
        )
        self.cache_ttl = 3600  # 1 heure en secondes

    async def generate_weekly_report(
        self,
        start_date: datetime,
        force_refresh: bool = False
    ) -> Dict[str, Any]:
        """Génère un rapport hebdomadaire intégrant données de production et météo"""
        cache_key = f"production:report:weekly:{start_date.isoformat()}"
        
        # Vérifier le cache si pas de force_refresh
        if not force_refresh:
            cached_report = self._get_from_cache(cache_key)
            if cached_report:
                return cached_report

        end_date = start_date + timedelta(days=7)
        
        # Récupération des données météo
        weather_metrics = await self.weather_service.get_agricultural_metrics()
        
        # Données de production de la semaine avec requêtes optimisées
        production_data = await self._get_production_data(start_date, end_date)
        
        # Analyse de l'impact météo sur la production
        weather_impact = self._analyze_weather_impact(
            production_data["recoltes"],
            weather_metrics
        )

        report = {
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
            ),
            "generated_at": datetime.utcnow().isoformat()
        }

        # Sauvegarder dans le cache
        self._save_to_cache(cache_key, report)

        # Envoyer des notifications si nécessaire
        await self._send_report_notifications(report)

        return report

    async def _get_production_data(
        self,
        start_date: datetime,
        end_date: datetime
    ) -> Dict[str, Any]:
        """Récupère les données de production pour la période avec requêtes optimisées"""
        
        # Récupération des récoltes avec une seule requête
        recoltes = (
            self.db.query(
                Recolte,
                Parcelle.code.label("parcelle_code"),
                Parcelle.culture_type
            )
            .join(Parcelle)
            .filter(Recolte.date_recolte.between(start_date, end_date))
            .all()
        )

        # Calcul des totaux par parcelle avec agrégation en mémoire
        totaux_parcelles = {}
        for recolte, parcelle_code, culture_type in recoltes:
            if recolte.parcelle_id not in totaux_parcelles:
                totaux_parcelles[recolte.parcelle_id] = {
                    "code": parcelle_code,
                    "culture_type": culture_type,
                    "quantite": 0,
                    "qualite_moyenne": 0,
                    "nombre_recoltes": 0
                }
            
            totaux = totaux_parcelles[recolte.parcelle_id]
            totaux["quantite"] += float(recolte.quantite_kg)
            totaux["qualite_moyenne"] += self._convert_qualite_to_number(recolte.qualite)
            totaux["nombre_recoltes"] += 1

        # Calcul des moyennes
        for totaux in totaux_parcelles.values():
            if totaux["nombre_recoltes"] > 0:
                totaux["qualite_moyenne"] /= totaux["nombre_recoltes"]

        return {
            "recoltes": [
                {
                    "id": recolte.id,
                    "parcelle_id": recolte.parcelle_id,
                    "parcelle_code": parcelle_code,
                    "culture_type": culture_type,
                    "date": recolte.date_recolte.isoformat(),
                    "quantite": float(recolte.quantite_kg),
                    "qualite": recolte.qualite.value
                }
                for recolte, parcelle_code, culture_type in recoltes
            ],
            "totaux_parcelles": totaux_parcelles,
            "total_global": sum(
                total["quantite"] 
                for total in totaux_parcelles.values()
            )
        }

    def _convert_qualite_to_number(self, qualite: str) -> float:
        """Convertit la qualité en valeur numérique"""
        conversion = {"A": 10, "B": 7, "C": 4}
        return conversion.get(qualite, 0)

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
                        "description": f"Améliorer la qualité des récoltes - Parcelle {totaux['code']}",
                        "details": (
                            f"Qualité moyenne: {totaux['qualite_moyenne']:.1f}/10 - "
                            f"Culture: {totaux['culture_type']}"
                        )
                    })

        return sorted(
            recommendations,
            key=lambda x: 0 if x["priorite"] == "HAUTE" else 1 if x["priorite"] == "MOYENNE" else 2
        )

    def _get_from_cache(self, key: str) -> Optional[Dict[str, Any]]:
        """Récupère les données du cache Redis"""
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None

    def _save_to_cache(self, key: str, data: Dict[str, Any]) -> None:
        """Sauvegarde les données dans le cache Redis"""
        self.redis_client.setex(
            key,
            self.cache_ttl,
            json.dumps(data)
        )

    async def _send_report_notifications(self, report: Dict[str, Any]) -> None:
        """Envoie des notifications basées sur le rapport"""
        
        # Notification pour impact météo élevé
        if report["meteo"]["impact"]["niveau"] == "ÉLEVÉ":
            factors = report["meteo"]["impact"]["facteurs"]
            message = "ALERTE PRODUCTION:\n"
            message += "\n".join(f"- {f['facteur']}: {f['impact']}" for f in factors)
            
            await self.notification_service.send_notification(
                "production",
                "Impact Météo Critique",
                message
            )

        # Notification pour problèmes de qualité
        low_quality_parcelles = [
            totaux for totaux in report["production"]["totaux_parcelles"].values()
            if totaux["qualite_moyenne"] < 7
        ]
        
        if low_quality_parcelles:
            message = "ALERTE QUALITÉ:\n"
            message += "\n".join(
                f"- Parcelle {p['code']}: Qualité {p['qualite_moyenne']:.1f}/10"
                for p in low_quality_parcelles
            )
            
            await self.notification_service.send_notification(
                "production",
                "Problèmes de Qualité Détectés",
                message
            )

    async def record_production_event(
        self,
        parcelle_id: str,
        event_type: str,
        description: str,
        metadata: Dict[str, Any] = None
    ) -> None:
        """Enregistre un événement de production avec notification"""
        
        event = ProductionEvent(
            parcelle_id=parcelle_id,
            type=event_type,
            date_debut=datetime.now(datetime.timezone.utc),
            description=description,
            metadata=metadata or {}
        )
        
        self.db.add(event)
        self.db.commit()

        # Notification de l'événement
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if parcelle:
            await self.notification_service.send_notification(
                "production",
                f"Nouvel événement - {parcelle.code}",
                f"Type: {event_type}\nDescription: {description}"
            )
