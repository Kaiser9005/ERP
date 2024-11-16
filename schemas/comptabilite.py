from typing import Optional, Dict, Any, List, Literal
from datetime import date, datetime
from enum import Enum
from decimal import Decimal
from pydantic import BaseModel, UUID4, Field, field_validator, model_validator

class TypeCompte(str, Enum):
    ACTIF = "ACTIF"
    PASSIF = "PASSIF"
    CHARGE = "CHARGE"
    PRODUIT = "PRODUIT"

class TypeJournal(str, Enum):
    ACHAT = "ACHAT"
    VENTE = "VENTE"
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    OPERATIONS_DIVERSES = "OPERATIONS_DIVERSES"

class StatutEcriture(str, Enum):
    BROUILLON = "BROUILLON"
    VALIDEE = "VALIDEE"
    ANNULEE = "ANNULEE"

class BaseSchema(BaseModel):
    """Schéma de base avec champs de traçabilité"""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by_id: Optional[UUID4] = None
    updated_by_id: Optional[UUID4] = None

    model_config = {
        "from_attributes": True,
        "json_schema_extra": lambda schema: {
            prop.pop("title", None) for prop in schema.get("properties", {}).values()
        }
    }

# Schémas de base
class CompteComptableBase(BaseSchema):
    numero: str = Field(..., min_length=1, max_length=10)
    libelle: str = Field(..., min_length=1, max_length=200)
    type_compte: TypeCompte
    compte_parent_id: Optional[UUID4] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class EcritureComptableBase(BaseSchema):
    date_ecriture: date
    numero_piece: str = Field(..., min_length=1, max_length=50)
    compte_id: UUID4
    libelle: str = Field(..., min_length=1, max_length=200)
    debit: Decimal = Field(default=Decimal('0'), ge=0, max_digits=15, decimal_places=2)
    credit: Decimal = Field(default=Decimal('0'), ge=0, max_digits=15, decimal_places=2)
    journal_id: UUID4
    transaction_id: Optional[UUID4] = None
    metadata: Optional[Dict[str, Any]] = None

    @field_validator('date_ecriture')
    @classmethod
    def validate_date_ecriture(cls, v: date) -> date:
        if v > date.today():
            raise ValueError('La date d\'écriture ne peut pas être dans le futur')
        return v

class JournalComptableBase(BaseSchema):
    code: str = Field(..., min_length=1, max_length=10)
    libelle: str = Field(..., min_length=1, max_length=100)
    type_journal: TypeJournal
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ExerciceComptableBase(BaseSchema):
    annee: str = Field(..., min_length=4, max_length=4)
    date_debut: date
    date_fin: date
    metadata: Optional[Dict[str, Any]] = None

    @field_validator('date_fin')
    @classmethod
    def validate_dates_exercice(cls, v: date, info: Dict[str, Any]) -> date:
        if 'date_debut' in info.data and v <= info.data['date_debut']:
            raise ValueError('La date de fin doit être postérieure à la date de début')
        return v

    @field_validator('annee')
    @classmethod
    def validate_annee(cls, v: str) -> str:
        try:
            annee = int(v)
            if annee < 1900 or annee > 2100:
                raise ValueError()
        except ValueError:
            raise ValueError('L\'année doit être un nombre entre 1900 et 2100')
        return v

# Schémas de création
class CompteComptableCreate(CompteComptableBase):
    pass

class EcritureComptableCreate(EcritureComptableBase):
    @model_validator(mode='after')
    def validate_montant_non_nul(self) -> 'EcritureComptableCreate':
        if self.debit > 0 and self.credit > 0:
            raise ValueError('Une écriture ne peut pas être à la fois débitrice et créditrice')
        return self

class JournalComptableCreate(JournalComptableBase):
    pass

class ExerciceComptableCreate(ExerciceComptableBase):
    pass

# Schémas de mise à jour
class CompteComptableUpdate(BaseModel):
    libelle: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    actif: Optional[bool] = None
    metadata: Optional[Dict[str, Any]] = None
    updated_by_id: Optional[UUID4] = None

class EcritureComptableUpdate(BaseModel):
    libelle: Optional[str] = Field(None, min_length=1, max_length=200)
    debit: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    credit: Optional[Decimal] = Field(None, ge=0, max_digits=15, decimal_places=2)
    metadata: Optional[Dict[str, Any]] = None
    updated_by_id: Optional[UUID4] = None

# Schémas de réponse
class CompteComptableResponse(CompteComptableBase):
    id: UUID4
    solde_debit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    solde_credit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    actif: bool

class EcritureComptableResponse(EcritureComptableBase):
    id: UUID4
    statut: StatutEcriture
    periode: str
    validee_par_id: Optional[UUID4] = None
    date_validation: Optional[datetime] = None

class JournalComptableResponse(JournalComptableBase):
    id: UUID4
    actif: bool

class ExerciceComptableResponse(ExerciceComptableBase):
    id: UUID4
    cloture: bool
    date_cloture: Optional[datetime] = None
    cloture_par_id: Optional[UUID4] = None

# Schémas pour les rapports
class LigneGrandLivre(BaseModel):
    date: date
    piece: str
    libelle: str
    debit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    credit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    solde: Decimal = Field(..., max_digits=15, decimal_places=2)

class CompteBalance(BaseModel):
    compte: Dict[str, Any]
    debit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    credit: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    solde: Decimal = Field(..., max_digits=15, decimal_places=2)

class BilanResponse(BaseModel):
    actif: Dict[str, Dict[str, Any]]
    passif: Dict[str, Dict[str, Any]]
    total_actif: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    total_passif: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)

class CompteResultatResponse(BaseModel):
    produits: Dict[str, Dict[str, Any]]
    charges: Dict[str, Dict[str, Any]]
    total_produits: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    total_charges: Decimal = Field(..., ge=0, max_digits=15, decimal_places=2)
    resultat_net: Decimal = Field(..., max_digits=15, decimal_places=2)
