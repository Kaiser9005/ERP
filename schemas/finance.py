from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict
from models.finance import TypeTransaction, StatutTransaction, CategorieTransaction, TypeCompte

class TransactionBase(BaseModel):
    reference: str
    date_transaction: datetime
    type_transaction: TypeTransaction
    categorie: CategorieTransaction
    montant: float
    devise: str = "XAF"
    description: Optional[str]
    compte_source_id: Optional[UUID4]
    compte_destination_id: Optional[UUID4]
    metadata: Optional[Dict]

class TransactionCreate(TransactionBase):
    piece_jointe: Optional[str]

class TransactionUpdate(TransactionBase):
    reference: Optional[str]
    statut: Optional[StatutTransaction]
    date_validation: Optional[datetime]
    validee_par_id: Optional[UUID4]

class TransactionResponse(TransactionBase):
    id: UUID4
    statut: StatutTransaction
    piece_jointe: Optional[str]
    date_validation: Optional[datetime]
    validee_par_id: Optional[UUID4]
    
    class Config:
        orm_mode = True

class CompteBase(BaseModel):
    numero: str
    libelle: str
    type_compte: TypeCompte
    devise: str = "XAF"
    banque: Optional[str]
    iban: Optional[str]
    swift: Optional[str]
    description: Optional[str]
    metadata: Optional[Dict]

class CompteCreate(CompteBase):
    pass

class CompteUpdate(CompteBase):
    numero: Optional[str]
    libelle: Optional[str]
    type_compte: Optional[TypeCompte]
    actif: Optional[bool]

class CompteResponse(CompteBase):
    id: UUID4
    solde: float
    actif: bool
    
    class Config:
        orm_mode = True

class BudgetBase(BaseModel):
    periode: str
    categorie: CategorieTransaction
    montant_prevu: float
    notes: Optional[str]
    metadata: Optional[Dict]

class BudgetCreate(BudgetBase):
    pass

class BudgetUpdate(BudgetBase):
    montant_realise: Optional[float]

class BudgetResponse(BudgetBase):
    id: UUID4
    montant_realise: float
    
    class Config:
        orm_mode = True