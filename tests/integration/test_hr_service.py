"""Tests d'intégration pour le service RH."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.hr_service import HRService
from models.hr import (
    Employe, Contrat, Conge, Presence,
    DepartementType, StatutEmploye, TypeContrat, TypeConge, StatutConge, TypePresence
)
from models import (
    CompetenceAgricole, CertificationAgricole, AffectationParcelle,
    ConditionTravailAgricole, FormationAgricole, EvaluationAgricole,
    TypePersonnel, SpecialiteAgricole, NiveauCompetence, TypeCertification
)
from unittest.mock import Mock
import uuid

@pytest.fixture
async def create_test_employe(db: Session):
    """Fixture pour créer un employé de test"""
    async def _create_employe(
        matricule: str,
        nom: str,
        prenom: str,
        departement: DepartementType = DepartementType.PRODUCTION,
        statut: StatutEmploye = StatutEmploye.ACTIF,
        salaire_base: int = 200000
    ) -> Employe:
        employe = Employe(
            matricule=matricule,
            nom=nom,
            prenom=prenom,
            date_naissance=datetime.now().date() - timedelta(days=365*30),
            sexe="M",
            departement=departement,
            poste="Ouvrier",
            date_embauche=datetime.now().date() - timedelta(days=180),
            type_contrat=TypeContrat.CDI,
            salaire_base=salaire_base,
            statut=statut
        )
        db.add(employe)
        db.commit()
        db.refresh(employe)
        return employe
    return _create_employe

@pytest.mark.asyncio
async def test_get_stats(db: Session, create_test_employe):
    """Test de récupération des statistiques RH"""
    service = HRService(db)
    
    # Créer des employés avec différents statuts
    for i in range(5):
        await create_test_employe(
            matricule=f"EMP00{i+1}",
            nom=f"Nom{i+1}",
            prenom=f"Prenom{i+1}",
            statut=StatutEmploye.ACTIF if i < 3 else StatutEmploye.CONGE
        )

    stats = await service.get_stats()
    assert stats["effectif_total"] == 5
    assert stats["actifs"] == 3
    assert stats["en_conge"] == 2

@pytest.mark.asyncio
async def test_create_leave_request(db: Session, create_test_employe):
    """Test de création d'une demande de congé"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP007",
        nom="Martin",
        prenom="Marie",
        departement=DepartementType.ADMINISTRATION
    )

    # Créer une demande de congé
    conge_data = {
        "employe_id": str(employe.id),
        "type_conge": TypeConge.ANNUEL,
        "date_debut": datetime.now().date() + timedelta(days=30),
        "date_fin": datetime.now().date() + timedelta(days=45),
        "motif": "Congés annuels"
    }

    conge = await service.create_leave_request(conge_data)
    assert conge.type_conge == TypeConge.ANNUEL
    assert conge.nb_jours == 15
    assert conge.statut == StatutConge.EN_ATTENTE

@pytest.mark.asyncio
async def test_track_attendance(db: Session, create_test_employe):
    """Test du suivi des présences"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP008",
        nom="Dubois",
        prenom="Pierre"
    )

    # Enregistrer une présence
    presence_data = {
        "employe_id": str(employe.id),
        "date": datetime.now().date(),
        "type_presence": TypePresence.PRESENT,
        "heure_arrivee": datetime.now().replace(hour=8, minute=0),
        "heure_depart": datetime.now().replace(hour=17, minute=0)
    }

    presence = await service.track_attendance(presence_data)
    assert presence.type_presence == TypePresence.PRESENT
    assert presence.heures_travaillees == 9

@pytest.mark.asyncio
async def test_approve_leave_request(db: Session, create_test_employe, test_user: dict):
    """Test d'approbation d'une demande de congé"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP009",
        nom="Petit",
        prenom="Sophie",
        departement=DepartementType.LOGISTIQUE
    )

    # Créer une demande de congé
    conge = Conge(
        employe_id=employe.id,
        type_conge=TypeConge.ANNUEL,
        date_debut=datetime.now().date() + timedelta(days=15),
        date_fin=datetime.now().date() + timedelta(days=30),
        nb_jours=15,
        motif="Congés annuels",
        statut=StatutConge.EN_ATTENTE
    )
    db.add(conge)
    db.commit()

    # Approuver la demande
    updated_conge = await service.approve_leave_request(
        str(conge.id),
        str(test_user.id)
    )
    assert updated_conge.statut == StatutConge.APPROUVE
    assert updated_conge.approuve_par_id == test_user.id

    # Vérifier le statut de l'employé
    db.refresh(employe)
    assert employe.statut == StatutEmploye.ACTIF  # Le statut changera à CONGE à la date de début

