from sqlalchemy.orm import Session
from typing import List, Dict, Any
from models.parametrage import Parametre, ConfigurationModule, ModuleSysteme
from schemas.parametrage import ParametreCreate, ParametreUpdate

class ParametrageService:
    def __init__(self, db: Session):
        self.db = db

    def get_parametres(self, module: ModuleSysteme = None, categorie: str = None) -> List[Parametre]:
        """Récupère les paramètres avec filtres optionnels"""
        query = self.db.query(Parametre)
        if module:
            query = query.filter(Parametre.module == module)
        if categorie:
            query = query.filter(Parametre.categorie == categorie)
        return query.order_by(Parametre.ordre).all()

    def create_parametre(self, parametre: ParametreCreate) -> Parametre:
        """Crée un nouveau paramètre"""
        db_parametre = Parametre(**parametre.dict())
        self.db.add(db_parametre)
        self.db.commit()
        self.db.refresh(db_parametre)
        return db_parametre

    def update_parametre(self, parametre_id: str, parametre: ParametreUpdate) -> Parametre:
        """Met à jour un paramètre existant"""
        db_parametre = self.db.query(Parametre).filter(Parametre.id == parametre_id).first()
        if not db_parametre:
            raise ValueError("Paramètre non trouvé")
        
        if not db_parametre.modifiable:
            raise ValueError("Ce paramètre n'est pas modifiable")
        
        for key, value in parametre.dict(exclude_unset=True).items():
            setattr(db_parametre, key, value)
        
        self.db.commit()
        self.db.refresh(db_parametre)
        return db_parametre

    def get_module_configuration(self, module: ModuleSysteme) -> ConfigurationModule:
        """Récupère la configuration d'un module"""
        return self.db.query(ConfigurationModule).filter(
            ConfigurationModule.module == module
        ).first()

    def update_module_configuration(
        self,
        module: ModuleSysteme,
        configuration: Dict[str, Any]
    ) -> ConfigurationModule:
        """Met à jour la configuration d'un module"""
        db_config = self.get_module_configuration(module)
        if not db_config:
            raise ValueError("Configuration du module non trouvée")
        
        for key, value in configuration.items():
            setattr(db_config, key, value)
        
        self.db.commit()
        self.db.refresh(db_config)
        return db_config

    def initialize_default_parameters(self):
        """Initialise les paramètres par défaut du système"""
        default_params = [
            {
                "code": "DEVISE_DEFAUT",
                "libelle": "Devise par défaut",
                "type_parametre": "GENERAL",
                "valeur": {"code": "XAF", "symbole": "FCFA"},
                "modifiable": True,
                "categorie": "FINANCE"
            },
            {
                "code": "LANGUE_DEFAUT",
                "libelle": "Langue par défaut",
                "type_parametre": "GENERAL",
                "valeur": "fr",
                "modifiable": True,
                "categorie": "SYSTEME"
            }
            # Ajoutez d'autres paramètres par défaut ici
        ]

        for param in default_params:
            if not self.db.query(Parametre).filter(Parametre.code == param["code"]).first():
                self.db.add(Parametre(**param))
        
        self.db.commit()