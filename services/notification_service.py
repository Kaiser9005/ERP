from typing import Optional, Dict
from models.notification import Notification, TypeNotification, ModuleNotification
from sqlalchemy.orm import Session
from fastapi import Depends
from db.database import get_db
from api.v1.endpoints.notifications import send_notification

class NotificationService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    async def create_notification(
        self,
        titre: str,
        message: str,
        type: TypeNotification,
        module: ModuleNotification,
        destinataire_id: str,
        lien: Optional[str] = None,
        donnees: Optional[Dict] = None
    ) -> Notification:
        """Crée et envoie une nouvelle notification"""
        notification = Notification(
            titre=titre,
            message=message,
            type=type,
            module=module,
            destinataire_id=destinataire_id,
            lien=lien,
            donnees=donnees
        )
        
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)

        # Envoyer la notification en temps réel
        await send_notification(
            str(destinataire_id),
            notification.dict()
        )

        return notification

    def get_unread_count(self, user_id: str) -> int:
        """Retourne le nombre de notifications non lues"""
        return self.db.query(Notification).filter(
            Notification.destinataire_id == user_id,
            Notification.lu == False
        ).count()

    def mark_all_as_read(self, user_id: str) -> None:
        """Marque toutes les notifications comme lues"""
        self.db.query(Notification).filter(
            Notification.destinataire_id == user_id,
            Notification.lu == False
        ).update({"lu": True})
        self.db.commit()