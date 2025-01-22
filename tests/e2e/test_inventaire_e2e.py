"""Tests End-to-End pour la gestion des stocks."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

def test_creation_produit(page: Page):
    """Test de création d'un produit dans l'inventaire."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Navigation vers l'inventaire
    page.get_by_role("link", name="Inventaire").click()
    
    # Créer un nouveau produit
    page.get_by_role("button", name="Nouveau produit").click()
    page.get_by_label("Nom").fill("Engrais NPK")
    page.get_by_label("Description").fill("Engrais complet pour cultures")
    page.get_by_label("Unité de mesure").select_option("KG")
    page.get_by_label("Prix unitaire").fill("1500")
    page.get_by_label("Stock initial").fill("1000")
    page.get_by_label("Stock minimum").fill("100")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Produit créé avec succès")).to_be_visible()
    expect(page.get_by_text("Engrais NPK")).to_be_visible()
    expect(page.get_by_text("1000 KG")).to_be_visible()

def test_mouvement_stock(page: Page):
    """Test des mouvements de stock."""
    # Navigation
    page.goto("/inventaire/mouvements")
    
    # Enregistrer une sortie
    page.get_by_role("button", name="Nouveau mouvement").click()
    page.get_by_label("Type").select_option("SORTIE")
    page.get_by_label("Produit").select_option("Engrais NPK")
    page.get_by_label("Quantité").fill("200")
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Motif").fill("Utilisation parcelle A")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier le mouvement
    expect(page.get_by_text("Mouvement enregistré")).to_be_visible()
    
    # Vérifier la mise à jour du stock
    page.goto("/inventaire")
    expect(page.get_by_text("800 KG")).to_be_visible()

def test_alerte_stock(page: Page):
    """Test des alertes de stock."""
    # Navigation
    page.goto("/inventaire/mouvements")
    
    # Créer une sortie importante
    page.get_by_role("button", name="Nouveau mouvement").click()
    page.get_by_label("Type").select_option("SORTIE")
    page.get_by_label("Produit").select_option("Engrais NPK")
    page.get_by_label("Quantité").fill("650")
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Motif").fill("Utilisation massive")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier l'alerte de stock bas
    expect(page.get_by_text("Stock bas")).to_be_visible()
    expect(page.get_by_text("Le stock d'Engrais NPK est bas (150 KG)")).to_be_visible()

def test_rapport_inventaire(page: Page):
    """Test de génération du rapport d'inventaire."""
    # Navigation
    page.goto("/inventaire/rapports")
    
    # Générer le rapport
    page.get_by_role("button", name="Générer le rapport").click()
    
    # Vérifier les sections
    expect(page.get_by_text("État des Stocks")).to_be_visible()
    expect(page.get_by_text("Mouvements Récents")).to_be_visible()
    expect(page.get_by_text("Alertes")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("Engrais NPK")).to_be_visible()
    expect(page.get_by_text("150 KG")).to_be_visible()
    expect(page.get_by_text("Stock bas")).to_be_visible()

def test_inventaire_physique(page: Page):
    """Test de l'inventaire physique."""
    # Navigation
    page.goto("/inventaire/physique")
    
    # Démarrer l'inventaire
    page.get_by_role("button", name="Nouvel inventaire").click()
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_role("button", name="Démarrer").click()
    
    # Saisir les quantités
    page.get_by_label("Quantité réelle").fill("145")
    page.get_by_label("Notes").fill("Légère perte constatée")
    page.get_by_role("button", name="Valider").click()
    
    # Vérifier l'ajustement
    expect(page.get_by_text("Inventaire validé")).to_be_visible()
    expect(page.get_by_text("Écart : -5 KG")).to_be_visible()

def test_gestion_fournisseurs(page: Page):
    """Test de la gestion des fournisseurs."""
    # Navigation
    page.goto("/inventaire/fournisseurs")
    
    # Créer un fournisseur
    page.get_by_role("button", name="Nouveau fournisseur").click()
    page.get_by_label("Nom").fill("AgriSupply SARL")
    page.get_by_label("Contact").fill("M. Dupont")
    page.get_by_label("Téléphone").fill("0123456789")
    page.get_by_label("Email").fill("contact@agrisupply.com")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Fournisseur créé avec succès")).to_be_visible()
    expect(page.get_by_text("AgriSupply SARL")).to_be_visible()

def test_commande_reapprovisionnement(page: Page):
    """Test de création d'une commande de réapprovisionnement."""
    # Navigation
    page.goto("/inventaire/commandes")
    
    # Créer une commande
    page.get_by_role("button", name="Nouvelle commande").click()
    page.get_by_label("Fournisseur").select_option("AgriSupply SARL")
    page.get_by_label("Produit").select_option("Engrais NPK")
    page.get_by_label("Quantité").fill("1000")
    page.get_by_label("Prix unitaire").fill("1450")
    page.get_by_label("Date livraison prévue").fill(
        (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    )
    page.get_by_role("button", name="Commander").click()
    
    # Vérifier la création
    expect(page.get_by_text("Commande créée avec succès")).to_be_visible()
    expect(page.get_by_text("En attente")).to_be_visible()

def test_reception_commande(page: Page):
    """Test de réception d'une commande."""
    # Navigation
    page.goto("/inventaire/commandes")
    
    # Sélectionner la commande
    page.get_by_text("En attente").click()
    
    # Réceptionner la commande
    page.get_by_role("button", name="Réceptionner").click()
    page.get_by_label("Quantité reçue").fill("1000")
    page.get_by_label("Date réception").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Numéro lot").fill("LOT-2025-001")
    page.get_by_role("button", name="Valider").click()
    
    # Vérifier la réception
    expect(page.get_by_text("Commande réceptionnée")).to_be_visible()
    expect(page.get_by_text("1145 KG")).to_be_visible()  # Stock mis à jour