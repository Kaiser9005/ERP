from sqlalchemy import Column, String, Enum, JSON, ForeignKey, Text, Date, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship, Mapped

from .base import Base
import enum
from datetime import datetime
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .hr_agricole import TypePersonnel
from models.tache import Tache
from models.hr_contract import Contract

class DepartementType(str, enum.Enum):
    """Types de départements possibles"""
    PRODUCTION = "PRODUCTION"
    FINANCE = "FINANCE"
    RH = "RH"
    LOGISTIQUE = "LOGISTIQUE"
    QUALITE = "QUALITE"
    MAINTENANCE = "MAINTENANCE"
    ADMINISTRATION = "ADMINISTRATION"

class StatutEmploye(str, enum.Enum):
    """Statuts possibles d'un employé"""
    ACTIF = "ACTIF"
    INACTIF = "INACTIF"
    CONGE = "CONGE"
    SUSPENDU = "SUSPENDU"

class TypeContrat(str, enum.Enum):
    """Types de contrats possibles"""
    CDI = "CDI"
    CDD = "CDD"
    STAGE = "STAGE"
    INTERIM = "INTERIM"

class NiveauAcces(str, enum.Enum):
    """Niveaux d'accès système"""
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    SUPERVISEUR = "SUPERVISEUR"
    UTILISATEUR = "UTILISATEUR"

class Employe(Base):
    """Modèle représentant un employé"""
    __tablename__ = "employes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    matricule = Column(String(50), unique=True, nullable=False)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    date_naissance = Column(Date)
    date_embauche = Column(Date, nullable=False)
    date_depart = Column(Date)
    statut = Column(Enum(StatutEmploye), default=StatutEmploye.ACTIF)
    type_contrat = Column(Enum(TypeContrat))
    type_personnel = Column(Enum(TypePersonnel))  # Nouveau: type de personnel agricole
    poste = Column(String(100))
    departement = Column(Enum(DepartementType))
    niveau_acces = Column(Enum(NiveauAcces), default=NiveauAcces.UTILISATEUR)
    email = Column(String(200))
    telephone = Column(String(20))
    adresse = Column(Text)
    salaire_base = Column(Numeric(10, 2))
    compte_bancaire = Column(String(50))
    donnees_supplementaires = Column(JSON)

    # Relations avec Production
    parcelles_gerees = relationship("Parcelle", back_populates="responsable")
    evenements_production = relationship("ProductionEvent", back_populates="responsable")

    # Relations avec Comptabilité
    ecritures_validees = relationship("EcritureComptable", back_populates="validee_par")
    exercices_clotures = relationship("ExerciceComptable", back_populates="cloture_par")

    # Relations avec Documents
    documents_charges = relationship("Document", back_populates="uploaded_by")

    # Relations avec Taches
    taches_assignees = relationship("Tache", back_populates="responsable")
    commentaires_tache = relationship("CommentaireTache", back_populates="auteur")

    # Relations RH
    presences = relationship("Presence", back_populates="employe", foreign_keys="[Presence.employe_id]")
    presences_validees = relationship("Presence", foreign_keys="[Presence.validee_par_id]")
    conges = relationship("Conge", back_populates="employe", foreign_keys="[Conge.employe_id]")
    conges_approuves = relationship("Conge", foreign_keys="[Conge.approuve_par_id]")
    participations_formations = relationship("ParticipationFormation", back_populates="employe")
    evaluations_recues = relationship("Evaluation", back_populates="employe", foreign_keys="[Evaluation.employe_id]")
    evaluations_donnees = relationship("Evaluation", back_populates="evaluateur", foreign_keys="[Evaluation.evaluateur_id]")
    documents_rh = relationship("DocumentRH", back_populates="employe")
    contracts: Mapped[List[Contract]] = relationship(Contract, back_populates="employe")
    projets_geres = relationship("Project", back_populates="responsable")

    # Relations RH Agricole
    competences_agricoles = relationship("CompetenceAgricole", back_populates="employe")
    affectations_parcelles = relationship("AffectationParcelle", back_populates="employe")
    conditions_travail = relationship("ConditionTravailAgricole", back_populates="employe")

class TypePresence(str, enum.Enum):
    """Types de présence possibles"""
    PRESENT = "PRESENT"
    ABSENT = "ABSENT"
    RETARD = "RETARD"
    MISSION = "MISSION"
    FORMATION = "FORMATION"
    TELETRAVAIL = "TELETRAVAIL"

class Presence(Base):
    """Modèle représentant une présence"""
    __tablename__ = "presences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    date = Column(Date, nullable=False)
    heure_arrivee = Column(DateTime)
    heure_depart = Column(DateTime)
    type_presence = Column(Enum(TypePresence), nullable=False)
    lieu = Column(String(100))  # Pour les missions/formations
    commentaire = Column(Text)
    validee = Column(Boolean, default=False)
    validee_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="presences", foreign_keys=[employe_id])
    validee_par = relationship("Employe", back_populates="presences_validees", foreign_keys=[validee_par_id])

class TypeConge(str, enum.Enum):
    """Types de congés possibles"""
    CONGE_PAYE = "CONGE_PAYE"
    MALADIE = "MALADIE"
    MATERNITE = "MATERNITE"
    PATERNITE = "PATERNITE"
    SANS_SOLDE = "SANS_SOLDE"
    FORMATION = "FORMATION"
    AUTRE = "AUTRE"

class StatutConge(str, enum.Enum):
    """Statuts possibles d'une demande de congé"""
    EN_ATTENTE = "EN_ATTENTE"
    APPROUVE = "APPROUVE"
    REFUSE = "REFUSE"
    ANNULE = "ANNULE"

class Conge(Base):
    """Modèle représentant un congé"""
    __tablename__ = "conges"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_conge = Column(Enum(TypeConge), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    statut = Column(Enum(StatutConge), default=StatutConge.EN_ATTENTE)
    motif = Column(Text)
    commentaire = Column(Text)
    piece_jointe_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"))
    approuve_par_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"))
    date_approbation = Column(DateTime)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="conges", foreign_keys=[employe_id])
    approuve_par = relationship("Employe", back_populates="conges_approuves", foreign_keys=[approuve_par_id])
    piece_jointe = relationship("Document")

class TypeFormation(str, enum.Enum):
    """Types de formations possibles"""
    TECHNIQUE = "TECHNIQUE"
    SECURITE = "SECURITE"
    MANAGEMENT = "MANAGEMENT"
    QUALITE = "QUALITE"
    AUTRE = "AUTRE"

class TypeEvaluation(str, enum.Enum):
    """Types d'évaluations possibles"""
    ANNUELLE = "ANNUELLE"
    PROBATION = "PROBATION"
    PROJET = "PROJET"
    PERFORMANCE = "PERFORMANCE"

class TypeDocumentRH(str, enum.Enum):
    """Types de documents RH"""
    CONTRAT = "CONTRAT"
    AVENANT = "AVENANT"
    DIPLOME = "DIPLOME"
    CERTIFICATION = "CERTIFICATION"
    EVALUATION = "EVALUATION"
    AUTRE = "AUTRE"

class DocumentRH(Base):
    """Modèle représentant un document RH"""
    __tablename__ = "documents_rh"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_document = Column(Enum(TypeDocumentRH), nullable=False)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=False)
    date_effet = Column(Date)
    date_expiration = Column(Date)
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="documents_rh")
    document = relationship("Document")
