from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from models.tache import Tache
from models.project import Project
from datetime import timedelta
from db.database import get_db
from core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token
)
from models.auth import Utilisateur, Role, Permission, TypeRole
from schemas.auth import (
    UserCreate,
    UserResponse,
    UserUpdate,
    Token,
    RoleCreate,
    RoleResponse,
    PermissionCreate,
    PermissionResponse,
    FirstAdminCreate
)
from fastapi.responses import Response
import logging
from sqlalchemy import text

# Configuration du logging
logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

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
    
    try:
        payload = verify_token(token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception
        
    user = db.query(Utilisateur).filter(
        Utilisateur.username == username,
        Utilisateur.is_active == True
    ).first()
    
    if user is None:
        raise credentials_exception
    return user

@router.get("/")
async def read_auth():
    """Endpoint de base pour l'authentification"""
    return {"message": "Authentification service"}

@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Authentification et génération du token"""
    logger.info(f"Tentative de connexion pour l'utilisateur: {form_data.username}")
    
    user = db.query(Utilisateur).filter(
        Utilisateur.username == form_data.username
    ).first()
    
    logger.info(f"Utilisateur trouvé: {user is not None}")
    if user:
        logger.info(f"Mot de passe haché de l'utilisateur: {user.hashed_password}")

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.error("Échec de l'authentification: nom d'utilisateur ou mot de passe incorrect")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=user.username)
    logger.info("Token d'accès créé avec succès")
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/first-admin", response_model=UserResponse)
async def create_first_admin(
    user: FirstAdminCreate,
    db: Session = Depends(get_db)
):
    """Création du premier utilisateur administrateur (sans authentification)"""
    logger.info("create_first_admin: Début de la création du premier administrateur")
    
    try:
        # Vérifier s'il existe déjà des utilisateurs
        logger.info("create_first_admin: Vérification de l'existence d'utilisateurs...")
        if db.query(Utilisateur).count() > 0:
            logger.error("create_first_admin: Des utilisateurs existent déjà.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Un administrateur existe déjà."
            )
        
        # Vérifier si l'email existe déjà
        logger.info("create_first_admin: Vérification de l'email...")
        if db.query(Utilisateur).filter(Utilisateur.email == user.email).first():
            logger.error("create_first_admin: Email déjà utilisé.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email déjà utilisé"
            )
        
        # Vérifier si le username existe déjà
        logger.info("create_first_admin: Vérification du nom d'utilisateur...")
        if db.query(Utilisateur).filter(Utilisateur.username == user.username).first():
            logger.error("create_first_admin: Nom d'utilisateur déjà utilisé.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username déjà utilisé"
            )

        # Créer les permissions de base pour l'administrateur
        logger.info("create_first_admin: Création des permissions de base...")
        admin_permissions = [
            Permission(
                code="ADMIN_ALL",
                description="Accès complet à toutes les fonctionnalités",
                module="system",
                actions={"create": True, "read": True, "update": True, "delete": True}
            ),
            Permission(
                code="USER_MANAGE",
                description="Gestion des utilisateurs",
                module="auth",
                actions={"create": True, "read": True, "update": True, "delete": True}
            )
        ]
        for permission in admin_permissions:
            db.add(permission)
        db.flush()  # Pour obtenir les IDs des permissions

        # Créer le rôle ADMIN s'il n'existe pas
        logger.info("create_first_admin: Création/récupération du rôle ADMIN...")
        admin_role = db.query(Role).filter(Role.type == TypeRole.ADMIN).first()
        if not admin_role:
            admin_role = Role(
                nom="Administrateur",
                description="Rôle administrateur système",
                type=TypeRole.ADMIN,
                is_active=True,
                permissions=admin_permissions
            )
            db.add(admin_role)
            db.flush()  # Pour obtenir l'ID sans commit
            logger.info("create_first_admin: Rôle ADMIN créé.")
        
        # Créer le nouvel utilisateur avec le rôle ADMIN
        logger.info("create_first_admin: Création de l'utilisateur...")
        hashed_password = get_password_hash(user.password)
        logger.info(f"create_first_admin: Mot de passe haché: {hashed_password}")
        
        db_user = Utilisateur(
            email=user.email,
            username=user.username,
            hashed_password=hashed_password,
            nom=user.nom,
            prenom=user.prenom,
            role_id=admin_role.id,
            is_superuser=True,
            is_active=True,
            is_staff=True
        )
        
        # Ajouter et commiter
        logger.info("create_first_admin: Sauvegarde des changements...")
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info("create_first_admin: Premier administrateur créé avec succès.")
        return db_user
        
    except HTTPException as e:
        logger.error(f"create_first_admin: Erreur lors de la création : {str(e)}")
        db.rollback()
        raise e
    except Exception as e:
        logger.error(f"create_first_admin: Erreur lors de la création : {str(e)}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erreur lors de la création de l'administrateur : {str(e)}"
        )

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
        **user.model_dump(exclude={'password'}),
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
    db_role = Role(**role.model_dump(exclude={'permissions'}))
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
    db_permission = Permission(**permission.model_dump())
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission
