from sqlalchemy import Column, String, Float, Enum, JSON, ForeignKey, Text, Numeric, Date, DateTime, Boolean
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid

class TypeCompte(str, enum.Enum):
    """Types de comptes comptables"""
    ACTIF = "ACTIF"
    PASSIF = "PASSIF"
    CHARGE = "CHARGE"
    PRODUIT = "PRODUIT"

class CompteComptable(Base):
    """Modèle représentant un compte comptable"""
    __tablename__ = "comptes_comptables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    numero = Column(String(10), unique=True, nullable=False, index=True)  # Plan comptable OHADA
    libelle = Column(String(200), nullable=False)
    type_compte = Column(Enum(TypeCompte), nullable=False)
    compte_parent_id = Column(UUID(as_uuid=True), ForeignKey("comptes_comptables.id"))
    solde_debit = Column(Numeric(15, 2), default=0)
    solde_credit = Column(Numeric(15, 2), default=0)
    actif = Column(Boolean, default=True)
    description = Column(Text)
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations
    compte_parent = relationship("CompteComptable", remote_side=[id])
    ecritures = relationship("EcritureComptable", back_populates="compte")
    sous_comptes = relationship("CompteComptable", back_populates="compte_parent")

class StatutEcriture(str, enum.Enum):
    """Statuts possibles d'une écriture comptable"""
    BROUILLON = "BROUILLON"
    VALIDEE = "VALIDEE"
    ANNULEE = "ANNULEE"

class EcritureComptable(Base):
    """Modèle représentant une écriture comptable"""
    __tablename__ = "ecritures_comptables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations avec les autres modules
    compte = relationship("CompteComptable", back_populates="ecritures")
    journal = relationship("JournalComptable", back_populates="ecritures")
    transaction = relationship("Transaction")
    validee_par = relationship("Employe")
    documents = relationship("Document", secondary="ecritures_documents")
    
    # Relations avec Production et Inventaire
    parcelle_id = Column(UUID(as_uuid=True), ForeignKey("parcelles.id"))
    recolte_id = Column(UUID(as_uuid=True), ForeignKey("recoltes.id"))
    mouvement_stock_id = Column(UUID(as_uuid=True), ForeignKey("mouvements_stock.id"))
    
    parcelle = relationship("Parcelle")
    recolte = relationship("Recolte")
    mouvement_stock = relationship("MouvementStock")

class TypeJournal(str, enum.Enum):
    """Types de journaux comptables"""
    ACHAT = "ACHAT"
    VENTE = "VENTE"
    BANQUE = "BANQUE"
    CAISSE = "CAISSE"
    OPERATIONS_DIVERSES = "OPERATIONS_DIVERSES"
    PRODUCTION = "PRODUCTION"  # Pour les opérations liées à la production
    STOCKS = "STOCKS"  # Pour les mouvements de stocks

class JournalComptable(Base):
    """Modèle représentant un journal comptable"""
    __tablename__ = "journaux_comptables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(10), unique=True, nullable=False)
    libelle = Column(String(100), nullable=False)
    type_journal = Column(Enum(TypeJournal), nullable=False)
    actif = Column(Boolean, default=True)
    description = Column(Text)
    responsable_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations
    ecritures = relationship("EcritureComptable", back_populates="journal")
    responsable = relationship("Employe")

class ExerciceComptable(Base):
    """Modèle représentant un exercice comptable"""
    __tablename__ = "exercices_comptables"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    annee = Column(String(4), unique=True, nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    cloture = Column(Boolean, default=False)
    date_cloture = Column(DateTime)
    cloture_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations
    cloture_par = relationship("Employe")
    documents = relationship("Document", secondary="exercices_documents")

class EcritureDocument(Base):
    """Table de liaison entre écritures et documents"""
    __tablename__ = "ecritures_documents"

    ecriture_id = Column(UUID(as_uuid=True), ForeignKey("ecritures_comptables.id"), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    type_document = Column(String(50))  # FACTURE, BON_LIVRAISON, etc.
    created_at = Column(DateTime, default=lambda: datetime.now())

class ExerciceDocument(Base):
    """Table de liaison entre exercices et documents"""
    __tablename__ = "exercices_documents"

    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices_comptables.id"), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    type_document = Column(String(50))  # BILAN, COMPTE_RESULTAT, etc.
    created_at = Column(DateTime, default=lambda: datetime.now())

class BudgetLigne(Base):
    """Modèle représentant une ligne budgétaire"""
    __tablename__ = "budget_lignes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices_comptables.id"), nullable=False)
    compte_id = Column(UUID(as_uuid=True), ForeignKey("comptes_comptables.id"), nullable=False)
    montant_prevu = Column(Numeric(15, 2), nullable=False)
    montant_realise = Column(Numeric(15, 2), default=0)
    periode = Column(String(7), nullable=False)  # Format: YYYY-MM
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations
    exercice = relationship("ExerciceComptable")
    compte = relationship("CompteComptable")

class AnalyseFinanciere(Base):
    """Modèle pour les analyses financières"""
    __tablename__ = "analyses_financieres"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exercice_id = Column(UUID(as_uuid=True), ForeignKey("exercices_comptables.id"), nullable=False)
    type_analyse = Column(String(50), nullable=False)  # RATIO, TRESORERIE, etc.
    date_analyse = Column(Date, nullable=False)
    resultats = Column(JSON, nullable=False)  # Stockage flexible des résultats d'analyse
    commentaire = Column(Text)
    creee_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    donnees_supplementaires = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now())
    updated_at = Column(DateTime, default=lambda: datetime.now(), onupdate=lambda: datetime.now())

    # Relations
    exercice = relationship("ExerciceComptable")
    creee_par = relationship("Employe")
    documents = relationship("Document", secondary="analyses_documents")

class AnalyseDocument(Base):
    """Table de liaison entre analyses financières et documents"""
    __tablename__ = "analyses_documents"

    analyse_id = Column(UUID(as_uuid=True), ForeignKey("analyses_financieres.id"), primary_key=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), primary_key=True)
    type_document = Column(String(50))  # RAPPORT, GRAPHIQUE, etc.
    created_at = Column(DateTime, default=lambda: datetime.now())
