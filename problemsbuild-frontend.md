0s
Current runner version: '2.321.0'
Operating System
Runner Image
Runner Image Provisioner
GITHUB_TOKEN Permissions
Secret source: Actions
Prepare workflow directory
Prepare all required actions
Getting action download info
Download action repository 'actions/checkout@v3' (SHA:f43a0e5ff2bd294095638e18286ca9a3d1956744)
Download action repository 'actions/setup-node@v3' (SHA:1a4442cacd436585916779262731d5b162bc6ec7)
Complete job name: build-frontend
3s
Run actions/checkout@v3
Syncing repository: Kaiser9005/ERP
Getting Git version info
Temporarily overriding HOME='/home/runner/work/_temp/39741761-0ce0-45ef-80a3-ddaf2fd3489a' before making global git config changes
Adding repository directory to the temporary git global config as a safe directory
/usr/bin/git config --global --add safe.directory /home/runner/work/ERP/ERP
Deleting the contents of '/home/runner/work/ERP/ERP'
Initializing the repository
Disabling automatic garbage collection
Setting up auth
Fetching the repository
Determining the checkout info
Checking out the ref
/usr/bin/git log -1 --format='%H'
'aa8f27b6567b92bcce9991cda5bac5be83212dee'
2s
Run actions/setup-node@v3
Attempting to download 16...
Acquiring 16.20.2 - x64 from https://github.com/actions/node-versions/releases/download/16.20.2-5819740093/node-16.20.2-linux-x64.tar.gz
Extracting ...
/usr/bin/tar xz --strip 1 --warning=no-unknown-keyword -C /home/runner/work/_temp/3fb8b6fb-4e37-4996-a764-c2c944cfc417 -f /home/runner/work/_temp/c94d64a9-3688-4bd6-b37e-df1cec82adf3
Adding to the cache ...
Environment details
14s
Run npm install
npm WARN EBADENGINE Unsupported engine {
npm WARN EBADENGINE   package: 'react-hook-form@7.53.1',
npm WARN EBADENGINE   required: { node: '>=18.0.0' },
npm WARN EBADENGINE   current: { node: 'v16.20.2', npm: '8.19.4' }
npm WARN EBADENGINE }
npm WARN deprecated rimraf@3.0.2: Rimraf versions prior to v4 are no longer supported
npm WARN deprecated inflight@1.0.6: This module is not supported, and leaks memory. Do not use it. Check out lru-cache if you want a good and tested way to coalesce async requests by a key value, which is much more comprehensive and powerful.
npm WARN deprecated glob@7.2.3: Glob versions prior to v9 are no longer supported
npm WARN deprecated domexception@4.0.0: Use your platform's native DOMException instead
npm WARN deprecated abab@2.0.6: Use your platform's native atob() and btoa() methods instead
npm WARN deprecated @types/react-leaflet@3.0.0: This is a stub types definition. react-leaflet provides its own type definitions, so you do not need this installed.
npm WARN deprecated @humanwhocodes/object-schema@2.0.3: Use @eslint/object-schema instead
npm WARN deprecated @humanwhocodes/config-array@0.13.0: Use @eslint/config-array instead
npm WARN deprecated eslint@8.57.1: This version is no longer supported. Please see https://eslint.org/version-support for other options.

added 517 packages, and audited 518 packages in 14s

119 packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
0s
Run echo "VITE_WEATHER_API_KEY=" >> .env
7s
Run npm run build

> fofal-erp@0.1.0 build
> tsc && vite build

Error: src/App.tsx(5,1): error TS6133: 'ThemeProvider' is declared but its value is never read.
Error: src/components/hr/AttendanceOverview.tsx(18,28): error TS6133: 'EmployeeStats' is declared but its value is never read.
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
Error: src/components/projects/ProjectStats.tsx(19,10): error TS2305: Module '"../../services/projects"' has no exported member 'projectService'.
Error: src/components/projects/ProjectStats.tsx(136,26): error TS2339: Property 'projets_actifs' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(137,26): error TS2339: Property 'total_projets' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(141,28): error TS2339: Property 'variation_projets_actifs' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(142,33): error TS2339: Property 'variation_projets_actifs' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(150,26): error TS2339: Property 'taches_completees' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(151,26): error TS2339: Property 'total_taches' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(160,26): error TS2339: Property 'taches_retard' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(164,28): error TS2339: Property 'variation_taches_retard' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(165,33): error TS2339: Property 'variation_taches_retard' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(173,26): error TS2339: Property 'heures_travaillees' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(177,28): error TS2339: Property 'variation_heures' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(178,33): error TS2339: Property 'variation_heures' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(197,47): error TS2339: Property 'repartition' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(202,49): error TS2339: Property 'repartition' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(207,47): error TS2339: Property 'repartition' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(212,48): error TS2339: Property 'repartition' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(229,28): error TS2339: Property 'taux_completion' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(233,34): error TS2339: Property 'taux_completion' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(238,28): error TS2339: Property 'projets_termines' does not exist on type '{}'.
Error: src/components/projects/ProjectStats.tsx(238,74): error TS2339: Property 'total_projets' does not exist on type '{}'.
Error: src/components/projects/ProjectsPage.tsx(5,26): error TS2307: Cannot find module './ProjectsList' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(6,29): error TS2307: Cannot find module './ProjectTimeline' or its corresponding type declarations.
Error: src/components/projects/ProjectsPage.tsx(7,27): error TS2307: Cannot find module './TasksOverview' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(2,31): error TS2307: Cannot find module '../components/parametrage/ParametrageLayout' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(3,32): error TS2307: Cannot find module '../components/parametrage/ParametresGeneraux' or its corresponding type declarations.
Error: src/routes/parametrage.tsx(4,34): error TS2307: Cannot find module '../components/parametrage/ConfigurationModules' or its corresponding type declarations.
Error: src/services/api.ts(4,24): error TS2339: Property 'env' does not exist on type 'ImportMeta'.
Error: src/services/dashboard.ts(1,1): error TS6133: 'api' is declared but its value is never read.
Error: src/types/project.ts(1,22): error TS2307: Cannot find module './task' or its corresponding type declarations.
Error: Process completed with exit code 2.
0s
0s
0s
