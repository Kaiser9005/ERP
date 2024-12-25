# Instructions pour la résolution des problèmes de build du frontend

Ce fichier fournit des instructions spécifiques pour résoudre les problèmes de build du frontend, regroupés par fichier.
Avant de commencer à résoudre les problèmes dans un fichier, lis le d'abord pour t'assurer que les problèmes sont toujours présents. Cela permettra de ne pas résoudre à nouveau lesproblèmes qui ont déjà été corrigés.

## Fichiers et instructions

### src/components/dashboard/__tests__/MLDashboard.test.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `../MLDashboard` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `MLDashboard.tsx` ou `MLDashboard.jsx` existe dans le répertoire `src/components/dashboard`.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.
-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre exporté mentionné dans l'erreur existe dans le module `../MLDashboard`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `../MLDashboard`.

### src/components/documents/DocumentUploadDialog.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `react-dropzone` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `react-dropzone.d.ts` existe dans le répertoire `node_modules/@types/react-dropzone` ou que le module lui-même inclut des déclarations de type.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.
-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `useDropzone` est correct.
    -   Consultez la documentation de `react-dropzone` pour connaître les types attendus.

### src/components/finance/__tests__/BudgetOverview.test.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `../BudgetOverview` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `BudgetOverview.tsx` ou `BudgetOverview.jsx` existe dans le répertoire `src/components/finance`.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.
-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `getBudgetOverview` est exporté par le module `../../../services/finance`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `../../../services/finance`.

### src/components/finance/__tests__/FinancePage.test.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `../FinancePage` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `FinancePage.tsx` ou `FinancePage.jsx` existe dans le répertoire `src/components/finance`.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.

### src/components/finance/__tests__/TransactionList.test.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `../TransactionList` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `TransactionList.tsx` ou `TransactionList.jsx` existe dans le répertoire `src/components/finance`.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.

### src/components/production/ParcelleMap.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que le module `/home/user/ERP/src/services/api` est correctement installé et que le chemin d'accès est correct.
    -   Assurez-vous que le fichier `api.ts` ou `api.js` existe dans le répertoire `/home/user/ERP/src/services`.
    -   Si le module est un package externe, vérifiez qu'il est bien présent dans le fichier `package.json` et qu'il a été installé avec `npm install`.

### src/routes/inventory.tsx

-   **TS2307: Cannot find module ... or its corresponding type declarations.**
    -   Vérifiez que les modules `../components/inventory/InventoryPage`, `../components/inventory/ProductForm` et `../components/inventory/ProductDetails` sont correctement installés et que les chemins d'accès sont corrects.
    -   Assurez-vous que les fichiers `InventoryPage.tsx`, `ProductForm.tsx` et `ProductDetails.tsx` existent dans le répertoire `src/components/inventory`.
    -   Si les modules sont des packages externes, vérifiez qu'ils sont bien présents dans le fichier `package.json` et qu'ils ont été installés avec `npm install`.

### src/components/dashboard/__tests__/StatsFinance.test.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que les types des propriétés `type` sont corrects. Assurez-vous qu'ils correspondent aux types attendus ('increase' | 'decrease').
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/StatsFinance.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que les types des propriétés `valeur` et `type` de l'objet `variation` sont corrects. Assurez-vous qu'ils correspondent aux types attendus.
-   **TS2353: Object literal may only specify known properties and ... does not exist in type ...**
    -   Vérifiez que la propriété `value` existe dans le type de l'objet `variation`.
-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `FinanceStats` est exporté par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/finance'`.

### src/components/hr/__tests__/LeaveRequestForm.test.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que les types des propriétés `open`, `onClose` et `employeeId` sont corrects. Assurez-vous qu'ils correspondent aux types attendus par le composant `LeaveRequestForm`.

### src/components/hr/AttendanceOverview.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que les types des propriétés `title`, `value`, `total`, `icon` et `color` sont corrects. Assurez-vous qu'ils correspondent aux types attendus par le composant `StatCard`.

