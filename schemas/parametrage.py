from pydantic import BaseModel, UUID4
from typing import Optional, Dict, Any, List
from models.parametrage import TypeParametre, ModuleSysteme

class ParametreBase(BaseModel):
    code: str
    libelle: str
    description: Optional[str]
    type_parametre: TypeParametre
    module: Optional[ModuleSysteme]
    valeur: Dict[str, Any]
    modifiable: bool = True
    visible: bool = True
    ordre: int = 0
    categorie: Optional[str]

class ParametreCreate(ParametreBase):
    pass

class ParametreUpdate(ParametreBase):
    code: Optional[str]
    libelle: Optional[str]
    valeur: Optional[Dict[str, Any]]

class ParametreResponse(ParametreBase):
    id: UUID4

    class Config:
        orm_mode = True

class ConfigurationModuleBase(BaseModel):
    module: ModuleSysteme
    actif: bool = True
    configuration: Optional[Dict[str, Any]]
    ordre_affichage: int = 0
    icone: Optional[str]
    couleur: Optional[str]
    roles_autorises: List[str] = []

class ConfigurationModuleCreate(ConfigurationModuleBase):
    pass

class ConfigurationModuleUpdate(ConfigurationModuleBase):
    actif: Optional[bool]
    configuration: Optional[Dict[str, Any]]
    ordre_affichage: Optional[int]

class ConfigurationModuleResponse(ConfigurationModuleBase):
    id: UUID4

    class Config:
        orm_mode = True