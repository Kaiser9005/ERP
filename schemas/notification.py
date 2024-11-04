from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict
from models.notification import TypeNotification, ModuleNotification

class NotificationBase(BaseModel):
    titre: str
    message: str
    type: TypeNotification
    module: ModuleNotification
    lien: Optional[str]
    donnees: Optional[Dict]

class NotificationCreate(NotificationBase):
    destinataire_id: UUID4

class NotificationResponse(NotificationBase):
    id: UUID4
    date_creation: datetime
    lu: bool
    destinataire_id: UUID4

    class Config:
        orm_mode = True