@pytest.mark.asyncio
async def test_reject_leave_request(db: Session, create_test_employe, test_user: dict):
    """Test de rejet d'une demande de congé"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP010",
        nom="Leroy",
        prenom="Paul"
    )

    # Créer une demande de congé
    conge = Conge(
        employe_id=employe.id,
        type_conge=TypeConge.ANNUEL,
        date_debut=datetime.now().date() + timedelta(days=15),
        date_fin=datetime.now().date() + timedelta(days=30),
        nb_jours=15,
        motif="Congés annuels",
        statut=StatutConge.EN_ATTENTE
    )
    db.add(conge)
    db.commit()

    # Rejeter la demande
    motif_rejet = "Période chargée"
    updated_conge = await service.reject_leave_request(
        str(conge.id),
        str(test_user.id),
        motif_rejet
    )
    assert updated_conge.statut == StatutConge.REJETE
    assert updated_conge.rejete_par_id == test_user.id
    assert updated_conge.motif_rejet == motif_rejet

@pytest.mark.asyncio
async def test_get_conges_employe(db: Session, create_test_employe):
    """Test de récupération des congés d'un employé"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP011",
        nom="Bernard",
        prenom="Alice",
        departement=DepartementType.ADMINISTRATION
    )

    # Créer plusieurs congés
    annee_courante = datetime.now().year
    conges = [
        Conge(
            employe_id=employe.id,
            type_conge=TypeConge.ANNUEL,
            date_debut=datetime(annee_courante, 1, 15).date(),
            date_fin=datetime(annee_courante, 1, 30).date(),
            nb_jours=15,
            motif="Congés hiver",
            statut=StatutConge.APPROUVE
        ),
        Conge(
            employe_id=employe.id,
            type_conge=TypeConge.ANNUEL,
            date_debut=datetime(annee_courante, 7, 1).date(),
            date_fin=datetime(annee_courante, 7, 31).date(),
            nb_jours=30,
            motif="Congés été",
            statut=StatutConge.EN_ATTENTE
        )
    ]
    db.add_all(conges)
    db.commit()

    # Récupérer les congés
    conges_employe = await service.get_conges_employe(str(employe.id), annee_courante)
    assert len(conges_employe) == 2

    # Vérifier le filtrage par année
    conges_autre_annee = await service.get_conges_employe(str(employe.id), annee_courante - 1)
    assert len(conges_autre_annee) == 0

@pytest.mark.asyncio
async def test_get_presences_employe(db: Session, create_test_employe):
    """Test de récupération des présences d'un employé"""
    service = HRService(db)
    
    # Créer un employé
    employe = await create_test_employe(
        matricule="EMP012",
        nom="Thomas",
        prenom="Julie"
    )

    # Créer des présences sur une semaine
    date_debut = datetime.now().date() - timedelta(days=7)
    presences = []
    for i in range(5):  # 5 jours de travail
        presence = Presence(
            employe_id=employe.id,
            date=date_debut + timedelta(days=i),
            type_presence=TypePresence.PRESENT,
            heure_arrivee=(datetime.now().replace(hour=8, minute=0) + timedelta(days=i)),
            heure_depart=(datetime.now().replace(hour=17, minute=0) + timedelta(days=i)),
            heures_travaillees=9
        )
        presences.append(presence)
    db.add_all(presences)
    db.commit()

    # Récupérer les présences
    presences_employe = await service.get_presences_employe(
        str(employe.id),
        date_debut,
        date_debut + timedelta(days=7)
    )
    assert len(presences_employe) == 5

@pytest.mark.asyncio
async def test_get_department_stats(db: Session, create_test_employe):
    """Test de récupération des statistiques d'un département"""
    service = HRService(db)
    
    # Créer plusieurs employés dans le même département
    for i in range(5):
        await create_test_employe(
            matricule=f"EMP02{i}",
            nom=f"Nom{i}",
            prenom=f"Prenom{i}",
            departement=DepartementType.PRODUCTION,
            statut=StatutEmploye.ACTIF if i < 4 else StatutEmploye.CONGE
        )

    # Récupérer les statistiques
    stats = await service.get_department_stats(DepartementType.PRODUCTION)
    assert stats["effectif_total"] == 5
    assert stats["actifs"] == 4
    assert stats["en_conge"] == 1
    assert stats["masse_salariale"] == 1000000  # 5 * 200000

