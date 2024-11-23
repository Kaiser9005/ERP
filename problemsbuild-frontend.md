Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(5,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/dashboard/WeatherWidget.tsx(9,5): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<unknown, Error, unknown, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<unknown, Error>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<unknown, Error, unknown, QueryKey>'.
Error: src/components/dashboard/WeatherWidget.tsx(21,11): error TS2339: Property 'conditions_meteo' does not exist on type '{}'.
Error: src/components/finance/BudgetOverview.tsx(16,53): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<Budget[], Error, Budget[], QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<Budget[], Error, Budget[], QueryKey>'.
Error: src/components/finance/BudgetOverview.tsx(32,20): error TS2339: Property 'map' does not exist on type 'never[] | TQueryFnData'.
  Property 'map' does not exist on type 'TQueryFnData'.
Error: src/components/finance/BudgetOverview.tsx(32,25): error TS7006: Parameter 'budget' implicitly has an 'any' type.
Error: src/components/finance/CashFlowChart.tsx(9,5): error TS2769: No overload matches this call.
  Overload 1 of 3, '(options: DefinedInitialDataOptions<CashFlowData, Error, CashFlowData, QueryKey>, queryClient?: QueryClient | undefined): DefinedUseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'DefinedInitialDataOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
  Overload 2 of 3, '(options: UndefinedInitialDataOptions<CashFlowData, Error, CashFlowData, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UndefinedInitialDataOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
  Overload 3 of 3, '(options: UseQueryOptions<CashFlowData, Error, CashFlowData, QueryKey>, queryClient?: QueryClient | undefined): UseQueryResult<...>', gave the following error.
    Argument of type 'string[]' is not assignable to parameter of type 'UseQueryOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
      Property 'queryKey' is missing in type 'string[]' but required in type 'UseQueryOptions<CashFlowData, Error, CashFlowData, QueryKey>'.
Error: src/components/finance/CashFlowChart.tsx(21,34): error TS2339: Property 'labels' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/finance/CashFlowChart.tsx(21,46): error TS7006: Parameter 'label' implicitly has an 'any' type.
Error: src/components/finance/CashFlowChart.tsx(21,53): error TS7006: Parameter 'index' implicitly has an 'any' type.
Error: src/components/finance/CashFlowChart.tsx(23,28): error TS2339: Property 'recettes' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/finance/CashFlowChart.tsx(24,28): error TS2339: Property 'depenses' does not exist on type 'NonNullable<TQueryFnData>'.
Error: src/components/finance/CashFlowChart.tsx(25,25): error TS2339: Property 'solde' does not exist on type 'NonNullable<TQueryFnData>'.
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
Error: src/components/projects/ProjectStats.tsx(18,41): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(5,26): error TS2307: Cannot find module './ProjectsList' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(6,29): error TS2307: Cannot find module './ProjectTimeline' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(7,27): error TS2307: Cannot find module './TasksOverview' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: Process completed with exit code 2.