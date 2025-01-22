"""Tests End-to-End pour la gestion de la production agricole."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

def test_creation_parcelle(page: Page):
    """Test de création d'une parcelle."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Navigation vers la production
    page.get_by_role("link", name="Production").click()
    
    # Créer une nouvelle parcelle
    page.get_by_role("button", name="Nouvelle parcelle").click()
    page.get_by_label("Code").fill("P001")
    page.get_by_label("Surface (hectares)").fill("10.5")
    page.get_by_label("Type de culture").select_option("PALMIER")
    page.get_by_label("Date de plantation").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Localisation").fill("Zone Nord")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Parcelle créée avec succès")).to_be_visible()
    expect(page.get_by_text("P001")).to_be_visible()
    expect(page.get_by_text("10.5 ha")).to_be_visible()

def test_suivi_culture(page: Page):
    """Test du suivi d'une culture."""
    # Navigation
    page.goto("/production/parcelles/P001")
    
    # Enregistrer une observation
    page.get_by_role("button", name="Nouvelle observation").click()
    page.get_by_label("Type").select_option("CROISSANCE")
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Notes").fill("Croissance normale, quelques signes de stress hydrique")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier l'enregistrement
    expect(page.get_by_text("Observation enregistrée")).to_be_visible()
    expect(page.get_by_text("Croissance normale")).to_be_visible()

def test_planification_recolte(page: Page):
    """Test de la planification d'une récolte."""
    # Navigation
    page.goto("/production/recoltes")
    
    # Planifier une récolte
    page.get_by_role("button", name="Planifier récolte").click()
    page.get_by_label("Parcelle").select_option("P001")
    page.get_by_label("Date prévue").fill(
        (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    )
    page.get_by_label("Production estimée (kg)").fill("5000")
    page.get_by_label("Notes").fill("Première récolte de la saison")
    page.get_by_role("button", name="Planifier").click()
    
    # Vérifier la planification
    expect(page.get_by_text("Récolte planifiée")).to_be_visible()
    expect(page.get_by_text("5000 kg")).to_be_visible()

def test_enregistrement_recolte(page: Page):
    """Test de l'enregistrement d'une récolte."""
    # Navigation
    page.goto("/production/recoltes")
    
    # Sélectionner la récolte planifiée
    page.get_by_text("P001").click()
    
    # Enregistrer la récolte
    page.get_by_role("button", name="Enregistrer récolte").click()
    page.get_by_label("Production réelle (kg)").fill("4800")
    page.get_by_label("Date récolte").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Qualité").select_option("A")
    page.get_by_label("Notes").fill("Récolte légèrement inférieure aux prévisions")
    page.get_by_role("button", name="Valider").click()
    
    # Vérifier l'enregistrement
    expect(page.get_by_text("Récolte enregistrée")).to_be_visible()
    expect(page.get_by_text("4800 kg")).to_be_visible()

def test_suivi_meteo(page: Page):
    """Test du suivi météorologique."""
    # Navigation
    page.goto("/production/meteo")
    
    # Vérifier les composants
    expect(page.get_by_text("Conditions Actuelles")).to_be_visible()
    expect(page.get_by_text("Prévisions")).to_be_visible()
    expect(page.get_by_text("Alertes")).to_be_visible()
    
    # Vérifier les données météo
    expect(page.get_by_text(r"Température :")).to_be_visible()
    expect(page.get_by_text(r"Humidité :")).to_be_visible()
    expect(page.get_by_text("Précipitations :")).to_be_visible()

def test_rapport_production(page: Page):
    """Test de génération du rapport de production."""
    # Navigation
    page.goto("/production/rapports")
    
    # Générer le rapport
    page.get_by_role("button", name="Générer rapport").click()
    
    # Vérifier les sections
    expect(page.get_by_text("Production par Parcelle")).to_be_visible()
    expect(page.get_by_text("Rendements")).to_be_visible()
    expect(page.get_by_text("Historique des Récoltes")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("P001")).to_be_visible()
    expect(page.get_by_text("4800 kg")).to_be_visible()

def test_gestion_traitements(page: Page):
    """Test de la gestion des traitements."""
    # Navigation
    page.goto("/production/parcelles/P001")
    
    # Enregistrer un traitement
    page.get_by_role("button", name="Nouveau traitement").click()
    page.get_by_label("Type").select_option("FERTILISATION")
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Produit").select_option("Engrais NPK")
    page.get_by_label("Quantité").fill("100")
    page.get_by_label("Notes").fill("Fertilisation de routine")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier l'enregistrement
    expect(page.get_by_text("Traitement enregistré")).to_be_visible()
    expect(page.get_by_text("Fertilisation de routine")).to_be_visible()

def test_analyse_rendements(page: Page):
    """Test de l'analyse des rendements."""
    # Navigation
    page.goto("/production/analyses")
    
    # Sélectionner la période
    page.get_by_label("Période").select_option("ANNEE_COURANTE")
    page.get_by_role("button", name="Analyser").click()
    
    # Vérifier les composants
    expect(page.get_by_text("Rendement Moyen")).to_be_visible()
    expect(page.get_by_text("Comparaison par Parcelle")).to_be_visible()
    expect(page.get_by_text("Tendances")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("457.14 kg/ha")).to_be_visible()  # 4800 kg / 10.5 ha