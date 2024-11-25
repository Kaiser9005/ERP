"""Tests End-to-End pour le dashboard IoT-Inventaire."""

import pytest
from playwright.sync_api import Page, expect
import json
from datetime import datetime, timezone, timedelta

class TestIoTInventoryDashboard:
    """Tests E2E pour le dashboard IoT et inventaire."""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Configuration initiale pour chaque test."""
        # Mock des données capteurs
        current_time = datetime.now(timezone.utc)
        page.route("**/api/v1/iot/sensors*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {
                    "id": "sensor1",
                    "code": "TEMP001",
                    "type": "TEMPERATURE_AIR",
                    "status": "ACTIF",
                    "last_reading": {
                        "value": 22.5,
                        "unit": "°C",
                        "timestamp": current_time.isoformat(),
                        "battery_level": 85,
                        "signal_quality": 95
                    }
                },
                {
                    "id": "sensor2",
                    "code": "HUM001",
                    "type": "HUMIDITE_AIR",
                    "status": "ACTIF",
                    "last_reading": {
                        "value": 55,
                        "unit": "%",
                        "timestamp": current_time.isoformat(),
                        "battery_level": 90,
                        "signal_quality": 98
                    }
                }
            ])
        ))

        # Mock des données stocks
        page.route("**/api/v1/inventory/stocks*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {
                    "id": "stock1",
                    "code": "S001",
                    "product": "Huile de Palme",
                    "quantity": 1000,
                    "unit": "litres",
                    "storage_conditions": {
                        "temperature_min": 15,
                        "temperature_max": 25,
                        "humidity_min": 30,
                        "humidity_max": 60
                    },
                    "current_conditions": {
                        "temperature": 22.5,
                        "humidity": 55,
                        "last_update": current_time.isoformat()
                    }
                }
            ])
        ))

        # Mock des alertes
        page.route("**/api/v1/iot/alerts*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {
                    "id": "alert1",
                    "type": "TEMPERATURE",
                    "severity": "WARNING",
                    "message": "Température proche du seuil maximum",
                    "timestamp": current_time.isoformat(),
                    "sensor_id": "sensor1"
                }
            ])
        ))

        # Mock des recommandations
        page.route("**/api/v1/iot/recommendations*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {
                    "id": "rec1",
                    "type": "MAINTENANCE",
                    "priority": "MEDIUM",
                    "message": "Maintenance préventive recommandée",
                    "sensor_id": "sensor1",
                    "due_date": (current_time + timedelta(days=7)).isoformat()
                }
            ])
        ))

        # Navigation vers le dashboard
        page.goto("/inventory/iot-dashboard")

    def test_dashboard_overview(self, page: Page):
        """Vérifie l'affichage général du dashboard."""
        # Vérification du titre
        expect(page.locator("[data-testid='page-title']")).to_contain_text("Monitoring IoT")
        
        # Vérification des sections principales
        expect(page.locator("[data-testid='sensors-overview']")).to_be_visible()
        expect(page.locator("[data-testid='storage-conditions']")).to_be_visible()
        expect(page.locator("[data-testid='active-alerts']")).to_be_visible()
        expect(page.locator("[data-testid='maintenance-recommendations']")).to_be_visible()

    def test_sensor_readings(self, page: Page):
        """Vérifie l'affichage des lectures des capteurs."""
        # Vérification des capteurs
        expect(page.locator("[data-testid='sensor-TEMP001']")).to_contain_text("22.5°C")
        expect(page.locator("[data-testid='sensor-HUM001']")).to_contain_text("55%")
        
        # Vérification des statuts
        expect(page.locator("[data-testid='sensor-TEMP001-status']")).to_contain_text("ACTIF")
        expect(page.locator("[data-testid='sensor-HUM001-status']")).to_contain_text("ACTIF")

    def test_storage_conditions_monitoring(self, page: Page):
        """Vérifie le monitoring des conditions de stockage."""
        # Vérification du stock
        expect(page.locator("[data-testid='stock-S001']")).to_contain_text("Huile de Palme")
        
        # Vérification des conditions actuelles
        expect(page.locator("[data-testid='stock-S001-temperature']")).to_contain_text("22.5°C")
        expect(page.locator("[data-testid='stock-S001-humidity']")).to_contain_text("55%")
        
        # Vérification des seuils
        expect(page.locator("[data-testid='stock-S001-limits']")).to_contain_text("15-25°C")

    def test_alerts_display(self, page: Page):
        """Vérifie l'affichage et la gestion des alertes."""
        # Vérification de l'alerte
        expect(page.locator("[data-testid='alert-temperature']")).to_be_visible()
        expect(page.locator("[data-testid='alert-severity-warning']")).to_be_visible()
        
        # Acquittement de l'alerte
        page.locator("[data-testid='acknowledge-alert-button']").click()
        expect(page.locator("[data-testid='alert-temperature']")).not_to_be_visible()

    def test_maintenance_recommendations(self, page: Page):
        """Vérifie l'affichage des recommandations de maintenance."""
        # Vérification de la recommandation
        expect(page.locator("[data-testid='maintenance-rec1']")).to_be_visible()
        expect(page.locator("[data-testid='maintenance-priority-medium']")).to_be_visible()
        
        # Planification de la maintenance
        page.locator("[data-testid='schedule-maintenance-button']").click()
        page.locator("[data-testid='maintenance-date-input']").fill(
            (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        )
        page.locator("[data-testid='confirm-maintenance-button']").click()
        
        # Vérification de la mise à jour
        expect(page.locator("[data-testid='maintenance-status-scheduled']")).to_be_visible()

    def test_sensor_details(self, page: Page):
        """Vérifie l'affichage détaillé des capteurs."""
        # Ouverture des détails
        page.locator("[data-testid='sensor-TEMP001']").click()
        
        # Vérification des informations détaillées
        expect(page.locator("[data-testid='sensor-details-dialog']")).to_be_visible()
        expect(page.locator("[data-testid='sensor-battery']")).to_contain_text("85%")
        expect(page.locator("[data-testid='sensor-signal']")).to_contain_text("95%")
        
        # Vérification du graphique historique
        expect(page.locator("[data-testid='sensor-history-chart']")).to_be_visible()

    def test_error_handling(self, page: Page):
        """Vérifie la gestion des erreurs."""
        # Simulation d'une erreur de capteur
        page.route("**/api/v1/iot/sensors*", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Erreur de communication"})
        ))
        
        # Rafraîchissement de la page
        page.reload()
        
        # Vérification du message d'erreur
        expect(page.locator("[data-testid='error-message']")).to_contain_text(
            "Impossible de récupérer les données des capteurs"
        )

    def test_realtime_updates(self, page: Page):
        """Vérifie les mises à jour en temps réel."""
        # Simulation d'une nouvelle lecture
        page.evaluate("""
            window.postMessage({
                type: 'SENSOR_UPDATE',
                data: {
                    sensor_id: 'sensor1',
                    value: 24.0,
                    unit: '°C',
                    timestamp: new Date().toISOString()
                }
            }, '*')
        """)
        
        # Vérification de la mise à jour
        expect(page.locator("[data-testid='sensor-TEMP001']")).to_contain_text("24.0°C")
