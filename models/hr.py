from sqlalchemy import Column, String, Enum, JSON, ForeignKey, Text, Date, DateTime, Boolean, Numeric
from sqlalchemy.orm import relationship
from .base import Base
import enum
from datetime import datetime
from typing import Optional
from sqlalchemy.dialects.postgresql import UUID
import uuid
from .hr_agricole import TypePersonnel

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

    # Relations avec Tasks
    taches_assignees = relationship("Task", back_populates="assignee")

    # Relations RH
    presences = relationship("Presence", back_populates="employe")
    conges = relationship("Conge", back_populates="employe")
    formations = relationship("Formation", back_populates="employe")
    evaluations = relationship("Evaluation", back_populates="employe")
    documents_rh = relationship("DocumentRH", back_populates="employe")

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
    validee_par = relationship("Employe", foreign_keys=[validee_par_id])

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
    approuve_par = relationship("Employe", foreign_keys=[approuve_par_id])
    piece_jointe = relationship("Document")

class TypeFormation(str, enum.Enum):
    """Types de formations possibles"""
    TECHNIQUE = "TECHNIQUE"
    SECURITE = "SECURITE"
    MANAGEMENT = "MANAGEMENT"
    QUALITE = "QUALITE"
    AUTRE = "AUTRE"

class Formation(Base):
    """Modèle représentant une formation"""
    __tablename__ = "formations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_formation = Column(Enum(TypeFormation), nullable=False)
    titre = Column(String(200), nullable=False)
    description = Column(Text)
    date_debut = Column(Date, nullable=False)
    date_fin = Column(Date, nullable=False)
    formateur = Column(String(100))
    lieu = Column(String(100))
    cout = Column(Numeric(10, 2))
    certification = Column(Boolean, default=False)
    resultat = Column(String(50))
    commentaire = Column(Text)
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="formations")
    details_agricoles = relationship("FormationAgricole", back_populates="formation")

class TypeEvaluation(str, enum.Enum):
    """Types d'évaluations possibles"""
    ANNUELLE = "ANNUELLE"
    PROBATION = "PROBATION"
    PROJET = "PROJET"
    PERFORMANCE = "PERFORMANCE"

class Evaluation(Base):
    """Modèle représentant une évaluation"""
    __tablename__ = "evaluations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    type_evaluation = Column(Enum(TypeEvaluation), nullable=False)
    date_evaluation = Column(Date, nullable=False)
    evaluateur_id = Column(UUID(as_uuid=True), ForeignKey("employes.id"), nullable=False)
    objectifs = Column(JSON)  # Liste des objectifs et leur statut
    competences = Column(JSON)  # Évaluation des compétences
    realisations = Column(JSON)  # Réalisations principales
    commentaire = Column(Text)
    plan_action = Column(JSON)  # Actions de développement prévues
    donnees_supplementaires = Column(JSON)

    # Relations
    employe = relationship("Employe", back_populates="evaluations", foreign_keys=[employe_id])
    evaluateur = relationship("Employe", foreign_keys=[evaluateur_id])
    details_agricoles = relationship("EvaluationAgricole", back_populates="evaluation")

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
