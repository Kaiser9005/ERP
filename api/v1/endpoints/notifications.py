from fastapi import APIRouter, Depends, HTTPException, WebSocket, status
from sqlalchemy.orm import Session
from typing import List
import json
from db.database import get_db
from models.notification import Notification
from schemas.notification import NotificationCreate, NotificationResponse
from api.v1.endpoints.auth import get_current_user
from models.auth import Utilisateur

router = APIRouter()

@router.get("/", response_model=List[NotificationResponse])
async def get_notifications(
    non_lues: bool = False,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les notifications de l'utilisateur"""
    query = db.query(Notification).filter(
        Notification.destinataire_id == current_user.id
    )
    if non_lues:
        query = query.filter(Notification.lu == False)
    return query.order_by(Notification.date_creation.desc()).all()

@router.put("/{notification_id}/read")
async def mark_as_read(
    notification_id: str,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Marque une notification comme lue"""
    notification = db.query(Notification).filter(
        Notification.id == notification_id,
        Notification.destinataire_id == current_user.id
    ).first()
    
    if not notification:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    
    notification.lu = True
    db.commit()
    return {"status": "success"}

# Gestionnaire de connexions WebSocket
connected_clients = {}

@router.websocket("/ws/{client_id}")
async def notifications_websocket(websocket: WebSocket, client_id: str):
    """Endpoint WebSocket pour les notifications en temps réel"""
    await websocket.accept()
    connected_clients[client_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            # Traitement des messages du client si nécessaire
    except Exception:
        connected_clients.pop(client_id, None)

async def send_notification(user_id: str, notification: dict):
    """Envoie une notification via WebSocket"""
    if user_id in connected_clients:
        websocket = connected_clients[user_id]
        try:
            await websocket.send_json(notification)
        except Exception:
            connected_clients.pop(user_id, None)