from pydantic import BaseModel, EmailStr, UUID4
from typing import Optional, List, Dict
from datetime import datetime
from models.auth import TypeRole

class PermissionBase(BaseModel):
    code: str
    description: Optional[str]
    module: str
    actions: Dict[str, bool]

class PermissionCreate(PermissionBase):
    pass

class PermissionResponse(PermissionBase):
    id: UUID4

    class Config:
        orm_mode = True

class RoleBase(BaseModel):
    nom: str
    description: Optional[str]
    type: TypeRole
    is_active: bool = True

class RoleCreate(RoleBase):
    permissions: List[str]  # Liste des codes de permission

class RoleUpdate(RoleBase):
    permissions: Optional[List[str]]

class RoleResponse(RoleBase):
    id: UUID4
    permissions: List[PermissionResponse]

    class Config:
        orm_mode = True

class FirstAdminCreate(BaseModel):
    """Schéma pour la création du premier administrateur"""
    username: str
    email: EmailStr
    password: str
    nom: str
    prenom: str

    class Config:
        json_schema_extra = {
            "example": {
                "username": "admin",
                "email": "admin@example.com",
                "password": "StrongP@ssw0rd",
                "nom": "Admin",
                "prenom": "Super"
            }
        }

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    nom: str
    prenom: str
    role_id: UUID4

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    nom: Optional[str]
    prenom: Optional[str]
    role_id: Optional[UUID4]
    is_active: Optional[bool]
    preferences: Optional[Dict]

class UserResponse(BaseModel):
    id: UUID4
    email: EmailStr
    username: str
    nom: str
    prenom: str
    role: RoleResponse
    is_active: bool
    is_superuser: bool
    is_staff: bool
    preferences: Optional[Dict]
    derniere_connexion: Optional[str]

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None
    permissions: List[str] = []