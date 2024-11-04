import pytest
from sqlalchemy.orm import Session
from services.parametrage_service import ParametrageService
from models.parametrage import Parametre, ConfigurationModule, ModuleSysteme, TypeParametre

def test_get_parametres(db: Session):
    """Test de récupération des paramètres"""
    service = ParametrageService(db)
    
    # Créer des paramètres de test
    param1 = Parametre(
        code="TEST_PARAM1",
        libelle="Paramètre test 1",
        type_parametre=TypeParametre.GENERAL,
        valeur={"test": "value1"},
        modifiable=True
    )
    param2 = Parametre(
        code="TEST_PARAM2",
        libelle="Paramètre test 2",
        type_parametre=TypeParametre.MODULE,
        module=ModuleSysteme.PRODUCTION,
        valeur={"test": "value2"},
        modifiable=True
    )
    db.add_all([param1, param2])
    db.commit()
    
    # Test sans filtre
    params = service.get_parametres()
    assert len(params) >= 2
    
    # Test avec filtre par module
    params = service.get_parametres(module=ModuleSysteme.PRODUCTION)
    assert len(params) == 1
    assert params[0].code == "TEST_PARAM2"

def test_create_parametre(db: Session):
    """Test de création d'un paramètre"""
    service = ParametrageService(db)
    
    param_data = {
        "code": "NEW_PARAM",
        "libelle": "Nouveau paramètre",
        "type_parametre": TypeParametre.GENERAL,
        "valeur": {"test": "value"},
        "modifiable": True
    }
    
    param = service.create_parametre(param_data)
    assert param.code == "NEW_PARAM"
    assert param.valeur["test"] == "value"

def test_update_parametre(db: Session):
    """Test de mise à jour d'un paramètre"""
    service = ParametrageService(db)
    
    # Créer un paramètre
    param = Parametre(
        code="UPDATE_PARAM",
        libelle="Paramètre à modifier",
        type_parametre=TypeParametre.GENERAL,
        valeur={"test": "old_value"},
        modifiable=True
    )
    db.add(param)
    db.commit()
    
    # Mettre à jour le paramètre
    updated_param = service.update_parametre(
        str(param.id),
        {"valeur": {"test": "new_value"}}
    )
    assert updated_param.valeur["test"] == "new_value"
    
    # Test mise à jour d'un paramètre non modifiable
    param.modifiable = False
    db.commit()
    
    with pytest.raises(ValueError, match="Ce paramètre n'est pas modifiable"):
        service.update_parametre(str(param.id), {"valeur": {"test": "another_value"}})

def test_module_configuration(db: Session):
    """Test de la configuration des modules"""
    service = ParametrageService(db)
    
    # Créer une configuration de module
    config = ConfigurationModule(
        module=ModuleSysteme.PRODUCTION,
        actif=True,
        configuration={"feature1": True},
        ordre_affichage=1
    )
    db.add(config)
    db.commit()
    
    # Récupérer la configuration
    module_config = service.get_module_configuration(ModuleSysteme.PRODUCTION)
    assert module_config is not None
    assert module_config.actif == True
    assert module_config.configuration["feature1"] == True
    
    # Mettre à jour la configuration
    updated_config = service.update_module_configuration(
        ModuleSysteme.PRODUCTION,
        {"actif": False, "configuration": {"feature1": False}}
    )
    assert updated_config.actif == False
    assert updated_config.configuration["feature1"] == False

def test_initialize_default_parameters(db: Session):
    """Test d'initialisation des paramètres par défaut"""
    service = ParametrageService(db)
    
    # Supprimer tous les paramètres existants
    db.query(Parametre).delete()
    db.commit()
    
    # Initialiser les paramètres par défaut
    service.initialize_default_parameters()
    
    # Vérifier que les paramètres ont été créés
    params = db.query(Parametre).all()
    assert len(params) > 0
    
    # Vérifier les paramètres spécifiques
    devise_param = db.query(Parametre).filter(
        Parametre.code == "DEVISE_DEFAUT"
    ).first()
    assert devise_param is not None
    assert devise_param.valeur["code"] == "XAF"
    
    langue_param = db.query(Parametre).filter(
        Parametre.code == "LANGUE_DEFAUT"
    ).first()
    assert langue_param is not None
    assert langue_param.valeur == "fr"