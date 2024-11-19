build-frontend
failed 1 minute ago in 27s
Search logs
1s
4s
0s
14s
0s
6s
Run cd frontend

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
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
Error: src/components/finance/TransactionDetails.tsx(152,48): error TS2339: Property 'libelle' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(163,53): error TS2339: Property 'libelle' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(174,46): error TS2339: Property 'nom' does not exist on type 'string'.
Error: src/components/finance/TransactionDetails.tsx(174,76): error TS2339: Property 'prenom' does not exist on type 'string'.
Error: src/components/finance/TransactionForm.tsx(31,34): error TS2769: No overload matches this call.
  Overload 1 of 4, '(keys: string | string[], builder: ConditionBuilder<StringSchema<string | undefined, AnyObject, undefined, "">>): StringSchema<string | undefined, AnyObject, undefined, "">', gave the following error.
    Object literal may only specify known properties, and 'is' does not exist in type 'ConditionBuilder<StringSchema<string | undefined, AnyObject, undefined, "">>'.
  Overload 2 of 4, '(keys: string | string[], options: ConditionConfig<StringSchema<string | undefined, AnyObject, undefined, "">>): StringSchema<string | undefined, AnyObject, undefined, "">', gave the following error.
    Type 'StringSchema<string, AnyObject, undefined, "">' is not assignable to type '(schema: StringSchema<string | undefined, AnyObject, undefined, "">) => ISchema<any, any, any, any>'.
      Type 'StringSchema<string, AnyObject, undefined, "">' provides no match for the signature '(schema: StringSchema<string | undefined, AnyObject, undefined, "">): ISchema<any, any, any, any>'.
Error: src/components/finance/TransactionForm.tsx(35,39): error TS2769: No overload matches this call.
  Overload 1 of 4, '(keys: string | string[], builder: ConditionBuilder<StringSchema<string | undefined, AnyObject, undefined, "">>): StringSchema<string | undefined, AnyObject, undefined, "">', gave the following error.
    Object literal may only specify known properties, and 'is' does not exist in type 'ConditionBuilder<StringSchema<string | undefined, AnyObject, undefined, "">>'.
  Overload 2 of 4, '(keys: string | string[], options: ConditionConfig<StringSchema<string | undefined, AnyObject, undefined, "">>): StringSchema<string | undefined, AnyObject, undefined, "">', gave the following error.
    Type 'StringSchema<string, AnyObject, undefined, "">' is not assignable to type '(schema: StringSchema<string | undefined, AnyObject, undefined, "">) => ISchema<any, any, any, any>'.
      Type 'StringSchema<string, AnyObject, undefined, "">' provides no match for the signature '(schema: StringSchema<string | undefined, AnyObject, undefined, "">): ISchema<any, any, any, any>'.
Error: src/components/finance/TransactionForm.tsx(53,38): error TS2769: No overload matches this call.
  The last overload gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'QueryKey'.
Error: src/components/finance/TransactionForm.tsx(56,5): error TS2322: Type 'Resolver<{ description?: string | undefined; compte_source_id?: string | undefined; compte_destination_id?: string | undefined; reference: string; date_transaction: Date; type_transaction: string; categorie: string; montant: number; }>' is not assignable to type 'Resolver<Transaction, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type 'Transaction' is not assignable to type '{ description?: string | undefined; compte_source_id?: string | undefined; compte_destination_id?: string | undefined; reference: string; date_transaction: Date; type_transaction: string; categorie: string; montant: number; }'.
      Types of property 'date_transaction' are incompatible.
        Type 'string' is not assignable to type 'Date'.
Error: src/components/finance/TransactionForm.tsx(57,5): error TS2322: Type '{ reference: string; date_transaction: Date; type_transaction: string; categorie: string; montant: string; description: string; compte_source_id: string; compte_destination_id: string; }' is not assignable to type 'AsyncDefaultValues<Transaction> | { id?: string | undefined; reference?: string | undefined; date_transaction?: string | undefined; type_transaction?: string | undefined; ... 8 more ...; date_validation?: string | undefined; } | undefined'.
  Types of property 'date_transaction' are incompatible.
    Type 'Date' is not assignable to type 'string'.
Error: src/components/finance/TransactionForm.tsx(75,39): error TS2769: No overload matches this call.
  Overload 1 of 2, '(filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<void>', gave the following error.
    Type '"transactions"' has no properties in common with type 'InvalidateQueryFilters<unknown>'.
  Overload 2 of 2, '(queryKey?: QueryKey | undefined, filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<...>', gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'readonly unknown[]'.
Error: src/components/finance/TransactionForm.tsx(98,11): error TS2769: No overload matches this call.
  Overload 1 of 2, '(props: { component: ElementType<any, keyof IntrinsicElements>; } & CardContentOwnProps & CommonProps & Omit<any, "children" | ... 3 more ... | "sx">): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2, '(props: DefaultComponentProps<CardContentTypeMap<{}, "div">>): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
Error: src/components/finance/TransactionForm.tsx(207,21): error TS2820: Type '"compte_source_id"' is not assignable to type '"id" | "reference" | "date_transaction" | "type_transaction" | "categorie" | "montant" | "description" | "statut" | "piece_jointe" | "compte_source" | "compte_destination" | "validee_par" | "date_validation"'. Did you mean '"compte_source"'?
Error: src/components/finance/TransactionForm.tsx(215,41): error TS2551: Property 'compte_source_id' does not exist on type 'FieldErrors<Transaction>'. Did you mean 'compte_source'?
Error: src/components/finance/TransactionForm.tsx(216,44): error TS2551: Property 'compte_source_id' does not exist on type 'FieldErrors<Transaction>'. Did you mean 'compte_source'?
Error: src/components/finance/TransactionForm.tsx(218,35): error TS2339: Property 'map' does not exist on type '{}'.
Error: src/components/finance/TransactionForm.tsx(218,40): error TS7006: Parameter 'compte' implicitly has an 'any' type.
Error: src/components/finance/TransactionForm.tsx(232,21): error TS2820: Type '"compte_destination_id"' is not assignable to type '"id" | "reference" | "date_transaction" | "type_transaction" | "categorie" | "montant" | "description" | "statut" | "piece_jointe" | "compte_source" | "compte_destination" | "validee_par" | "date_validation"'. Did you mean '"compte_destination"'?
Error: src/components/finance/TransactionForm.tsx(240,41): error TS2551: Property 'compte_destination_id' does not exist on type 'FieldErrors<Transaction>'. Did you mean 'compte_destination'?
Error: src/components/finance/TransactionForm.tsx(241,44): error TS2551: Property 'compte_destination_id' does not exist on type 'FieldErrors<Transaction>'. Did you mean 'compte_destination'?
Error: src/components/finance/TransactionForm.tsx(243,35): error TS2339: Property 'map' does not exist on type '{}'.
Error: src/components/finance/TransactionForm.tsx(243,40): error TS7006: Parameter 'compte' implicitly has an 'any' type.
Error: src/components/finance/TransactionsList.tsx(27,43): error TS2769: No overload matches this call.
  The last overload gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'QueryKey'.
Error: src/components/finance/TransactionsList.tsx(29,46): error TS2339: Property 'filter' does not exist on type '{}'.
Error: src/components/finance/TransactionsList.tsx(29,53): error TS7006: Parameter 'transaction' implicitly has an 'any' type.
Error: src/components/finance/TransactionsList.tsx(78,41): error TS7006: Parameter 'transaction' implicitly has an 'any' type.
Error: src/components/hr/EmployeeForm.tsx(18,61): error TS2307: Cannot find module '../../services/hr' or its corresponding type declarations.
Error: src/components/hr/EmployeeForm.tsx(69,39): error TS2769: No overload matches this call.
  Overload 1 of 2, '(filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<void>', gave the following error.
    Type '"employees"' has no properties in common with type 'InvalidateQueryFilters<unknown>'.
  Overload 2 of 2, '(queryKey?: QueryKey | undefined, filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<...>', gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'readonly unknown[]'.
Error: src/components/hr/EmployeeForm.tsx(92,11): error TS2769: No overload matches this call.
  Overload 1 of 2, '(props: { component: ElementType<any, keyof IntrinsicElements>; } & CardContentOwnProps & CommonProps & Omit<any, "children" | ... 3 more ... | "sx">): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2, '(props: DefaultComponentProps<CardContentTypeMap<{}, "div">>): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
Error: src/components/hr/HRPage.tsx(4,27): error TS2307: Cannot find module './EmployeeStats' or its corresponding type declarations.
Error: src/components/hr/HRPage.tsx(5,27): error TS2307: Cannot find module './EmployeesList' or its corresponding type declarations.
Error: src/components/hr/HRPage.tsx(6,27): error TS2307: Cannot find module './LeaveRequests' or its corresponding type declarations.
Error: src/components/hr/HRPage.tsx(7,32): error TS2307: Cannot find module './AttendanceOverview' or its corresponding type declarations.
Error: src/components/inventory/InventoryPage.tsx(4,28): error TS2307: Cannot find module './InventoryStats' or its corresponding type declarations.
Error: src/components/inventory/InventoryPage.tsx(5,23): error TS2307: Cannot find module './StockList' or its corresponding type declarations.
Error: src/components/inventory/InventoryPage.tsx(6,29): error TS2307: Cannot find module './MovementHistory' or its corresponding type declarations.
Error: src/components/inventory/ProductForm.tsx(17,58): error TS2307: Cannot find module '../../services/inventory' or its corresponding type declarations.
Error: src/components/inventory/ProductForm.tsx(66,39): error TS2769: No overload matches this call.
  Overload 1 of 2, '(filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<void>', gave the following error.
    Type '"products"' has no properties in common with type 'InvalidateQueryFilters<unknown>'.
  Overload 2 of 2, '(queryKey?: QueryKey | undefined, filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<...>', gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'readonly unknown[]'.
Error: src/components/inventory/ProductForm.tsx(89,11): error TS2769: No overload matches this call.
  Overload 1 of 2, '(props: { component: ElementType<any, keyof IntrinsicElements>; } & CardContentOwnProps & CommonProps & Omit<any, "children" | ... 3 more ... | "sx">): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2, '(props: DefaultComponentProps<CardContentTypeMap<{}, "div">>): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
Error: src/components/production/ParcelleForm.tsx(18,10): error TS2614: Module '"../../services/production"' has no exported member 'createParcelle'. Did you mean to use 'import createParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(18,26): error TS2614: Module '"../../services/production"' has no exported member 'updateParcelle'. Did you mean to use 'import updateParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(18,42): error TS2614: Module '"../../services/production"' has no exported member 'getParcelle'. Did you mean to use 'import getParcelle from "../../services/production"' instead?
Error: src/components/production/ParcelleForm.tsx(61,39): error TS2769: No overload matches this call.
  Overload 1 of 2, '(filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<void>', gave the following error.
    Type '"parcelles"' has no properties in common with type 'InvalidateQueryFilters<unknown>'.
  Overload 2 of 2, '(queryKey?: QueryKey | undefined, filters?: InvalidateQueryFilters<unknown> | undefined, options?: InvalidateOptions | undefined): Promise<...>', gave the following error.
    Argument of type 'string' is not assignable to parameter of type 'readonly unknown[]'.
Error: src/components/production/ParcelleForm.tsx(84,11): error TS2769: No overload matches this call.
  Overload 1 of 2, '(props: { component: ElementType<any, keyof IntrinsicElements>; } & CardContentOwnProps & CommonProps & Omit<any, "children" | ... 3 more ... | "sx">): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
  Overload 2 of 2, '(props: DefaultComponentProps<CardContentTypeMap<{}, "div">>): Element | null', gave the following error.
    Type 'unknown' is not assignable to type 'ReactNode'.
Error: src/components/production/ParcelleMap.tsx(6,21): error TS2307: Cannot find module '/home/user/ERP/src/services/api' or its corresponding type declarations.
Error: src/components/production/ProductionDashboard.tsx(61,13): error TS6133: 'detailedData' is declared but its value is never read.
Error: src/components/production/ProductionDashboard.tsx(68,28): error TS6133: 'event' is declared but its value is never read.
Error: src/components/production/ProductionPage.tsx(4,29): error TS2307: Cannot find module './ProductionStats' or its corresponding type declarations.
Error: src/components/production/ProductionPage.tsx(5,27): error TS2307: Cannot find module './ParcellesList' or its corresponding type declarations.
Error: src/components/projects/ProjectDetails.tsx(9,3): error TS6133: 'Button' is declared but its value is never read.
Error: src/components/projects/ProjectDetails.tsx(10,3): error TS6133: 'Link' is declared but its value is never read.
Error: src/components/projects/ProjectDetails.tsx(19,22): error TS2307: Cannot find module './TaskList' or its corresponding type declarations.
Error: src/components/projects/ProjectForm.tsx(10,3): error TS6133: 'MenuItem' is declared but its value is never read.
Error: src/components/projects/ProjectForm.tsx(49,5): error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; nom: string; date_debut: Date; responsable_id: string; date_fin_prevue: Date; budget: number; }>' is not assignable to type 'Resolver<Project, any>'.
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