from datetime import date
from typing import Optional
from pydantic import BaseModel, Field

class ContractBase(BaseModel):
    """Schéma de base pour les contrats"""
    type: str = Field(..., description="Type de contrat (CDI, CDD, Saisonnier)")
    start_date: date = Field(..., description="Date de début du contrat")
    end_date: Optional[date] = Field(None, description="Date de fin du contrat (optionnel pour CDI)")
    wage: float = Field(..., description="Salaire")
    position: str = Field(..., description="Poste occupé")
    department: str = Field(..., description="Département/Service")

class ContractCreate(ContractBase):
    """Schéma pour la création d'un contrat"""
    employee_id: str = Field(..., description="ID de l'employé")

class ContractUpdate(ContractBase):
    """Schéma pour la mise à jour d'un contrat"""
    is_active: Optional[bool] = Field(None, description="Statut actif/inactif du contrat")

class ContractInDB(ContractBase):
    """Schéma pour un contrat en base de données"""
    id: str
    employee_id: str
    is_active: bool
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True

class ContractResponse(ContractInDB):
    """Schéma pour la réponse API"""
    employee_name: str = Field(..., description="Nom de l'employé")
