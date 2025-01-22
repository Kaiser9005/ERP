# Tests End-to-End (E2E)

Ce document explique comment exécuter et maintenir les tests end-to-end de l'ERP agricole.

## Prérequis

1. Python 3.8+ avec pip
2. Node.js 16+ avec npm
3. Playwright installé :
   ```bash
   pip install playwright
   playwright install
   ```
4. Variables d'environnement configurées :
   - OPENWEATHER_API_KEY
   - IOT_API_KEY

## Structure des tests

Les tests e2e sont organisés par module fonctionnel :
- `test_authentification_e2e.py` : Tests d'authentification et gestion des utilisateurs
- `test_finance_e2e.py` : Tests de gestion financière
- `test_inventaire_e2e.py` : Tests de gestion des stocks
- `test_production_e2e.py` : Tests de gestion de la production agricole
- `test_rh_e2e.py` : Tests de gestion des ressources humaines
- `test_tableau_bord_e2e.py` : Tests du tableau de bord unifié

## Exécution des tests

### Script d'exécution automatisé

Utilisez le script `scripts/run_e2e_tests.py` pour exécuter tous les tests :

```bash
# Mode headless (par défaut)
python scripts/run_e2e_tests.py

# Mode visible (pour debug)
python scripts/run_e2e_tests.py --no-headless

# Mode ralenti (pour debug)
python scripts/run_e2e_tests.py --slow-mo 100
```

### Options disponibles

- `--no-headless` : Exécute les tests avec le navigateur visible
- `--slow-mo <ms>` : Ajoute un délai entre les actions (utile pour le debug)

### Exécution individuelle des tests

Pour exécuter un module spécifique :

```bash
pytest tests/e2e/test_authentification_e2e.py -v
```

## Rapports de test

Les rapports sont générés automatiquement dans le dossier `reports/e2e` avec un timestamp :
- Format HTML auto-contenu
- Screenshots des erreurs
- Logs de la console
- Durée d'exécution
- Statistiques de réussite/échec

### Structure du rapport

- Vue d'ensemble
  * Nombre total de tests
  * Taux de réussite
  * Durée totale
- Détails par module
  * Résultats individuels
  * Screenshots en cas d'échec
  * Logs d'erreur
- Métriques de performance
  * Temps de chargement
  * Temps de réponse

## Maintenance des tests

### Bonnes pratiques

1. **Isolation** : Chaque test doit être indépendant
2. **Données de test** : Utiliser des fixtures pour les données
3. **Sélecteurs** : Préférer les attributs data-testid
4. **Assertions** : Vérifier l'état final ET les effets de bord
5. **Timeouts** : Configurer des délais raisonnables

### Ajout de nouveaux tests

1. Créer le fichier de test dans `tests/e2e/`
2. Suivre la structure existante :
   ```python
   def test_nouvelle_fonctionnalite(page: Page):
       """Description du test."""
       # Setup
       # Actions
       # Vérifications
   ```
3. Ajouter le test au script d'exécution

### Debug des tests

1. Utiliser le mode visible :
   ```bash
   python scripts/run_e2e_tests.py --no-headless
   ```

2. Ajouter des délais :
   ```bash
   python scripts/run_e2e_tests.py --slow-mo 100
   ```

3. Consulter les logs dans les rapports

## Intégration Continue

Les tests e2e sont exécutés :
- À chaque pull request
- Avant chaque déploiement
- Quotidiennement sur la branche principale

### Configuration CI

```yaml
e2e_tests:
  stage: test
  script:
    - python scripts/run_e2e_tests.py
  artifacts:
    paths:
      - reports/e2e/
```

## Résolution des problèmes courants

1. **Timeouts** :
   - Augmenter les délais d'attente
   - Vérifier la connectivité réseau
   - Vérifier la charge serveur

2. **Sélecteurs cassés** :
   - Mettre à jour les data-testid
   - Vérifier les changements UI
   - Adapter les sélecteurs

3. **Erreurs d'API** :
   - Vérifier les clés API
   - Vérifier les quotas/limites
   - Vérifier la configuration

4. **Problèmes de state** :
   - Nettoyer l'état avant chaque test
   - Utiliser des fixtures fraîches
   - Vérifier les dépendances

## Support

Pour toute question ou problème :
1. Consulter les logs détaillés
2. Vérifier la documentation
3. Contacter l'équipe QA