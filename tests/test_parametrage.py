import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.parametrage import Parametre, ConfigurationModule, ModuleSysteme
from services.parametrage_service import ParametrageService

def test_get_parametres(client: TestClient, db: Session, test_user: dict):
    """Test de récupération des paramètres"""
    # Créer des paramètres de test
    param = Parametre(
        code="TEST_PARAM",
        libelle="Paramètre de test",
        type_parametre="GENERAL",
        valeur={"test": "value"},
        modifiable=True
    )
    db.add(param)
    db.commit()

    response = client.get("/api/v1/parametrage/parametres")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["code"] == "TEST_PARAM"

def test_create_parametre(client: TestClient, db: Session, test_user: dict):
    """Test de création d'un paramètre"""
    param_data = {
        "code": "NEW_PARAM",
        "libelle": "Nouveau paramètre",
        "type_parametre": "GENERAL",
        "valeur": {"test": "value"},
        "modifiable": True
    }

    response = client.post("/api/v1/parametrage/parametres", json=param_data)
    assert response.status_code == 200
    data = response.json()
    assert data["code"] == "NEW_PARAM"

def test_update_parametre(client: TestClient, db: Session, test_user: dict):
    """Test de mise à jour d'un paramètre"""
    # Créer un paramètre
    param = Parametre(
        code="UPDATE_PARAM",
        libelle="Paramètre à modifier",
        type_parametre="GENERAL",
        valeur={"test": "old_value"},
        modifiable=True
    )
    db.add(param)
    db.commit()

    update_data = {
        "valeur": {"test": "new_value"}
    }

    response = client.put(f"/api/v1/parametrage/parametres/{param.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["valeur"]["test"] == "new_value"

def test_get_modules_configuration(client: TestClient, db: Session, test_user: dict):
    """Test de récupération de la configuration des modules"""
    # Créer une configuration de test
    config = ConfigurationModule(
        module=ModuleSysteme.PRODUCTION,
        actif=True,
        configuration={"feature1": True},
        ordre_affichage=1
    )
    db.add(config)
    db.commit()

    response = client.get("/api/v1/parametrage/modules/configuration")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert data[0]["module"] == "PRODUCTION"

def test_update_module_configuration(client: TestClient, db: Session, test_user: dict):
    """Test de mise à jour de la configuration d'un module"""
    # Créer une configuration
    config = ConfigurationModule(
        module=ModuleSysteme.PRODUCTION,
        actif=True,
        configuration={"feature1": True},
        ordre_affichage=1
    )
    db.add(config)
    db.commit()

    update_data = {
        "actif": False,
        "configuration": {"feature1": False}
    }

    response = client.put(
        f"/api/v1/parametrage/modules/{config.module}/configuration",
        json=update_data
    )
    assert response.status_code == 200
    data = response.json()
    assert data["actif"] == False
    assert data["configuration"]["feature1"] == False

def test_parametrage_service(db: Session):
    """Test du service de paramétrage"""
    service = ParametrageService(db)

    # Test d'initialisation des paramètres par défaut
    service.initialize_default_parameters()
    params = service.get_parametres()
    assert len(params) > 0

    # Test de création de paramètre
    param = service.create_parametre({
        "code": "TEST_SERVICE",
        "libelle": "Test service",
        "type_parametre": "GENERAL",
        "valeur": {"test": "value"},
        "modifiable": True
    })
    assert param.code == "TEST_SERVICE"

    # Test de mise à jour de paramètre
    updated_param = service.update_parametre(
        param.id,
        {"valeur": {"test": "updated"}}
    )
    assert updated_param.valeur["test"] == "updated"