from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
from models.notification import Notification
from models.production import Recolte
from models.inventory import MouvementStock

class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    async def get_recent_activities(self, limit: int = 10) -> List[dict]:
        """Récupère les activités récentes tous types confondus"""
        activities = []

        # Récupérer les récoltes récentes
        recoltes = self.db.query(Recolte).order_by(
            desc(Recolte.date_recolte)
        ).limit(limit).all()

        for recolte in recoltes:
            activities.append({
                "id": str(recolte.id),
                "type": "PRODUCTION",
                "title": f"Récolte - {recolte.parcelle.code}",
                "description": f"Récolte de {recolte.quantite_kg} kg",
                "date": recolte.date_recolte.isoformat(),
                "color": "success"
            })

        # Récupérer les mouvements de stock récents
        mouvements = self.db.query(MouvementStock).order_by(
            desc(MouvementStock.date_mouvement)
        ).limit(limit).all()

        for mouvement in mouvements:
            activities.append({
                "id": str(mouvement.id),
                "type": "INVENTORY",
                "title": f"{mouvement.type_mouvement} - {mouvement.produit.nom}",
                "description": f"Quantité: {mouvement.quantite} {mouvement.produit.unite_mesure}",
                "date": mouvement.date_mouvement.isoformat(),
                "color": "info"
            })

        # Trier toutes les activités par date
        activities.sort(key=lambda x: x["date"], reverse=True)
        return activities[:limit]

    async def track_activity(self, activity_data: dict) -> None:
        """Enregistre une nouvelle activité"""
        # Implémentation du suivi d'activité si nécessaire
        pass