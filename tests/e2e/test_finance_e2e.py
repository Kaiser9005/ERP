"""Tests End-to-End pour la gestion financière."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

def test_creation_transaction(page: Page):
    """Test de création d'une transaction financière."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Navigation vers la section finance
    page.get_by_role("link", name="Finance").click()
    
    # Créer une nouvelle transaction
    page.get_by_role("button", name="Nouvelle transaction").click()
    page.get_by_label("Type").select_option("DEPENSE")
    page.get_by_label("Montant").fill("1500")
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Catégorie").select_option("MATERIEL")
    page.get_by_label("Description").fill("Achat de matériel agricole")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Transaction créée avec succès")).to_be_visible()
    expect(page.get_by_text("1500")).to_be_visible()
    expect(page.get_by_text("Achat de matériel agricole")).to_be_visible()

def test_filtrage_transactions(page: Page):
    """Test du filtrage des transactions."""
    # Navigation
    page.goto("/finance/transactions")
    
    # Filtrer par catégorie
    page.get_by_label("Catégorie").select_option("MATERIEL")
    page.get_by_role("button", name="Filtrer").click()
    
    # Vérifier le filtre
    expect(page.get_by_text("Achat de matériel agricole")).to_be_visible()
    
    # Filtrer par date
    today = datetime.now().strftime("%Y-%m-%d")
    page.get_by_label("Date début").fill(today)
    page.get_by_label("Date fin").fill(today)
    page.get_by_role("button", name="Filtrer").click()
    
    # Vérifier le filtre
    expect(page.get_by_text("1500")).to_be_visible()

def test_analyse_budget(page: Page):
    """Test de l'analyse budgétaire."""
    # Navigation
    page.goto("/finance/budget")
    
    # Vérifier les composants
    expect(page.get_by_text("Analyse Budgétaire")).to_be_visible()
    expect(page.get_by_text("Dépenses par Catégorie")).to_be_visible()
    expect(page.get_by_text("Budget vs Réel")).to_be_visible()
    
    # Vérifier le graphique
    expect(page.locator("[data-testid=budget-chart]")).to_be_visible()
    
    # Vérifier les alertes
    if page.get_by_text("Dépassement de budget").is_visible():
        expect(page.get_by_text("Dépassement de budget")).to_be_visible()
        expect(page.get_by_text("Catégorie : MATERIEL")).to_be_visible()

def test_rapport_financier(page: Page):
    """Test de génération du rapport financier."""
    # Navigation
    page.goto("/finance/rapports")
    
    # Sélectionner la période
    page.get_by_label("Période").select_option("MOIS_COURANT")
    
    # Générer le rapport
    page.get_by_role("button", name="Générer le rapport").click()
    
    # Vérifier les sections du rapport
    expect(page.get_by_text("Résumé des Transactions")).to_be_visible()
    expect(page.get_by_text("Analyse des Dépenses")).to_be_visible()
    expect(page.get_by_text("Tendances")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("Total des dépenses :")).to_be_visible()
    expect(page.get_by_text("1500")).to_be_visible()

def test_tableau_bord_finance(page: Page):
    """Test du tableau de bord financier."""
    # Navigation
    page.goto("/finance/tableau-de-bord")
    
    # Vérifier les widgets
    expect(page.get_by_text("Solde Actuel")).to_be_visible()
    expect(page.get_by_text("Dépenses du Mois")).to_be_visible()
    expect(page.get_by_text("Revenus du Mois")).to_be_visible()
    
    # Vérifier les graphiques
    expect(page.locator("[data-testid=evolution-tresorerie]")).to_be_visible()
    expect(page.locator("[data-testid=repartition-depenses]")).to_be_visible()
    
    # Vérifier les alertes
    alerts = page.locator("[data-testid=alerte-financiere]")
    if alerts.count() > 0:
        expect(alerts.first).to_be_visible()

def test_export_donnees(page: Page):
    """Test d'export des données financières."""
    # Navigation
    page.goto("/finance/transactions")
    
    # Exporter en CSV
    page.get_by_role("button", name="Exporter").click()
    page.get_by_role("menuitem", name="CSV").click()
    
    # Vérifier le message de confirmation
    expect(page.get_by_text("Export réussi")).to_be_visible()
    
    # Exporter en PDF
    page.get_by_role("button", name="Exporter").click()
    page.get_by_role("menuitem", name="PDF").click()
    
    # Vérifier le message de confirmation
    expect(page.get_by_text("Export réussi")).to_be_visible()

def test_gestion_categories(page: Page):
    """Test de la gestion des catégories financières."""
    # Navigation
    page.goto("/finance/parametres")
    
    # Créer une nouvelle catégorie
    page.get_by_role("button", name="Nouvelle catégorie").click()
    page.get_by_label("Nom").fill("CARBURANT")
    page.get_by_label("Type").select_option("DEPENSE")
    page.get_by_label("Budget mensuel").fill("500")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Catégorie créée avec succès")).to_be_visible()
    expect(page.get_by_text("CARBURANT")).to_be_visible()
    
    # Modifier la catégorie
    page.get_by_text("CARBURANT").click()
    page.get_by_label("Budget mensuel").fill("600")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier la modification
    expect(page.get_by_text("Catégorie mise à jour")).to_be_visible()
    expect(page.get_by_text("600")).to_be_visible()

def test_validation_saisie(page: Page):
    """Test de la validation des saisies financières."""
    # Navigation
    page.goto("/finance/transactions")
    page.get_by_role("button", name="Nouvelle transaction").click()
    
    # Test validation montant négatif
    page.get_by_label("Montant").fill("-100")
    expect(page.get_by_text("Le montant doit être positif")).to_be_visible()
    
    # Test validation date future
    future_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    page.get_by_label("Date").fill(future_date)
    expect(page.get_by_text("La date ne peut pas être dans le futur")).to_be_visible()
    
    # Test validation description vide
    page.get_by_label("Description").fill("")
    page.get_by_role("button", name="Enregistrer").click()
    expect(page.get_by_text("La description est requise")).to_be_visible()