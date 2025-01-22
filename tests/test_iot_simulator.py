"""Tests pour le simulateur IoT."""

import pytest
import json
import threading
import time
import requests
from scripts.iot_simulator import IoTSimulator, IoTSensor

def test_sensor_initialization():
    """Test l'initialisation d'un capteur."""
    sensor = IoTSensor("TEST001", "TEMPERATURE", 0, 100, "°C")
    assert sensor.id == "TEST001"
    assert sensor.type == "TEMPERATURE"
    assert sensor.min_value == 0
    assert sensor.max_value == 100
    assert sensor.unit == "°C"
    assert 0 <= sensor.value <= 100
    assert sensor.battery_level == 100
    assert sensor.signal_quality == 100

def test_sensor_update():
    """Test la mise à jour des valeurs d'un capteur."""
    sensor = IoTSensor("TEST001", "TEMPERATURE", 20, 30, "°C")
    initial_value = sensor.value
    initial_battery = sensor.battery_level
    
    # Mise à jour du capteur
    sensor.update()
    
    # Vérification que les valeurs ont changé dans les limites
    assert 20 <= sensor.value <= 30
    assert sensor.value != initial_value  # La valeur devrait avoir changé
    assert sensor.battery_level <= initial_battery  # La batterie devrait avoir diminué

def test_sensor_to_dict():
    """Test la conversion des données du capteur en dictionnaire."""
    sensor = IoTSensor("TEST001", "TEMPERATURE", 0, 100, "°C")
    data = sensor.to_dict()
    
    assert data["id"] == "TEST001"
    assert data["type"] == "TEMPERATURE"
    assert "last_reading" in data
    assert "value" in data["last_reading"]
    assert "unit" in data["last_reading"]
    assert "timestamp" in data["last_reading"]
    assert "battery_level" in data["last_reading"]
    assert "signal_quality" in data["last_reading"]

def test_simulator_initialization():
    """Test l'initialisation du simulateur."""
    simulator = IoTSimulator()
    assert len(simulator.sensors) == 3  # TEMP001, HUM001, RAIN001
    assert simulator.running == False

@pytest.mark.integration
def test_simulator_api():
    """Test l'API du simulateur."""
    # Démarrage du simulateur dans un thread séparé
    simulator = IoTSimulator()
    simulator.start()
    
    # Attente du démarrage du serveur
    time.sleep(2)
    
    try:
        # Test de l'API
        response = requests.get("http://localhost:8081/api/v1/iot/sensors")
        assert response.status_code == 200
        
        data = response.json()
        assert len(data) == 3  # 3 capteurs
        
        # Vérification des données de chaque capteur
        sensor_ids = [sensor["id"] for sensor in data]
        assert "TEMP001" in sensor_ids
        assert "HUM001" in sensor_ids
        assert "RAIN001" in sensor_ids
        
        # Vérification du format des données
        for sensor in data:
            assert "id" in sensor
            assert "type" in sensor
            assert "last_reading" in sensor
            assert "value" in sensor["last_reading"]
            assert "unit" in sensor["last_reading"]
            assert "timestamp" in sensor["last_reading"]
            assert "battery_level" in sensor["last_reading"]
            assert "signal_quality" in sensor["last_reading"]
    
    finally:
        # Arrêt du simulateur
        simulator.stop()

def test_simulator_data_consistency():
    """Test la cohérence des données du simulateur."""
    simulator = IoTSimulator()
    simulator.start()
    
    try:
        # Récupération des données à deux moments différents
        data1 = simulator.get_sensor_data()
        time.sleep(2)
        data2 = simulator.get_sensor_data()
        
        # Vérification que les valeurs ont changé
        for sensor1, sensor2 in zip(data1, data2):
            assert sensor1["id"] == sensor2["id"]  # Même capteur
            # Les valeurs devraient être différentes
            assert sensor1["last_reading"]["value"] != sensor2["last_reading"]["value"]
            # Les valeurs devraient rester dans les limites
            if sensor1["id"] == "TEMP001":
                assert 15 <= sensor2["last_reading"]["value"] <= 35
            elif sensor1["id"] == "HUM001":
                assert 30 <= sensor2["last_reading"]["value"] <= 80
            elif sensor1["id"] == "RAIN001":
                assert 0 <= sensor2["last_reading"]["value"] <= 50
    
    finally:
        simulator.stop()

def test_simulator_error_handling():
    """Test la gestion des erreurs du simulateur."""
    simulator = IoTSimulator()
    
    # Test d'arrêt sans démarrage
    simulator.stop()  # Ne devrait pas lever d'erreur
    
    # Test de double démarrage
    simulator.start()
    simulator.start()  # Ne devrait pas créer de second thread
    
    # Nettoyage
    simulator.stop()

if __name__ == "__main__":
    pytest.main([__file__])