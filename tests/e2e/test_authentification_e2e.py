"""Tests End-to-End pour l'authentification."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime

def test_creation_premier_admin(page: Page):
    """Test de la création du premier administrateur."""
    # Accéder à la page de création du premier admin
    page.goto("/auth/premier-admin")
    
    # Vérifier les éléments du formulaire
    expect(page.get_by_label("Nom d'utilisateur")).to_be_visible()
    expect(page.get_by_label("Email")).to_be_visible()
    expect(page.get_by_label("Mot de passe")).to_be_visible()
    expect(page.get_by_label("Nom")).to_be_visible()
    expect(page.get_by_label("Prénom")).to_be_visible()
    
    # Remplir le formulaire
    page.get_by_label("Nom d'utilisateur").fill("admin")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_label("Nom").fill("Admin")
    page.get_by_label("Prénom").fill("Super")
    
    # Soumettre le formulaire
    page.get_by_role("button", name="Créer l'administrateur").click()
    
    # Vérifier la redirection et le message de succès
    expect(page.get_by_text("Administrateur créé avec succès")).to_be_visible()
    expect(page.get_by_text("Vous pouvez maintenant vous connecter")).to_be_visible()

def test_connexion_admin(page: Page):
    """Test de connexion en tant qu'administrateur."""
    # Accéder à la page de connexion
    page.goto("/auth/connexion")
    
    # Vérifier les éléments du formulaire
    expect(page.get_by_label("Email")).to_be_visible()
    expect(page.get_by_label("Mot de passe")).to_be_visible()
    expect(page.get_by_role("button", name="Se connecter")).to_be_visible()
    
    # Remplir le formulaire
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    
    # Se connecter
    page.get_by_role("button", name="Se connecter").click()
    
    # Vérifier la redirection vers le tableau de bord
    expect(page.get_by_text("Tableau de Bord")).to_be_visible()
    expect(page.get_by_text("Super Admin")).to_be_visible()

def test_gestion_utilisateurs(page: Page):
    """Test de la gestion des utilisateurs."""
    # Connexion en tant qu'admin
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Accéder à la gestion des utilisateurs
    page.get_by_role("link", name="Administration").click()
    page.get_by_role("link", name="Utilisateurs").click()
    
    # Créer un nouvel utilisateur
    page.get_by_role("button", name="Ajouter un utilisateur").click()
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Nom").fill("User")
    page.get_by_label("Prénom").fill("Test")
    page.get_by_label("Mot de passe").fill("User123!")
    page.get_by_label("Rôle").select_option("OPERATEUR")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Utilisateur créé avec succès")).to_be_visible()
    expect(page.get_by_text("user@example.com")).to_be_visible()

def test_connexion_utilisateur(page: Page):
    """Test de connexion en tant qu'utilisateur normal."""
    # Accéder à la page de connexion
    page.goto("/auth/connexion")
    
    # Se connecter en tant qu'utilisateur
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_label("Mot de passe").fill("User123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Vérifier l'accès limité
    expect(page.get_by_text("Tableau de Bord")).to_be_visible()
    expect(page.get_by_text("Test User")).to_be_visible()
    expect(page.get_by_role("link", name="Administration")).not_to_be_visible()

def test_deconnexion(page: Page):
    """Test de déconnexion."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Déconnexion
    page.get_by_role("button", name="Menu utilisateur").click()
    page.get_by_role("menuitem", name="Déconnexion").click()
    
    # Vérifier la redirection
    expect(page.get_by_role("button", name="Se connecter")).to_be_visible()
    
    # Vérifier que l'accès est restreint
    page.goto("/tableau-de-bord")
    expect(page.get_by_text("Connexion requise")).to_be_visible()

def test_mot_de_passe_oublie(page: Page):
    """Test du processus de réinitialisation du mot de passe."""
    # Accéder à la page de connexion
    page.goto("/auth/connexion")
    
    # Cliquer sur "Mot de passe oublié"
    page.get_by_role("link", name="Mot de passe oublié ?").click()
    
    # Remplir le formulaire
    page.get_by_label("Email").fill("user@example.com")
    page.get_by_role("button", name="Réinitialiser le mot de passe").click()
    
    # Vérifier le message de confirmation
    expect(page.get_by_text("Email de réinitialisation envoyé")).to_be_visible()

def test_validation_formulaire(page: Page):
    """Test de la validation des formulaires."""
    # Accéder à la page de connexion
    page.goto("/auth/connexion")
    
    # Tester la validation du format email
    page.get_by_label("Email").fill("invalid-email")
    page.get_by_label("Mot de passe").click()  # Déclencher la validation
    expect(page.get_by_text("Format d'email invalide")).to_be_visible()
    
    # Tester la validation du mot de passe
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("123")  # Trop court
    page.get_by_role("button", name="Se connecter").click()
    expect(page.get_by_text("Le mot de passe doit contenir au moins 8 caractères")).to_be_visible()

def test_tentatives_connexion(page: Page):
    """Test de la limitation des tentatives de connexion."""
    # Accéder à la page de connexion
    page.goto("/auth/connexion")
    
    # Faire plusieurs tentatives avec un mauvais mot de passe
    for _ in range(5):
        page.get_by_label("Email").fill("admin@example.com")
        page.get_by_label("Mot de passe").fill("WrongPass123!")
        page.get_by_role("button", name="Se connecter").click()
        expect(page.get_by_text("Email ou mot de passe incorrect")).to_be_visible()
    
    # Vérifier le blocage temporaire
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("WrongPass123!")
    page.get_by_role("button", name="Se connecter").click()
    expect(page.get_by_text("Compte temporairement bloqué")).to_be_visible()