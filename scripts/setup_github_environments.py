#!/usr/bin/env python3
"""Script pour configurer les environnements GitHub Actions."""

import os
import sys
import yaml
import requests
from base64 import b64encode
from typing import Dict, List, Any

def load_config() -> Dict[str, Any]:
    """Charge la configuration des environnements."""
    config_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '.github',
        'environments.yml'
    )
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_github_token() -> str:
    """Récupère le token GitHub."""
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Erreur: GITHUB_TOKEN n'est pas défini")
        print("Définissez-le avec: export GITHUB_TOKEN=votre_token")
        sys.exit(1)
    return token

def get_repo_info() -> tuple:
    """Récupère les informations du repository."""
    remote_url = os.popen('git config --get remote.origin.url').read().strip()
    if 'github.com' not in remote_url:
        print("Erreur: Ce n'est pas un repository GitHub")
        sys.exit(1)
    
    # Extrait owner/repo de l'URL git
    parts = remote_url.split('github.com/')[-1].replace('.git', '').split('/')
    return parts[0], parts[1]

class GitHubAPI:
    """Classe pour interagir avec l'API GitHub."""
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}"
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    def create_environment(self, name: str, config: Dict[str, Any]) -> None:
        """Crée ou met à jour un environnement."""
        url = f"{self.base_url}/environments/{name}"
        
        # Prépare la configuration
        env_config = {
            'wait_timer': config.get('deployment_protection_rules', {}).get('wait_timer', 0),
            'reviewers': config.get('required_reviewers', []),
            'deployment_branch_policy': config.get('deployment_branch_policy', {
                'protected_branches': True,
                'custom_branches': []
            })
        }
        
        response = requests.put(url, json=env_config, headers=self.headers)
        if response.status_code not in [200, 201]:
            print(f"Erreur lors de la création de l'environnement {name}")
            print(response.text)
            return

        # Configure les variables d'environnement
        if 'variables' in config:
            for var_name, var_value in config['variables'].items():
                self.set_variable(name, var_name, var_value)

        print(f"Environnement {name} configuré avec succès")

    def set_variable(self, env_name: str, var_name: str, var_value: str) -> None:
        """Configure une variable d'environnement."""
        url = f"{self.base_url}/environments/{env_name}/variables"
        
        data = {
            'name': var_name,
            'value': var_value
        }
        
        response = requests.post(url, json=data, headers=self.headers)
        if response.status_code not in [201, 204]:
            print(f"Erreur lors de la configuration de la variable {var_name}")
            print(response.text)

    def create_secret(self, env_name: str, secret_name: str, secret_value: str) -> None:
        """Crée un secret d'environnement."""
        # Récupère la clé publique pour le chiffrement
        key_response = requests.get(
            f"{self.base_url}/environments/{env_name}/secrets/public-key",
            headers=self.headers
        )
        if key_response.status_code != 200:
            print(f"Erreur lors de la récupération de la clé publique pour {env_name}")
            return

        key_data = key_response.json()
        
        # Chiffre le secret
        encrypted_value = self.encrypt_secret(
            secret_value,
            key_data['key']
        )
        
        # Crée le secret
        url = f"{self.base_url}/environments/{env_name}/secrets/{secret_name}"
        data = {
            'encrypted_value': encrypted_value,
            'key_id': key_data['key_id']
        }
        
        response = requests.put(url, json=data, headers=self.headers)
        if response.status_code not in [201, 204]:
            print(f"Erreur lors de la création du secret {secret_name}")
            print(response.text)

    @staticmethod
    def encrypt_secret(secret_value: str, public_key: str) -> str:
        """Chiffre un secret avec la clé publique GitHub."""
        from nacl import encoding, public
        
        public_key = public.PublicKey(
            public_key.encode("utf-8"),
            encoding.Base64Encoder()
        )
        sealed_box = public.SealedBox(public_key)
        encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
        return b64encode(encrypted).decode("utf-8")

def main():
    """Point d'entrée principal."""
    # Charge la configuration
    config = load_config()
    
    # Récupère les informations nécessaires
    token = get_github_token()
    owner, repo = get_repo_info()
    
    # Initialise l'API GitHub
    github = GitHubAPI(token, owner, repo)
    
    # Configure chaque environnement
    for env_name, env_config in config.items():
        if env_name in ['global_variables', 'secret_scanning', 'deployment_rules', 'notifications']:
            continue
            
        print(f"\nConfiguration de l'environnement: {env_name}")
        github.create_environment(env_name, env_config)
        
        # Configure les variables globales
        if 'global_variables' in config:
            for var_name, var_value in config['global_variables'].items():
                github.set_variable(env_name, var_name, var_value)

    print("\nConfiguration terminée avec succès!")

if __name__ == "__main__":
    main()