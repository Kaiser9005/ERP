# Analyse des incohérences de nommage Frontend/Backend

## Module Tableau de Bord

### Types et Interfaces
1. **ModuleStats (frontend/src/types/dashboard.ts)**
   - ❌ `projects` vs `projets` dans le backend
   - ❌ `inventory` vs `inventaire` dans le backend
   - ❌ `weather` vs `meteo` dans le backend
   - ❌ `hr` vs `rh` dans le backend

2. **Interfaces de résumé**
   - ❌ `HRSummary` devrait être `RHSummary`
   - ❌ `InventorySummary` devrait être `InventaireSummary`
   - ❌ `WeatherSummary` devrait être `MeteoSummary`
   - ❌ `ProjectsSummary` devrait être `ProjetsSummary`

### Services
1. **DashboardService (frontend/src/services/dashboard.ts)**
   - ❌ `getUnifiedDashboard()` vs `getTableauBordUnifie()` dans le backend
   - ❌ `getModuleDetails()` vs `getDetailsModule()` dans le backend
   - ❌ `getCriticalAlerts()` vs `getAlertesCritiques()` dans le backend
   - ❌ `getMLPredictions()` vs `getPredictionsML()` dans le backend

### Composants
1. **DashboardPage (frontend/src/components/dashboard/DashboardPage.tsx)**
   - ❌ Nom du composant devrait être `TableauBordPage`
   - ❌ `StatCard` devrait être `CarteStatistique`
   - ❌ `ProductionChart` devrait être `GraphiqueProduction`
   - ❌ `CashFlowChart` devrait être `GraphiqueTresorerie`
   - ❌ `RecentActivities` devrait être `ActivitesRecentes`
   - ❌ `WidgetMeteo` est correct (déjà en français)

## Module RH

### Types et Interfaces
1. **Types RH (frontend/src/types/hr.ts)**
   - ❌ `Employee` vs `Employe` dans le backend
   - ❌ `Contract` vs `Contrat` dans le backend
   - ❌ `Training` vs `Formation` dans le backend

### Services
1. **HRService (frontend/src/services/hr.ts)**
   - ❌ `getEmployeeList()` vs `getListeEmployes()` dans le backend
   - ❌ `getContractDetails()` vs `getDetailsContrat()` dans le backend
   - ❌ `getTrainingStatus()` vs `getStatutFormation()` dans le backend

## Module Inventaire

### Types et Interfaces
1. **Types Inventaire (frontend/src/types/inventory.ts)**
   - ❌ `StockItem` vs `ArticleStock` dans le backend
   - ❌ `StockMovement` vs `MouvementStock` dans le backend
   - ❌ `StockPrediction` vs `PredictionStock` dans le backend

### Services
1. **InventoryService (frontend/src/services/inventory.ts)**
   - ❌ `getStockItems()` vs `getArticlesStock()` dans le backend
   - ❌ `getMovements()` vs `getMouvements()` dans le backend
   - ❌ `getLowStockItems()` vs `getArticlesStockBas()` dans le backend

## Actions Requises

1. Mettre à jour les types et interfaces dans le frontend pour utiliser la terminologie française
2. Renommer les services frontend pour correspondre aux noms du backend
3. Renommer les composants React pour utiliser des noms en français
4. Mettre à jour les imports et références dans tous les fichiers affectés
5. Mettre à jour la documentation pour refléter les nouveaux noms

## Impact du Changement

- Nécessite une mise à jour coordonnée du frontend et du backend
- Peut nécessiter des modifications dans les tests
- Nécessite une mise à jour de la documentation
- Peut impacter temporairement le développement en cours

## Plan d'Action

1. Créer une branche dédiée pour ces modifications
2. Effectuer les changements par module
3. Mettre à jour les tests pour chaque module
4. Vérifier la compatibilité avec les API existantes
5. Tester l'intégration complète
6. Déployer les changements de manière coordonnée