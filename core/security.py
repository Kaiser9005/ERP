from datetime import datetime, timedelta
from typing import Optional, Union, Any, List, Callable
from enum import Enum
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.config import SECURITY_CONFIG
from sqlalchemy.orm import Session
from db.database import get_db
from models.auth import Utilisateur
import logging
from functools import wraps

# Configuration du logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

class Permission(str, Enum):
    """Permissions du système"""
    ADMIN = "admin"
    STAFF = "staff"
    USER = "user"
    FINANCE = "finance"
    COMPTABILITE = "comptabilite"
    PRODUCTION = "production"
    INVENTAIRE = "inventaire"
    RH = "rh"
    LECTURE = "lecture"
    ECRITURE = "ecriture"

def require_permissions(permissions: List[Permission]) -> Callable:
    """Décorateur pour vérifier les permissions requises"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Récupération de l'utilisateur courant
            user = kwargs.get('current_user')
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Non authentifié"
                )

            # Vérification des permissions
            user_permissions = set(user.permissions or [])
            required_permissions = set(permissions)

            # Les admins ont toutes les permissions
            if Permission.ADMIN in user_permissions:
                return await func(*args, **kwargs)

            # Vérification des permissions spécifiques
            if not required_permissions.issubset(user_permissions):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Permissions insuffisantes"
                )

            return await func(*args, **kwargs)
        return wrapper
    return decorator

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe en clair correspond au hash"""
    logger.debug(f"Tentative de vérification du mot de passe")
    logger.debug(f"Mot de passe en clair: {plain_password}")
    logger.debug(f"Mot de passe haché: {hashed_password}")
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.debug(f"Résultat de la vérification: {result}")
        return result
    except Exception as e:
        logger.error(f"Erreur lors de la vérification du mot de passe: {str(e)}")
        logger.error(f"Type d'erreur: {type(e)}")
        logger.error(f"Arguments de l'erreur: {e.args}")
        return False

def get_password_hash(password: str) -> str:
    """Génère le hash d'un mot de passe"""
    logger.debug(f"Génération du hash pour le mot de passe")
    hashed = pwd_context.hash(password)
    logger.debug(f"Hash généré: {hashed}")
    return hashed

def verify_token(token: str) -> dict:
    """Vérifie et décode un token JWT"""
    try:
        payload = jwt.decode(
            token,
            SECURITY_CONFIG["secret_key"],
            algorithms=[SECURITY_CONFIG["algorithm"]]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalide",
            headers={"WWW-Authenticate": "Bearer"},
        )

def create_access_token(
    subject: Union[str, Any],
    expires_delta: Optional[timedelta] = None
) -> str:
    """Crée un JWT token"""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=SECURITY_CONFIG["access_token_expire_minutes"]
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        SECURITY_CONFIG["secret_key"],
        algorithm=SECURITY_CONFIG["algorithm"]
    )
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Utilisateur:
    """Récupère l'utilisateur courant à partir du token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token,
            SECURITY_CONFIG["secret_key"],
            algorithms=[SECURITY_CONFIG["algorithm"]]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        user = db.query(Utilisateur).filter(Utilisateur.id == user_id).first()
        if user is None:
            raise credentials_exception
            
        return user
    except JWTError:
        raise credentials_exception
