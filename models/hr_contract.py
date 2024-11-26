from datetime import date
from typing import Optional
from sqlalchemy import Column, String, Date, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from models.base import Base
from models.hr import Employee

class Contract(Base):
    """Modèle pour les contrats des employés agricoles"""
    __tablename__ = "hr_contracts"

    id = Column(String, primary_key=True)
    employee_id = Column(String, ForeignKey("hr_employees.id"), nullable=False)
    type = Column(String, nullable=False)  # CDI, CDD, Saisonnier
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    wage = Column(Float, nullable=False)
    position = Column(String, nullable=False)
    department = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relations
    employee = relationship("Employee", back_populates="contracts")
    
    # Métadonnées
    created_at = Column(Date, nullable=False, default=date.today)
    updated_at = Column(Date, nullable=False, default=date.today, onupdate=date.today)
    
    def __repr__(self):
        return f"<Contract {self.id} - {self.employee.name} - {self.type}>"
    
    def to_dict(self):
        """Convertit le contrat en dictionnaire"""
        return {
            "id": self.id,
            "employee_id": self.employee_id,
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
