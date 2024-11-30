from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TypeTransaction(str, enum.Enum):
    """Types de transactions financières"""
    RECETTE = "RECETTE"
    DEPENSE = "DEPENSE"
    VIREMENT = "VIREMENT"

class StatutTransaction(str, enum.Enum):
    """Statuts possibles d'une transaction"""
    EN_ATTENTE = "EN_ATTENTE"
    VALIDEE = "VALIDEE"
    REJETEE = "REJETEE"
    ANNULEE = "ANNULEE"

class CategorieTransaction(str, enum.Enum):
    """Catégories de transactions"""
    VENTE = "VENTE"
    ACHAT_INTRANT = "ACHAT_INTRANT"
    SALAIRE = "SALAIRE"
    MAINTENANCE = "MAINTENANCE"
    TRANSPORT = "TRANSPORT"
    AUTRE = "AUTRE"

class Transaction(Base):
    """Modèle représentant une transaction financière"""
    __tablename__ = "transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    reference = Column(String(50), unique=True, index=True, nullable=False)
    date_transaction = Column(DateTime, nullable=False)
    type_transaction = Column(Enum(TypeTransaction), nullable=False)
    categorie = Column(Enum(CategorieTransaction), nullable=False)
    montant = Column(Numeric(15, 2), nullable=False)
    devise = Column(String(3), default="XAF")
    description = Column(Text)
    statut = Column(Enum(StatutTransaction), default=StatutTransaction.EN_ATTENTE)
    compte_source_id = Column(UUID(as_uuid=True), ForeignKey("comptes.id"))
    compte_destination_id = Column(UUID(as_uuid=True), ForeignKey("comptes.id"))
    piece_jointe = Column(String(500))  # Chemin vers le document justificatif
    donnees_supplementaires = Column(JSON)  # Données supplémentaires spécifiques au type
    validee_par_id = Column(UUID(as_uuid=True), ForeignKey("utilisateurs.id"))
    date_validation = Column(DateTime)

    # Relations
    compte_source = relationship("Compte", foreign_keys=[compte_source_id])
    compte_destination = relationship("Compte", foreign_keys=[compte_destination_id])
    validee_par = relationship("Utilisateur", foreign_keys=[validee_par_id])

class TypeCompte(str, enum.Enum):
    """Types de comptes financiers"""
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    EPARGNE = "EPARGNE"

class Compte(Base):
    """Modèle représentant un compte financier"""
    __tablename__ = "comptes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero = Column(String(50), unique=True, index=True, nullable=False)
    libelle = Column(String(200), nullable=False)
    type_compte = Column(Enum(TypeCompte), nullable=False)
    devise = Column(String(3), default="XAF")
    solde = Column(Numeric(15, 2), default=0)
    banque = Column(String(100))  # Pour les comptes bancaires
    iban = Column(String(50))
    swift = Column(String(20))
    actif = Column(Boolean, default=True)
    description = Column(Text)
    donnees_supplementaires = Column(JSON)  # Informations supplémentaires

class Budget(Base):
    """Modèle représentant un budget"""
    __tablename__ = "budgets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    categorie = Column(Enum(CategorieTransaction), nullable=False)
    montant_prevu = Column(Numeric(15, 2), nullable=False)
    montant_realise = Column(Numeric(15, 2), default=0)
    notes = Column(Text)
    donnees_supplementaires = Column(JSON)  # Données de ventilation ou autres
