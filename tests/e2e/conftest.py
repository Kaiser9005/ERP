import pytest
import os
import jwt
from datetime import datetime, timedelta
from typing import Generator
from playwright.sync_api import Browser, BrowserContext, Page, expect

# Configuration des fixtures pour les tests E2E
@pytest.fixture(scope="session")
def auth_token() -> str:
    """Génère un token JWT valide pour les tests."""
    secret_key = os.getenv("SECRET_KEY", "test_secret_key")
    payload = {
        "sub": "1",  # ID utilisateur de test
        "exp": datetime.now(datetime.timezone.utc) + timedelta(days=1),
        "roles": ["admin"]
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, auth_token):
    """Configure le contexte du navigateur avec les paramètres nécessaires."""
    return {
        **browser_context_args,
        "base_url": "http://localhost:3000",
        "viewport": {
            "width": 1280,
            "height": 720
        },
        "ignore_https_errors": True,
        "extra_http_headers": {
            "Authorization": f"Bearer {auth_token}"
        }
    }

@pytest.fixture(scope="function")
def test_page(page: Page) -> Generator[Page, None, None]:
    """Configure une page de test avec des utilitaires supplémentaires."""
    
    # Ajouter des helpers à la page
    page.wait_for_loaded = lambda: page.wait_for_selector('[data-testid="page-loaded"]')
    page.wait_for_toast = lambda message: page.wait_for_selector(f'text={message}')
    
    # Intercepter les erreurs console
    page.on("console", lambda msg: print(f"Browser console {msg.type}: {msg.text}"))
    
    # Attendre que la page soit chargée
    page.goto("/")
    page.wait_for_loaded()
    
    yield page

@pytest.fixture(scope="function")
def authenticated_page(test_page: Page, auth_token: str) -> Page:
    """Configure une page authentifiée pour les tests."""
    # Stocker le token dans le localStorage
    test_page.evaluate(f"""
        window.localStorage.setItem('auth_token', '{auth_token}');
    """)
    
    # Recharger la page pour appliquer l'authentification
    test_page.reload()
    test_page.wait_for_loaded()
    
    return test_page

@pytest.fixture(scope="function")
def task_page(authenticated_page: Page) -> Page:
    """Configure une page spécifique pour les tests de tâches."""
    authenticated_page.goto("/projects/1/tasks")
    authenticated_page.wait_for_loaded()
    return authenticated_page

# Helpers pour les tests
def fill_task_form(page: Page, task_data: dict) -> None:
    """Helper pour remplir le formulaire de tâche."""
    if "title" in task_data:
        page.fill("[name=title]", task_data["title"])
    if "description" in task_data:
        page.fill("[name=description]", task_data["description"])
    if "status" in task_data:
        page.click("text=Statut")
        page.click(f"text={task_data['status']}")
    if "priority" in task_data:
        page.click("text=Priorité")
        page.click(f"text={task_data['priority']}")
    if "category" in task_data:
        page.click("text=Catégorie")
        page.click(f"text={task_data['category']}")
    if "due_date" in task_data:
        page.fill("[name=due_date]", task_data["due_date"])
    if "weather_dependent" in task_data and task_data["weather_dependent"]:
        page.click("text=Tâche dépendante de la météo")
        if "min_temperature" in task_data:
            page.fill("[name=min_temperature]", str(task_data["min_temperature"]))
        if "max_temperature" in task_data:
            page.fill("[name=max_temperature]", str(task_data["max_temperature"]))
        if "max_wind_speed" in task_data:
            page.fill("[name=max_wind_speed]", str(task_data["max_wind_speed"]))
        if "max_precipitation" in task_data:
            page.fill("[name=max_precipitation]", str(task_data["max_precipitation"]))
    if "completion_percentage" in task_data:
        page.fill("[name=completion_percentage]", str(task_data["completion_percentage"]))

def assert_task_in_list(page: Page, task_title: str) -> None:
    """Helper pour vérifier qu'une tâche est présente dans la liste."""
    expect(page.locator(f"text={task_title}")).to_be_visible()

def assert_task_not_in_list(page: Page, task_title: str) -> None:
    """Helper pour vérifier qu'une tâche n'est pas présente dans la liste."""
    expect(page.locator(f"text={task_title}")).not_to_be_visible()

def assert_toast_message(page: Page, message: str) -> None:
    """Helper pour vérifier l'affichage d'un message toast."""
    expect(page.locator(f"text={message}")).to_be_visible()

def assert_validation_error(page: Page, field: str, message: str) -> None:
    """Helper pour vérifier l'affichage d'une erreur de validation."""
    error_selector = f"[data-testid='{field}-error']"
    expect(page.locator(error_selector)).to_contain_text(message)
