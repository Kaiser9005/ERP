2s
Run actions/setup-node@v3
Found in cache @ /opt/hostedtoolcache/node/18.20.5/x64
Environment details
19s
0s
Run echo "VITE_WEATHER_API_KEY=" >> .env
6s
Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(7,27): error TS2307: Cannot find module '../finance/CashFlowChart' or its corresponding type declarations.
Error: src/components/dashboard/ProductionChart.tsx(6,27): error TS2307: Cannot find module '../../config/queryClient' or its corresponding type declarations.
Error: src/components/dashboard/WeatherWidget.tsx(6,27): error TS2307: Cannot find module '../../config/queryClient' or its corresponding type declarations.
Error: src/components/hr/AttendanceOverview.tsx(18,28): error TS6133: 'EmployeeStats' is declared but its value is never read.
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
Error: src/components/inventaire/FormulaireProduit.tsx(73,62): error TS2345: Argument of type 'ProduitFormData' is not assignable to parameter of type 'Partial<Produit>'.
  Types of property 'categorie' are incompatible.
    Type 'string' is not assignable to type 'CategoryProduit | undefined'.
Error: src/components/inventaire/FormulaireProduit.tsx(73,83): error TS2345: Argument of type 'ProduitFormData' is not assignable to parameter of type 'Partial<Produit>'.
  Types of property 'categorie' are incompatible.
    Type 'string' is not assignable to type 'CategoryProduit | undefined'.
Error: src/components/inventaire/HistoriqueMouvements.tsx(16,25): error TS2459: Module '"../../services/inventaire"' declares 'MouvementStock' locally, but it is not exported.
Error: src/components/inventaire/ListeStock.tsx(35,61): error TS2769: No overload matches this call.
  Overload 1 of 3, '(queryKey: QueryKey, options?: Omit<UseQueryOptions<Stock[], unknown, Stock[], QueryKey>, "queryKey"> | undefined): UseQueryResult<...>', gave the following error.
    Type '() => Promise<Stock[]>' has no properties in common with type 'Omit<UseQueryOptions<Stock[], unknown, Stock[], QueryKey>, "queryKey">'.
  Overload 2 of 3, '(queryKey: QueryKey, queryFn: QueryFunction<Stock[], QueryKey>, options?: Omit<UseQueryOptions<Stock[], unknown, Stock[], QueryKey>, "queryKey" | "queryFn"> | undefined): UseQueryResult<...>', gave the following error.
    Argument of type '() => Promise<Stock[]>' is not assignable to parameter of type 'QueryFunction<Stock[], QueryKey>'.
      Type 'Promise<Stock[]>' is not assignable to type 'Stock[] | Promise<Stock[]>'.
        Type 'Promise<import("/home/runner/work/ERP/ERP/src/types/inventaire").Stock[]>' is not assignable to type 'Promise<Stock[]>'.
          Type 'import("/home/runner/work/ERP/ERP/src/types/inventaire").Stock[]' is not assignable to type 'Stock[]'.
            Type 'Stock' is missing the following properties from type 'Stock': code, name, quantity, unit, and 2 more.
Error: src/components/inventaire/ListeStock.tsx(37,33): error TS2339: Property 'filter' does not exist on type 'never[] | TQueryFnData'.
  Property 'filter' does not exist on type 'TQueryFnData'.
Error: src/components/inventaire/ListeStock.tsx(37,40): error TS7006: Parameter 'stock' implicitly has an 'any' type.
Error: src/components/inventaire/ListeStock.tsx(81,34): error TS7006: Parameter 'stock' implicitly has an 'any' type.
Error: src/components/inventaire/StatsInventaire.tsx(6,30): error TS2724: '"../../services/inventaire"' has no exported member named 'StatsInventaire'. Did you mean 'getStatsInventaire'?
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
Error: src/components/production/ProductionDashboard.tsx(61,13): error TS6133: 'detailedData' is declared but its value is never read.
Error: src/components/production/ProductionDashboard.tsx(68,28): error TS6133: 'event' is declared but its value is never read.
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
Error: src/components/projects/ProjectForm.tsx(49,5): error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; budget: number; }>' is not assignable to type 'Resolver<{}, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type '{}' is missing the following properties from type '{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; budget: number; }': code, date_debut, responsable_id, nom, and 2 more.
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
Error: src/routes/index.tsx(6,31): error TS2307: Cannot find module './finance' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: Process completed with exit code 2.