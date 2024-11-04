from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional
from models.hr import DepartementType, StatutEmploye, TypeContrat

class EmployeBase(BaseModel):
    matricule: str
    nom: str
    prenom: str
    date_naissance: date
    lieu_naissance: Optional[str] = None
    sexe: str
    adresse: Optional[str] = None
    telephone: Optional[str] = None
    email: Optional[EmailStr] = None
    departement: DepartementType
    poste: str
    date_embauche: date
    type_contrat: TypeContrat
    salaire_base: float

class EmployeCreate(EmployeBase):
    pass

class EmployeUpdate(EmployeBase):
    statut: Optional[StatutEmploye] = None

class EmployeResponse(EmployeBase):
    id: str
    statut: StatutEmploye
    
    class Config:
        orm_mode = True