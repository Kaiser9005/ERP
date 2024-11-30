from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
from uuid import UUID
from models.parametrage import TypeModule, TypeParametre

class ModuleSystemeBase(BaseModel):
    """Schéma de base pour un module système"""
    code: str
    nom: str
    description: Optional[str] = None
    type_module: TypeModule
    version: Optional[str] = None
    actif: bool = True
    configuration: Optional[Dict[str, Any]] = None
    dependances: Optional[List[str]] = None

class ModuleSystemeCreate(ModuleSystemeBase):
    """Schéma pour la création d'un module système"""
    pass

class ModuleSystemeUpdate(ModuleSystemeBase):
    """Schéma pour la mise à jour d'un module système"""
    code: Optional[str] = None
    nom: Optional[str] = None
    type_module: Optional[TypeModule] = None

class ModuleSystemeResponse(ModuleSystemeBase):
    """Schéma pour la réponse d'un module système"""
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class ParametreSystemeBase(BaseModel):
    """Schéma de base pour un paramètre système"""
    code: str
    nom: str
    description: Optional[str] = None
    type_parametre: TypeParametre
    valeur: Dict[str, Any]
    actif: bool = True
    metadata_config: Optional[Dict[str, Any]] = None

class ParametreSystemeCreate(ParametreSystemeBase):
    """Schéma pour la création d'un paramètre système"""
    module_id: UUID

class ParametreSystemeUpdate(ParametreSystemeBase):
    """Schéma pour la mise à jour d'un paramètre système"""
    code: Optional[str] = None
    nom: Optional[str] = None
    type_parametre: Optional[TypeParametre] = None
    valeur: Optional[Dict[str, Any]] = None
    module_id: Optional[UUID] = None

class ParametreSystemeResponse(ParametreSystemeBase):
    """Schéma pour la réponse d'un paramètre système"""
    id: UUID
    module_id: UUID
    model_config = ConfigDict(from_attributes=True)
