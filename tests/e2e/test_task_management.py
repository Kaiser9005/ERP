import pytest
from playwright.sync_api import Page, expect
import json
from datetime import datetime, timezone, timedelta

class TestTaskManagement:
    """Tests End-to-End pour la gestion des tâches"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Configuration initiale pour chaque test"""
        # Mock des données de tâches
        current_time = datetime.now(timezone.utc)
        page.route("**/api/v1/projects/*/tasks*", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "tasks": [
                    {
                        "id": 1,
                        "title": "Plantation palmiers zone A",
                        "description": "Planter 50 palmiers dans la zone A",
                        "status": "EN_COURS",
                        "priority": "HAUTE",
                        "category": "PLANTATION",
                        "start_date": current_time.isoformat(),
                        "due_date": (current_time + timedelta(days=2)).isoformat(),
                        "completion_percentage": 30,
                        "weather_dependent": True
                    }
                ],
                "total": 1,
                "page": 1,
                "size": 20,
                "total_pages": 1
            })
        ))

        # Mock des données météo
        page.route("**/api/v1/tasks/*/weather", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps({
                "id": 1,
                "title": "Plantation palmiers zone A",
                "weather_suitable": True,
                "weather_conditions": {
                    "temperature": 25,
                    "humidity": 70,
                    "precipitation": 0,
                    "wind_speed": 15,
                    "conditions": "Ensoleillé",
                    "uv_index": 6,
                    "cloud_cover": 30
                },
                "weather_warnings": []
            })
        ))

        # Mock des ressources
        page.route("**/api/v1/resources", lambda route: route.fulfill(
            status=200,
            content_type="application/json",
            body=json.dumps([
                {
                    "id": 1,
                    "name": "Palmiers",
                    "quantity_available": 100,
                    "unit": "unités"
                }
            ])
        ))

        # Navigation vers la page des tâches
        page.goto("/projects/1/tasks")

    def test_task_list_display(self, page: Page):
        """Vérifie l'affichage de la liste des tâches"""
        # Vérification du titre
        expect(page.locator("[data-testid='page-title']")).to_contain_text("Tâches du Projet")
        
        # Vérification des filtres
        expect(page.locator("[data-testid='status-filter']")).to_be_visible()
        expect(page.locator("[data-testid='category-filter']")).to_be_visible()
        
        # Vérification de la tâche affichée
        expect(page.locator("[data-testid='task-title']")).to_contain_text("Plantation palmiers zone A")
        expect(page.locator("[data-testid='task-status']")).to_contain_text("EN_COURS")
        expect(page.locator("[data-testid='task-priority']")).to_contain_text("HAUTE")
        expect(page.locator("[data-testid='task-completion']")).to_contain_text("30%")

    def test_task_creation(self, page: Page):
        """Vérifie la création d'une nouvelle tâche"""
        # Clic sur le bouton de création
        page.locator("[data-testid='new-task-button']").click()
        
        # Remplissage du formulaire
        page.locator("[data-testid='task-title-input']").fill("Nouvelle plantation")
        page.locator("[data-testid='task-description-input']").fill("Description de test")
        page.locator("[data-testid='task-status-select']").select_option("A_FAIRE")
        page.locator("[data-testid='task-priority-select']").select_option("MOYENNE")
        page.locator("[data-testid='task-category-select']").select_option("PLANTATION")
        
        # Activation des conditions météo
        page.locator("[data-testid='weather-dependent-checkbox']").check()
        page.locator("[data-testid='min-temperature-input']").fill("20")
        page.locator("[data-testid='max-temperature-input']").fill("35")
        
        # Ajout d'une ressource
        page.locator("[data-testid='add-resource-button']").click()
        page.locator("[data-testid='resource-select']").select_option("1")
        page.locator("[data-testid='resource-quantity-input']").fill("50")
        
        # Sauvegarde
        page.locator("[data-testid='submit-button']").click()
        
        # Vérification du retour à la liste
        expect(page.url).to_end_with("/tasks")

    def test_task_weather_details(self, page: Page):
        """Vérifie l'affichage des détails météo d'une tâche"""
        # Clic sur l'icône météo
        page.locator("[data-testid='weather-conditions-button']").click()
        
        # Vérification des informations affichées
        expect(page.locator("[data-testid='weather-dialog-title']")).to_contain_text("Conditions Météorologiques Actuelles")
        expect(page.locator("[data-testid='temperature-value']")).to_contain_text("25°C")
        expect(page.locator("[data-testid='humidity-value']")).to_contain_text("70%")
        expect(page.locator("[data-testid='wind-speed-value']")).to_contain_text("15 km/h")
        expect(page.locator("[data-testid='weather-status']")).to_contain_text("Conditions météo favorables")

    def test_task_filtering(self, page: Page):
        """Vérifie le filtrage des tâches"""
        # Test du filtre par statut
        page.locator("[data-testid='status-filter']").select_option("EN_COURS")
        expect(page.locator("[data-testid='task-title']")).to_contain_text("Plantation palmiers zone A")
        
        page.locator("[data-testid='status-filter']").select_option("TERMINEE")
        expect(page.locator("[data-testid='task-title']")).not_to_be_visible()
        
        # Test du filtre par catégorie
        page.locator("[data-testid='status-filter']").select_option("ALL")
        page.locator("[data-testid='category-filter']").select_option("PLANTATION")
        expect(page.locator("[data-testid='task-title']")).to_contain_text("Plantation palmiers zone A")
        
        page.locator("[data-testid='category-filter']").select_option("MAINTENANCE")
        expect(page.locator("[data-testid='task-title']")).not_to_be_visible()

    def test_task_editing(self, page: Page):
        """Vérifie l'édition d'une tâche"""
        # Clic sur l'icône d'édition
        page.locator("[data-testid='edit-task-button']").click()
        
        # Modification des champs
        page.locator("[data-testid='task-title-input']").fill("Plantation palmiers zone A - Modifié")
        page.locator("[data-testid='completion-percentage-input']").fill("50")
        
        # Sauvegarde
        page.locator("[data-testid='submit-button']").click()
        
        # Vérification du retour à la liste
        expect(page.url).to_end_with("/tasks")

    def test_task_deletion(self, page: Page):
        """Vérifie la suppression d'une tâche"""
        # Mock de la confirmation
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Clic sur l'icône de suppression
        page.locator("[data-testid='delete-task-button']").click()
        
        # Vérification que la tâche n'est plus visible
        expect(page.locator("[data-testid='task-title']")).not_to_be_visible()

    def test_error_handling(self, page: Page):
        """Vérifie la gestion des erreurs"""
        # Simulation d'une erreur serveur
        page.route("**/api/v1/projects/*/tasks*", lambda route: route.fulfill(
            status=500,
            content_type="application/json",
            body=json.dumps({"error": "Erreur serveur"})
        ))
        
        # Rafraîchissement de la page
        page.reload()
        
        # Vérification du message d'erreur
        expect(page.locator("[data-testid='error-message']")).to_contain_text("Impossible de charger les tâches")
