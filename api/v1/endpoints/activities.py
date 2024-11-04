from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from models.auth import Utilisateur
from api.v1.endpoints.auth import get_current_user
from services.activity_service import ActivityService
from schemas.activity import ActivityResponse

router = APIRouter()

@router.get("/recent", response_model=List[ActivityResponse])
async def get_recent_activities(
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Récupère les activités récentes"""
    activity_service = ActivityService(db)
    return await activity_service.get_recent_activities(limit)