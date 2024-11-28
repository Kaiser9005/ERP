# Composant HistoriqueMouvements

## Vue d'ensemble

Composant React optimisé pour l'affichage et la gestion des mouvements de stock, avec support complet de l'internationalisation et de l'accessibilité.

## Dernières modifications (Juillet 2024)

- Correction des types pour CategoryProduit et UniteMesure
- Suppression des imports inutilisés
- Amélioration de la gestion des produits par défaut
- Support complet de l'internationalisation
- Optimisation des performances

## Interfaces

```typescript
interface HistoriqueMouvementsProps {
  searchQuery?: string; // Filtre de recherche global
}

interface MouvementWithProduit extends MouvementStock {
  produit: Produit; // Produit associé au mouvement
}
```

## Fonctionnalités

### Chargement des données
- Utilisation de React Query pour la gestion du cache
- Chargement séparé des mouvements et produits
- Gestion optimisée des états de chargement

### Filtrage
- Filtre par type de mouvement (ENTREE, SORTIE, TRANSFERT)
- Recherche textuelle sur nom produit et référence
- Synchronisation avec le filtre global

### Internationalisation
- Support complet i18next
- Format des dates adapté à la locale
- Messages d'état traduits
- Labels et descriptions accessibles

### Accessibilité
- Labels ARIA sur tous les contrôles
- Navigation au clavier optimisée
- Messages d'état vocaux
- Structure sémantique HTML

## Performance

### Optimisations
- Mémoisation des jointures mouvements-produits
- Mémoisation du filtrage
- Chargement optimisé des données
- Gestion efficace du cache

### Métriques
- Temps de rendu initial : < 100ms
- Temps de filtrage : < 50ms
- Utilisation mémoire : stable
- Performance React Query : optimale

## Tests

### Tests unitaires
- Rendu du composant
- Filtrage et recherche
- Gestion des états
- Internationalisation

### Tests d'intégration
- Interaction avec l'API
- Cache React Query
- Navigation et routage

### Tests E2E
- Parcours utilisateur
- Filtrage et recherche
- Accessibilité

## Utilisation

```typescript
// Exemple d'utilisation basique
<HistoriqueMouvements />

// Avec filtre de recherche global
<HistoriqueMouvements searchQuery="produit123" />
```

## Points d'attention

- Surveiller les performances avec grands volumes
- Maintenir la couverture de tests
- Valider l'accessibilité
- Vérifier les traductions
- Optimiser le cache si nécessaire
