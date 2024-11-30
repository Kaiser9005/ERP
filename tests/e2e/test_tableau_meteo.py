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

def test_tableau_meteo_parcellaire(page: Page):
    """Test l'affichage et les fonctionnalités du tableau météo parcellaire."""
    # Accéder à la page
    page.goto("/production/meteo/parcelles")
    
    # Vérifier le titre
    expect(page.get_by_text("Tableau Météo Parcellaire")).to_be_visible()
    
    # Vérifier la présence du tableau
    expect(page.get_by_role("table")).to_be_visible()
    
    # Vérifier les colonnes du tableau
    expect(page.get_by_text("Parcelle")).to_be_visible()
    expect(page.get_by_text("Température")).to_be_visible()
    expect(page.get_by_text("Humidité")).to_be_visible()
    expect(page.get_by_text("Précipitations")).to_be_visible()
    expect(page.get_by_text("Vent")).to_be_visible()
    expect(page.get_by_text("Alertes")).to_be_visible()
    
    # Vérifier la présence de données pour au moins une parcelle
    expect(page.get_by_role("row").nth(1)).to_be_visible()
    
    # Vérifier le fonctionnement des filtres
    expect(page.get_by_label("Filtrer par culture")).to_be_visible()
    expect(page.get_by_label("Filtrer par état")).to_be_visible()

def test_details_meteo_tache(page: Page):
    """Test l'affichage des détails météo pour une tâche."""
    # Accéder à la page des tâches
    page.goto("/projets/taches")
    
    # Ouvrir les détails d'une tâche
    page.get_by_role("button", name="Voir les détails").first.click()
    
    # Vérifier la section météo
    expect(page.get_by_text("Conditions Météorologiques")).to_be_visible()
    
    # Vérifier les informations météo
    expect(page.get_by_text("Compatibilité Météo")).to_be_visible()
    expect(page.get_by_text("Prévisions")).to_be_visible()
    
    # Vérifier les indicateurs de compatibilité
    compatibility = page.get_by_role("status").first
    expect(compatibility).to_be_visible()
    expect(compatibility).to_have_attribute("aria-label", re.compile(r"Compatibilité"))
    
    # Vérifier les recommandations
    expect(page.get_by_text("Recommandations")).to_be_visible()
    recommendations = page.get_by_role("list").filter(has_text="Recommandations").locator("li")
    expect(recommendations).to_have_count(greater_than=0)

def test_filtrage_tableau_parcellaire(page: Page):
    """Test le filtrage des données dans le tableau météo parcellaire."""
    # Accéder à la page
    page.goto("/production/meteo/parcelles")
    
    # Sélectionner une culture spécifique
    page.get_by_label("Filtrer par culture").select_option("Palmier")
    
    # Vérifier que le tableau est filtré
    rows = page.get_by_role("row").all()
    for row in rows[1:]:  # Skip header row
        expect(row.get_by_text("Palmier")).to_be_visible()
    
    # Sélectionner un état
    page.get_by_label("Filtrer par état").select_option("En alerte")
    
    # Vérifier que seules les parcelles en alerte sont affichées
    alerts = page.get_by_role("alert").all()
    assert len(alerts) == len(rows) - 1  # -1 pour la ligne d'en-tête

def test_mise_a_jour_meteo_tache(page: Page):
    """Test la mise à jour des informations météo pour une tâche."""
    # Accéder aux détails d'une tâche
    page.goto("/projets/taches/1")
    
    # Vérifier la présence de l'horodatage
    expect(page.get_by_text(r"Dernière mise à jour")).to_be_visible()
    
    # Attendre la mise à jour automatique
    page.wait_for_timeout(31 * 60 * 1000)
    
    # Vérifier que les données ont été mises à jour
    initial_timestamp = page.get_by_text(r"Dernière mise à jour").text_content()
    expect(initial_timestamp).not_to_be_empty()
    
    # Vérifier que les prévisions sont à jour
    expect(page.get_by_text("Prévisions")).to_be_visible()
    forecast_items = page.get_by_role("list").filter(has_text="Prévisions").locator("li")
    expect(forecast_items).to_have_count(greater_than=0)

def test_alertes_meteo_parcellaire(page: Page):
    """Test le système d'alertes dans le tableau météo parcellaire."""
    # Accéder à la page
    page.goto("/production/meteo/parcelles")
    
    # Vérifier la présence d'alertes
    alerts = page.get_by_role("alert").all()
    if len(alerts) > 0:
        # Vérifier le contenu d'une alerte
        expect(alerts[0]).to_contain_text(re.compile(r"(Température|Précipitations|Vent)"))
        
        # Vérifier la couleur de l'alerte
        expect(alerts[0]).to_have_css("background-color", re.compile(r"rgb\(.*,.*,.*\)"))
        
        # Vérifier l'icône d'alerte
        expect(alerts[0].get_by_role("img")).to_be_visible()
