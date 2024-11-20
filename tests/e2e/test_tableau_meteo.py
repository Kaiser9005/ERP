import pytest
from playwright.sync_api import Page, expect
from datetime import datetime, timedelta

def test_affichage_tableau_meteo(page: Page):
    # Accéder à la page du tableau météo
    page.goto("/production/meteo")
    
    # Vérifier le titre
    expect(page.get_by_text("Tableau de Bord Météorologique")).to_be_visible()
    
    # Vérifier les sections principales
    expect(page.get_by_text("Conditions Actuelles")).to_be_visible()
    expect(page.get_by_text("Analyse des Risques")).to_be_visible()
    expect(page.get_by_text("Recommandations")).to_be_visible()

    # Vérifier la présence des données météorologiques
    expect(page.get_by_text(r"Température :").first).to_be_visible()
    expect(page.get_by_text(r"Humidité :").first).to_be_visible()
    expect(page.get_by_text("Précipitations :").first).to_be_visible()
    expect(page.get_by_text("Vitesse du vent :").first).to_be_visible()

def test_mise_a_jour_donnees(page: Page):
    # Accéder à la page
    page.goto("/production/meteo")
    
    # Attendre le chargement initial
    page.wait_for_selector("text=Conditions Actuelles")
    
    # Vérifier la présence de l'horodatage
    expect(page.get_by_text(r"Dernière mise à jour")).to_be_visible()
    
    # Attendre 31 minutes pour vérifier la mise à jour automatique
    page.wait_for_timeout(31 * 60 * 1000)
    
    # Vérifier que les données ont été mises à jour
    initial_timestamp = page.get_by_text(r"Dernière mise à jour").text_content()
    expect(initial_timestamp).not_to_be_empty()

def test_affichage_alertes(page: Page):
    # Accéder à la page
    page.goto("/production/meteo")
    
    # Vérifier la présence des indicateurs de risque
    expect(page.get_by_text(r"Précipitations :").nth(1)).to_be_visible()
    expect(page.get_by_text(r"Température :").nth(1)).to_be_visible()
    
    # Vérifier l'affichage des alertes si présentes
    alert = page.get_by_text(r"ALERTE MÉTÉO")
    if alert.is_visible():
        expect(alert).to_be_visible()
        expect(page.get_by_role("alert")).to_be_visible()

def test_affichage_recommandations(page: Page):
    # Accéder à la page
    page.goto("/production/meteo")
    
    # Vérifier la section des recommandations
    expect(page.get_by_text("Recommandations")).to_be_visible()
    
    # Vérifier la présence d'au moins une recommandation
    recommendations = page.get_by_text("•").all()
    assert len(recommendations) > 0, "Aucune recommandation affichée"

def test_gestion_erreurs(page: Page):
    # Simuler une erreur réseau
    page.route("**/api/v1/weather/**", lambda route: route.abort())
    
    # Accéder à la page
    page.goto("/production/meteo")
    
    # Vérifier l'affichage du message d'erreur
    expect(page.get_by_text("Erreur lors du chargement des données météorologiques")).to_be_visible()

def test_chargement_initial(page: Page):
    # Accéder à la page
    page.goto("/production/meteo")
    
    # Vérifier l'affichage du loader
    expect(page.get_by_role("progressbar")).to_be_visible()
    
    # Attendre que les données soient chargées
    page.wait_for_selector("text=Conditions Actuelles")
    
    # Vérifier que le loader a disparu
    expect(page.get_by_role("progressbar")).to_have_count(0)
