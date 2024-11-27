import pytest
from datetime import datetime, timedelta
from playwright.sync_api import expect, Page

def test_formation_crud_workflow(page: Page, auth_headers):
    """Test le workflow complet de création, modification et suppression d'une formation"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    expect(page.get_by_text("Gestion des Formations")).to_be_visible()

    # Créer une nouvelle formation
    page.get_by_text("Nouvelle Formation").click()
    
    # Remplir le formulaire
    page.get_by_label("Titre").fill("Formation E2E Test")
    page.get_by_label("Description").fill("Description test e2e")
    page.get_by_label("Type").select_option("technique")
    page.get_by_label("Durée (heures)").fill("8")
    page.get_by_text("Créer").click()

    # Vérifier que la formation a été créée
    expect(page.get_by_text("Formation E2E Test")).to_be_visible()

    # Modifier la formation
    page.get_by_role("button", name="Modifier").first.click()
    page.get_by_label("Titre").fill("Formation E2E Test Modifiée")
    page.get_by_text("Modifier").click()

    # Vérifier la modification
    expect(page.get_by_text("Formation E2E Test Modifiée")).to_be_visible()

def test_session_management(page: Page, auth_headers):
    """Test la gestion des sessions de formation"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    
    # Sélectionner une formation
    page.get_by_text("Formation E2E Test Modifiée").click()
    
    # Créer une nouvelle session
    page.get_by_text("Nouvelle Session").click()
    
    # Remplir le formulaire de session
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    page.get_by_label("Date de début").fill(f"{tomorrow}T09:00")
    page.get_by_label("Date de fin").fill(f"{tomorrow}T17:00")
    page.get_by_label("Lieu").fill("Salle E2E Test")
    page.get_by_label("Formateur").fill("Formateur E2E")
    page.get_by_label("Nombre de places").fill("10")
    page.get_by_text("Créer").click()

    # Vérifier que la session a été créée
    expect(page.get_by_text("Salle E2E Test")).to_be_visible()

def test_participation_workflow(page: Page, auth_headers):
    """Test le workflow d'inscription et de participation à une formation"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    
    # Sélectionner une formation
    page.get_by_text("Formation E2E Test Modifiée").click()
    
    # Sélectionner une session
    page.get_by_text("Salle E2E Test").click()
    
    # Ajouter un participant
    page.get_by_text("Ajouter Participant").click()
    page.get_by_role("combobox", name="Employé").click()
    page.get_by_text("Jean Test").click()
    page.get_by_text("Inscrire").click()

    # Vérifier l'inscription
    expect(page.get_by_text("Jean Test")).to_be_visible()
    
    # Marquer la présence
    page.get_by_role("button", name="Présent").click()
    
    # Ajouter une note
    page.get_by_role("button", name="Noter").click()
    page.get_by_label("Note").fill("85")
    page.get_by_text("Valider").click()

    # Vérifier la note
    expect(page.get_by_text("85/100")).to_be_visible()

def test_evaluation_workflow(page: Page, auth_headers):
    """Test le workflow d'évaluation"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    
    # Accéder aux évaluations
    page.get_by_text("Évaluations").click()
    
    # Créer une nouvelle évaluation
    page.get_by_text("Nouvelle Évaluation").click()
    
    # Remplir le formulaire d'évaluation
    page.get_by_role("combobox", name="Employé").click()
    page.get_by_text("Jean Test").click()
    page.get_by_label("Type").select_option("formation")
    page.get_by_label("Date d'évaluation").fill(datetime.now().strftime("%Y-%m-%dT%H:%M"))
    
    # Remplir les compétences
    page.get_by_label("Compétences techniques").fill("4")
    page.get_by_label("Points forts").fill("Très bonne participation")
    page.get_by_label("Points à améliorer").fill("Communication à renforcer")
    page.get_by_label("Note globale").fill("85")
    
    page.get_by_text("Créer").click()

    # Vérifier la création
    expect(page.get_by_text("Jean Test")).to_be_visible()
    expect(page.get_by_text("85/100")).to_be_visible()

def test_statistics_display(page: Page, auth_headers):
    """Test l'affichage des statistiques"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    
    # Vérifier les statistiques globales
    expect(page.get_by_text("Statistiques des Formations")).to_be_visible()
    
    # Sélectionner une formation
    page.get_by_text("Formation E2E Test Modifiée").click()
    
    # Vérifier les statistiques de la formation
    expect(page.get_by_text("Taux de réussite")).to_be_visible()
    expect(page.get_by_text("Note moyenne")).to_be_visible()
    
    # Vérifier les statistiques par employé
    page.get_by_text("Statistiques par employé").click()
    expect(page.get_by_text("Jean Test")).to_be_visible()
    expect(page.get_by_text("85/100")).to_be_visible()

def test_cleanup(page: Page, auth_headers):
    """Nettoyer les données de test"""
    
    # Accéder à la page des formations
    page.goto("/hr/formations")
    
    # Supprimer la formation de test
    page.get_by_text("Formation E2E Test Modifiée").click()
    page.get_by_role("button", name="Supprimer").click()
    page.get_by_role("button", name="Confirmer").click()

    # Vérifier la suppression
    expect(page.get_by_text("Formation E2E Test Modifiée")).not_to_be_visible()
