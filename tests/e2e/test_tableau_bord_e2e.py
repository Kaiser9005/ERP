"""Tests End-to-End pour le tableau de bord."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime

def test_acces_tableau_bord(page: Page):
    """Test d'accès au tableau de bord."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Vérifier la redirection automatique
    expect(page.get_by_text("Tableau de Bord")).to_be_visible()
    
    # Vérifier les composants principaux
    expect(page.get_by_text("Vue d'ensemble")).to_be_visible()
    expect(page.get_by_text("Production")).to_be_visible()
    expect(page.get_by_text("Finances")).to_be_visible()
    expect(page.get_by_text("Stocks")).to_be_visible()
    expect(page.get_by_text("Ressources Humaines")).to_be_visible()

def test_widgets_production(page: Page):
    """Test des widgets de production."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier les widgets de production
    expect(page.get_by_text("Production en cours")).to_be_visible()
    expect(page.get_by_text("Parcelles actives")).to_be_visible()
    expect(page.get_by_text("Récoltes prévues")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("P001")).to_be_visible()
    expect(page.get_by_text("10.5 ha")).to_be_visible()
    expect(page.get_by_text("4800 kg")).to_be_visible()

def test_widgets_finance(page: Page):
    """Test des widgets financiers."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier les widgets financiers
    expect(page.get_by_text("Trésorerie")).to_be_visible()
    expect(page.get_by_text("Dépenses du mois")).to_be_visible()
    expect(page.get_by_text("Budget vs Réel")).to_be_visible()
    
    # Vérifier les graphiques
    expect(page.locator("[data-testid=tresorerie-chart]")).to_be_visible()
    expect(page.locator("[data-testid=depenses-chart]")).to_be_visible()
    expect(page.locator("[data-testid=budget-chart]")).to_be_visible()

def test_widgets_stocks(page: Page):
    """Test des widgets de stocks."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier les widgets de stocks
    expect(page.get_by_text("État des stocks")).to_be_visible()
    expect(page.get_by_text("Alertes stock")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("Engrais NPK")).to_be_visible()
    expect(page.get_by_text("1145 KG")).to_be_visible()
    expect(page.get_by_text("Stock bas")).to_be_visible()

def test_widgets_rh(page: Page):
    """Test des widgets RH."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier les widgets RH
    expect(page.get_by_text("Effectifs")).to_be_visible()
    expect(page.get_by_text("Congés en cours")).to_be_visible()
    expect(page.get_by_text("Formations")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("Total : 1")).to_be_visible()
    expect(page.get_by_text("Diallo Mamadou")).to_be_visible()
    expect(page.get_by_text("Techniques agricoles modernes")).to_be_visible()

def test_alertes_notifications(page: Page):
    """Test des alertes et notifications."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier le panneau d'alertes
    expect(page.get_by_text("Alertes")).to_be_visible()
    expect(page.get_by_text("Stock bas : Engrais NPK")).to_be_visible()
    expect(page.get_by_text("Récolte prévue dans 30 jours")).to_be_visible()
    
    # Marquer une alerte comme lue
    page.get_by_text("Stock bas : Engrais NPK").click()
    page.get_by_role("button", name="Marquer comme lu").click()
    
    # Vérifier la mise à jour
    expect(page.get_by_text("Alerte marquée comme lue")).to_be_visible()

def test_meteo_integration(page: Page):
    """Test de l'intégration météo."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Vérifier le widget météo
    expect(page.get_by_text("Météo")).to_be_visible()
    expect(page.get_by_text("Température")).to_be_visible()
    expect(page.get_by_text("Humidité")).to_be_visible()
    expect(page.get_by_text("Précipitations")).to_be_visible()
    
    # Vérifier les données des capteurs
    expect(page.locator("[data-testid=temp-sensor]")).to_be_visible()
    expect(page.locator("[data-testid=humidity-sensor]")).to_be_visible()
    expect(page.locator("[data-testid=rain-sensor]")).to_be_visible()

def test_filtres_periode(page: Page):
    """Test des filtres de période."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Changer la période
    page.get_by_label("Période").select_option("MOIS")
    page.get_by_role("button", name="Appliquer").click()
    
    # Vérifier la mise à jour des données
    expect(page.get_by_text("Chargement...")).to_be_visible()
    expect(page.get_by_text("Données du mois")).to_be_visible()
    
    # Vérifier les graphiques mis à jour
    expect(page.locator("[data-testid=tresorerie-chart]")).to_be_visible()
    expect(page.locator("[data-testid=production-chart]")).to_be_visible()

def test_export_rapport(page: Page):
    """Test d'export du rapport du tableau de bord."""
    # Navigation
    page.goto("/tableau-de-bord")
    
    # Exporter le rapport
    page.get_by_role("button", name="Exporter rapport").click()
    page.get_by_role("menuitem", name="PDF").click()
    
    # Vérifier l'export
    expect(page.get_by_text("Rapport exporté avec succès")).to_be_visible()