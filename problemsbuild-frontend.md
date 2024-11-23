19s
Run npm install
npm warn deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm warn deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm warn deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm warn deprecated domexception@4.0.0: Use your platform's native DOMException instead
npm warn deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm warn deprecated @humanwhocodes/object-schema@2.0.3: Use @eslint/object-schema instead
npm warn deprecated @humanwhocodes/config-array@0.13.0: Use @eslint/config-array instead
npm warn deprecated eslint@8.57.1: This version is no longer supported. Please see https://eslint.org/version-support for other options.

added 569 packages, and audited 570 packages in 19s

129 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
0s
Run echo "VITE_WEATHER_API_KEY=" >> .env
7s
Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(5,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/finance/BudgetOverview.tsx(13,10): error TS2305: Module '"../../services/finance"' has no exported member 'getBudgetOverview'.
Error: src/components/finance/BudgetOverview.tsx(13,29): error TS2459: Module '"../../services/finance"' declares 'Budget' locally, but it is not exported.
Error: src/components/finance/BudgetOverview.tsx(16,53): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<Budget[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<Budget[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<Budget[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
Error: src/components/finance/BudgetOverview.tsx(32,20): error TS2339: Property 'map' does not exist on type 'never[] | TQueryFnData'.
  Property 'map' does not exist on type 'TQueryFnData'.
Error: src/components/finance/BudgetOverview.tsx(32,25): error TS7006: Parameter 'budget' implicitly has an 'any' type.
Error: src/components/finance/TransactionDetails.tsx(153,49): error TS2339: Property 'numero' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(156,49): error TS2339: Property 'libelle' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(173,54): error TS2339: Property 'numero' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(176,54): error TS2339: Property 'libelle' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(193,47): error TS2339: Property 'nom' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(193,80): error TS2339: Property 'prenom' does not exist on type 'string'.
Error: src/components/finance/TransactionForm.tsx(18,64): error TS2305: Module '"../../services/finance"' has no exported member 'getComptes'.
Error: src/components/finance/TransactionForm.tsx(18,76): error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
Error: src/components/finance/TransactionForm.tsx(64,5): error TS2554: Expected 1-2 arguments, but got 3.
Error: src/components/finance/TransactionForm.tsx(67,43): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
Error: src/components/finance/TransactionForm.tsx(82,5): error TS2322: Type 'Resolver<{ description?: string | undefined; compte_source?: string | undefined; compte_destination?: string | undefined; categorie: string; statut: string; reference: string; date_transaction: string; type_transaction: string; montant: number; }>' is not assignable to type 'Resolver<TransactionFormData, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type 'TransactionFormData' is missing the following properties from type '{ description?: string | undefined; compte_source?: string | undefined; compte_destination?: string | undefined; categorie: string; statut: string; reference: string; date_transaction: string; type_transaction: string; montant: number; }': categorie, statut, reference, date_transaction, and 2 more.
Error: src/components/finance/TransactionForm.tsx(89,5): error TS2559: Type '(data: TransactionFormData) => Promise<Transaction>' has no properties in common with type 'UseMutationOptions<unknown, Error, void, unknown>'.
Error: src/components/finance/TransactionForm.tsx(94,83): error TS2345: Argument of type '{ date_transaction: string; compte_source?: string; compte_destination?: string; }' is not assignable to parameter of type 'TransactionFormData'.
  Type '{ date_transaction: string; compte_source?: string | undefined; compte_destination?: string | undefined; }' is missing the following properties from type 'TransactionFormData': type_transaction, categorie, montant
Error: src/components/finance/TransactionForm.tsx(98,39): error TS2559: Type 'string[]' has no properties in common with type 'InvalidateQueryFilters'.
Error: src/components/finance/TransactionForm.tsx(105,21): error TS2345: Argument of type 'TransactionFormData' is not assignable to parameter of type 'void'.
Error: src/components/finance/TransactionForm.tsx(116,60): error TS2339: Property 'reference' does not exist on type '{}'.
Error: src/components/finance/TransactionForm.tsx(241,26): error TS18046: 'comptes' is of type 'unknown'.
Error: src/components/finance/TransactionForm.tsx(241,39): error TS7006: Parameter 'compte' implicitly has an 'any' type.
Error: src/components/finance/TransactionForm.tsx(266,26): error TS18046: 'comptes' is of type 'unknown'.
Error: src/components/finance/TransactionForm.tsx(266,39): error TS7006: Parameter 'compte' implicitly has an 'any' type.
Error: src/components/finance/TransactionForm.tsx(306,39): error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown, Error, void, unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown, Error, void, unknown>, { mutate: UseMutateFunction<unknown, Error, void, unknown>; }> & { ...; }'.
Error: src/components/finance/TransactionsList.tsx(19,27): error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?
Error: src/components/finance/TransactionsList.tsx(27,63): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<Transaction[], Error, Transaction[], QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<Transaction[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<Transaction[], Error, Transaction[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[], Error, Transaction[], QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<Transaction[], Error, Transaction[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<Transaction[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<Transaction[], Error, Transaction[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[], Error, Transaction[], QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<Transaction[], Error, Transaction[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<Transaction[], Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<Transaction[], Error, Transaction[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Transaction[], Error, Transaction[], QueryKey>'.
Error: src/components/finance/TransactionsList.tsx(29,45): error TS2339: Property 'filter' does not exist on type 'never[] | TQueryFnData'.
  Property 'filter' does not exist on type 'TQueryFnData'.
Error: src/components/finance/TransactionsList.tsx(29,52): error TS7006: Parameter 'transaction' implicitly has an 'any' type.
Error: src/components/finance/TransactionsList.tsx(78,40): error TS7006: Parameter 'transaction' implicitly has an 'any' type.
Error: src/components/hr/AttendanceOverview.tsx(17,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/hr/AttendanceOverview.tsx(18,28): error TS6133: 'EmployeeStats' is declared but its value is never read.
Error: src/components/hr/EmployeeDetails.tsx(21,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/hr/EmployeeForm.tsx(55,5): error TS2554: Expected 1-2 arguments, but got 3.
Error: src/components/hr/EmployeeForm.tsx(80,5): error TS2559: Type '(data: EmployeeFormData) => Promise<Employee>' has no properties in common with type 'UseMutationOptions<unknown, Error, void, unknown>'.
Error: src/components/hr/EmployeeForm.tsx(90,39): error TS2559: Type 'string[]' has no properties in common with type 'InvalidateQueryFilters'.
Error: src/components/hr/EmployeeForm.tsx(97,21): error TS2345: Argument of type 'EmployeeFormData' is not assignable to parameter of type 'void'.
Error: src/components/hr/EmployeeForm.tsx(108,57): error TS2339: Property 'prenom' does not exist on type '{}'.
Error: src/components/hr/EmployeeForm.tsx(108,77): error TS2339: Property 'nom' does not exist on type '{}'.
Error: src/components/hr/EmployeeForm.tsx(375,39): error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown, Error, void, unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown, Error, void, unknown>, { mutate: UseMutateFunction<unknown, Error, void, unknown>; }> & { ...; }'.
Error: src/components/hr/EmployeeStats.tsx(28,51): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<EmployeeStats, Error, EmployeeStats, QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<EmployeeStats, Error, EmployeeStats, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<EmployeeStats, Error, EmployeeStats, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<EmployeeStats, Error, EmployeeStats, QueryKey>'.
Error: src/components/hr/EmployeeStats.tsx(39,24): error TS2339: Property 'activeEmployees' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(41,27): error TS2339: Property 'employeeGrowth' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(42,25): error TS2339: Property 'employeeGrowth' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(52,24): error TS2339: Property 'onLeave' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(54,27): error TS2339: Property 'leaveRate' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(55,25): error TS2339: Property 'leaveRate' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(65,24): error TS2339: Property 'inTraining' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(67,27): error TS2339: Property 'trainingRate' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(68,25): error TS2339: Property 'trainingRate' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeeStats.tsx(78,24): error TS2339: Property 'totalEmployees' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/hr/EmployeesList.tsx(16,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/hr/EmployeesList.tsx(63,30): error TS7006: Parameter 'employee' implicitly has an 'any' type.
Error: src/components/hr/LeaveRequestForm.tsx(13,45): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/hr/LeaveRequests.tsx(16,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/hr/LeaveRequests.tsx(59,29): error TS7006: Parameter 'request' implicitly has an 'any' type.
Error: src/components/inventaire/DetailsProduit.tsx(17,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/DetailsProduit.tsx(77,28): error TS7053: Element implicitly has an 'any' type because expression of type 'any' can't be used to index type 'typeof CategoryProduit'.
Error: src/components/inventaire/DetailsProduit.tsx(142,35): error TS7006: Parameter 'movement' implicitly has an 'any' type.
Error: src/components/inventaire/DialogueMouvementStock.tsx(15,45): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/FormulaireProduit.tsx(15,55): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/FormulaireProduit.tsx(73,62): error TS2345: Argument of type 'ProduitFormData' is not assignable to parameter of type 'Partial<Produit>'.
  Types of property 'categorie' are incompatible.
    Type 'string' is not assignable to type 'CategoryProduit | undefined'.
Error: src/components/inventaire/FormulaireProduit.tsx(73,83): error TS2345: Argument of type 'ProduitFormData' is not assignable to parameter of type 'Partial<Produit>'.
  Types of property 'categorie' are incompatible.
    Type 'string' is not assignable to type 'CategoryProduit | undefined'.
Error: src/components/inventaire/HistoriqueMouvements.tsx(15,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/HistoriqueMouvements.tsx(16,25): error TS2459: Module '"../../services/inventaire"' declares 'MouvementStock' locally, but it is not exported.
Error: src/components/inventaire/HistoriqueMouvements.tsx(53,28): error TS7006: Parameter 'mouvement' implicitly has an 'any' type.
Error: src/components/inventaire/ListeStock.tsx(18,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/ListeStock.tsx(37,40): error TS7006: Parameter 'stock' implicitly has an 'any' type.
Error: src/components/inventaire/ListeStock.tsx(81,34): error TS7006: Parameter 'stock' implicitly has an 'any' type.
Error: src/components/inventaire/StatsInventaire.tsx(5,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/inventaire/StatsInventaire.tsx(6,30): error TS2724: '"../../services/inventaire"' has no exported member named 'StatsInventaire'. Did you mean 'getStatsInventaire'?
Error: src/components/production/ParcelleDetails.tsx(19,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/production/ParcelleDetails.tsx(159,38): error TS7006: Parameter 'event' implicitly has an 'any' type.
Error: src/components/production/ParcelleDetails.tsx(193,46): error TS7006: Parameter 'recolte' implicitly has an 'any' type.
Error: src/components/production/ParcelleForm.tsx(18,10): error TS2614: Module '"../../services/production"' has no exported member 'createParcelle'. Did you mean to use 'import createParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(18,26): error TS2614: Module '"../../services/production"' has no exported member 'updateParcelle'. Did you mean to use 'import updateParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(18,42): error TS2614: Module '"../../services/production"' has no exported member 'getParcelle'. Did you mean to use 'import getParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(42,5): error TS2554: Expected 1-2 arguments, but got 3.
Error: src/components/production/ParcelleForm.tsx(46,5): error TS2322: Type 'Resolver<{ code: string; statut: string; responsable_id: string; culture_type: string; surface_hectares: number; date_plantation: Date; }>' is not assignable to type 'Resolver<{}, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type '{}' is missing the following properties from type '{ code: string; statut: string; responsable_id: string; culture_type: string; surface_hectares: number; date_plantation: Date; }': code, statut, responsable_id, culture_type, and 2 more.
Error: src/components/production/ParcelleForm.tsx(58,5): error TS2560: Value of type '(data: any) => any' has no properties in common with type 'UseMutationOptions<unknown, Error, void, unknown>'. Did you mean to call it?
Error: src/components/production/ParcelleForm.tsx(61,39): error TS2559: Type '"parcelles"' has no properties in common with type 'InvalidateQueryFilters'.
Error: src/components/production/ParcelleForm.tsx(79,57): error TS2339: Property 'code' does not exist on type '{}'.
Error: src/components/production/ParcelleForm.tsx(94,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/production/ParcelleForm.tsx(101,39): error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(102,42): error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(110,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/production/ParcelleForm.tsx(118,39): error TS2339: Property 'culture_type' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(119,42): error TS2339: Property 'culture_type' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(130,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/production/ParcelleForm.tsx(138,39): error TS2339: Property 'surface_hectares' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(139,42): error TS2339: Property 'surface_hectares' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(147,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/production/ParcelleForm.tsx(156,43): error TS2339: Property 'date_plantation' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(157,46): error TS2339: Property 'date_plantation' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(167,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/production/ParcelleForm.tsx(175,39): error TS2339: Property 'statut' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(176,42): error TS2339: Property 'statut' does not exist on type 'FieldErrors<{}>'.
Error: src/components/production/ParcelleForm.tsx(197,39): error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown, Error, void, unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown, Error, void, unknown>, { mutate: UseMutateFunction<unknown, Error, void, unknown>; }> & { ...; }'.
Error: src/components/production/ParcelleMap.tsx(6,21): error TS2307: Cannot find module '/home/user/ERP/src/services/api' or its corresponding type declarations.
Error: src/components/production/ParcellesList.tsx(19,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/production/ProductionDashboard.tsx(61,13): error TS6133: 'detailedData' is declared but its value is never read.
Error: src/components/production/ProductionDashboard.tsx(68,28): error TS6133: 'event' is declared but its value is never read.
Error: src/components/production/ProductionStats.tsx(10,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/production/WeatherDashboard.tsx(40,61): error TS2345: Argument of type 'string' is not assignable to parameter of type '"current" | "forecast"'.
Error: src/components/production/WeatherDashboard.tsx(41,24): error TS2345: Argument of type 'WeatherData' is not assignable to parameter of type 'SetStateAction<WeatherData | null>'.
  Type 'WeatherData' is missing the following properties from type 'WeatherData': humidite, ensoleillement, vent, previsions
Error: src/components/projects/ProjectDetails.tsx(9,3): error TS6133: 'Button' is declared but its value is never read.
Error: src/components/projects/ProjectDetails.tsx(10,3): error TS6133: 'Link' is declared but its value is never read.
Error: src/components/projects/ProjectDetails.tsx(19,22): error TS2307: Cannot find module './TaskList' or its corresponding type declarations.
Error: src/components/projects/ProjectDetails.tsx(24,38): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<unknown, Error>', gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type '(string | undefined)[]' is not assignable to parameter of type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type '(string | undefined)[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
Error: src/components/projects/ProjectDetails.tsx(44,35): error TS2339: Property 'code' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(45,28): error TS2339: Property 'nom' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(67,37): error TS2339: Property 'statut' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(68,52): error TS2339: Property 'statut' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(80,40): error TS2339: Property 'budget' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(89,38): error TS2339: Property 'date_debut' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(90,47): error TS2339: Property 'date_debut' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(93,43): error TS2339: Property 'date_fin_prevue' does not exist on type '{}'.
Error: src/components/projects/ProjectDetails.tsx(94,47): error TS2339: Property 'date_fin_prevue' does not exist on type '{}'.
Error: src/components/projects/ProjectForm.tsx(10,3): error TS6133: 'MenuItem' is declared but its value is never read.
Error: src/components/projects/ProjectForm.tsx(45,5): error TS2554: Expected 1-2 arguments, but got 3.
Error: src/components/projects/ProjectForm.tsx(49,5): error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; budget: number; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; }>' is not assignable to type 'Resolver<{}, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type '{}' is missing the following properties from type '{ description?: string | undefined; code: string; budget: number; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; }': code, budget, date_debut, responsable_id, and 2 more.
Error: src/components/projects/ProjectForm.tsx(64,5): error TS2559: Type '(data: any) => Promise<Project>' has no properties in common with type 'UseMutationOptions<unknown, Error, void, unknown>'.
Error: src/components/projects/ProjectForm.tsx(67,39): error TS2559: Type '"projects"' has no properties in common with type 'InvalidateQueryFilters'.
Error: src/components/projects/ProjectForm.tsx(85,56): error TS2339: Property 'nom' does not exist on type '{}'.
Error: src/components/projects/ProjectForm.tsx(100,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(107,39): error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(108,42): error TS2339: Property 'code' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(116,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(123,39): error TS2339: Property 'nom' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(124,42): error TS2339: Property 'nom' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(132,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(141,39): error TS2339: Property 'description' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(142,42): error TS2339: Property 'description' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(150,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(159,43): error TS2339: Property 'date_debut' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(160,46): error TS2339: Property 'date_debut' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(170,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(179,43): error TS2339: Property 'date_fin_prevue' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(180,46): error TS2339: Property 'date_fin_prevue' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(190,19): error TS2322: Type 'string' is not assignable to type 'never'.
Error: src/components/projects/ProjectForm.tsx(198,39): error TS2339: Property 'budget' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(199,42): error TS2339: Property 'budget' does not exist on type 'FieldErrors<{}>'.
Error: src/components/projects/ProjectForm.tsx(216,39): error TS2339: Property 'isLoading' does not exist on type 'UseMutationResult<unknown, Error, void, unknown>'.
  Property 'isLoading' does not exist on type 'Override<MutationObserverIdleResult<unknown, Error, void, unknown>, { mutate: UseMutateFunction<unknown, Error, void, unknown>; }> & { ...; }'.
Error: src/components/projects/ProjectsPage.tsx(5,26): error TS2307: Cannot find module './ProjectsList' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(6,29): error TS2307: Cannot find module './ProjectTimeline' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(7,27): error TS2307: Cannot find module './TasksOverview' or its corresponding type declarations.
Error: src/config/queryClient.ts(7,7): error TS2353: Object literal may only specify known properties, and 'cacheTime' does not exist in type 'OmitKeyof<QueryObserverOptions<unknown, Error, unknown, unknown, QueryKey, never>, "suspense" | "queryKey", "strictly">'.
Error: src/routes/finance.tsx(20,19): error TS2741: Property 'transactionId' is missing in type '{}' but required in type 'TransactionDetailsProps'.
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: Process completed with exit code 2.