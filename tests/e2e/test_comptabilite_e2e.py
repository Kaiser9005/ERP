import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, date

def test_comptabilite_dashboard(page: Page):
    """Test E2E du dashboard comptable"""
    
    # Connexion
    page.goto("/login")
    page.fill("[data-testid=email-input]", "test@example.com")
    page.fill("[data-testid=password-input]", "password123")
    page.click("[data-testid=login-button]")
    
    # Navigation vers la comptabilité
    page.click("text=Comptabilité")
    
    # Vérification des composants principaux
    expect(page.locator("text=Statistiques Financières")).to_be_visible()
    expect(page.locator("text=Évolution de la Trésorerie")).to_be_visible()
    expect(page.locator("text=Aperçu Budgétaire")).to_be_visible()
    
    # Vérification des onglets
    tabs = [
        "Plan Comptable",
        "Saisie d'Écritures",
        "Journaux",
        "Grand Livre",
        "Balance",
        "Bilan",
        "Compte de Résultat"
    ]
    for tab in tabs:
        expect(page.locator(f"text={tab}")).to_be_visible()

def test_creation_ecriture_comptable(page: Page):
    """Test E2E de la création d'une écriture comptable"""
    
    # Navigation
    page.goto("/comptabilite")
    page.click("text=Nouvelle Écriture")
    
    # Remplissage du formulaire
    page.fill("[data-testid=date-ecriture]", date.today().isoformat())
    page.fill("[data-testid=numero-piece]", "FAC2024-001")
    page.click("[data-testid=select-compte]")
    page.click("text=601000 - Achats matières premières")
    page.fill("[data-testid=libelle]", "Achat test e2e")
    page.fill("[data-testid=montant-debit]", "1000")
    page.click("[data-testid=select-journal]")
    page.click("text=ACH - Journal des achats")
    
    # Soumission
    page.click("[data-testid=submit-ecriture]")
    
    # Vérification
    expect(page.locator("text=Écriture créée avec succès")).to_be_visible()

def test_consultation_rapports(page: Page):
    """Test E2E de la consultation des rapports comptables"""
    
    # Navigation
    page.goto("/comptabilite")
    
    # Grand Livre
    page.click("text=Grand Livre")
    expect(page.locator("[data-testid=grand-livre-table]")).to_be_visible()
    expect(page.locator("text=Achat test e2e")).to_be_visible()
    
    # Balance
    page.click("text=Balance")
    expect(page.locator("[data-testid=balance-table]")).to_be_visible()
    
    # Bilan
    page.click("text=Bilan")
    expect(page.locator("[data-testid=bilan-actif]")).to_be_visible()
    expect(page.locator("[data-testid=bilan-passif]")).to_be_visible()
    
    # Compte de Résultat
    page.click("text=Compte de Résultat")
    expect(page.locator("[data-testid=compte-resultat-produits]")).to_be_visible()
    expect(page.locator("[data-testid=compte-resultat-charges]")).to_be_visible()

def test_analyse_budgetaire(page: Page):
    """Test E2E de l'analyse budgétaire"""
    
    # Navigation
    page.goto("/comptabilite")
    
    # Vérification du composant BudgetOverview
    budget_card = page.locator("[data-testid=budget-overview]")
    expect(budget_card).to_be_visible()
    
    # Vérification des éléments
    expect(page.locator("text=Progression globale")).to_be_visible()
    expect(page.locator("text=Impact météo")).to_be_visible()
    expect(page.locator("[data-testid=budget-categories]")).to_be_visible()
    expect(page.locator("[data-testid=weather-impact]")).to_be_visible()

def test_suivi_tresorerie(page: Page):
    """Test E2E du suivi de trésorerie"""
    
    # Navigation
    page.goto("/comptabilite")
    
    # Vérification du graphique
    chart = page.locator("[data-testid=cashflow-chart]")
    expect(chart).to_be_visible()
    
    # Changement de période
    page.click("[data-testid=periode-select]")
    page.click("text=90 jours")
    
    # Vérification de la mise à jour
    expect(page.locator("text=Chargement...")).to_be_visible()
    expect(page.locator("[data-testid=cashflow-chart]")).to_be_visible()

def test_statistiques_financieres(page: Page):
    """Test E2E des statistiques financières"""
    
    # Navigation
    page.goto("/comptabilite")
    
    # Vérification des cartes de statistiques
    stats = [
        "Chiffre d'affaires",
        "Bénéfice",
        "Trésorerie",
        "Charges"
    ]
    for stat in stats:
        card = page.locator(f"[data-testid=stat-card-{stat.lower().replace(' ', '-')}]")
        expect(card).to_be_visible()
        expect(card.locator(".MuiChip-root")).to_be_visible()  # Variation
        expect(card.locator("button")).to_be_visible()  # Info button

def test_responsive_design(page: Page):
    """Test E2E du design responsive"""
    
    # Test sur mobile
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto("/comptabilite")
    
    # Vérification de l'adaptation du layout
    expect(page.locator("[data-testid=stats-grid]")).to_have_css("flex-direction", "column")
    expect(page.locator("[data-testid=cashflow-chart]")).to_be_visible()
    
    # Test sur tablette
    page.set_viewport_size({"width": 768, "height": 1024})
    page.reload()
    
    # Vérification de l'adaptation du layout
    expect(page.locator("[data-testid=stats-grid]")).to_have_css("grid-template-columns", "repeat(2, 1fr)")
    
    # Test sur desktop
    page.set_viewport_size({"width": 1920, "height": 1080})
    page.reload()
    
    # Vérification de l'adaptation du layout
    expect(page.locator("[data-testid=stats-grid]")).to_have_css("grid-template-columns", "repeat(4, 1fr)")
