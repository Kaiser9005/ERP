"""Configuration de l'environnement Alembic pour les migrations de base de données."""

from logging.config import fileConfig
from sqlalchemy import engine_from_config, text
from sqlalchemy import pool
from alembic import context
import os
import sys
import logging

# Ajout du chemin racine au PYTHONPATH pour l'import des modèles
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.base import Base
from core.config import settings

# Configuration du logging
logger = logging.getLogger('alembic.env')

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
        version_table_schema="public",
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
        try:
            # Désactiver l'autocommit pour gérer manuellement les transactions
            connection.execution_options(isolation_level="SERIALIZABLE")
            
            # Définir le schéma de recherche
            connection.execute(text("SET search_path TO public"))
            
            # Configuration du contexte avec le schéma explicite
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                version_table_schema="public",
                transaction_per_migration=True,
            )

            # Exécuter les migrations dans une transaction
            with context.begin_transaction():
                logger.info("Début des migrations")
                context.run_migrations()
                logger.info("Migrations terminées avec succès")
                
                # Forcer le commit
                connection.commit()

        except Exception as e:
            logger.error(f"Erreur pendant les migrations: {str(e)}")
            connection.rollback()
            raise

# Choix du mode d'exécution
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
