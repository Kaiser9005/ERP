from sqlalchemy import Column, String, Float, ForeignKey, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid

from .base import Base
from .auth import Utilisateur

class CategoryProduit(str, enum.Enum):
    INTRANT = "INTRANT"
    EQUIPEMENT = "EQUIPEMENT"
    RECOLTE = "RECOLTE"
    EMBALLAGE = "EMBALLAGE"
    PIECE_RECHANGE = "PIECE_RECHANGE"

class UniteMesure(str, enum.Enum):
    KG = "KG"
    LITRE = "LITRE"
    UNITE = "UNITE"
    TONNE = "TONNE"
    METRE = "METRE"

class TypeMouvement(str, enum.Enum):
    ENTREE = "ENTREE"
    SORTIE = "SORTIE"
    TRANSFERT = "TRANSFERT"

class Produit(Base):
    __tablename__ = "produits"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    code = Column(String, unique=True, nullable=False)
    nom = Column(String, nullable=False)
    description = Column(String)
    categorie = Column(Enum(CategoryProduit), nullable=False)
    unite_mesure = Column(Enum(UniteMesure), nullable=False)
    prix_unitaire = Column(Float)
    seuil_alerte = Column(Float)
    specifications = Column(JSON)
    date_derniere_maj = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    stocks = relationship("Stock", back_populates="produit", cascade="all, delete-orphan")
    mouvements = relationship("MouvementStock", back_populates="produit", cascade="all, delete-orphan")

class Stock(Base):
    __tablename__ = "stocks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    produit_id = Column(String, ForeignKey("produits.id"), nullable=False)
    entrepot_id = Column(String, ForeignKey("entrepots.id"), nullable=False)
    quantite = Column(Float, nullable=False, default=0)
    valeur_unitaire = Column(Float)
    emplacement = Column(String)
    lot = Column(String)
    date_derniere_maj = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    produit = relationship("Produit", back_populates="stocks")

class MouvementStock(Base):
    __tablename__ = "mouvements_stock"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    produit_id = Column(String, ForeignKey("produits.id"), nullable=False)
    type_mouvement = Column(Enum(TypeMouvement), nullable=False)
    quantite = Column(Float, nullable=False)
    date_mouvement = Column(DateTime, default=datetime.utcnow)
    entrepot_source_id = Column(String, ForeignKey("entrepots.id"))
    entrepot_destination_id = Column(String, ForeignKey("entrepots.id"))
    responsable_id = Column(String, ForeignKey("utilisateurs.id"))
    reference_document = Column(String)
    notes = Column(String)
    cout_unitaire = Column(Float)

    produit = relationship("Produit", back_populates="mouvements")
    responsable = relationship("Utilisateur")

    def to_dict(self):
        return {
            "id": self.id,
            "produit_id": self.produit_id,
            "type_mouvement": self.type_mouvement,
            "quantite": self.quantite,
            "date_mouvement": self.date_mouvement.isoformat() if self.date_mouvement else None,
            "entrepot_source_id": self.entrepot_source_id,
            "entrepot_destination_id": self.entrepot_destination_id,
            "responsable_id": self.responsable_id,
            "responsable": {
                "id": self.responsable.id,
                "nom": self.responsable.nom,
                "prenom": self.responsable.prenom
            } if self.responsable else None,
            "reference_document": self.reference_document,
            "notes": self.notes,
            "cout_unitaire": self.cout_unitaire
        }
