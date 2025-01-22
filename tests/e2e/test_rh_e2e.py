"""Tests End-to-End pour la gestion des ressources humaines."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

def test_creation_employe(page: Page):
    """Test de création d'un employé."""
    # Connexion
    page.goto("/auth/connexion")
    page.get_by_label("Email").fill("admin@example.com")
    page.get_by_label("Mot de passe").fill("Admin123!")
    page.get_by_role("button", name="Se connecter").click()
    
    # Navigation vers RH
    page.get_by_role("link", name="Ressources Humaines").click()
    
    # Créer un nouvel employé
    page.get_by_role("button", name="Nouvel employé").click()
    page.get_by_label("Nom").fill("Diallo")
    page.get_by_label("Prénom").fill("Mamadou")
    page.get_by_label("Date de naissance").fill("1990-05-15")
    page.get_by_label("Email").fill("m.diallo@example.com")
    page.get_by_label("Téléphone").fill("0123456789")
    page.get_by_label("Adresse").fill("123 Rue de l'Agriculture")
    page.get_by_label("Poste").fill("Responsable Production")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Employé créé avec succès")).to_be_visible()
    expect(page.get_by_text("Diallo Mamadou")).to_be_visible()

def test_gestion_contrats(page: Page):
    """Test de la gestion des contrats."""
    # Navigation
    page.goto("/rh/employes")
    page.get_by_text("Diallo Mamadou").click()
    
    # Ajouter un contrat
    page.get_by_role("button", name="Nouveau contrat").click()
    page.get_by_label("Type de contrat").select_option("CDI")
    page.get_by_label("Date début").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Salaire mensuel").fill("450000")
    page.get_by_label("Durée période essai (mois)").fill("3")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Contrat créé avec succès")).to_be_visible()
    expect(page.get_by_text("CDI")).to_be_visible()
    expect(page.get_by_text("450000 FCFA")).to_be_visible()

def test_gestion_conges(page: Page):
    """Test de la gestion des congés."""
    # Navigation
    page.goto("/rh/conges")
    
    # Créer une demande de congé
    page.get_by_role("button", name="Nouvelle demande").click()
    page.get_by_label("Employé").select_option("Diallo Mamadou")
    page.get_by_label("Type").select_option("CONGE_ANNUEL")
    start_date = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=44)).strftime("%Y-%m-%d")
    page.get_by_label("Date début").fill(start_date)
    page.get_by_label("Date fin").fill(end_date)
    page.get_by_label("Motif").fill("Congés annuels")
    page.get_by_role("button", name="Soumettre").click()
    
    # Vérifier la soumission
    expect(page.get_by_text("Demande soumise avec succès")).to_be_visible()
    
    # Approuver la demande
    page.get_by_text("En attente").click()
    page.get_by_role("button", name="Approuver").click()
    page.get_by_label("Commentaire").fill("Demande approuvée")
    page.get_by_role("button", name="Confirmer").click()
    
    # Vérifier l'approbation
    expect(page.get_by_text("Approuvé")).to_be_visible()

def test_gestion_formations(page: Page):
    """Test de la gestion des formations."""
    # Navigation
    page.goto("/rh/formations")
    
    # Créer une formation
    page.get_by_role("button", name="Nouvelle formation").click()
    page.get_by_label("Titre").fill("Techniques agricoles modernes")
    page.get_by_label("Description").fill("Formation sur les nouvelles techniques d'agriculture")
    page.get_by_label("Date début").fill(
        (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
    )
    page.get_by_label("Durée (jours)").fill("3")
    page.get_by_label("Formateur").fill("Dr. Koné")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la création
    expect(page.get_by_text("Formation créée avec succès")).to_be_visible()
    
    # Ajouter des participants
    page.get_by_text("Techniques agricoles modernes").click()
    page.get_by_role("button", name="Ajouter participants").click()
    page.get_by_text("Diallo Mamadou").click()
    page.get_by_role("button", name="Ajouter").click()
    
    # Vérifier l'ajout
    expect(page.get_by_text("Participants ajoutés")).to_be_visible()

def test_suivi_presence(page: Page):
    """Test du suivi des présences."""
    # Navigation
    page.goto("/rh/presences")
    
    # Enregistrer une présence
    page.get_by_role("button", name="Nouvelle présence").click()
    page.get_by_label("Date").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Employé").select_option("Diallo Mamadou")
    page.get_by_label("Heure arrivée").fill("08:00")
    page.get_by_label("Heure départ").fill("17:00")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier l'enregistrement
    expect(page.get_by_text("Présence enregistrée")).to_be_visible()

def test_evaluation_performance(page: Page):
    """Test de l'évaluation des performances."""
    # Navigation
    page.goto("/rh/evaluations")
    
    # Créer une évaluation
    page.get_by_role("button", name="Nouvelle évaluation").click()
    page.get_by_label("Employé").select_option("Diallo Mamadou")
    page.get_by_label("Période").fill(datetime.now().strftime("%Y-%m"))
    page.get_by_label("Objectifs atteints").select_option("4")  # Sur 5
    page.get_by_label("Qualité travail").select_option("4")
    page.get_by_label("Ponctualité").select_option("5")
    page.get_by_label("Commentaires").fill("Excellent travail, très impliqué")
    page.get_by_role("button", name="Enregistrer").click()
    
    # Vérifier l'enregistrement
    expect(page.get_by_text("Évaluation enregistrée")).to_be_visible()
    expect(page.get_by_text("4.33/5")).to_be_visible()  # Moyenne

def test_rapport_rh(page: Page):
    """Test de génération du rapport RH."""
    # Navigation
    page.goto("/rh/rapports")
    
    # Générer le rapport
    page.get_by_role("button", name="Générer rapport").click()
    
    # Vérifier les sections
    expect(page.get_by_text("Effectifs")).to_be_visible()
    expect(page.get_by_text("Congés")).to_be_visible()
    expect(page.get_by_text("Formations")).to_be_visible()
    expect(page.get_by_text("Évaluations")).to_be_visible()
    
    # Vérifier les données
    expect(page.get_by_text("Total employés : 1")).to_be_visible()
    expect(page.get_by_text("Formations en cours : 1")).to_be_visible()
    expect(page.get_by_text("Congés approuvés : 1")).to_be_visible()