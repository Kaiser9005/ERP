"""Configuration de l'environnement Alembic pour les migrations de base de données."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Ajout du chemin racine au PYTHONPATH pour l'import des modèles
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.base import Base
from core.config import settings

# Objet de configuration Alembic
config = context.config

# Configuration du logging via le fichier alembic.ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# MetaData pour la génération des migrations
target_metadata = Base.metadata

def get_url():
    """Récupère l'URL de connexion à la base de données depuis les paramètres."""
    return settings.SQLALCHEMY_DATABASE_URI

def run_migrations_offline():
    """Exécute les migrations en mode 'offline'.
    
    Ce mode permet de générer les requêtes SQL sans connexion à la base de données.
    Utile pour la génération de scripts SQL à exécuter manuellement.
    """
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Exécute les migrations en mode 'online'.
    
    Ce mode établit une connexion à la base de données et exécute les migrations
    directement. C'est le mode d'exécution standard.
    """
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()

# Choix du mode d'exécution
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
