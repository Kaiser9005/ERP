# Rapport d'Analyse des Doublons

## État Actuel de la Réorganisation

### Composants Météo Standardisés

Les composants météo ont été renommés en français :

1. Dashboard et Production :
   - WeatherWidget.tsx → WidgetMeteo.tsx
   - WeatherModule.tsx → ModuleMétéo.tsx
   - WeatherDashboard.tsx → TableauDeBordMétéo.tsx
   - WeatherAnalytics.tsx → AnalyseMétéo.tsx
   - TableauMeteoParcelleaire.tsx (nouveau)

2. RH et Projets :
   - WeatherStatCard.tsx → CarteMétéo.tsx
   - TaskWeatherDetails.tsx → DétailsMétéoTâche.tsx

3. Tests associés :
   - Tests renommés pour correspondre aux nouveaux noms
   - Tests tableau de bord migrés vers tests/ml/tableau_bord/
   - Structure cohérente avec les autres modules ML

### Services ML Réorganisés

Les services ML suivants ont été réorganisés avec succès :

1. Module Projets ML
   - Services migrés vers services/ml/projets/
   - Tests migrés vers tests/ml/projets/
   - Anciens fichiers supprimés de services/projects_ml/
   - Tests validés et fonctionnels

2. Module Inventaire ML
   - Services migrés vers services/ml/inventaire/
   - Tests migrés vers tests/ml/inventaire/
   - Structure validée et cohérente avec core/
   - Tests de non-régression passés

3. Module Finance/Comptabilité ML
   - Tests migrés vers tests/ml/finance_comptabilite/
   - Structure validée et cohérente avec core/
   - Tests de non-régression passés
   - Documentation mise à jour

### Services ML à Réorganiser

1. Module Production ML
   - Déplacer services/production_ml_service.py vers services/ml/production/
   - Créer la structure modulaire (base.py, analysis.py, etc.)
   - Migrer les tests vers tests/ml/production/
   - Valider l'intégration avec core/

2. Module Tableau de Bord ML
   - Réorganiser services/ml/tableau_bord/
   - Migrer les tests correspondants
   - Standardiser l'architecture

## Analyse des Composants Frontend

### Statistiques
- Composants dans src/: 36
- Composants dans frontend/src/: 220

### Composants Dupliqués

Les composants suivants existent dans les deux dossiers :

1. Composants de Layout
   - DashboardLayout.tsx
   - TopBar.tsx
   - PageHeader.tsx
   - SideBar.tsx

2. Composants Métier
   - ParcelleDetails.tsx
   - WeatherDashboard.tsx
   - ProjectDetails.tsx
   - LeaveRequestForm.tsx
   - HistoriqueMouvements.tsx
   - ProjectForm.tsx
   - EmployeeForm.tsx
   - EmployeesList.tsx
   - ProjectsPage.tsx
   - ParcellesList.tsx
   - PageInventaire.tsx
   - ProjectStats.tsx
   - DialogueMouvementStock.tsx
   - DetailsProduit.tsx
   - HarvestQualityForm.tsx
   - ParcelleForm.tsx
   - ProductionStats.tsx
   - ProductionCalendar.tsx
   - EmployeeStats.tsx
   - AttendanceOverview.tsx
   - EmployeeDetails.tsx
   - StatsInventaire.tsx
   - StatCard.tsx
   - ParcelleMap.tsx
   - ProductionPage.tsx
   - LeaveRequests.tsx
   - ProductionDashboard.tsx
   - HRPage.tsx
   - ListeStock.tsx

## Structure Actuelle des Services ML

### Core (Base commune)
- services/ml/core/
  - config.py
  - types.py
  - base.py
  - __init__.py

### Modules Métier
- services/ml/projets/ (✓)
  - service.py
  - base.py
  - analysis.py
  - optimization.py
  - weather.py
  - __init__.py

- services/ml/inventaire/ (✓)
  - analysis.py
  - optimization.py
  - quality.py
  - base.py
  - __init__.py

- services/ml/tableau_bord/
  - predictions.py
  - alertes.py
  - unification.py
  - __init__.py

- services/finance_comptabilite/ (✓)
  - analyse.py
  - couts.py
  - meteo.py
  - iot.py
  - cloture.py
  - __init__.py

### Modules à Migrer
- services/production_ml_service.py → services/ml/production/
- services/ml/tableau_bord/ → Réorganiser selon architecture standard

## Plan d'Action

### Court Terme
1. Migration Production ML
   - Créer la structure dans services/ml/production/
   - Migrer le code existant
   - Adapter les tests
   - Valider l'intégration

2. Réorganisation Tableau de Bord ML
   - Standardiser l'architecture
   - Migrer les tests
   - Valider l'intégration

### Moyen Terme
1. Frontend
   - Unifier les composants dans frontend/src/components/
   - Standardiser les noms en français
   - Mettre à jour les imports

2. Tests
   - Finaliser la migration des tests ML
   - Valider la couverture de tests
   - Documenter les nouveaux patterns de test