### src/components/inventaire/__tests__/ListeStock.test.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que les types des propriétés de l'objet `Stock` correspondent aux types définis dans l'interface `Stock`.
    -   Assurez-vous que la propriété `entrepot_id` est présente dans l'objet `Stock`.

### src/components/projects/ProjectForm.tsx

-   **TS2322: Type ... is not assignable to type ...**
    -   Vérifiez que le type du `resolver` est correct. Assurez-vous qu'il correspond au type attendu par `react-hook-form`.
    -   Vérifiez que les types des propriétés `name`, `nom`, `description`, `date_debut`, `date_fin_prevue` et `budget` sont corrects. Assurez-vous qu'ils correspondent aux types attendus par le composant `TextField`.

### src/components/comptabilite/JournauxList.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `setEcritures` est correct. Assurez-vous qu'il correspond au type attendu (`EcritureComptable[]`).

### src/components/documents/DocumentList.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `deleteMutation.mutate` est correct. Assurez-vous qu'il correspond au type attendu (`string`).
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `isLoading` car elle n'est pas utilisée dans ce fichier.

### src/components/finance/__tests__/AnalyseBudget.test.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `mockGetAnalyseBudget.mockResolvedValue` est correct. Assurez-vous qu'il correspond au type attendu (`AnalyseBudgetaire`).
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/GraphiqueTresorerie.test.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `mockGetDonneesTresorerie.mockResolvedValue` est correct. Assurez-vous qu'il correspond au type attendu (`DonneesTresorerie`).

### src/components/finance/__tests__/ListeTransactions.test.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `mockGetTransactions.mockResolvedValue` est correct. Assurez-vous qu'il correspond au type attendu (`TransactionListResponse`).

### src/components/finance/TransactionForm.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `updateTransaction` ou `createTransaction` est correct. Assurez-vous qu'il correspond au type attendu (`TransactionFormData`).
    -   Vérifiez que le type de l'argument passé à la fonction `mutation.mutate` est correct. Assurez-vous qu'il correspond au type attendu (`void`).
-   **TS2559: Type ... has no properties in common with type ...**
    -   Vérifiez que le type de la variable `transactionData` est correct. Assurez-vous qu'il correspond au type attendu (`TransactionFormData`).
    -   Vérifiez que le type de l'argument passé à la fonction `queryClient.invalidateQueries` est correct. Assurez-vous qu'il correspond au type attendu (`InvalidateQueryFilters`).
-   **TS18046: ... is of type 'unknown'.**
    -   Ajoutez une annotation de type pour la variable `comptes`. Par exemple, `const comptes: Compte[] = data?.comptes || [];`.
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `TypeTransaction` car elle n'est pas utilisée dans ce fichier.

### src/components/inventaire/DialogueMouvementStock.tsx

-   **TS2345: Argument of type ... is not assignable to parameter of type ...**
    -   Vérifiez que le type de l'argument passé à la fonction `mutation.mutate` est correct. Assurez-vous qu'il correspond au type attendu (`Omit<MouvementStock, "id" | "date_mouvement">`).
    -   Ajoutez la propriété manquante `responsable_id` à l'objet passé à `mutation.mutate`.

### src/components/dashboard/__tests__/WidgetMeteo.test.tsx

-   **TS2353: Object literal may only specify known properties and ... does not exist in type ...**
    -   Vérifiez que les propriétés de l'objet `weatherData` correspondent aux propriétés définies dans le type `WeatherCondition`.
    -   Supprimez la propriété `timestamp` si elle n'est pas définie dans le type `WeatherCondition`.

### src/components/production/__tests__/TableauMeteo.test.tsx

-   **TS2353: Object literal may only specify known properties and ... does not exist in type ...**
    -   Vérifiez que les propriétés de l'objet `weatherData` correspondent aux propriétés définies dans le type `WeatherCondition`.
    -   Supprimez la propriété `timestamp` si elle n'est pas définie dans le type `WeatherCondition`.

