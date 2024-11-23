## Guide de Développement FOFAL ERP

### Mise à Jour des Composants Frontend

#### Composant StatCard

Nous avons amélioré le composant StatCard pour une meilleure cohérence linguistique et technique :

- Utilisation de termes en français pour les variations de données
- Amélioration du typage TypeScript
- Standardisation des propriétés de variation

Exemple de mise à jour :
```typescript
interface StatCardProps {
  title: string;
  value: number;
  unit?: string;
  variation?: {
    valeur: number;  // Nouveau nom de propriété
    type: 'hausse' | 'baisse';  // Termes français
  };
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning' | 'info';
}
```

#### Gestion d'État avec React Query

Nous avons standardisé l'utilisation de react-query dans l'application :

1. Configuration des Requêtes
```typescript
const { data, isLoading, error } = useQuery({
  queryKey: queryKeys.domain.action(),
  queryFn: () => service.getData(),
  staleTime: 1000 * 60 * 5, // 5 minutes
  refetchInterval: 1000 * 60 * 15 // 15 minutes
});
```

2. Gestion Standard des États
```typescript
// État de chargement
if (isLoading) {
  return (
    <Card>
      <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
        <CircularProgress />
      </CardContent>
    </Card>
  );
}

// État d'erreur
if (error) {
  return (
    <Card>
      <CardContent>
        <Typography color="error">
          Erreur lors du chargement des données
        </Typography>
      </CardContent>
    </Card>
  );
}

// État sans données
if (!data) {
  return (
    <Card>
      <CardContent>
        <Typography color="textSecondary">
          Aucune donnée disponible
        </Typography>
      </CardContent>
    </Card>
  );
}
```

3. Organisation des Clés de Requête
```typescript
// Dans config/queryClient.ts
export const queryKeys = {
  finance: {
    stats: () => ['finance', 'stats'],
    cashflow: () => ['finance', 'cashflow']
  },
  production: {
    stats: () => ['production', 'stats'],
    events: (filter: string) => ['production', 'events', filter]
  },
  weather: {
    current: () => ['weather', 'current']
  }
};
```

#### Améliorations des Composants de Statistiques

- Mise à jour des composants FinanceStats, EmployeeStats et StatsInventaire
- Transformation cohérente des données
- Gestion des variations de manière standardisée
- Amélioration de la lisibilité et de la maintenabilité du code

#### Détails des Modifications

1. Transformation des Variations
   - Remplacement de `value` par `valeur`
   - Conversion des types de variation en français
   ```typescript
   // Avant
   variation: { value: number; type: 'increase' | 'decrease' }
   
   // Après
   variation: { valeur: number; type: 'hausse' | 'baisse' }
   ```

2. Composants Mis à Jour
   - `src/components/finance/FinanceStats.tsx`
   - `src/components/hr/EmployeeStats.tsx`
   - `src/components/inventaire/StatsInventaire.tsx`

3. Gestion des Transformations de Données
   ```typescript
   const transformStatsInventaire = (stats: StatsInventaireService): StatistiquesInventaire => ({
     valeurTotale: stats.valeur_totale,
     variationValeur: stats.valeur_stock,
     // Autres transformations similaires
   });
   ```

### Standards de Développement Frontend

#### Typage TypeScript

- Utilisation de types stricts
- Éviter `any` autant que possible
- Créer des interfaces spécifiques pour chaque composant
- Utiliser des unions de types pour les variations

#### Gestion des États

1. États de Chargement
   - Utiliser CircularProgress dans une Card
   - Hauteur minimale cohérente
   - Centrage avec flexbox

2. États d'Erreur
   - Messages d'erreur en français
   - Style cohérent avec Typography color="error"
   - Conteneur Card pour l'alignement

3. États Sans Données
   - Messages explicites
   - Style cohérent avec Typography color="textSecondary"
   - Maintien de la structure visuelle

#### Gestion des Erreurs

- Utilisation de try/catch dans les services
- Gestion explicite des erreurs dans les composants
- Affichage de messages d'erreur traduits en français

#### Conventions de Nommage

- Noms de variables et fonctions en camelCase
- Noms de composants en PascalCase
- Préfixes descriptifs (`use` pour les hooks, `handle` pour les gestionnaires d'événements)

### Intégration Continue

#### Configuration GitHub Actions

- Gestion sécurisée des secrets d'environnement
- Tests automatisés sur chaque pull request
- Vérification de la couverture de tests
- Lint et formatage du code

### Bonnes Pratiques

1. Modularité
   - Composants petits et réutilisables
   - Séparation claire des responsabilités
   - Utilisation de hooks personnalisés

2. Performance
   - Memoization avec `useMemo` et `useCallback`
   - Lazy loading des composants
   - Optimisation des requêtes API

3. Accessibilité
   - Utilisation de composants Material-UI accessibles
   - Gestion des contrastes et tailles de police
   - Support des lecteurs d'écran

### Outils Recommandés

- ESLint pour le linting TypeScript
- Prettier pour le formatage
- Jest et React Testing Library pour les tests
- Redux DevTools pour le débogage
- Lighthouse pour les audits de performance

### Processus de Développement

1. Créer une branche feature
2. Implémenter la fonctionnalité
3. Écrire des tests unitaires
4. Vérifier la couverture des tests
5. Effectuer une revue de code
6. Merger sur la branche principale après validation

### Notes Spécifiques aux Dernières Mises à Jour

#### Améliorations Techniques

- Standardisation du composant StatCard
  - Typage strict des variations
  - Utilisation de termes en français
  - Transformation cohérente des données

- Corrections de Typage
  - Résolution des erreurs TypeScript dans plusieurs composants
  - Amélioration de la gestion des types de données
  - Réduction de l'utilisation de `any`

- Optimisation des Composants
  - Transformation des données plus explicite
  - Amélioration de la lisibilité du code
  - Standardisation des méthodes de transformation

#### Recommandations pour les Développeurs

- Privilégier les types stricts
- Utiliser des transformations de données explicites
- Documenter les changements de type
- Maintenir la cohérence linguistique
- Effectuer des tests approfondis après modifications

### Références

- [Documentation TypeScript](https://www.typescriptlang.org/docs/)
- [React avec TypeScript](https://react-typescript-cheatsheet.netlify.app/)
- [Material-UI Documentation](https://mui.com/material-ui/getting-started/overview/)
- [React Query Documentation](https://tanstack.com/query/latest/docs/react/overview)
