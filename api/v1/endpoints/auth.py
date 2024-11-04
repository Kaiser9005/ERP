from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import timedelta
from db.database import get_db
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)
from models.auth import Utilisateur, Role, Permission
from schemas.auth import (
    UserCreate,
    UserResponse,
    UserUpdate,
    Token,
    RoleCreate,
    RoleResponse,
    PermissionCreate,
    PermissionResponse
)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dépendance pour obtenir l'utilisateur courant
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Utilisateur:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Identifiants invalides",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    username = verify_token(token)
    if username is None:
        raise credentials_exception
        
    user = db.query(Utilisateur).filter(
        Utilisateur.username == username,
        Utilisateur.is_active == True
    ).first()
    
    if user is None:
        raise credentials_exception
    return user

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authentification et génération du token"""
    user = db.query(Utilisateur).filter(
        Utilisateur.username == form_data.username
    ).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.username)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Création d'un nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    if db.query(Utilisateur).filter(Utilisateur.email == user.email).first():
        raise HTTPException(
            status_code=400,
            detail="Email déjà utilisé"
        )
    
    # Vérifier si le username existe déjà
    if db.query(Utilisateur).filter(Utilisateur.username == user.username).first():
        raise HTTPException(
            status_code=400,
            detail="Username déjà utilisé"
        )
    
    # Créer le nouvel utilisateur
    db_user = Utilisateur(
        **user.dict(exclude={'password'}),
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users/me", response_model=UserResponse)
async def read_users_me(current_user: Utilisateur = Depends(get_current_user)):
    """Récupère les informations de l'utilisateur connecté"""
    return current_user

# Endpoints pour la gestion des rôles
@router.post("/roles", response_model=RoleResponse)
async def create_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Création d'un nouveau rôle"""
    db_role = Role(**role.dict(exclude={'permissions'}))
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/roles", response_model=List[RoleResponse])
async def get_roles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Liste tous les rôles"""
    return db.query(Role).offset(skip).limit(limit).all()

# Endpoints pour la gestion des permissions
@router.post("/permissions", response_model=PermissionResponse)
async def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: Utilisateur = Depends(get_current_user)
):
    """Création d'une nouvelle permission"""
    db_permission = Permission(**permission.dict())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission