Run cd frontend

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(5,26): error TS2307: Cannot find module 'react-query' or its corresponding type declarations.
Error: src/components/dashboard/DashboardPage.tsx(8,29): error TS2307: Cannot find module './ProductionChart' or its corresponding type declarations.
Error: src/components/dashboard/DashboardPage.tsx(9,30): error TS2307: Cannot find module './RecentActivities' or its corresponding type declarations.
Error: src/components/dashboard/DashboardPage.tsx(10,27): error TS2307: Cannot find module './WeatherWidget' or its corresponding type declarations.
Error: src/components/dashboard/DashboardPage.tsx(13,24): error TS6133: 'isLoading' is declared but its value is never read.
Error: src/components/finance/BudgetOverview.tsx(16,38): error TS2769: No overload matches this call.
  The last overload gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'QueryKey'.
Error: src/components/finance/BudgetOverview.tsx(32,21): error TS2339: Property 'map' does not exist on type '{}'.
Error: src/components/finance/BudgetOverview.tsx(32,26): error TS7006: Parameter 'budget' implicitly has an 'any' type.
Error: src/components/finance/CashFlowChart.tsx(28,39): error TS2769: No overload matches this call.
  The last overload gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'QueryKey'.
Error: src/components/finance/CashFlowChart.tsx(52,23): error TS2339: Property 'labels' does not exist on type '{}'.
Error: src/components/finance/CashFlowChart.tsx(56,25): error TS2339: Property 'recettes' does not exist on type '{}'.
Error: src/components/finance/CashFlowChart.tsx(63,25): error TS2339: Property 'depenses' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(9,36): error TS2769: No overload matches this call.
  The last overload gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'QueryKey'.
Error: src/components/finance/FinanceStats.tsx(16,25): error TS2339: Property 'revenue' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(18,29): error TS2339: Property 'revenueVariation' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(27,25): error TS2339: Property 'profit' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(29,29): error TS2339: Property 'profitVariation' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(38,25): error TS2339: Property 'cashflow' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(40,29): error TS2339: Property 'cashflowVariation' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(49,25): error TS2339: Property 'expenses' does not exist on type '{}'.
Error: src/components/finance/FinanceStats.tsx(51,29): error TS2339: Property 'expensesVariation' does not exist on type '{}'.
Error: src/components/finance/TransactionDetails.tsx(9,3): error TS6133: 'Button' is declared but its value is never read.
Error: src/components/finance/TransactionDetails.tsx(119,31): error TS2339: Property 'piece_jointe' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(125,41): error TS2339: Property 'piece_jointe' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(146,29): error TS2339: Property 'compte_source' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(152,34): error TS2339: Property 'compte_source' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(157,29): error TS2339: Property 'compte_destination' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(163,34): error TS2339: Property 'compte_destination' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(168,29): error TS2339: Property 'validee_par' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(174,34): error TS2339: Property 'validee_par' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(174,64): error TS2339: Property 'validee_par' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(177,34): error TS2339: Property 'date_validation' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionDetails.tsx(178,51): error TS2339: Property 'date_validation' does not exist on type 'Transaction'.
Error: src/components/finance/TransactionForm.tsx(31,34): error TS2769: No overload matches this call.
  Types of parameters 'values' and 'values' are incompatible.
    Property 'responsable_id' is missing in type 'Project' but required in type '{ description?: string | undefined; code: string; nom: string; date_debut: Date; responsable_id: string; date_fin_prevue: Date; budget: number; }'.
Error: src/components/projects/ProjectForm.tsx(50,5): error TS2322: Type '{ code: string; nom: string; description: string; date_debut: null; date_fin_prevue: null; budget: string; responsable_id: string; objectifs: never[]; risques: never[]; }' is not assignable to type 'AsyncDefaultValues<Project> | { id?: string | undefined; code?: string | undefined; nom?: string | undefined; description?: string | undefined; date_debut?: string | undefined; ... 5 more ...; taches?: ({ ...; } | undefined)[] | undefined; } | undefined'.
  Types of property 'date_debut' are incompatible.
    Type 'null' is not assignable to type 'string | undefined'.
Error: src/components/projects/ProjectForm.tsx(67,39): error TS2769: No overload matches this call.
  Overload 1 of 2, '(filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<void>', gave the following error.
    Type '"projects"' has no properties in common with type 'InvalidateQueryFilters<unknown>'.
  Overload 2 of 2, '(queryKey?: QueryKey | undefined, filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<...>', gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'readonly unknown[]'.
Error: src/components/projects/ProjectForm.tsx(90,11): error TS2769: No overload matches this call.
  Overload 1 of 2, '(props: { component: ElementType<any, keyof IntrinsicElements>; } & CardContentOwnProps & CommonProps & Omit<any, "children" | ... 3 more ... | "sx">): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2, '(props: DefaultComponentProps<CardContentTypeMap<{}, "div">>): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
Error: src/components/projects/ProjectsPage.tsx(4,26): error TS2307: Cannot find module './ProjectStats' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(5,26): error TS2307: Cannot find module './ProjectsList' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(6,29): error TS2307: Cannot find module './ProjectTimeline' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(7,27): error TS2307: Cannot find module './TasksOverview' or its corresponding type declarations.
Error: src/routes/hr.tsx(4,29): error TS2307: Cannot find module '../components/hr/EmployeeDetails' or its corresponding type declarations.
Error: src/routes/hr.tsx(5,30): error TS2307: Cannot find module '../components/hr/LeaveRequestForm' or its corresponding type declarations.
Error: src/routes/inventory.tsx(4,28): error TS2307: Cannot find module '../components/inventory/ProductDetails' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/routes/production.tsx(4,29): error TS2307: Cannot find module '../components/production/ParcelleDetails' or its corresponding type declarations.
Error: src/services/api.ts(4,24): error TS2339: Property 'env' does not exist on type 'ImportMeta'.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: Process completed with exit code 2.
0s
0s
0s
Post job cleanup.
/usr/bin/git version
git version 2.47.0
Temporarily overriding HOME='/home/runner/work/_temp/ddef9c0a-238a-4763-906a-caca5286c872' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ERP/ERP
/usr/bin/git config --local --name-only --get-regexp core\.sshCommand
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"
/usr/bin/git config --local --name-only --get-regexp http\.https\:\/\/github\.com\/\.extraheader
http.https://github.com/.extraheader
/usr/bin/git config --local --unset-all http.https://github.com/.extraheader
/usr/bin/git submodule foreach --recursive sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/github\.com\/\.extraheader' && git config --local --unset-all 'http.https://github.com/.extraheader' || :"
0s
Cleaning up orphan processes