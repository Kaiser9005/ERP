"""Tests End-to-End pour la gestion agricole."""

import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta
import re

def test_creation_parcelle(page: Page):
    """Test de création et suivi d'une parcelle."""
    # Accéder à la page de création de parcelle
    page.goto("/production/parcelles/nouvelle")
    
    # Remplir le formulaire
    page.get_by_label("Code").fill("P001")
    page.get_by_label("Type de culture").select_option("PALMIER")
    page.get_by_label("Surface (hectares)").fill("10.5")
    page.get_by_label("Date de plantation").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la redirection et le message de succès
    expect(page.get_by_text("Parcelle créée avec succès")).to_be_visible()
    
    # Vérifier les détails de la parcelle
    expect(page.get_by_text("Code: P001")).to_be_visible()
    expect(page.get_by_text("Surface: 10.5 ha")).to_be_visible()
    expect(page.get_by_text("Type: PALMIER")).to_be_visible()

def test_creation_employe(page: Page):
    """Test de création et gestion d'un employé."""
    # Accéder à la page de création d'employé
    page.goto("/rh/employes/nouveau")
    
    # Remplir le formulaire
    page.get_by_label("Matricule").fill("EMP001")
    page.get_by_label("Nom").fill("Dupont")
    page.get_by_label("Prénom").fill("Jean")
    page.get_by_label("Date de naissance").fill("1990-01-01")
    page.get_by_label("Sexe").select_option("M")
    page.get_by_label("Département").select_option("PRODUCTION")
    page.get_by_label("Poste").fill("Ouvrier agricole")
    page.get_by_label("Date d'embauche").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Type de contrat").select_option("CDI")
    page.get_by_label("Salaire de base").fill("200000")
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la redirection et le message de succès
    expect(page.get_by_text("Employé créé avec succès")).to_be_visible()
    
    # Vérifier la fiche employé
    expect(page.get_by_text("Matricule: EMP001")).to_be_visible()
    expect(page.get_by_text("Dupont Jean")).to_be_visible()
    expect(page.get_by_text("Département: PRODUCTION")).to_be_visible()

def test_creation_tache(page: Page):
    """Test de création et suivi d'une tâche."""
    # Accéder à la page de création de tâche
    page.goto("/projets/taches/nouvelle")
    
    # Remplir le formulaire
    page.get_by_label("Titre").fill("Plantation zone A")
    page.get_by_label("Description").fill("Planter 100 palmiers")
    page.get_by_label("Catégorie").select_option("PLANTATION")
    page.get_by_label("Priorité").select_option("HAUTE")
    page.get_by_label("Date de début").fill(datetime.now().strftime("%Y-%m-%d"))
    page.get_by_label("Date de fin prévue").fill(
        (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    )
    
    # Sélectionner une parcelle
    page.get_by_label("Parcelle").select_option("P001")
    
    # Sélectionner un responsable
    page.get_by_label("Responsable").select_option("EMP001")
    
    # Ajouter des ressources
    page.get_by_role("button", name="Ajouter une ressource").click()
    page.get_by_label("Ressource").select_option("Palmiers")
    page.get_by_label("Quantité requise").fill("100")
    
    page.get_by_role("button", name="Créer").click()
    
    # Vérifier la redirection et le message de succès
    expect(page.get_by_text("Tâche créée avec succès")).to_be_visible()
    
    # Vérifier les détails de la tâche
    expect(page.get_by_text("Plantation zone A")).to_be_visible()
    expect(page.get_by_text("Statut: À FAIRE")).to_be_visible()
    expect(page.get_by_text("Responsable: Dupont Jean")).to_be_visible()

def test_workflow_tache(page: Page):
    """Test du workflow complet d'une tâche."""
    # Accéder à la liste des tâches
    page.goto("/projets/taches")
    
    # Ouvrir les détails de la tâche
    page.get_by_text("Plantation zone A").click()
    
    # Démarrer la tâche
    page.get_by_role("button", name="Démarrer").click()
    expect(page.get_by_text("Statut: EN COURS")).to_be_visible()
    
    # Mettre à jour l'avancement
    page.get_by_label("Pourcentage d'avancement").fill("50")
    page.get_by_role("button", name="Mettre à jour").click()
    expect(page.get_by_text("50%")).to_be_visible()
    
    # Ajouter un commentaire
    page.get_by_label("Commentaire").fill("Plantation en cours, 50 palmiers plantés")
    page.get_by_role("button", name="Ajouter un commentaire").click()
    expect(page.get_by_text("Plantation en cours, 50 palmiers plantés")).to_be_visible()
    
    # Terminer la tâche
    page.get_by_label("Pourcentage d'avancement").fill("100")
    page.get_by_role("button", name="Terminer").click()
    expect(page.get_by_text("Statut: TERMINÉE")).to_be_visible()

def test_tableau_bord(page: Page):
    """Test du tableau de bord."""
    # Accéder au tableau de bord
    page.goto("/dashboard")
    
    # Vérifier les sections principales
    expect(page.get_by_text("Tâches en cours")).to_be_visible()
    expect(page.get_by_text("État des parcelles")).to_be_visible()
    expect(page.get_by_text("Alertes")).to_be_visible()
    
    # Vérifier les statistiques
    expect(page.get_by_text(re.compile(r"Tâches à faire: \d+"))).to_be_visible()
    expect(page.get_by_text(re.compile(r"Tâches en cours: \d+"))).to_be_visible()
    expect(page.get_by_text(re.compile(r"Tâches terminées: \d+"))).to_be_visible()
    
    # Vérifier la présence de la tâche créée
    expect(page.get_by_text("Plantation zone A")).to_be_visible()
    
    # Vérifier la présence de la parcelle créée
    expect(page.get_by_text("P001")).to_be_visible()

def test_gestion_employes(page: Page):
    """Test de la gestion des employés."""
    # Accéder à la liste des employés
    page.goto("/rh/employes")
    
    # Vérifier la présence de l'employé créé
    expect(page.get_by_text("Dupont Jean")).to_be_visible()
    
    # Ouvrir les détails de l'employé
    page.get_by_text("Dupont Jean").click()
    
    # Vérifier les tâches assignées
    expect(page.get_by_text("Tâches assignées")).to_be_visible()
    expect(page.get_by_text("Plantation zone A")).to_be_visible()
    
    # Vérifier le planning
    expect(page.get_by_text("Planning")).to_be_visible()
    expect(page.get_by_text(re.compile(r"\d+ tâches cette semaine"))).to_be_visible()

def test_gestion_parcelles(page: Page):
    """Test de la gestion des parcelles."""
    # Accéder à la liste des parcelles
    page.goto("/production/parcelles")
    
    # Vérifier la présence de la parcelle créée
    expect(page.get_by_text("P001")).to_be_visible()
    
    # Ouvrir les détails de la parcelle
    page.get_by_text("P001").click()
    
    # Vérifier les informations
    expect(page.get_by_text("Surface: 10.5 ha")).to_be_visible()
    expect(page.get_by_text("Type: PALMIER")).to_be_visible()
    
    # Vérifier les tâches associées
    expect(page.get_by_text("Tâches")).to_be_visible()
    expect(page.get_by_text("Plantation zone A")).to_be_visible()
    
    # Vérifier les statistiques
    expect(page.get_by_text("Statistiques")).to_be_visible()
    expect(page.get_by_text(re.compile(r"Tâches terminées: \d+"))).to_be_visible()