class TestHRAgricoleService:
    """Tests d'intégration pour les fonctionnalités RH agricoles"""

    async def test_gestion_competences_agricoles(self, db_session, create_test_employe):
        """Test de gestion des compétences agricoles"""
        service = HRService(db_session)
        
        # Créer un employé
        employe = await create_test_employe(
            matricule="EMP013",
            nom="Dupont",
            prenom="Jean",
            departement=DepartementType.PRODUCTION
        )

        # Ajouter une compétence agricole
        competence_data = {
            "employe_id": str(employe.id),
            "specialite": SpecialiteAgricole.CULTURE,
            "niveau": NiveauCompetence.INTERMEDIAIRE,
            "cultures": ["Blé", "Maïs"],
            "equipements": ["Tracteur", "Moissonneuse"],
            "date_acquisition": datetime.now().date()
        }

        competence = await service.add_competence_agricole(competence_data)
        assert competence.specialite == SpecialiteAgricole.CULTURE
        assert len(competence.cultures) == 2
        assert len(competence.equipements) == 2

    async def test_gestion_certifications_agricoles(self, db_session, create_test_employe):
        """Test de gestion des certifications agricoles"""
        service = HRService(db_session)
        
        # Créer un employé avec une compétence
        employe = await create_test_employe(
            matricule="EMP014",
            nom="Martin",
            prenom="Luc"
        )

        competence = CompetenceAgricole(
            employe_id=employe.id,
            specialite=SpecialiteAgricole.CULTURE,
            niveau=NiveauCompetence.AVANCE,
            date_acquisition=datetime.now().date()
        )
        db_session.add(competence)
        db_session.commit()

        # Ajouter une certification
        certification_data = {
            "competence_id": str(competence.id),
            "type_certification": TypeCertification.PHYTOSANITAIRE,
            "organisme": "CertifAgri",
            "date_obtention": datetime.now().date(),
            "date_expiration": datetime.now().date() + timedelta(days=365)
        }

        certification = await service.add_certification_agricole(certification_data)
        assert certification.type_certification == TypeCertification.PHYTOSANITAIRE
        assert certification.organisme == "CertifAgri"

    async def test_gestion_affectations_parcelles(self, db_session, create_test_employe):
        """Test de gestion des affectations aux parcelles"""
        service = HRService(db_session)
        
        # Créer un employé
        employe = await create_test_employe(
            matricule="EMP015",
            nom="Dubois",
            prenom="Marc"
        )

        # Créer une parcelle (mock)
        parcelle = Mock(id=uuid.uuid4())
        db_session.query().get.return_value = parcelle

        # Créer une affectation
        affectation_data = {
            "employe_id": str(employe.id),
            "parcelle_id": str(parcelle.id),
            "date_debut": datetime.now().date(),
            "role": "Responsable culture",
            "responsabilites": ["Semis", "Irrigation"],
            "objectifs": ["Rendement +10%"],
            "equipements_requis": ["Tracteur"]
        }

        affectation = await service.create_affectation_parcelle(affectation_data)
        assert affectation.role == "Responsable culture"
        assert len(affectation.responsabilites) == 2
        assert len(affectation.objectifs) == 1

    async def test_suivi_conditions_travail(self, db_session, create_test_employe):
        """Test du suivi des conditions de travail agricoles"""
        service = HRService(db_session)
        
        # Créer un employé
        employe = await create_test_employe(
            matricule="EMP016",
            nom="Petit",
            prenom="Paul"
        )

        # Enregistrer les conditions de travail
        conditions_data = {
            "employe_id": str(employe.id),
            "date": datetime.now().date(),
            "temperature": 25.5,
            "humidite": 65,
            "precipitation": False,
            "vent": 15.0,
            "exposition_soleil": 240,
            "charge_physique": 7,
            "equipements_protection": ["Chapeau", "Gants"]
        }

        conditions = await service.track_conditions_travail(conditions_data)
        assert conditions.temperature == 25.5
        assert conditions.humidite == 65
        assert len(conditions.equipements_protection) == 2

    async def test_gestion_formations_agricoles(self, db_session, create_test_employe):
        """Test de gestion des formations agricoles"""
        service = HRService(db_session)
        
        # Créer une formation de base (mock)
        formation_base = Mock(id=uuid.uuid4())
        db_session.query().get.return_value = formation_base

        # Ajouter les détails agricoles
        formation_data = {
            "formation_id": str(formation_base.id),
            "specialite": SpecialiteAgricole.CULTURE,
            "cultures_concernees": ["Blé", "Orge"],
            "equipements_concernes": ["Tracteur"],
            "evaluation_terrain": True,
            "resultats_evaluation": {"technique": 8, "securite": 9}
        }

        formation = await service.add_formation_agricole_details(formation_data)
        assert formation.specialite == SpecialiteAgricole.CULTURE
        assert len(formation.cultures_concernees) == 2
        assert formation.evaluation_terrain is True

    async def test_gestion_evaluations_agricoles(self, db_session, create_test_employe):
        """Test de gestion des évaluations agricoles"""
        service = HRService(db_session)
        
        # Créer une évaluation de base (mock)
        evaluation_base = Mock(id=uuid.uuid4())
        db_session.query().get.return_value = evaluation_base

        # Ajouter les détails agricoles
        evaluation_data = {
            "evaluation_id": str(evaluation_base.id),
            "performances_cultures": {"ble": 8, "mais": 7},
            "maitrise_equipements": {"tracteur": 9},
            "respect_securite": {"epi": 10, "procedures": 9},
            "adaptabilite_meteo": {"pluie": 8, "chaleur": 7},
            "qualite_travail": {"precision": 8, "rapidite": 7}
        }

        evaluation = await service.add_evaluation_agricole_details(evaluation_data)
        assert len(evaluation.performances_cultures) == 2
        assert len(evaluation.maitrise_equipements) == 1
        assert len(evaluation.respect_securite) == 2
