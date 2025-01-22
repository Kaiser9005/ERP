#!/usr/bin/env python3
"""Simulateur de capteurs IoT pour le développement."""

import json
import time
import random
import threading
import http.server
import socketserver
from datetime import datetime
from typing import Dict, List

class IoTSensor:
    """Classe représentant un capteur IoT."""
    def __init__(
        self,
        sensor_id: str,
        sensor_type: str,
        min_value: float,
        max_value: float,
        unit: str
    ):
        self.id = sensor_id
        self.type = sensor_type
        self.min_value = min_value
        self.max_value = max_value
        self.unit = unit
        self.value = (min_value + max_value) / 2
        self.battery_level = 100
        self.signal_quality = 100

    def update(self):
        """Met à jour les valeurs du capteur."""
        # Simulation de variation de valeur
        variation = random.uniform(-0.5, 0.5)
        self.value = max(self.min_value, min(self.max_value, self.value + variation))
        
        # Simulation de batterie et signal
        self.battery_level = max(0, min(100, self.battery_level - random.uniform(0, 0.1)))
        self.signal_quality = max(0, min(100, self.signal_quality + random.uniform(-1, 1)))

    def to_dict(self) -> Dict:
        """Convertit les données du capteur en dictionnaire."""
        return {
            "id": self.id,
            "type": self.type,
            "last_reading": {
                "value": round(self.value, 2),
                "unit": self.unit,
                "timestamp": datetime.now().isoformat(),
                "battery_level": round(self.battery_level, 2),
                "signal_quality": round(self.signal_quality, 2)
            }
        }

class IoTSimulator:
    """Simulateur de réseau de capteurs IoT."""
    def __init__(self):
        self.sensors: List[IoTSensor] = [
            IoTSensor("TEMP001", "TEMPERATURE_AIR", 15, 35, "°C"),
            IoTSensor("HUM001", "HUMIDITE_AIR", 30, 80, "%"),
            IoTSensor("RAIN001", "PLUVIOMETRIE", 0, 50, "mm")
        ]
        self.running = False

    def start(self):
        """Démarre la simulation."""
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop)
        self.update_thread.start()

    def stop(self):
        """Arrête la simulation."""
        self.running = False
        if hasattr(self, 'update_thread'):
            self.update_thread.join()

    def _update_loop(self):
        """Boucle de mise à jour des capteurs."""
        while self.running:
            for sensor in self.sensors:
                sensor.update()
            time.sleep(1)

    def get_sensor_data(self) -> List[Dict]:
        """Récupère les données de tous les capteurs."""
        return [sensor.to_dict() for sensor in self.sensors]

class IoTRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Gestionnaire de requêtes HTTP pour le simulateur IoT."""
    simulator: IoTSimulator = None

    def do_GET(self):
        """Gère les requêtes GET."""
        if self.path == '/api/v1/iot/sensors':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = self.simulator.get_sensor_data()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_error(404)

def main():
    """Point d'entrée principal."""
    # Configuration du serveur
    PORT = 8081
    simulator = IoTSimulator()
    IoTRequestHandler.simulator = simulator

    # Démarrage du simulateur
    simulator.start()
    print(f"Simulateur IoT démarré sur le port {PORT}")
    print("Capteurs disponibles :")
    for sensor in simulator.sensors:
        print(f"- {sensor.id} ({sensor.type})")
    print("\nURL de l'API : http://localhost:8081/api/v1/iot/sensors")

    # Démarrage du serveur HTTP
    with socketserver.TCPServer(("", PORT), IoTRequestHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nArrêt du simulateur...")
            simulator.stop()
            httpd.server_close()

if __name__ == "__main__":
    main()