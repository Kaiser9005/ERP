import requests
import os
from dotenv import load_dotenv
import logging

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Forcer le rechargement des variables d'environnement
load_dotenv(override=True)

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "password123")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@example.com")
ADMIN_NOM = os.getenv("ADMIN_NOM", "Admin")
ADMIN_PRENOM = os.getenv("ADMIN_PRENOM", "Super")
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8002")

def create_admin_user():
    """Crée le premier utilisateur administrateur."""
    url = f"{BACKEND_URL}/api/v1/auth/first-admin"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
        "email": ADMIN_EMAIL,
        "nom": ADMIN_NOM,
        "prenom": ADMIN_PRENOM
    }

    logger.info("Tentative de création du premier administrateur...")
    logger.info(f"URL configurée dans .env : {BACKEND_URL}")
    logger.info(f"URL finale : {url}")
    logger.info(f"Username: {ADMIN_USERNAME}")
    logger.info(f"Email: {ADMIN_EMAIL}")
    logger.info(f"Nom: {ADMIN_NOM}")
    logger.info(f"Prénom: {ADMIN_PRENOM}")

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        logger.info("Premier utilisateur administrateur créé avec succès.")
        logger.info(f"Réponse : {response.json()}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erreur lors de la création de l'utilisateur administrateur : {e}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Statut : {e.response.status_code}")
            logger.error(f"Réponse : {e.response.text}")
            
            # Analyse détaillée des erreurs courantes
            if e.response.status_code == 400:
                logger.error("Erreur de validation des données. Vérifiez que tous les champs sont corrects.")
            elif e.response.status_code == 409:
                logger.error("Un administrateur existe déjà dans le système.")
            elif e.response.status_code == 500:
                logger.error("Erreur interne du serveur. Vérifiez les logs du backend.")
        else:
            logger.error("Impossible de se connecter au serveur. Vérifiez qu'il est bien démarré.")

if __name__ == "__main__":
    create_admin_user()