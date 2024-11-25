"""Tests d'intégration pour le service RH."""

import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.hr_service import HRService
from models.hr import Employe, Contrat, Conge, Presence
from models.hr import DepartementType, StatutEmploye, TypeContrat, TypeConge, StatutConge, TypePresence

@pytest.mark.asyncio
async def test_get_employee_stats(db: Session):
    """Test de récupération des statistiques RH"""
    service = HRService(db)
    
    # Créer des employés avec différents statuts
    for i in range(5):
        employe = Employe(
            matricule=f"EMP00{i+1}",
            nom=f"Nom{i+1}",
            prenom=f"Prenom{i+1}",
            date_naissance=datetime.now().date() - timedelta(days=365*30),
            sexe="M",
            departement=DepartementType.PRODUCTION,
            poste="Ouvrier",
            date_embauche=datetime.now().date() - timedelta(days=365),
            type_contrat=TypeContrat.CDI,
            salaire_base=150000,
            statut=StatutEmploye.ACTIF if i < 3 else StatutEmploye.CONGE
        )
        db.add(employe)
    db.commit()

    stats = await service.get_stats()
    assert stats["effectif_total"] == 5
    assert stats["actifs"] == 3
    assert stats["en_conge"] == 2

@pytest.mark.asyncio
async def test_create_employee(db: Session):
    """Test de création d'un employé"""
    service = HRService(db)
    
    employe_data = {
        "matricule": "EMP006",
        "nom": "Dupont",
        "prenom": "Jean",
        "date_naissance": datetime.now().date() - timedelta(days=365*25),
        "sexe": "M",
        "departement": DepartementType.PRODUCTION,
        "poste": "Technicien",
        "date_embauche": datetime.now().date(),
        "type_contrat": TypeContrat.CDI,
        "salaire_base": 200000
    }

    employe = await service.create_employee(employe_data)
    assert employe.matricule == "EMP006"
    assert employe.statut == StatutEmploye.ACTIF

@pytest.mark.asyncio
async def test_create_leave_request(db: Session, test_user: dict):
    """Test de création d'une demande de congé"""
    service = HRService(db)
    
    # Créer un employé
    employe = Employe(
        matricule="EMP007",
        nom="Martin",
        prenom="Marie",
        date_naissance=datetime.now().date() - timedelta(days=365*28),
        sexe="F",
        departement=DepartementType.ADMINISTRATION,
        poste="Comptable",
        date_embauche=datetime.now().date() - timedelta(days=180),
        type_contrat=TypeContrat.CDI,
        salaire_base=250000
    )
    db.add(employe)
    db.commit()

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
async def test_track_attendance(db: Session, test_user: dict):
    """Test du suivi des présences"""
    service = HRService(db)
    
    # Créer un employé
    employe = Employe(
        matricule="EMP008",
        nom="Dubois",
        prenom="Pierre",
        date_naissance=datetime.now().date() - timedelta(days=365*35),
        sexe="M",
        departement=DepartementType.PRODUCTION,
        poste="Chef d'équipe",
        date_embauche=datetime.now().date() - timedelta(days=365),
        type_contrat=TypeContrat.CDI,
        salaire_base=300000
    )
    db.add(employe)
    db.commit()

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
async def test_approve_leave_request(db: Session, test_user: dict):
    """Test d'approbation d'une demande de congé"""
    service = HRService(db)
    
    # Créer un employé
    employe = Employe(
        matricule="EMP009",
        nom="Petit",
        prenom="Sophie",
        date_naissance=datetime.now().date() - timedelta(days=365*30),
        sexe="F",
        departement=DepartementType.LOGISTIQUE,
        poste="Responsable logistique",
        date_embauche=datetime.now().date() - timedelta(days=730),
        type_contrat=TypeContrat.CDI,
        salaire_base=350000
    )
    db.add(employe)
    db.commit()

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
