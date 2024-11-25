# Guide des Tests End-to-End (E2E)

## Vue d'ensemble

Les tests E2E utilisent Playwright pour tester l'application FOFAL ERP dans des conditions réelles d'utilisation.

## Configuration

### Installation
```bash
# Installation de Playwright
pip install pytest-playwright
playwright install

# Installation des dépendances
pip install -r requirements.txt
cd frontend && npm install
```

### Configuration de Base
```python
# tests/e2e/conftest.py
import pytest
from playwright.sync_api import Page, Browser, BrowserContext

@pytest.fixture
def browser_context_args(browser_context_args):
    """Configuration du contexte du navigateur."""
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720
        },
        "record_video_dir": "test-results/videos/"
    }

@pytest.fixture
def auth_token():
    """Token JWT pour l'authentification."""
    return generate_test_token()

@pytest.fixture
def authenticated_page(page: Page, auth_token: str):
    """Page avec authentification."""
    page.goto("/")
    page.evaluate(f"localStorage.setItem('token', '{auth_token}')")
    return page
```

## Structure des Tests

### Organisation
```
tests/e2e/
├── conftest.py                    # Fixtures partagées
├── test_auth.py                   # Tests d'authentification
├── test_inventory.py              # Tests inventaire
├── test_finance.py               # Tests finance
└── test_production.py            # Tests production
```

### Exemple de Test Complet
```python
def test_inventory_workflow(authenticated_page: Page):
    """Test du workflow complet d'inventaire."""
    # 1. Navigation
    authenticated_page.goto("/inventory")
    
    # 2. Création d'un produit
    authenticated_page.click("[data-testid='add-product-button']")
    authenticated_page.fill("[data-testid='product-name']", "Test Product")
    authenticated_page.fill("[data-testid='product-quantity']", "100")
    authenticated_page.click("[data-testid='submit-button']")
    
    # 3. Vérification
    expect(authenticated_page.locator("text=Test Product")).to_be_visible()
    expect(authenticated_page.locator("text=100")).to_be_visible()
    
    # 4. Modification
    authenticated_page.click("[data-testid='edit-button']")
    authenticated_page.fill("[data-testid='product-quantity']", "150")
    authenticated_page.click("[data-testid='submit-button']")
    
    # 5. Vérification finale
    expect(authenticated_page.locator("text=150")).to_be_visible()
```

## Standards de Test

### 1. Sélection des Éléments
```python
# ✅ Bon : Utiliser data-testid
page.click("[data-testid='submit-button']")

# ✅ Bon : Utiliser des rôles
page.click("button[role='submit']")

# ❌ Mauvais : Sélecteurs CSS complexes
page.click(".form > div > button.submit")
```

### 2. Attentes et Assertions
```python
# ✅ Bon : Attendre la visibilité
expect(page.locator("[data-testid='result']")).to_be_visible()

# ✅ Bon : Attendre le texte
expect(page.locator("h1")).to_have_text("Dashboard")

# ❌ Mauvais : Attentes arbitraires
page.wait_for_timeout(2000)
```

### 3. Actions Utilisateur
```python
# ✅ Bon : Simulation réaliste
page.click("[data-testid='menu-button']")
page.click("text=Settings")

# ✅ Bon : Remplissage de formulaire
page.fill("[data-testid='username']", "test@example.com")
page.fill("[data-testid='password']", "password123")
page.click("[data-testid='login-button']")

# ❌ Mauvais : Manipulation directe d'état
page.evaluate("localStorage.setItem('loggedIn', true)")
```

## Fixtures Communes

### 1. Navigation
```python
@pytest.fixture
def inventory_page(authenticated_page: Page):
    """Page inventaire authentifiée."""
    authenticated_page.goto("/inventory")
    return authenticated_page

@pytest.fixture
def dashboard_page(authenticated_page: Page):
    """Page tableau de bord authentifiée."""
    authenticated_page.goto("/dashboard")
    return authenticated_page
```

### 2. Données de Test
```python
@pytest.fixture
def test_product():
    """Produit de test."""
    return {
        "name": "Test Product",
        "quantity": 100,
        "category": "Test Category"
    }

@pytest.fixture
def test_user():
    """Utilisateur de test."""
    return {
        "email": "test@example.com",
        "password": "password123"
    }
```

## Helpers

### 1. Navigation
```python
def navigate_to_section(page: Page, section: str):
    """Navigation vers une section."""
    page.click(f"[data-testid='nav-{section}']")
    expect(page.locator(f"[data-testid='{section}-page']")).to_be_visible()

def open_modal(page: Page, modal_name: str):
    """Ouverture d'une modale."""
    page.click(f"[data-testid='open-{modal_name}-modal']")
    expect(page.locator(f"[data-testid='{modal_name}-modal']")).to_be_visible()
```

### 2. Formulaires
```python
def fill_form(page: Page, form_data: dict):
    """Remplissage d'un formulaire."""
    for field, value in form_data.items():
        page.fill(f"[data-testid='{field}-input']", str(value))

def submit_form(page: Page, form_id: str):
    """Soumission d'un formulaire."""
    page.click(f"[data-testid='{form_id}-submit']")
    expect(page.locator("[data-testid='success-message']")).to_be_visible()
```

## Bonnes Pratiques

### 1. Organisation des Tests
- Un fichier par fonctionnalité majeure
- Tests indépendants
- Setup et teardown appropriés

### 2. Performance
- Minimiser les attentes
- Réutiliser l'authentification
- Nettoyer les données de test

### 3. Fiabilité
- Gérer les timeouts
- Vérifier les états intermédiaires
- Capturer les échecs avec screenshots

### 4. Maintenance
- Utiliser des sélecteurs stables
- Documenter les scénarios complexes
- Maintenir les fixtures à jour

## Maintenance

### Documentation
- Documenter les nouveaux sélecteurs
- Expliquer les workflows complexes
- Maintenir les exemples à jour

### Mise à Jour
- Revoir les tests après changements UI
- Mettre à jour les sélecteurs
- Adapter les workflows si nécessaire

### Performance
- Optimiser les temps d'attente
- Paralléliser les tests
- Monitorer les temps d'exécution
