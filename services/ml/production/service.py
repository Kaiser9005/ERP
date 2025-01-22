"""
Service d'apprentissage automatique pour la production agricole.
Utilise des services spécialisés pour chaque type d'analyse.
"""

from typing import Dict, Any, Optional
from datetime import date
from sqlalchemy.orm import Session

from .rendement import PredicteurRendement
from .cycle import OptimiseurCycle
from .meteo import MeteoAnalyzer
from .qualite import QualitePredictor

class ProductionMLService:
    """Service ML pour l'optimisation de la production"""
    
    def __init__(self, db: Session):
        self.db = db
        self.rendement_predictor = PredicteurRendement(db)
        self.cycle_optimizer = OptimiseurCycle(db)
        self.meteo_analyzer = MeteoAnalyzer(db)
        self.qualite_predictor = QualitePredictor(db)

    async def predict_rendement(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Prédit le rendement d'une parcelle pour une période donnée"""
        return await self.rendement_predictor.predict_rendement(
            parcelle_id,
            date_debut,
            date_fin
        )

    async def optimize_cycle_culture(
        self,
        parcelle_id: str,
        date_debut: Optional[date] = None
    ) -> Dict[str, Any]:
        """Optimise le planning d'un cycle de culture"""
        return await self.cycle_optimizer.optimize_cycle_culture(
            parcelle_id,
            date_debut
        )

    async def analyze_meteo_impact(
        self,
        parcelle_id: str,
        date_debut: date,
        date_fin: date
    ) -> Dict[str, Any]:
        """Analyse l'impact des conditions météo sur la production"""
        return await self.meteo_analyzer.analyze_meteo_impact(
            parcelle_id,
            date_debut,
            date_fin
        )

    async def predict_qualite(
        self,
        parcelle_id: str,
        date_recolte: date
    ) -> Dict[str, Any]:
        """Prédit la qualité de la récolte"""
        return await self.qualite_predictor.predict_qualite(
            parcelle_id,
            date_recolte
        )
