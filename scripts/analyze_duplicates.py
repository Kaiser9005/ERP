#!/usr/bin/env python3
"""
Script d'analyse des doublons dans le projet ERP
"""

import os
import hashlib
from collections import defaultdict
from typing import Dict, List, Set, Tuple
import re

def get_file_hash(filepath: str) -> str:
    """Calcule le hash SHA-256 du contenu d'un fichier."""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def get_normalized_content(filepath: str) -> str:
    """Retourne le contenu normalisé du fichier (sans espaces/commentaires)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Supprime les commentaires et les espaces
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+', ' ', content)
    return content.strip()

def find_duplicates(root_dir: str) -> Tuple[Dict[str, List[str]], Dict[str, List[str]]]:
    """
    Trouve les fichiers dupliqués basés sur leur contenu.
    Retourne deux dictionnaires:
    1. Fichiers avec contenu identique
    2. Fichiers avec contenu similaire
    """
    exact_duplicates = defaultdict(list)
    similar_files = defaultdict(list)
    
    # Extensions à analyser
    extensions = {'.ts', '.tsx', '.js', '.jsx', '.py', '.md'}
    
    # Parcours récursif des fichiers
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if os.path.splitext(filename)[1] in extensions:
                filepath = os.path.join(dirpath, filename)
                try:
                    # Hash exact pour les doublons identiques
                    file_hash = get_file_hash(filepath)
                    exact_duplicates[file_hash].append(filepath)
                    
                    # Contenu normalisé pour les fichiers similaires
                    normalized = get_normalized_content(filepath)
                    if normalized:  # Ignore les fichiers vides
                        similar_files[normalized].append(filepath)
                except (IOError, UnicodeDecodeError):
                    print(f"Erreur lors de la lecture de {filepath}")
                    continue

    # Filtre pour ne garder que les entrées avec des doublons
    exact_duplicates = {k: v for k, v in exact_duplicates.items() if len(v) > 1}
    similar_files = {k: v for k, v in similar_files.items() if len(v) > 1}
    
    return exact_duplicates, similar_files

def analyze_component_structure():
    """Analyse la structure des composants entre src/ et frontend/src/."""
    src_components = set()
    frontend_components = set()
    
    # Liste des composants dans src/
    if os.path.exists('src/components'):
        for root, _, files in os.walk('src/components'):
            for file in files:
                if file.endswith(('.tsx', '.jsx')):
                    src_components.add(os.path.join(root, file))
    
    # Liste des composants dans frontend/src/
    if os.path.exists('frontend/src/components'):
        for root, _, files in os.walk('frontend/src/components'):
            for file in files:
                if file.endswith(('.tsx', '.jsx')):
                    frontend_components.add(os.path.join(root, file))
    
    return src_components, frontend_components

def analyze_services():
    """Analyse la structure des services ML."""
    services = defaultdict(list)
    
    # Chemins à analyser
    service_paths = [
        'services/ml',
        'services/inventory_ml',
        'services/projects_ml',
        'services/finance_comptabilite'
    ]
    
    for service_path in service_paths:
        if os.path.exists(service_path):
            for root, _, files in os.walk(service_path):
                for file in files:
                    if file.endswith('.py'):
                        services[service_path].append(os.path.join(root, file))
    
    return services

def generate_report(
    exact_dupes: Dict[str, List[str]],
    similar_files: Dict[str, List[str]],
    src_components: Set[str],
    frontend_components: Set[str],
    services: Dict[str, List[str]]
) -> str:
    """Génère un rapport d'analyse."""
    report = ["# Rapport d'Analyse des Doublons\n"]
    
    # 1. Doublons exacts
    report.append("## Doublons Exacts\n")
    if exact_dupes:
        for _, files in exact_dupes.items():
            report.append(f"* Groupe de fichiers identiques:\n")
            for f in files:
                report.append(f"  - {f}\n")
    else:
        report.append("Aucun doublon exact trouvé.\n")
    
    # 2. Fichiers similaires
    report.append("\n## Fichiers Similaires\n")
    if similar_files:
        for _, files in similar_files.items():
            report.append(f"* Groupe de fichiers similaires:\n")
            for f in files:
                report.append(f"  - {f}\n")
    else:
        report.append("Aucun fichier similaire trouvé.\n")
    
    # 3. Analyse des composants
    report.append("\n## Analyse des Composants\n")
    report.append(f"* Composants dans src/: {len(src_components)}\n")
    report.append(f"* Composants dans frontend/src/: {len(frontend_components)}\n")
    
    # Composants potentiellement dupliqués
    common_names = {os.path.basename(c) for c in src_components} & \
                  {os.path.basename(c) for c in frontend_components}
    if common_names:
        report.append("\n### Composants avec noms identiques:\n")
        for name in common_names:
            report.append(f"* {name}\n")
    
    # 4. Analyse des services
    report.append("\n## Analyse des Services ML\n")
    for service_path, files in services.items():
        report.append(f"\n### {service_path}\n")
        for file in files:
            report.append(f"* {file}\n")
    
    # 5. Recommandations
    report.append("\n## Recommandations\n")
    
    # Recommandations pour les composants
    if src_components and frontend_components:
        report.append("### Composants\n")
        report.append("1. Unifier tous les composants dans frontend/src/components\n")
        report.append("2. Standardiser les noms en français\n")
        report.append("3. Mettre à jour les imports\n")
    
    # Recommandations pour les services
    if len(services) > 1:
        report.append("\n### Services ML\n")
        report.append("1. Centraliser tous les services ML dans services/ml/\n")
        report.append("2. Organiser par domaine (tableau_bord, inventory, projects)\n")
        report.append("3. Créer une interface commune\n")
    
    return "\n".join(report)

def main():
    """Fonction principale."""
    # Analyse des doublons
    exact_dupes, similar_files = find_duplicates('.')
    
    # Analyse des composants
    src_components, frontend_components = analyze_component_structure()
    
    # Analyse des services
    services = analyze_services()
    
    # Génération du rapport
    report = generate_report(
        exact_dupes,
        similar_files,
        src_components,
        frontend_components,
        services
    )
    
    # Écriture du rapport
    with open('docs/analyse_doublons.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("Analyse terminée. Rapport généré dans docs/analyse_doublons.md")

if __name__ == '__main__':
    main()
