import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from fastapi import HTTPException

from models.tache import Tache, RessourceTache, DependanceTache
from models.resource import Resource, ResourceStatus
from services.tache_service import TacheService
from services.weather_service import WeatherService
from schemas.tache import TacheCreate, TacheFormData

@pytest.fixture
def test_db(test_session: Session):
    """Fixture pour la base de données de test"""
    # Création des ressources de test
    resource = Resource(
        name="Palmiers",
        type="MATERIEL",
        status=ResourceStatus.DISPONIBLE,
        quantity_total=100,
        quantity_available=100,
        quantity_reserved=0,
        unit="unités"
    )
    test_session.add(resource)
    test_session.commit()

    # Création d'une tâche de test
    tache = Tache(
        titre="Tâche test",
        description="Description test",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        dependant_meteo=True,
        min_temperature=20,
        max_temperature=35
    )
    test_session.add(tache)
    test_session.commit()

    yield test_session

    # Nettoyage
    test_session.query(RessourceTache).delete()
    test_session.query(DependanceTache).delete()
    test_session.query(Tache).delete()
    test_session.query(Resource).delete()
    test_session.commit()

@pytest.mark.asyncio
async def test_create_weather_dependent_task(test_db: Session, test_client: TestClient):
    """Test de création d'une tâche dépendante de la météo"""
    tache_service = TacheService(test_db)
    weather_service = WeatherService()

    # Création de la tâche
    tache_data = TacheFormData(
        titre="Plantation zone B",
        description="Planter 50 palmiers",
        projet_id=1,
        statut="A_FAIRE",
        priorite="HAUTE",
        categorie="PLANTATION",
        dependant_meteo=True,
        min_temperature=20,
        max_temperature=35,
        max_wind_speed=20,
        max_precipitation=5,
        ressources=[{
            "ressource_id": 1,
            "quantite_requise": 50,
            "quantite_utilisee": 0
        }]
    )

    tache = await tache_service.create_task(tache_data)
    assert tache.dependant_meteo == True
    assert tache.min_temperature == 20
    assert tache.max_temperature == 35

    # Vérification des conditions météo
    tache_meteo = await tache_service.get_task_with_weather(tache.id)
    assert "conditions_favorables" in tache_meteo
    assert "conditions_meteo" in tache_meteo
    assert "alertes_meteo" in tache_meteo

    # Vérification de la réservation des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 50
    assert resource.quantity_reserved == 50

@pytest.mark.asyncio
async def test_task_resource_management(test_db: Session):
    """Test de la gestion des ressources d'une tâche"""
    tache_service = TacheService(test_db)

    # Création d'une tâche avec ressources
    tache_data = TacheFormData(
        titre="Tâche avec ressources",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        ressources=[{
            "ressource_id": 1,
            "quantite_requise": 30,
            "quantite_utilisee": 0
        }]
    )

    tache = await tache_service.create_task(tache_data)
    
    # Vérification de la réservation initiale
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 70
    assert resource.quantity_reserved == 30

    # Mise à jour de l'utilisation des ressources
    await tache_service.update_task_resource(tache.id, 1, 20)
    ressource_tache = test_db.query(RessourceTache).first()
    assert ressource_tache.quantite_utilisee == 20

    # Marquage de la tâche comme terminée
    tache_update = TacheFormData(
        titre=tache.titre,
        projet_id=tache.projet_id,
        statut="TERMINEE",
        priorite=tache.priorite,
        categorie=tache.categorie,
        pourcentage_completion=100
    )
    tache_mise_a_jour = await tache_service.update_task(tache.id, tache_update)

    # Vérification de la libération des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE

@pytest.mark.asyncio
async def test_task_dependencies(test_db: Session):
    """Test de la gestion des dépendances entre tâches"""
    tache_service = TacheService(test_db)

    # Création de deux tâches avec une dépendance
    tache1_data = TacheFormData(
        titre="Tâche 1",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION"
    )
    tache1 = await tache_service.create_task(tache1_data)

    tache2_data = TacheFormData(
        titre="Tâche 2",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        dependances=[{
            "dependance_id": tache1.id,
            "type_dependance": "fin_vers_debut"
        }]
    )
    tache2 = await tache_service.create_task(tache2_data)

    # Vérification de la dépendance
    dependances = test_db.query(DependanceTache).all()
    assert len(dependances) == 1
    assert dependances[0].tache_id == tache2.id
    assert dependances[0].dependance_id == tache1.id

    # Vérification de la détection des dépendances circulaires
    tache3_data = TacheFormData(
        titre="Tâche 3",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        dependances=[{
            "dependance_id": tache2.id,
            "type_dependance": "fin_vers_debut"
        }]
    )
    tache3 = await tache_service.create_task(tache3_data)

    # Tentative de création d'une dépendance circulaire
    with pytest.raises(HTTPException) as exc_info:
        tache1_update = TacheFormData(
            titre=tache1.titre,
            projet_id=tache1.projet_id,
            statut=tache1.statut,
            priorite=tache1.priorite,
            categorie=tache1.categorie,
            dependances=[{
                "dependance_id": tache3.id,
                "type_dependance": "fin_vers_debut"
            }]
        )
        await tache_service.update_task(tache1.id, tache1_update)

    assert exc_info.value.status_code == 400
    assert "dépendance circulaire" in str(exc_info.value.detail).lower()