### src/components/finance/TransactionDetails.tsx

-   **TS2551: Property ... does not exist on type ... Did you mean ...?**
    -   Remplacez `validee_par_id` par `validee_par` dans l'objet `transaction`.

### src/components/parametrage/__tests__/ParametrageLayout.test.tsx

-   **TS2559: Type ... has no properties in common with type ...**
    -   Vérifiez que les propriétés de l'objet passé au composant `ParametrageLayout` correspondent aux propriétés attendues par ce composant.

### src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx

-   **TS2561: Object literal may only specify known properties but ... does not exist in type ... Did you mean to write ...?**
    -   Remplacez la propriété `responsable` par `responsable_id` dans l'objet `MouvementStock`.

### src/components/dashboard/__tests__/StatsProduction.test.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `getStatsProduction` est exporté par le module `'../../../services/production'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../../services/production'`.

### src/components/dashboard/StatisticsCards.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `getDashboardStats` est exporté par le module `'../../services/dashboard'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/dashboard'`.

### src/components/dashboard/StatsProduction.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `getStatsProduction` est exporté par le module `'../../services/production'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/production'`.

### src/components/finance/AnalyseBudget.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `AnalyseBudgetaire` est exporté par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/finance'`.
-   **TS18046: ... is of type 'unknown'.**
    -   Ajoutez une annotation de type pour la variable `donnees`.
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `theme` car elle n'est pas utilisée dans ce fichier.
-   **TS7006: Parameter '...' implicitly has an 'any' type.**
    -   Ajoutez une annotation de type pour les paramètres `facteur`, `index` et `recommandation`.
-   **TS2769: No overload matches this call.**
    -   Vérifiez que les arguments passés à la fonction `map` correspondent aux types attendus.

### src/components/finance/FormulaireTransaction.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que les membres `modifierTransaction`, `getComptes`, `StatutTransaction` et `Compte` sont exportés par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation des membres est correcte (nom, casse, etc.).
    -   Si les membres sont censés être exportés mais ne le sont pas, corrigez l'export dans le module `'../../services/finance'`.
-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que les membres `Transaction` et `TypeTransaction` sont exportés par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation des membres est correcte (nom, casse, etc.).
    -   Si les membres sont censés être exportés mais ne le sont pas, corrigez l'export dans le module `'../../services/finance'`.
-   **TS18046: ... is of type 'unknown'.**
    -   Ajoutez une annotation de type pour la variable `comptes`.
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `TypeTransaction` car elle n'est pas utilisée dans ce fichier.

### src/components/projects/__tests__/TaskList.test.tsx

-   **TS2614: Module ... has no exported member ... Did you mean to use 'import ... from ...' instead?**
    -   Vérifiez que le membre `getProjectTasks` est exporté par le module `'../../../services/projects'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../../services/projects'`.

### src/components/comptabilite/rapports/GrandLivre.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `LigneGrandLivre` est exporté par le module `'../../../types/comptabilite'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../../types/comptabilite'`.

### src/components/finance/__tests__/FormulaireTransaction.test.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `creerTransaction` est exporté par le module `'../../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../../services/finance'`.
-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.
    -   Supprimez les variables `modifierTransaction` et `getTransaction` car elles ne sont pas utilisées dans ce fichier.

### src/components/finance/__tests__/ListeTransactions.test.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `TypeTransaction` est exporté par le module `'../../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../../services/finance'`.

### src/components/finance/ListeTransactions.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que les membres `Transaction` et `TypeTransaction` sont exportés par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation des membres est correcte (nom, casse, etc.).
    -   Si les membres sont censés être exportés mais ne le sont pas, corrigez l'export dans le module `'../../services/finance'`.

### src/components/finance/ProjectionsFinancieres.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `ProjectionsFinancieres` est exporté par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/finance'`.

### src/components/finance/StatsFinance.tsx

