from datetime import date
from typing import Optional, Dict
from pydantic import BaseModel, Field

class PayrollBase(BaseModel):
    """Schéma de base pour la paie"""
    contract_id: str
    period_start: date
    period_end: date
    worked_hours: float = Field(ge=0)
    overtime_hours: float = Field(ge=0, default=0)
    overtime_amount: float = Field(ge=0, default=0)
    bonus: float = Field(ge=0, default=0)
    deductions: float = Field(ge=0, default=0)
    bonus_details: Dict[str, float] = Field(default_factory=dict)
    deduction_details: Dict[str, float] = Field(default_factory=dict)
    employer_contributions: float = Field(ge=0, default=0)
    employee_contributions: float = Field(ge=0, default=0)

class PayrollCreate(PayrollBase):
    """Schéma pour la création d'une paie"""
    pass

class PayrollUpdate(BaseModel):
    """Schéma pour la mise à jour d'une paie"""
    worked_hours: Optional[float] = Field(None, ge=0)
    overtime_hours: Optional[float] = Field(None, ge=0)
    overtime_amount: Optional[float] = Field(None, ge=0)
    bonus: Optional[float] = Field(None, ge=0)
    deductions: Optional[float] = Field(None, ge=0)
    bonus_details: Optional[Dict[str, float]] = None
    deduction_details: Optional[Dict[str, float]] = None
    employer_contributions: Optional[float] = Field(None, ge=0)
    employee_contributions: Optional[float] = Field(None, ge=0)
    is_paid: Optional[bool] = None
    payment_date: Optional[date] = None

class PayrollResponse(PayrollBase):
    """Schéma pour les réponses de paie"""
    id: str
    base_salary: float
    gross_total: float
    net_total: float
    is_paid: bool
    payment_date: Optional[date] = None
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class PayrollStats(BaseModel):
    """Schéma pour les statistiques de paie"""
    total_gross: float
    total_net: float
    total_employer_contributions: float
    total_employee_contributions: float
    total_bonus: float
    total_deductions: float
    average_gross: float
    average_net: float
    period_start: date
    period_end: date
