"""Configuration de l'environnement pour l'ERP FOFAL."""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FOFAL ERP"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 jours
    ALGORITHM: str = "HS256"
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "jjifdm")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "Jejuivfadama90")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "fofal_erp_2024")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    DATABASE_URL: Optional[str] = None
    
    # Redis
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6379"))
    REDIS_URL: Optional[str] = None
    
    # Weather API
    WEATHER_API_KEY: str = os.getenv("WEATHER_API_KEY", "L6JNFAY48CA9P9G5NCGBYCNDA")
    WEATHER_CACHE_TTL: int = int(os.getenv("WEATHER_CACHE_TTL", "1800"))  # 30 minutes
    WEATHER_API_TIMEOUT: float = float(os.getenv("WEATHER_API_TIMEOUT", "10.0"))
    WEATHER_API_MAX_RETRIES: int = int(os.getenv("WEATHER_API_MAX_RETRIES", "3"))
    WEATHER_API_URL: Optional[str] = None
    
    # Storage
    MAP_PROVIDER_KEY: Optional[str] = None
    STORAGE_PROVIDER: str = os.getenv("STORAGE_PROVIDER", "local")
    STORAGE_ACCESS_KEY: str = os.getenv("STORAGE_ACCESS_KEY", "")
    STORAGE_SECRET_KEY: str = os.getenv("STORAGE_SECRET_KEY", "")
    STORAGE_BUCKET: str = os.getenv("STORAGE_BUCKET", "fofal-storage")
    STORAGE_REGION: str = os.getenv("STORAGE_REGION", "eu-west-1")
    STORAGE_LOCAL_PATH: str = os.getenv("STORAGE_LOCAL_PATH", "./storage")
    
    # Currency
    DEFAULT_CURRENCY: Optional[str] = None
    EXCHANGE_RATE_API_KEY: Optional[str] = None
    
    # Email
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        case_sensitive = True
        env_file = ".env"
        extra = "allow"  # Permet les variables d'environnement supplémentaires

    def __init__(self, **data):
        super().__init__(**data)
        if self.DATABASE_URL is None:
            self.SQLALCHEMY_DATABASE_URI = (
                f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
                f"@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"
            )
        else:
            self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL
        self.REDIS_URL = f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"
        self.WEATHER_API_URL = "https://api.weather.com"

@lru_cache()
def get_settings() -> Settings:
    """Retourne une instance singleton des paramètres"""
    return Settings()

settings = get_settings()

# Export des configurations pour l'application
APP_CONFIG = {
    "title": settings.PROJECT_NAME,
    "description": "API pour la gestion de l'exploitation agricole FOFAL",
    "version": "1.0.0"
}

SECURITY_CONFIG = {
    "secret_key": settings.SECRET_KEY,
    "access_token_expire_minutes": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    "algorithm": settings.ALGORITHM
}

DATABASE_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": settings.SQLALCHEMY_DATABASE_URI,
    "POSTGRES_SERVER": settings.POSTGRES_SERVER,
    "POSTGRES_USER": settings.POSTGRES_USER,
    "POSTGRES_PASSWORD": settings.POSTGRES_PASSWORD,
    "POSTGRES_DB": settings.POSTGRES_DB
}

REDIS_CONFIG = {
    "HOST": settings.REDIS_HOST,
    "PORT": settings.REDIS_PORT,
    "URL": settings.REDIS_URL
}

STORAGE_CONFIG = {
    "PROVIDER": settings.STORAGE_PROVIDER,
    "ACCESS_KEY": settings.STORAGE_ACCESS_KEY,
    "SECRET_KEY": settings.STORAGE_SECRET_KEY,
    "BUCKET": settings.STORAGE_BUCKET,
    "REGION": settings.STORAGE_REGION,
    "LOCAL_PATH": settings.STORAGE_LOCAL_PATH
}

WEATHER_CONFIG = {
    "API_KEY": settings.WEATHER_API_KEY,
    "CACHE_TTL": settings.WEATHER_CACHE_TTL,
    "API_TIMEOUT": settings.WEATHER_API_TIMEOUT,
    "MAX_RETRIES": settings.WEATHER_API_MAX_RETRIES,
    "API_URL": settings.WEATHER_API_URL
}
