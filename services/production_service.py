"""
Service de gestion de la production agricole
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from models.production import (
    Parcelle,
    CycleCulture,
    Recolte,
    ProductionEvent,
    CultureType,
    QualiteRecolte
)
from services.weather_service import WeatherService
from services.iot_service import IoTService
from services.ml.production.service import ProductionMLService
from services.cache_service import CacheService

class ProductionService:
    """Service de gestion de la production"""
    
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)
        self.iot_service = IoTService(db, self.weather_service)
        self.ml_service = ProductionMLService(db)
        self.cache = CacheService()

    async def get_parcelle_details(
        self,
        parcelle_id: str,
        include_predictions: bool = False
    ) -> Dict[str, Any]:
        """Récupère les détails d'une parcelle avec prédictions optionnelles"""
        # Récupération parcelle
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Données de base
        details = {
            "id": parcelle.id,
            "code": parcelle.code,
            "culture_type": parcelle.culture_type,
            "surface_hectares": float(parcelle.surface_hectares),
            "date_plantation": parcelle.date_plantation.isoformat(),
            "statut": parcelle.statut,
            "coordonnees_gps": parcelle.coordonnees_gps
        }
        
        # Cycle actuel
        cycle_actuel = self.db.query(CycleCulture).filter(
            and_(
                CycleCulture.parcelle_id == parcelle_id,
                CycleCulture.date_fin == None
            )
        ).first()
        
        if cycle_actuel:
            details["cycle_actuel"] = {
                "id": cycle_actuel.id,
                "date_debut": cycle_actuel.date_debut.isoformat(),
                "rendement_prevu": float(cycle_actuel.rendement_prevu or 0)
            }
            
            if include_predictions:
                # Prédictions ML
                predictions = await self.ml_service.predict_rendement(
                    parcelle_id,
                    cycle_actuel.date_debut,
                    date.today() + timedelta(days=90)
                )
                details["predictions"] = predictions
                
                # Impact météo
                meteo_impact = await self.ml_service.analyze_meteo_impact(
                    parcelle_id,
                    cycle_actuel.date_debut,
                    date.today()
                )
                details["meteo_impact"] = meteo_impact
        
        return details

    async def create_cycle_culture(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        optimize: bool = True
    ) -> Dict[str, Any]:
        """Crée un nouveau cycle de culture avec optimisation optionnelle"""
        # Vérification parcelle
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Optimisation avec ML si demandée
        if optimize:
            optimisation = await self.ml_service.optimize_cycle_culture(
                parcelle_id,
                date_debut
            )
            date_debut = optimisation["date_debut_optimale"]
            rendement_prevu = optimisation["rendement_prevu"]["rendement_prevu"]
        else:
            date_debut = date_debut or date.today()
            rendement_prevu = 0
            
        # Création cycle
        cycle = CycleCulture(
            parcelle_id=parcelle_id,
            date_debut=date_debut,
            rendement_prevu=Decimal(str(rendement_prevu))
        )
        self.db.add(cycle)
        self.db.commit()
        
        return {
            "id": cycle.id,
            "date_debut": cycle.date_debut.isoformat(),
            "rendement_prevu": float(cycle.rendement_prevu),
            "optimisation": optimisation if optimize else None
        }

    async def create_recolte(
        self,
        parcelle_id: str,
        date_recolte: date,
        quantite_kg: float,
        predict_quality: bool = True
    ) -> Dict[str, Any]:
        """Crée une nouvelle récolte avec prédiction de qualité optionnelle"""
        # Vérification parcelle
        parcelle = self.db.query(Parcelle).get(parcelle_id)
        if not parcelle:
            raise ValueError("Parcelle non trouvée")
            
        # Prédiction qualité avec ML si demandée
        qualite = None
        prediction_qualite = None
        if predict_quality:
            prediction_qualite = await self.ml_service.predict_qualite(
                parcelle_id,
                date_recolte
            )
            qualite = prediction_qualite["qualite_prevue"]
        
        # Création récolte
        recolte = Recolte(
            parcelle_id=parcelle_id,
            date_recolte=datetime.combine(date_recolte, datetime.min.time()),
            quantite_kg=Decimal(str(quantite_kg)),
            qualite=qualite or QualiteRecolte.B,  # Qualité par défaut si pas de prédiction
            conditions_meteo=await self.weather_service.get_current_conditions(parcelle_id)
        )
        self.db.add(recolte)
        self.db.commit()
        
        return {
            "id": recolte.id,
            "date_recolte": recolte.date_recolte.isoformat(),
            "quantite_kg": float(recolte.quantite_kg),
            "qualite": recolte.qualite,
            "conditions_meteo": recolte.conditions_meteo,
            "prediction_qualite": prediction_qualite
        }

    async def get_production_stats(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None,
        include_predictions: bool = False
    ) -> Dict[str, Any]:
        """Récupère les statistiques de production avec prédictions optionnelles"""
        # Période par défaut: 30 derniers jours
        if not date_debut:
            date_fin = date.today()
            date_debut = date_fin - timedelta(days=30)
            
        # Statistiques de base
        stats = {
            "periode": {
                "debut": date_debut.isoformat(),
                "fin": date_fin.isoformat()
            }
        }
        
        # Récoltes sur la période
        recoltes = self.db.query(Recolte).filter(
            and_(
                Recolte.parcelle_id == parcelle_id,
                Recolte.date_recolte.between(date_debut, date_fin)
            )
        ).all()
        
        stats["recoltes"] = {
            "nombre": len(recoltes),
            "quantite_totale": float(sum(r.quantite_kg for r in recoltes)),
            "qualite": {
                "A": len([r for r in recoltes if r.qualite == QualiteRecolte.A]),
                "B": len([r for r in recoltes if r.qualite == QualiteRecolte.B]),
                "C": len([r for r in recoltes if r.qualite == QualiteRecolte.C])
            }
        }
        
        if include_predictions:
            # Prédictions futures
            predictions = await self.ml_service.predict_rendement(
                parcelle_id,
                date.today(),
                date.today() + timedelta(days=90)
            )
            stats["predictions"] = predictions
            
            # Impact météo
            meteo_impact = await self.ml_service.analyze_meteo_impact(
                parcelle_id,
                date_debut,
                date_fin
            )
            stats["meteo_impact"] = meteo_impact
            
        return stats

    async def get_production_recommendations(
        self,
        parcelle_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère les recommandations pour la production"""
        # Récupération données actuelles
        cycle_actuel = self.db.query(CycleCulture).filter(
            and_(
                CycleCulture.parcelle_id == parcelle_id,
                CycleCulture.date_fin == None
            )
        ).first()
        
        if not cycle_actuel:
            return []
            
        # Analyse ML
        predictions = await self.ml_service.predict_rendement(
            parcelle_id,
            cycle_actuel.date_debut,
            date.today() + timedelta(days=90)
        )
        
        meteo_impact = await self.ml_service.analyze_meteo_impact(
            parcelle_id,
            cycle_actuel.date_debut,
            date.today()
        )
        
        # Génération recommandations
        recommendations = []
        
        # Recommandations basées sur les prédictions
        if predictions["rendement_prevu"] < float(cycle_actuel.rendement_prevu or 0):
            recommendations.append({
                "type": "ALERTE",
                "message": "Rendement prévu inférieur à l'objectif",
                "details": predictions["facteurs_impact"]
            })
            
        # Recommandations basées sur la météo
        if meteo_impact["impact_score"] > 0.7:
            recommendations.extend([{
                "type": "ACTION",
                "message": rec
            } for rec in meteo_impact["recommandations"]])
            
        return recommendations

    async def get_production_graph_data(
        self,
        periode: str = "mois",
        date_debut: Optional[date] = None,
        date_fin: Optional[date] = None
    ) -> Dict[str, Any]:
        """Récupère les données pour le graphique de production"""
        if not date_debut:
            date_debut = datetime.now().date() - timedelta(days=30)
        if not date_fin:
            date_fin = datetime.now().date()

        # Requête de base pour les récoltes
        query = self.db.query(
            func.date_trunc(periode, Recolte.date_recolte).label('periode'),
            func.sum(Recolte.quantite_kg).label('quantite')
        ).filter(
            Recolte.date_recolte.between(date_debut, date_fin)
        )

        # Groupement selon la période
        query = query.group_by(func.date_trunc(periode, Recolte.date_recolte))
        query = query.order_by(func.date_trunc(periode, Recolte.date_recolte))

        # Exécution de la requête
        resultats = query.all()

        # Formatage des données
        donnees = []
        for resultat in resultats:
            donnees.append({
                "periode": resultat.periode.strftime("%Y-%m-%d"),
                "quantite": float(resultat.quantite)
            })

        return {
            "periode": periode,
            "date_debut": date_debut.isoformat(),
            "date_fin": date_fin.isoformat(),
            "donnees": donnees
        }
