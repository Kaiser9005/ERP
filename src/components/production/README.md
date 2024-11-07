# Composants de Production FOFAL ERP

## Description
Ce dossier contient les composants React pour le module de production de FOFAL ERP, gérant les cultures de palmier à huile et de papayes.

## Composants

### ParcelleMap
Carte interactive pour la visualisation et la gestion des parcelles agricoles.

### ProductionCalendar
Calendrier de gestion des cycles de culture et des événements de production.

### WeatherDashboard
Interface de suivi météorologique et système d'alertes climatiques.

### HarvestQualityForm
Formulaire de saisie et de contrôle qualité des récoltes.

### ProductionDashboard
Composant principal intégrant tous les autres éléments du module.

## Utilisation

```typescript
import { ProductionDashboard } from './components/production';

function App() {
  return (
    <ProductionDashboard />
  );
}
```

## Documentation
Documentation complète disponible dans `/docs/modules/production.md`

## Tests
```bash
# Exécuter les tests unitaires
npm test

# Vérifier la couverture
npm run test:coverage
```

## Maintenance
Suivre les directives de développement dans `/docs/development_guidelines.md`
