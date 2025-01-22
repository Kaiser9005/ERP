from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from datetime import datetime, timedelta
from models.notification import Notification, ModuleNotification
from models.production import Recolte
from models.inventory import MouvementStock
from models.tache import Tache

class ActivityService:
    def __init__(self, db: Session):
        self.db = db

    async def get_recent_activities(self, limit: int = 10) -> List[dict]:
        """Récupère les activités récentes tous types confondus"""
        activities = []
        date_limite = datetime.utcnow() - timedelta(days=7)

        # Récupérer les notifications récentes
        notifications = self.db.query(Notification).filter(
            Notification.date_creation >= date_limite
        ).order_by(desc(Notification.date_creation)).limit(limit).all()

        for notif in notifications:
            activities.append({
                "id": str(notif.id),
                "type": "NOTIFICATION",
                "title": notif.titre,
                "description": notif.message,
                "date": notif.date_creation.isoformat(),
                "color": "warning" if notif.module == ModuleNotification.WEATHER else "info",
                "module": notif.module
            })

        # Récupérer les tâches récentes
        taches = self.db.query(Tache).filter(
            Tache.date_modification >= date_limite
        ).order_by(desc(Tache.date_modification)).limit(limit).all()

        for tache in taches:
            activities.append({
                "id": str(tache.id),
                "type": "TASK",
                "title": tache.nom,
                "description": tache.description or "",
                "date": tache.date_modification.isoformat(),
                "color": "primary",
                "module": "TASKS"
            })

        # Récupérer les récoltes récentes
        recoltes = self.db.query(Recolte).filter(
            Recolte.date_recolte >= date_limite
        ).order_by(desc(Recolte.date_recolte)).limit(limit).all()

        for recolte in recoltes:
            activities.append({
                "id": str(recolte.id),
                "type": "PRODUCTION",
                "title": f"Récolte - {recolte.parcelle.code}",
                "description": f"Récolte de {recolte.quantite_kg} kg",
                "date": recolte.date_recolte.isoformat(),
                "color": "success",
                "module": "PRODUCTION"
            })

        # Récupérer les mouvements de stock récents
        mouvements = self.db.query(MouvementStock).filter(
            MouvementStock.date_mouvement >= date_limite
        ).order_by(desc(MouvementStock.date_mouvement)).limit(limit).all()

        for mouvement in mouvements:
            activities.append({
                "id": str(mouvement.id),
                "type": "INVENTORY",
                "title": f"{mouvement.type_mouvement} - {mouvement.produit.nom}",
                "description": f"Quantité: {mouvement.quantite} {mouvement.produit.unite_mesure}",
                "date": mouvement.date_mouvement.isoformat(),
                "color": "info",
                "module": "INVENTORY"
            })

        # Trier toutes les activités par date
        activities.sort(key=lambda x: x["date"], reverse=True)
        return activities[:limit]

    async def track_activity(self, activity_data: dict) -> None:
        """Enregistre une nouvelle activité"""
        # Implémentation du suivi d'activité si nécessaire
        pass