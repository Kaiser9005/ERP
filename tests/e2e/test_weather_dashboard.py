import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta
import json

class TestWeatherDashboard:
    """Tests E2E pour le dashboard météo"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Configuration initiale pour chaque test"""
        # Mock des données météo
        page.route("**/api/v1/weather/agricultural-metrics", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "current_conditions": {
                    "temperature": 28.5,
                    "humidity": 75,
                    "precipitation": 0.5,
                    "wind_speed": 12,
                    "conditions": "Partiellement nuageux",
                    "uv_index": 6,
                    "cloud_cover": 40
                },
                "risks": {
                    "precipitation": {
                        "level": "LOW",
                        "message": "Conditions de précipitation normales"
                    },
                    "temperature": {
                        "level": "MEDIUM",
                        "message": "Températures élevées - Surveillance recommandée"
                    },
                    "level": "MEDIUM"
                },
                "recommendations": [
                    "Maintenir une surveillance de l'hydratation des plants",
                    "Conditions favorables pour les activités agricoles normales"
                ]
            })
        ))

        # Navigation vers le dashboard
        page.goto("/production/weather")
        
    def test_current_conditions_display(self, page: Page):
        """Vérifie l'affichage des conditions météorologiques actuelles"""
        # Vérification du titre
        expect(page.get_by_text("Conditions Météorologiques Actuelles")).to_be_visible()
        
        # Vérification des valeurs
        expect(page.get_by_text("28.5°C")).to_be_visible()
        expect(page.get_by_text("75%")).to_be_visible()
        expect(page.get_by_text("12 km/h")).to_be_visible()
        expect(page.get_by_text("Partiellement nuageux")).to_be_visible()

    def test_risk_alerts_display(self, page: Page):
        """Vérifie l'affichage des alertes et risques"""
        # Vérification du titre
        expect(page.get_by_text("Alertes et Risques")).to_be_visible()
        
        # Vérification du niveau de risque
        expect(page.get_by_text("Niveau de risque global: MEDIUM")).to_be_visible()
        
        # Vérification des messages de risque
        expect(page.get_by_text("Conditions de précipitation normales")).to_be_visible()
        expect(page.get_by_text("Températures élevées - Surveillance recommandée")).to_be_visible()

    def test_recommendations_display(self, page: Page):
        """Vérifie l'affichage des recommandations"""
        # Vérification du titre
        expect(page.get_by_text("Recommandations")).to_be_visible()
        
        # Vérification des recommandations
        expect(page.get_by_text("Maintenir une surveillance de l'hydratation des plants")).to_be_visible()
        expect(page.get_by_text("Conditions favorables pour les activités agricoles normales")).to_be_visible()

    def test_auto_refresh(self, page: Page):
        """Vérifie le rafraîchissement automatique des données"""
        # Mock d'une mise à jour des données après 30 minutes
        page.route("**/api/v1/weather/agricultural-metrics", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "current_conditions": {
                    "temperature": 30.0,  # Température mise à jour
                    "humidity": 70,
                    "precipitation": 0,
                    "wind_speed": 15,
                    "conditions": "Ensoleillé",
                    "uv_index": 8,
                    "cloud_cover": 20
                },
                "risks": {
                    "precipitation": {
                        "level": "LOW",
                        "message": "Conditions de précipitation normales"
                    },
                    "temperature": {
                        "level": "HIGH",
                        "message": "Risque de stress thermique pour les cultures"
                    },
                    "level": "HIGH"
                },
                "recommendations": [
                    "Augmenter l'irrigation",
                    "Protéger les plants sensibles"
                ]
            })
        ))

        # Attente du rafraîchissement (simulé à 1 minute pour le test)
        page.wait_for_timeout(1000)

        # Vérification des nouvelles valeurs
        expect(page.get_by_text("30.0°C")).to_be_visible()
        expect(page.get_by_text("Ensoleillé")).to_be_visible()
        expect(page.get_by_text("Niveau de risque global: HIGH")).to_be_visible()

    def test_error_handling(self, page: Page):
        """Vérifie la gestion des erreurs"""
        # Simulation d'une erreur API
        page.route("**/api/v1/weather/agricultural-metrics", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Erreur serveur"})
        ))

        # Rafraîchissement de la page
        page.reload()

        # Vérification du message d'erreur
        expect(page.get_by_text("Erreur lors de la récupération des données météo")).to_be_visible()

    def test_loading_state(self, page: Page):
        """Vérifie l'affichage de l'état de chargement"""
        # Simulation d'une réponse lente
        page.route("**/api/v1/weather/agricultural-metrics", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({}),
            delay=1000
        ))

        # Rafraîchissement de la page
        page.reload()

        # Vérification de l'indicateur de chargement
        expect(page.get_by_role("progressbar")).to_be_visible()
