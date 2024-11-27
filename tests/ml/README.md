# Tests ML du Tableau de Bord

Ce dossier contient les tests pour les fonctionnalités ML (Machine Learning) du tableau de bord unifié.

## Structure des Tests

### Tests Unitaires

- `frontend/src/services/__tests__/dashboard.test.ts`
  - Tests du service dashboard côté frontend
  - Vérifie les appels API pour les prédictions ML
  - Teste la gestion des erreurs
  - Vérifie le formatage des données

### Tests d'Intégration

- `tests/integration/test_ml_services_integration.py`
  - Tests d'intégration entre les différents services ML
  - Vérifie la cohérence des données entre les services
  - Teste les flux de données complets

- `tests/integration/test_tableau_bord_unified.py`
  - Tests d'intégration du tableau de bord unifié
  - Vérifie l'agrégation des données ML
  - Teste le système de cache
  - Vérifie la gestion des erreurs au niveau système

### Tests End-to-End

- `tests/e2e/test_tableau_bord_ml_e2e.py`
  - Tests de bout en bout du tableau de bord ML
  - Vérifie l'intégration complète avec l'interface utilisateur
  - Teste les scénarios utilisateur réels
  - Vérifie les performances du système

## Configuration

Les fixtures et la configuration des tests sont définies dans :

- `tests/conftest.py`
  - Fixtures pour les données ML de test
  - Mock des services ML
  - Configuration du cache de test

## Exécution des Tests

Pour exécuter les tests ML :

```bash
# Tests unitaires frontend
npm test -- --testPathPattern=dashboard.test.ts

# Tests d'intégration Python
pytest tests/integration/test_ml_services_integration.py
pytest tests/integration/test_tableau_bord_unified.py

# Tests end-to-end
pytest tests/e2e/test_tableau_bord_ml_e2e.py

# Tous les tests ML
pytest tests/ml/
```

## Couverture des Tests

Les tests couvrent les aspects suivants :

### Prédictions ML
- Récupération des prédictions
- Formatage des données
- Gestion des erreurs
- Cache des résultats

### Alertes
- Priorisation des alertes
- Filtrage par module
- Mise à jour des statuts

### Tableau de Bord Unifié
- Agrégation des données
- Rafraîchissement des données
- Gestion du cache
- Gestion des erreurs

### Interface Utilisateur
- Affichage des prédictions
- Interaction utilisateur
- Mise à jour en temps réel
- Performance du système

## Maintenance

Pour ajouter de nouveaux tests :

1. Identifiez le niveau de test approprié (unitaire, intégration, e2e)
2. Utilisez les fixtures existantes dans conftest.py
3. Suivez les conventions de nommage existantes
4. Documentez les nouveaux cas de test
5. Vérifiez la couverture de code

## Bonnes Pratiques

- Utilisez les fixtures partagées de conftest.py
- Isolez les tests avec des mocks appropriés
- Nettoyez les données de test après chaque test
- Documentez les cas de test complexes
- Maintenez les tests indépendants
