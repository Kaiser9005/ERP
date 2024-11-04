from datetime import datetime, timedelta
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from core.config import SECURITY_CONFIG

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si le mot de passe en clair correspond au hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Génère le hash d'un mot de passe"""
    return pwd_context.hash(password)

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

def verify_token(token: str) -> Optional[str]:
    """Vérifie la validité d'un token"""
    try:
        payload = jwt.decode(
            token,
            SECURITY_CONFIG["secret_key"],
            algorithms=[SECURITY_CONFIG["algorithm"]]
        )
        return payload.get("sub")
    except JWTError:
        return None