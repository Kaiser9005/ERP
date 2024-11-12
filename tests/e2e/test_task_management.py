import pytest
from playwright.sync_api import Page, expect
import json

class TestTaskManagement:
    """Tests End-to-End pour la gestion des tâches"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """Configuration initiale pour chaque test"""
        # Mock des données de tâches
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
                        "start_date": "2024-02-01T08:00:00Z",
                        "due_date": "2024-02-03T17:00:00Z",
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
        expect(page.get_by_text("Tâches du Projet")).to_be_visible()
        
        # Vérification des filtres
        expect(page.get_by_label("Statut")).to_be_visible()
        expect(page.get_by_label("Catégorie")).to_be_visible()
        
        # Vérification de la tâche affichée
        expect(page.get_by_text("Plantation palmiers zone A")).to_be_visible()
        expect(page.get_by_text("EN_COURS")).to_be_visible()
        expect(page.get_by_text("HAUTE")).to_be_visible()
        expect(page.get_by_text("30%")).to_be_visible()

    def test_task_creation(self, page: Page):
        """Vérifie la création d'une nouvelle tâche"""
        # Clic sur le bouton de création
        page.get_by_text("Nouvelle Tâche").click()
        
        # Remplissage du formulaire
        page.get_by_label("Titre").fill("Nouvelle plantation")
        page.get_by_label("Description").fill("Description de test")
        page.get_by_label("Statut").select_option("A_FAIRE")
        page.get_by_label("Priorité").select_option("MOYENNE")
        page.get_by_label("Catégorie").select_option("PLANTATION")
        
        # Activation des conditions météo
        page.get_by_label("Tâche dépendante de la météo").check()
        page.get_by_label("Température minimale (°C)").fill("20")
        page.get_by_label("Température maximale (°C)").fill("35")
        
        # Ajout d'une ressource
        page.get_by_text("Ajouter une ressource").click()
        page.get_by_label("Ressource").select_option("1")  # Premier élément
        page.get_by_label("Quantité requise").fill("50")
        
        # Sauvegarde
        page.get_by_text("Enregistrer").click()
        
        # Vérification du retour à la liste
        expect(page.url).to_end_with("/tasks")

    def test_task_weather_details(self, page: Page):
        """Vérifie l'affichage des détails météo d'une tâche"""
        # Clic sur l'icône météo
        page.get_by_title("Conditions météo").click()
        
        # Vérification des informations affichées
        expect(page.get_by_text("Conditions Météorologiques Actuelles")).to_be_visible()
        expect(page.get_by_text("25°C")).to_be_visible()
        expect(page.get_by_text("70%")).to_be_visible()
        expect(page.get_by_text("15 km/h")).to_be_visible()
        expect(page.get_by_text("Conditions météo favorables")).to_be_visible()

    def test_task_filtering(self, page: Page):
        """Vérifie le filtrage des tâches"""
        # Test du filtre par statut
        page.get_by_label("Statut").select_option("EN_COURS")
        expect(page.get_by_text("Plantation palmiers zone A")).to_be_visible()
        
        page.get_by_label("Statut").select_option("TERMINEE")
        expect(page.get_by_text("Plantation palmiers zone A")).not_to_be_visible()
        
        # Test du filtre par catégorie
        page.get_by_label("Statut").select_option("ALL")
        page.get_by_label("Catégorie").select_option("PLANTATION")
        expect(page.get_by_text("Plantation palmiers zone A")).to_be_visible()
        
        page.get_by_label("Catégorie").select_option("MAINTENANCE")
        expect(page.get_by_text("Plantation palmiers zone A")).not_to_be_visible()

    def test_task_editing(self, page: Page):
        """Vérifie l'édition d'une tâche"""
        # Clic sur l'icône d'édition
        page.get_by_title("Modifier").click()
        
        # Modification des champs
        page.get_by_label("Titre").fill("Plantation palmiers zone A - Modifié")
        page.get_by_label("Progression (%)").fill("50")
        
        # Sauvegarde
        page.get_by_text("Enregistrer").click()
        
        # Vérification du retour à la liste
        expect(page.url).to_end_with("/tasks")

    def test_task_deletion(self, page: Page):
        """Vérifie la suppression d'une tâche"""
        # Mock de la confirmation
        page.on("dialog", lambda dialog: dialog.accept())
        
        # Clic sur l'icône de suppression
        page.get_by_title("Supprimer").click()
        
        # Vérification que la tâche n'est plus visible
        expect(page.get_by_text("Plantation palmiers zone A")).not_to_be_visible()

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
        expect(page.get_by_text("Impossible de charger les tâches")).to_be_visible()