-   **TS2724: ... has no exported member named ... Did you mean ...?**
    -   Vérifiez que le membre `FinanceStats` est exporté par le module `'../../services/finance'`.
    -   Assurez-vous que l'importation du membre est correcte (nom, casse, etc.).
    -   Si le membre est censé être exporté mais ne l'est pas, corrigez l'export dans le module `'../../services/finance'`.

### src/components/production/RecolteForm.tsx

-   **TS2740: Type ... is missing the following properties from type ...**
    -   Vérifiez que l'objet passé à la fonction `setFormData` a toutes les propriétés requises par le type `WeatherConditions`.

### src/components/finance/__tests__/TransactionDetails.test.tsx

-   **TS2741: Property ... is missing in type ... but required in type ...**
    -   Ajoutez la propriété manquante `transactionId` à l'objet passé à `TransactionDetails`.

### src/components/dashboard/__tests__/DashboardPage.perf.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `wrapper` car elle n'est pas utilisée dans ce fichier.

### src/components/dashboard/__tests__/StatsFinance.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/dashboard/__tests__/StatsProduction.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/dashboard/__tests__/StatsRH.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/dashboard/__tests__/WidgetMeteo.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/dashboard/AlertsPanel.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la fonction `getSeverityColor` car elle n'est pas utilisée dans ce fichier.

### src/components/dashboard/ModuleCard.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez le paramètre `module` car il n'est pas utilisé dans ce fichier.

### src/components/dashboard/modules/InventoryModule.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la fonction `formatCurrency` car elle n'est pas utilisée dans ce fichier.

### src/components/documents/DocumentList.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `isLoading` car elle n'est pas utilisée dans ce fichier.

### src/components/finance/__tests__/AnalyseBudget.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/FormulaireTransaction.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.
    -   Supprimez les variables `modifierTransaction` et `getTransaction` car elles ne sont pas utilisées dans ce fichier.

### src/components/finance/__tests__/GraphiqueTresorerie.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/ListeTransactions.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/PageFinance.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/ProjectionsFinancieres.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/StatsFinance.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/__tests__/VueBudget.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/finance/AnalyseBudget.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `theme` car elle n'est pas utilisée dans ce fichier.

### src/components/finance/FormulaireTransaction.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `TypeTransaction` car elle n'est pas utilisée dans ce fichier.

### src/components/finance/ListeTransactions.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `isLoading` car elle n'est pas utilisée dans ce fichier.

### src/components/finance/PageFinance.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez le paramètre `event` car il n'est pas utilisé dans ce fichier.

### src/components/finance/ProjectionsFinancieres.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `Grid` car il n'est pas utilisé dans ce fichier.
    -   Supprimez la variable `theme` car elle n'est pas utilisée dans ce fichier.

### src/components/hr/__tests__/AttendanceChart.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/__tests__/EmployeeDetails.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez la variable `waitFor` car elle n'est pas utilisée dans ce fichier.

### src/components/hr/__tests__/EmployeeForm.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez les variables `updateEmployee` et `getEmployee` car elles ne sont pas utilisées dans ce fichier.

### src/components/hr/analytics/__tests__/HRAnalyticsDashboard.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/analytics/HRAnalyticsDashboard.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `queryKeys` car il n'est pas utilisé dans ce fichier.

### src/components/hr/formation/__tests__/FormationForm.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/formation/__tests__/FormationList.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/formation/__tests__/FormationPage.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/types/formTypes.ts

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `UseFormRegister` car il n'est pas utilisé dans ce fichier.

### src/components/hr/weather/__tests__/CarteMeteo.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/hr/weather/__tests__/TableauDeBordMeteo.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/inventaire/__tests__/DetailsProduit.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'est pas utilisé dans ce fichier.

### src/components/inventaire/__tests__/DialogueMouvementStock.test.tsx

-   **TS6133: ... is declared but its value is never read.**
    -   Supprimez l'import `React` car il n'
