from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime, UUID
from datetime import datetime, timezone
import uuid

Base = declarative_base()

class BaseModel(Base):
    """Classe de base pour tous les modèles"""
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), 
                       onupdate=lambda: datetime.now(timezone.utc), nullable=False)
