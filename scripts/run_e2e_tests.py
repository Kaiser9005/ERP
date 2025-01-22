#!/usr/bin/env python3
"""Script pour exécuter tous les tests e2e."""

import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_tests(headless: bool = True, slow_mo: int = None):
    """Exécute tous les tests e2e."""
    # Configuration
    test_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests/e2e")
    report_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports/e2e")
    os.makedirs(report_dir, exist_ok=True)
    
    # Timestamp pour le rapport
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = os.path.join(report_dir, f"e2e_report_{timestamp}.html")
    
    # Construction de la commande pytest
    cmd = [
        "pytest",
        test_dir,
        "-v",
        "--html=" + report_file,
        "--self-contained-html",
        "--capture=tee-sys"
    ]
    
    # Options Playwright
    playwright_opts = []
    if headless:
        playwright_opts.append("--headless")
    if slow_mo is not None:
        playwright_opts.append(f"--slow-mo={slow_mo}")
    
    if playwright_opts:
        cmd.extend(["--browser-args", " ".join(playwright_opts)])
    
    # Exécution des tests
    print("\n=== Démarrage des tests e2e ===\n")
    print(f"Rapport sera généré dans : {report_file}\n")
    
    try:
        # Tests d'authentification
        print("\n--- Tests d'authentification ---")
        subprocess.run([*cmd, "test_authentification_e2e.py"], check=True)
        
        # Tests financiers
        print("\n--- Tests financiers ---")
        subprocess.run([*cmd, "test_finance_e2e.py"], check=True)
        
        # Tests d'inventaire
        print("\n--- Tests d'inventaire ---")
        subprocess.run([*cmd, "test_inventaire_e2e.py"], check=True)
        
        # Tests de production
        print("\n--- Tests de production ---")
        subprocess.run([*cmd, "test_production_e2e.py"], check=True)
        
        # Tests RH
        print("\n--- Tests RH ---")
        subprocess.run([*cmd, "test_rh_e2e.py"], check=True)
        
        # Tests du tableau de bord
        print("\n--- Tests du tableau de bord ---")
        subprocess.run([*cmd, "test_tableau_bord_e2e.py"], check=True)
        
        print(f"\n=== Tests terminés avec succès ===")
        print(f"Rapport disponible : {report_file}")
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n!!! Échec des tests !!!")
        print(f"Erreur : {str(e)}")
        print(f"Rapport d'erreur disponible : {report_file}")
        return 1

def main():
    """Point d'entrée principal."""
    parser = argparse.ArgumentParser(description="Exécute les tests e2e")
    parser.add_argument(
        "--no-headless",
        action="store_true",
        help="Exécute les tests avec le navigateur visible"
    )
    parser.add_argument(
        "--slow-mo",
        type=int,
        help="Délai en ms entre les actions (pour debug)"
    )
    
    args = parser.parse_args()
    
    # Vérification de l'environnement
    if not os.environ.get("OPENWEATHER_API_KEY"):
        print("ATTENTION: OPENWEATHER_API_KEY non définie")
        print("Les tests météo pourraient échouer")
    
    if not os.environ.get("IOT_API_KEY"):
        print("ATTENTION: IOT_API_KEY non définie")
        print("Les tests IoT pourraient échouer")
    
    # Exécution des tests
    sys.exit(run_tests(
        headless=not args.no_headless,
        slow_mo=args.slow_mo
    ))

if __name__ == "__main__":
    main()