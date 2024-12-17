# Erreurs de type TS2322

Ce fichier liste les erreurs de type TS2322 rencontrées lors du build du frontend.

## Description de l'erreur

TS2322: Type ... is not assignable to type ...

## Liste des erreurs

- src/components/dashboard/__tests__/StatsFinance.test.tsx:20:9 - error TS2322: Type '"hausse"' is not assignable to type '"increase" | "decrease"'.

  20         type: 'hausse'
             ~~~~

- src/components/dashboard/__tests__/StatsFinance.test.tsx:55:9 - error TS2322: Type '"baisse"' is not assignable to type '"increase" | "decrease"'.

  55         type: 'baisse'
             ~~~~

- src/components/finance/StatsFinance.tsx:35:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.

  35           variation={stats ? {
               ~~~~~~~~~

- src/components/finance/StatsFinance.tsx:50:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.

  50           variation={stats ? {
               ~~~~~~~~~

- src/components/finance/StatsFinance.tsx:65:11 - error TS2322: Type '{ valeur: Variation; type: "hausse" | "baisse"; } | undefined' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; } | undefined'.
  Type '{ valeur: Variation; type: "hausse" | "baisse"; }' is not assignable to type '{ valeur: number; type: "hausse" | "baisse"; }'.

  65           variation={stats ? {
               ~~~~~~~~~

- src/components/hr/__tests__/LeaveRequestForm.test.tsx:35:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.

  35         open={true}
             ~~~~

- src/components/hr/__tests__/LeaveRequestForm.test.tsx:50:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.

  50         open={true}
             ~~~~

- src/components/hr/__tests__/LeaveRequestForm.test.tsx:66:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.

  66         open={true}
             ~~~~

- src/components/hr/__tests__/LeaveRequestForm.test.tsx:89:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.

  89         open={true}
             ~~~~

- src/components/hr/__tests__/LeaveRequestForm.test.tsx:120:9 - error TS2322: Type '{ open: boolean; onClose: Mock<any any any>; employeeId: string; }' is not assignable to type 'IntrinsicAttributes'.
  Property 'open' does not exist on type 'IntrinsicAttributes'.

  120         open={true}
              ~~~~

- src/components/hr/AttendanceOverview.tsx:65:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "primary"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.

  65             total={stats.totalEmployees}
                 ~~~~~

- src/components/hr/AttendanceOverview.tsx:75:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "info"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.

  75             total={stats.totalEmployees}
                 ~~~~~

- src/components/hr/AttendanceOverview.tsx:85:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "warning"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.

  85             total={stats.totalEmployees}
                 ~~~~~

- src/components/hr/AttendanceOverview.tsx:95:13 - error TS2322: Type '{ title: string; value: number; total: number; icon: Element; color: "error"; }' is not assignable to type 'IntrinsicAttributes & StatCardProps'.
  Property 'total' does not exist on type 'IntrinsicAttributes & StatCardProps'.

  95             total={stats.totalEmployees}
                 ~~~~~

- src/components/inventaire/__tests__/ListeStock.test.tsx:14:3 - error TS2322: Type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: UniteMesure.KG; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' is not assignable to type 'Stock & { produit: Produit; }'.
  Property 'entrepot_id' is missing in type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: UniteMesure.KG; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' but required in type 'Stock'.

   14   {
        ~
   15     id: '1'
      ~~~~~~~~~~~~
  ...
   30     }
      ~~~~~
   31   }
      ~~~

- src/components/inventaire/__tests__/ListeStock.test.tsx:32:3 - error TS2322: Type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: any; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' is not assignable to type 'Stock & { produit: Produit; }'.
  Property 'entrepot_id' is missing in type '{ id: string; produit_id: string; quantite: number; valeur_unitaire: number; emplacement: string; date_derniere_maj: string; produit: { id: string; code: string; nom: string; categorie: CategoryProduit.INTRANT; unite_mesure: any; prix_unitaire: number; seuil_alerte: number; specifications: {}; }; }' but required in type 'Stock'.

   32   {
        ~
   33     id: '2'
      ~~~~~~~~~~~~
  ...
   48     }
      ~~~~~
   49   }
      ~~~

- src/components/projects/ProjectForm.tsx:49:5 - error TS2322: Type 'Resolver<{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; budget: number; nom: string; date_fin_prevue: Date; }>' is not assignable to type 'Resolver<{} any>'.
  Types of parameters 'values' and 'values' are incompatible.
    Type '{}' is missing the following properties from type '{ description?: string | undefined; code: string; date_debut: Date; responsable_id: string; budget: number; nom: string; date_fin_prevue: Date; }': code date_debut responsable_id budget and 2 more.

  49     resolver: yupResolver(schema)
         ~~~~~~~~

- src/components/projects/ProjectForm.tsx:100:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  100                   name="code"
                        ~~~~

- src/components/projects/ProjectForm.tsx:116:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  116                   name="nom"
                        ~~~~

- src/components/projects/ProjectForm.tsx:132:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  132                   name="description"
                        ~~~~

- src/components/projects/ProjectForm.tsx:150:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  150                   name="date_debut"
                        ~~~~

- src/components/projects/ProjectForm.tsx:170:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  170                   name="date_fin_prevue"
                        ~~~~

- src/components/projects/ProjectForm.tsx:190:19 - error TS2322: Type 'string' is not assignable to type 'never'.

  190                   name="budget"
                        ~~~~
