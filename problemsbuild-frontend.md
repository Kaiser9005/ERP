6s
Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(13,24): error TS6133: 'isLoading' is declared but its value is never read.
Error: src/components/dashboard/DashboardPage.tsx(28,13): error TS2322: Type '{ value: number; type: "increase" | "decrease"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Property 'valeur' is missing in type '{ value: number; type: "increase" | "decrease"; }' but required in type '{ valeur: number; type: "hausse" | "baisse"; }'.
Error: src/components/dashboard/DashboardPage.tsx(39,13): error TS2322: Type '{ value: number; type: "increase" | "decrease"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Property 'valeur' is missing in type '{ value: number; type: "increase" | "decrease"; }' but required in type '{ valeur: number; type: "hausse" | "baisse"; }'.
Error: src/components/dashboard/DashboardPage.tsx(50,13): error TS2322: Type '{ value: number; type: "increase" | "decrease"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Property 'valeur' is missing in type '{ value: number; type: "increase" | "decrease"; }' but required in type '{ valeur: number; type: "hausse" | "baisse"; }'.
Error: src/components/dashboard/DashboardPage.tsx(60,13): error TS2322: Type '{ value: number; type: "increase" | "decrease"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Property 'valeur' is missing in type '{ value: number; type: "increase" | "decrease"; }' but required in type '{ valeur: number; type: "hausse" | "baisse"; }'.
Error: src/components/hr/HRPage.tsx(5,27): error TS2307: Cannot find module './EmployeesList' or its corresponding type declarations.
Error: src/components/hr/HRPage.tsx(6,27): error TS2307: Cannot find module './LeaveRequests' or its corresponding type declarations.
Error: src/components/hr/HRPage.tsx(7,32): error TS2307: Cannot find module './AttendanceOverview' or its corresponding type declarations.
Error: src/components/inventaire/DetailsProduit.tsx(18,49): error TS2307: Cannot find module '../../services/inventory' or its corresponding type declarations.
Error: src/components/inventaire/DetailsProduit.tsx(23,33): error TS2307: Cannot find module './StockMovementDialog' or its corresponding type declarations.
Error: src/components/inventaire/DetailsProduit.tsx(40,9): error TS6133: 'getStockLevel' is declared but its value is never read.
Error: src/components/inventaire/DetailsProduit.tsx(138,36): error TS7006: Parameter 'movement' implicitly has an 'any' type.
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
Error: src/components/projects/ProjectForm.tsx(49,5): error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; budget: number; }>' is not assignable to type 'Resolver<Project, any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Property 'responsable_id' is missing in type 'Project' but required in type '{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; nom: string; date_fin_prevue: Date; budget: number; }'.
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
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/routes/production.tsx(4,29): error TS2307: Cannot find module '../components/production/ParcelleDetails' or its corresponding type declarations.
Error: src/services/api.ts(4,24): error TS2339: Property 'env' does not exist on type 'ImportMeta'.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: Process completed with exit code 2.