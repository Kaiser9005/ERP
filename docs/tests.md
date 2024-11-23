# Guide des Tests FOFAL ERP

## Vue d'ensemble

Le système de tests de FOFAL ERP utilise plusieurs niveaux de tests :

- Tests unitaires (Unit tests)
- Tests d'intégration (Integration tests)
- Tests end-to-end (E2E tests)
- Tests de services (Service tests)

## Configuration

### Prérequis
```bash
# Installation des dépendances de test
pip install -r requirements.txt
```

### Exécution des tests
```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_dashboard.py

# Tests E2E
pytest tests/e2e/
```

## Structure des Tests

```
tests/
├── conftest.py              # Fixtures partagées globales
├── test_dashboard.py        # Tests du tableau de bord
├── test_weather.py          # Tests du service météo
├── test_activities.py       # Tests des activités
├── e2e/                     # Tests end-to-end
│   ├── conftest.py         # Fixtures E2E
│   ├── test_task_management.py
│   └── test_tableau_meteo.py
└── integration/            # Tests d'intégration
    ├── test_task_integration.py
    └── test_comptabilite_integration.py
```

## Tests React avec React Query

### Structure des Tests React Query
Les tests des composants utilisant react-query doivent vérifier :
- L'état de chargement initial
- Le rendu avec les données
- La gestion des erreurs
- Les états sans données
- La configuration correcte des requêtes

Exemple de structure :
```typescript
describe('MonComposant', () => {
  let queryClient: QueryClient;

  beforeEach(() => {
    queryClient = new QueryClient({
      defaultOptions: {
        queries: {
          retry: false
        }
      }
    });
  });

  it('affiche le chargement', () => {
    // Test de l'état de chargement
  });

  it('affiche les données', async () => {
    // Test du rendu avec données
  });

  it('affiche une erreur', async () => {
    // Test de la gestion d'erreur
  });

  it('utilise la bonne configuration', () => {
    // Test de la configuration react-query
  });
});
```

### Standards de Test React Query
1. Toujours wrapper les composants avec QueryClientProvider
2. Désactiver les retry en test
3. Mocker les fonctions de service
4. Vérifier les états de chargement
5. Tester la configuration des requêtes (staleTime, etc.)
6. Vérifier la gestion des erreurs
7. Tester les cas sans données

## Tests E2E

Les tests E2E utilisent Playwright pour tester l'application dans un vrai navigateur.

### Configuration E2E

Les tests E2E nécessitent :
- Playwright
- Un serveur de développement en cours d'exécution
- Une base de données de test

### Data-testid

Les composants React utilisent des data-testid pour faciliter la sélection dans les tests :

```typescript
// Exemple de composant avec data-testid
<TextField
  data-testid="task-title-input"
  label="Titre"
/>
```

Liste des data-testid principaux :
- `page-title` : Titre de la page
- `error-message` : Messages d'erreur
- `task-form` : Formulaire de tâche
- `task-title-input` : Champ titre de tâche
- `task-description-input` : Champ description
- `task-status-select` : Sélecteur de statut
- `task-priority-select` : Sélecteur de priorité
- `task-category-select` : Sélecteur de catégorie
- `start-date-input` : Champ date de début
- `due-date-input` : Champ date de fin
- `weather-dependent-checkbox` : Case à cocher météo
- `submit-button` : Bouton de soumission
- `cancel-button` : Bouton d'annulation

### Fixtures E2E

Les fixtures E2E sont définies dans `tests/e2e/conftest.py` :
- `auth_token` : Token JWT pour l'authentification
- `browser_context_args` : Configuration du navigateur
- `test_page` : Page de test avec helpers
- `authenticated_page` : Page authentifiée
- `task_page` : Page spécifique aux tâches

### Helpers E2E

Des helpers sont disponibles pour faciliter les tests :
- `fill_task_form` : Remplissage du formulaire de tâche
- `assert_task_in_list` : Vérification de présence d'une tâche
- `assert_task_not_in_list` : Vérification d'absence d'une tâche
- `assert_toast_message` : Vérification des messages toast
- `assert_validation_error` : Vérification des erreurs de validation

## Bonnes Pratiques

1. Tests Unitaires
   - Un test par fonction/comportement
   - Utiliser les fixtures pour la configuration
   - Mocker les dépendances externes
   - Nommer clairement les tests

2. Tests E2E
   - Utiliser les data-testid pour la sélection
   - Tester les flux complets
   - Gérer l'état initial
   - Nettoyer après les tests

3. Général
   - Maintenir une couverture > 80%
   - Documenter les cas complexes
   - Tests indépendants
   - Utiliser les fixtures appropriées

## Maintenance

- Mettre à jour les tests lors des changements de fonctionnalités
- Vérifier régulièrement la couverture
- Maintenir la documentation des tests à jour
- Revoir et optimiser les tests lents

## Support

Pour toute question sur les tests :
- Consulter la documentation dans `/docs/tests/`
- Voir les exemples dans les fichiers de test
- Contacter l'équipe de développement
