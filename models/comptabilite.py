from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID

class TypeCompte(str, enum.Enum):
    """Types de comptes comptables"""
    ACTIF = "ACTIF"
    PASSIF = "PASSIF"
    CHARGE = "CHARGE"
    PRODUIT = "PRODUIT"

class CompteComptable(Base):
    """Modèle représentant un compte comptable"""
    __tablename__ = "comptes_comptables"

    numero = Column(String(10), unique=True, nullable=False, index=True)  # Plan comptable OHADA
    libelle = Column(String(200), nullable=False)
    type_compte = Column(Enum(TypeCompte), nullable=False)
    compte_parent_id = Column(UUID(as_uuid=True), ForeignKey("comptes_comptables.id"))
    solde_debit = Column(Numeric(15, 2), default=0)
    solde_credit = Column(Numeric(15, 2), default=0)
    actif = Column(Boolean, default=True)
    description = Column(Text)
    metadata = Column(JSON)

    # Relations
    compte_parent = relationship("CompteComptable", remote_side=[id])
    ecritures = relationship("EcritureComptable", back_populates="compte")

class StatutEcriture(str, enum.Enum):
    """Statuts possibles d'une écriture comptable"""
    BROUILLON = "BROUILLON"
    VALIDEE = "VALIDEE"
    ANNULEE = "ANNULEE"

class EcritureComptable(Base):
    """Modèle représentant une écriture comptable"""
    __tablename__ = "ecritures_comptables"

    date_ecriture = Column(Date, nullable=False)
    numero_piece = Column(String(50), nullable=False)
    compte_id = Column(UUID(as_uuid=True), ForeignKey("comptes_comptables.id"), nullable=False)
    libelle = Column(String(200), nullable=False)
    debit = Column(Numeric(15, 2), default=0)
    credit = Column(Numeric(15, 2), default=0)
    statut = Column(Enum(StatutEcriture), default=StatutEcriture.BROUILLON)
    journal_id = Column(UUID(as_uuid=True), ForeignKey("journaux_comptables.id"), nullable=False)
    transaction_id = Column(UUID(as_uuid=True), ForeignKey("transactions.id"))
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    validee_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    date_validation = Column(DateTime)
    metadata = Column(JSON)

    # Relations
    compte = relationship("CompteComptable", back_populates="ecritures")
    journal = relationship("JournalComptable")
    transaction = relationship("Transaction")
    validee_par = relationship("Employe")

class TypeJournal(str, enum.Enum):
    """Types de journaux comptables"""
    ACHAT = "ACHAT"
    VENTE = "VENTE"
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    OPERATIONS_DIVERSES = "OPERATIONS_DIVERSES"

class JournalComptable(Base):
    """Modèle représentant un journal comptable"""
    __tablename__ = "journaux_comptables"

    code = Column(String(10), unique=True, nullable=False)
    libelle = Column(String(100), nullable=False)
    type_journal = Column(Enum(TypeJournal), nullable=False)
    actif = Column(Boolean, default=True)
    description = Column(Text)
    metadata = Column(JSON)

    # Relations
    ecritures = relationship("EcritureComptable", back_populates="journal")

class ExerciceComptable(Base):
    """Modèle représentant un exercice comptable"""
    __tablename__ = "exercices_comptables"

    annee = Column(String(4), unique=True, nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    cloture = Column(Boolean, default=False)
    date_cloture = Column(DateTime)
    cloture_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    metadata = Column(JSON)

    # Relations
    cloture_par = relationship("Employe")
