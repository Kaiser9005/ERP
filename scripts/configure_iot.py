#!/usr/bin/env python3
"""Script de configuration des clés API IoT."""

import json
import base64
import argparse
import os
from typing import Dict, List

def create_device_config(
    device_id: str,
    device_type: str,
    token: str,
    attributes: Dict[str, any]
) -> Dict:
    """Crée la configuration pour un device IoT."""
    return {
        "id": device_id,
        "type": device_type,
        "token": token,
        "attributes": attributes
    }

def encode_config(config: List[Dict]) -> str:
    """Encode la configuration en base64."""
    config_json = json.dumps(config)
    return base64.b64encode(config_json.encode()).decode()

def main():
    parser = argparse.ArgumentParser(description="Configure les clés API IoT")
    parser.add_argument("--env-file", default=".env", help="Chemin vers le fichier .env")
    args = parser.parse_args()

    # Configuration des devices
    devices = [
        create_device_config(
            "TEMP001",
            "TEMPERATURE_AIR",
            input("Token pour TEMP001 (température) : "),
            {
                "unit": "°C",
                "min_value": -10,
                "max_value": 50,
                "precision": 0.1
            }
        ),
        create_device_config(
            "HUM001",
            "HUMIDITE_AIR",
            input("Token pour HUM001 (humidité) : "),
            {
                "unit": "%",
                "min_value": 0,
                "max_value": 100,
                "precision": 1
            }
        ),
        create_device_config(
            "RAIN001",
            "PLUVIOMETRIE",
            input("Token pour RAIN001 (pluviométrie) : "),
            {
                "unit": "mm",
                "min_value": 0,
                "max_value": 500,
                "precision": 0.1
            }
        )
    ]

    # Encodage de la configuration
    iot_api_key = encode_config(devices)

    # Mise à jour du fichier .env
    env_path = args.env_file
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
        
        # Recherche et mise à jour de IOT_API_KEY
        found = False
        for i, line in enumerate(lines):
            if line.startswith('IOT_API_KEY='):
                lines[i] = f'IOT_API_KEY={iot_api_key}\n'
                found = True
                break
        
        # Ajout de la clé si elle n'existe pas
        if not found:
            lines.append(f'\nIOT_API_KEY={iot_api_key}\n')
        
        with open(env_path, 'w') as f:
            f.writelines(lines)
    else:
        with open(env_path, 'w') as f:
            f.write(f'IOT_API_KEY={iot_api_key}\n')

    print("\nConfiguration IoT terminée !")
    print(f"La clé API IoT a été enregistrée dans {env_path}")
    print("\nPour vérifier la configuration :")
    print("1. Démarrez le backend : python main.py")
    print("2. Testez la connexion aux capteurs : curl http://localhost:8000/api/v1/iot/sensors")

if __name__ == "__main__":
    main()