@pytest.mark.asyncio
async def test_weather_dependent_tasks_list(test_db: Session):
    """Test de la récupération des tâches dépendantes de la météo"""
    tache_service = TacheService(test_db)

    # Création de tâches avec et sans dépendance météo
    tache_meteo = TacheFormData(
        titre="Tâche météo",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        dependant_meteo=True,
        min_temperature=20,
        max_temperature=35
    )
    await tache_service.create_task(tache_meteo)

    tache_normale = TacheFormData(
        titre="Tâche normale",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="PLANTATION",
        dependant_meteo=False
    )
    await tache_service.create_task(tache_normale)

    # Récupération des tâches météo-dépendantes
    taches_meteo = await tache_service.get_weather_dependent_tasks()
    
    assert len(taches_meteo) == 1
    assert taches_meteo[0].titre == "Tâche météo"
    assert "conditions_favorables" in taches_meteo[0]
    assert "conditions_meteo" in taches_meteo[0]
    assert "alertes_meteo" in taches_meteo[0]

@pytest.mark.asyncio
async def test_task_completion_workflow(test_db: Session):
    """Test du workflow complet de réalisation d'une tâche"""
    tache_service = TacheService(test_db)

    # Création d'une tâche avec ressources
    tache_data = TacheFormData(
        titre="Tâche workflow",
        projet_id=1,
        statut="A_FAIRE",
        priorite="HAUTE",
        categorie="PLANTATION",
        dependant_meteo=True,
        min_temperature=20,
        max_temperature=35,
        ressources=[{
            "ressource_id": 1,
            "quantite_requise": 40,
            "quantite_utilisee": 0
        }]
    )

    # Création
    tache = await tache_service.create_task(tache_data)
    assert tache.statut == "A_FAIRE"
    assert tache.pourcentage_completion == 0

    # Mise en cours
    tache_update = TacheFormData(
        titre=tache.titre,
        projet_id=tache.projet_id,
        statut="EN_COURS",
        priorite=tache.priorite,
        categorie=tache.categorie,
        pourcentage_completion=30
    )
    tache = await tache_service.update_task(tache.id, tache_update)
    assert tache.statut == "EN_COURS"
    assert tache.pourcentage_completion == 30

    # Utilisation des ressources
    await tache_service.update_task_resource(tache.id, 1, 20)
    resource = test_db.query(Resource).first()
    assert resource.quantity_reserved == 40
    assert resource.quantity_available == 60

    # Vérification météo
    tache_meteo = await tache_service.get_task_with_weather(tache.id)
    assert "conditions_favorables" in tache_meteo

    # Finalisation
    tache_update = TacheFormData(
        titre=tache.titre,
        projet_id=tache.projet_id,
        statut="TERMINEE",
        priorite=tache.priorite,
        categorie=tache.categorie,
        pourcentage_completion=100
    )
    tache = await tache_service.update_task(tache.id, tache_update)
    assert tache.statut == "TERMINEE"
    assert tache.pourcentage_completion == 100
    assert tache.date_fin_reelle is not None

    # Vérification finale des ressources
    resource = test_db.query(Resource).first()
    assert resource.quantity_available == 100
    assert resource.quantity_reserved == 0
    assert resource.status == ResourceStatus.DISPONIBLE

@pytest.mark.asyncio
async def test_task_parcelle_integration(test_db: Session):
    """Test de l'intégration entre tâches et parcelles"""
    from services.production_service import ProductionService
    from models.production import Parcelle, CultureType, ParcelleStatus
    
    tache_service = TacheService(test_db)
    production_service = ProductionService(test_db)

    # Création d'une parcelle
    parcelle = Parcelle(
        code="P001",
        culture_type=CultureType.PALMIER,
        surface_hectares=10.5,
        date_plantation=datetime.now().date(),
        statut=ParcelleStatus.ACTIVE
    )
    test_db.add(parcelle)
    test_db.commit()

    # Création d'une tâche liée à la parcelle
    tache_data = TacheFormData(
        titre="Plantation palmiers",
        description="Planter 100 palmiers",
        projet_id=1,
        statut="A_FAIRE",
        priorite="HAUTE",
        categorie="PLANTATION",
        parcelle_id=parcelle.id
    )
    tache = await tache_service.create_task(tache_data)
    assert tache.parcelle_id == parcelle.id

    # Vérification dans les détails de la parcelle
    details = await production_service.get_parcelle_details(str(parcelle.id))
    assert len(details["taches"]) == 1
    assert details["taches"][0]["id"] == tache.id

@pytest.mark.asyncio
async def test_task_employe_integration(test_db: Session):
    """Test de l'intégration entre tâches et employés"""
    from services.hr_service import HRService
    from models.hr import Employe, DepartementType, StatutEmploye, TypeContrat
    
    tache_service = TacheService(test_db)
    hr_service = HRService(test_db)

    # Création d'un employé
    employe = Employe(
        matricule="EMP001",
        nom="Test",
        prenom="Employe",
        date_naissance=datetime.now().date() - timedelta(days=365*30),
        sexe="M",
        departement=DepartementType.PRODUCTION,
        poste="Ouvrier",
        date_embauche=datetime.now().date() - timedelta(days=180),
        type_contrat=TypeContrat.CDI,
        salaire_base=200000,
        statut=StatutEmploye.ACTIF
    )
    test_db.add(employe)
    test_db.commit()

    # Création d'une tâche assignée à l'employé
    tache_data = TacheFormData(
        titre="Tâche assignée",
        description="Description",
        projet_id=1,
        statut="A_FAIRE",
        priorite="MOYENNE",
        categorie="AUTRE",
        responsable_id=employe.id
    )
    tache = await tache_service.create_task(tache_data)
    assert tache.responsable_id == employe.id

    # Vérification de la disponibilité de l'employé
    disponibilite = await hr_service.get_employee_availability(
        str(employe.id),
        datetime.now().date(),
        (datetime.now() + timedelta(days=1)).date()
    )
    assert not disponibilite["disponible"]
    assert len(disponibilite["taches"]) == 1
    assert disponibilite["taches"][0]["id"] == tache.id