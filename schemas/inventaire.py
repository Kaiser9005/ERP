from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional, Dict
from enum import Enum

class CategoryProduit(str, Enum):
    INTRANT = "INTRANT"
    EQUIPEMENT = "EQUIPEMENT"
    RECOLTE = "RECOLTE"
    EMBALLAGE = "EMBALLAGE"
    PIECE_RECHANGE = "PIECE_RECHANGE"

class UniteMesure(str, Enum):
    KG = "KG"
    LITRE = "LITRE"
    UNITE = "UNITE"
    TONNE = "TONNE"
    METRE = "METRE"

class TypeMouvement(str, Enum):
    ENTREE = "ENTREE"
    SORTIE = "SORTIE"
    TRANSFERT = "TRANSFERT"

class ProduitBase(BaseModel):
    code: str
    nom: str
    categorie: CategoryProduit
    description: Optional[str]
    unite_mesure: UniteMesure
    seuil_alerte: Optional[float]
    prix_unitaire: Optional[float]
    specifications: Optional[Dict]

class ProduitCreate(ProduitBase):
    pass

class ProduitResponse(ProduitBase):
    id: UUID4
    
    class Config:
        orm_mode = True

class MouvementStockBase(BaseModel):
    produit_id: UUID4
    type_mouvement: TypeMouvement
    quantite: float
    entrepot_source_id: Optional[UUID4]
    entrepot_destination_id: Optional[UUID4]
    responsable_id: UUID4
    reference_document: Optional[str]
    notes: Optional[str]
    cout_unitaire: Optional[float]

class MouvementStockCreate(MouvementStockBase):
    pass

class MouvementStockResponse(MouvementStockBase):
    id: UUID4
    date_mouvement: datetime
    
    class Config:
        orm_mode = True

class StockBase(BaseModel):
    produit_id: UUID4
    entrepot_id: UUID4
    quantite: float
    valeur_unitaire: Optional[float]
    emplacement: Optional[str]
    lot: Optional[str]

class StockResponse(StockBase):
    id: UUID4
    date_derniere_maj: datetime
    
    class Config:
        orm_mode = True
