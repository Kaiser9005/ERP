from datetime import date
from typing import Optional, List
from sqlalchemy import Column, String, Date, Float, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

from models.base import Base
from models.hr_contract import Contract

class Payroll(Base):
    """Modèle pour la gestion de la paie"""
    __tablename__ = "hr_payrolls"

    id = Column(String, primary_key=True)
    contract_id = Column(String, ForeignKey("hr_contracts.id"), nullable=False)
    period_start = Column(Date, nullable=False)
    period_end = Column(Date, nullable=False)
    
    # Temps de travail
    worked_hours = Column(Float, nullable=False, default=0)
    overtime_hours = Column(Float, nullable=False, default=0)
    
    # Montants
    base_salary = Column(Float, nullable=False)  # Salaire de base depuis le contrat
    overtime_amount = Column(Float, nullable=False, default=0)
    bonus = Column(Float, nullable=False, default=0)
    deductions = Column(Float, nullable=False, default=0)
    
    # Détails des primes et déductions
    bonus_details = Column(JSON)  # {type: montant} ex: {"prime_agricole": 100}
    deduction_details = Column(JSON)  # {type: montant} ex: {"absence": -50}
    
    # Cotisations
    employer_contributions = Column(Float, nullable=False, default=0)
    employee_contributions = Column(Float, nullable=False, default=0)
    
    # Totaux
    gross_total = Column(Float, nullable=False)
    net_total = Column(Float, nullable=False)
    
    # Statut
    is_paid = Column(Boolean, default=False)
    payment_date = Column(Date)
    
    # Relations
    contract = relationship("Contract", back_populates="payrolls")
    
    # Métadonnées
    created_at = Column(Date, nullable=False, default=date.today)
    updated_at = Column(Date, nullable=False, default=date.today, onupdate=date.today)
    
    def __repr__(self):
        return f"<Payroll {self.id} - {self.contract.employee.name} - {self.period_start}>"
    
    def calculate_totals(self):
        """Calcule les totaux brut et net"""
        # Calcul du brut
        self.gross_total = (
            self.base_salary +
            self.overtime_amount +
            self.bonus -
            self.deductions
        )
        
        # Calcul du net
        self.net_total = self.gross_total - self.employee_contributions
        
        return self.gross_total, self.net_total
    
    def to_dict(self):
        """Convertit la paie en dictionnaire"""
        return {
            "id": self.id,
            "contract_id": self.contract_id,
            "period_start": self.period_start.isoformat(),
            "period_end": self.period_end.isoformat(),
            "worked_hours": self.worked_hours,
            "overtime_hours": self.overtime_hours,
            "base_salary": self.base_salary,
            "overtime_amount": self.overtime_amount,
            "bonus": self.bonus,
            "deductions": self.deductions,
            "bonus_details": self.bonus_details,
            "deduction_details": self.deduction_details,
            "employer_contributions": self.employer_contributions,
            "employee_contributions": self.employee_contributions,
            "gross_total": self.gross_total,
            "net_total": self.net_total,
            "is_paid": self.is_paid,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
