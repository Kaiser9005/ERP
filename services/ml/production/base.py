"""
Classes et fonctions de base pour le module ML production.
"""

from typing import Dict, Any, List, Optional
from datetime import date
import numpy as np
from sqlalchemy.orm import Session

from models.production import (
    Parcelle,
    CycleCulture,
    Recolte,
    ProductionEvent,
    CultureType,
    QualiteRecolte
)

class BaseProductionML:
    """Classe de base pour les services ML de production"""
    
    def __init__(self, db: Session):
        self.db = db

    def _calculate_features(
        self,
        historique: List[Dict[str, Any]],
        meteo: List[Dict[str, Any]],
        iot_data: List[Dict[str, Any]]
    ) -> np.ndarray:
        """Calcule les features pour le modèle ML"""
        features = []
        
        # Features historiques
        if historique:
            features.extend([
                np.mean([h["quantite"] for h in historique]),
                np.std([h["quantite"] for h in historique]),
                len(historique)
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features météo
        if meteo:
            features.extend([
                np.mean([m["temperature"] for m in meteo]),
                np.mean([m["humidite"] for m in meteo]),
                np.sum([m["precipitation"] for m in meteo])
            ])
        else:
            features.extend([0, 0, 0])
            
        # Features IoT
        if iot_data:
            features.extend([
                np.mean([d["valeur"] for d in iot_data]),
                np.std([d["valeur"] for d in iot_data]),
                len(iot_data)
            ])
        else:
            features.extend([0, 0, 0])
            
        return np.array(features)

    async def _get_historique_rendements(
        self,
        parcelle_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère l'historique des rendements d'une parcelle"""
        recoltes = self.db.query(Recolte).filter(
            Recolte.parcelle_id == parcelle_id
        ).order_by(Recolte.date_recolte).all()
        
        return [{
            "date": r.date_recolte,
            "quantite": float(r.quantite_kg),
            "qualite": r.qualite,
            "conditions_meteo": r.conditions_meteo
        } for r in recoltes]

    async def _get_historique_cycles(
        self,
        parcelle_id: str
    ) -> List[Dict[str, Any]]:
        """Récupère l'historique des cycles de culture"""
        cycles = self.db.query(CycleCulture).filter(
            CycleCulture.parcelle_id == parcelle_id
        ).order_by(CycleCulture.date_debut).all()
        
        return [{
            "date_debut": c.date_debut,
            "date_fin": c.date_fin,
            "rendement_prevu": float(c.rendement_prevu or 0),
            "rendement_reel": float(c.rendement_reel or 0)
        } for c in cycles]
