from datetime import date
from typing import Optional, List
from sqlalchemy import Column, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from models.base import Base

class Contract(Base):
    """Modèle pour les contrats des employés agricoles"""
    __tablename__ = "hr_contracts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type = Column(String(50), nullable=False)  # CDI, CDD, Saisonnier
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    wage = Column(Float, nullable=False)
    position = Column(String(100), nullable=False)
    department = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relations
    employe = relationship("Employe", back_populates="contracts")
    payrolls = relationship("Payroll", back_populates="contract")
    
    # Métadonnées
    created_at = Column(Date, nullable=False, default=date.today)
    updated_at = Column(Date, nullable=False, default=date.today, onupdate=date.today)
    
    def __repr__(self):
        return f"<Contract {self.id} - {self.employe.nom} - {self.type}>"
    
    def to_dict(self):
        """Convertit le contrat en dictionnaire"""
        return {
            "id": str(self.id),
            "employe_id": str(self.employe_id),
            "type": self.type,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "wage": self.wage,
            "position": self.position,
            "department": self.department,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
