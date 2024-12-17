# Erreurs de type TS6133

Ce fichier liste les erreurs de type TS6133 rencontrées lors du build du frontend.

## Description de l'erreur

TS6133: ... is declared but its value is never read.

## Liste des erreurs

- src/components/dashboard/__tests__/DashboardPage.perf.tsx:23:7 - error TS6133: 'wrapper' is declared but its value is never read.

  23 const wrapper = ({ children }: { children: React.ReactNode }) => (
           ~~~~~~~

- src/components/dashboard/__tests__/StatsFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/dashboard/__tests__/StatsProduction.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/dashboard/__tests__/StatsRH.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/dashboard/__tests__/WidgetMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/dashboard/AlertsPanel.tsx:38:7 - error TS6133: 'getSeverityColor' is declared but its value is never read.

  38 const getSeverityColor = (severity: 'low' | 'medium' | 'high') => {
           ~~~~~~~~~~~~~~~~

- src/components/dashboard/ModuleCard.tsx:20:3 - error TS6133: 'module' is declared but its value is never read.

  20   module
       ~~~~~~

- src/components/dashboard/modules/InventoryModule.tsx:15:9 - error TS6133: 'formatCurrency' is declared but its value is never read.

  15   const formatCurrency = (amount: number) => {
             ~~~~~~~~~~~~~~

- src/components/documents/DocumentList.tsx:35:28 - error TS6133: 'isLoading' is declared but its value is never read.

  35   const { data: documents isLoading } = useQuery(
                                ~~~~~~~~~

- src/components/finance/__tests__/AnalyseBudget.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:28 - error TS6133: 'modifierTransaction' is declared but its value is never read.

  10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                ~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:49 - error TS6133: 'getTransaction' is declared but its value is never read.

  10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                                     ~~~~~~~~~~~~~~

- src/components/finance/__tests__/GraphiqueTresorerie.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/ListeTransactions.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/PageFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/ProjectionsFinancieres.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/StatsFinance.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/VueBudget.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/AnalyseBudget.tsx:25:9 - error TS6133: 'theme' is declared but its value is never read.

  25   const theme = useTheme();
             ~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:90 - error TS6133: 'TypeTransaction' is declared but its value is never read.

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                                ~~~~~~~~~~~~~~~

- src/components/finance/ListeTransactions.tsx:27:36 - error TS6133: 'isLoading' is declared but its value is never read.

  27   const { data: transactions = [] isLoading } = useQuery<Transaction[]>('transactions' getTransactions);
                                        ~~~~~~~~~

- src/components/finance/PageFinance.tsx:43:35 - error TS6133: 'event' is declared but its value is never read.

  43   const handleChangementOnglet = (event: React.SyntheticEvent nouvelOnglet: number) => {
                                       ~~~~~

- src/components/finance/ProjectionsFinancieres.tsx:7:3 - error TS6133: 'Grid' is declared but its value is never read.

  7   Grid
      ~~~~

- src/components/finance/ProjectionsFinancieres.tsx:28:9 - error TS6133: 'theme' is declared but its value is never read.

  28   const theme = useTheme();
             ~~~~~

- src/components/hr/__tests__/AttendanceChart.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/__tests__/EmployeeDetails.test.tsx:2:37 - error TS6133: 'waitFor' is declared but its value is never read.

  2 import { render screen fireEvent waitFor } from '@testing-library/react';
                                        ~~~~~~~

- src/components/hr/__tests__/EmployeeForm.test.tsx:6:26 - error TS6133: 'updateEmployee' is declared but its value is never read.

  6 import { createEmployee updateEmployee getEmployee } from '../../../services/hr';
                             ~~~~~~~~~~~~~~

- src/components/hr/__tests__/EmployeeForm.test.tsx:6:42 - error TS6133: 'getEmployee' is declared but its value is never read.

  6 import { createEmployee updateEmployee getEmployee } from '../../../services/hr';
                                             ~~~~~~~~~~~

- src/components/hr/analytics/__tests__/HRAnalyticsDashboard.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/analytics/HRAnalyticsDashboard.tsx:7:1 - error TS6133: 'queryKeys' is declared but its value is never read.

  7 import { queryKeys } from '../../../config/queryClient';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/formation/__tests__/FormationForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/formation/__tests__/FormationList.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/formation/__tests__/FormationPage.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/types/formTypes.ts:1:38 - error TS6133: 'UseFormRegister' is declared but its value is never read.

  1 import { Control FieldErrors Path UseFormRegister } from 'react-hook-form';
                                         ~~~~~~~~~~~~~~~

- src/components/hr/weather/__tests__/CarteMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/hr/weather/__tests__/TableauDeBordMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/DetailsProduit.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/DialogueMouvementStock.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/FormulaireProduit.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/StatsInventaire.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/parametrage/ConfigurationModules.tsx:10:3 - error TS6133: 'IconButton' is declared but its value is never read.

  10   IconButton
       ~~~~~~~~~~

- src/components/production/__tests__/ParcelleForm.test.tsx:6:26 - error TS6133: 'updateParcelle' is declared but its value is never read.

  6 import { createParcelle updateParcelle getParcelle } from '../../../services/production';
                             ~~~~~~~~~~~~~~

- src/components/production/__tests__/ParcelleForm.test.tsx:6:42 - error TS6133: 'getParcelle' is declared but its value is never read.

  6 import { createParcelle updateParcelle getParcelle } from '../../../services/production';
                                             ~~~~~~~~~~~

- src/components/production/__tests__/ParcellesList.test.tsx:2:26 - error TS6133: 'fireEvent' is declared but its value is never read.

  2 import { render screen fireEvent } from '@testing-library/react';
                             ~~~~~~~~~

- src/components/production/__tests__/TableauMeteo.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/projects/__tests__/ProjectDetails.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/projects/__tests__/ProjectForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/projects/__tests__/TaskForm.test.tsx:1:1 - error TS6133: 'React' is declared but its value is never read.

  1 import React from 'react';
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/components/projects/ProjectDetails.tsx:9:3 - error TS6133: 'Button' is declared but its value is never read.

  9   Button
      ~~~~~~

- src/components/projects/ProjectDetails.tsx:10:3 - error TS6133: 'Link' is declared but its value is never read.

  10   Link
       ~~~~

- src/components/projects/TaskForm.tsx:23:50 - error TS6133: 'Task' is declared but its value is never read.

  23 import { TaskStatus TaskPriority TaskCategory Task TaskFormData } from '../../types/task';
                                                      ~~~~

- src/routes/comptabilite.tsx:1:8 - error TS6133: 'React' is declared but its value is never read.

  1 import React { lazy Suspense } from 'react';
           ~~~~~

- src/services/comptabilite.ts:17:3 - error TS6133: 'RapportComptable' is declared but its value is never read.

  17   RapportComptable
       ~~~~~~~~~~~~~~~~

- src/services/hr.ts:42:36 - error TS6133: 'queryKey' is declared but its value is never read.

  42 export const getEmployees = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'employees']>): Promise<Employee[]> => {
                                        ~~~~~~~~~~~~

- src/services/hr.ts:96:33 - error TS6133: 'queryKey' is declared but its value is never read.

  96 export const getLeaves = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'leaves']>): Promise<Leave[]> => {
                                     ~~~~~~~~~~~~

- src/services/hr.ts:156:36 - error TS6133: 'queryKey' is declared but its value is never read.

  156 export const getTrainings = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'trainings']>): Promise<Training[]> => {
                                         ~~~~~~~~~~~~

- src/services/hr.ts:184:38 - error TS6133: 'queryKey' is declared but its value is never read.

  184 export const getAttendances = async ({ queryKey }: QueryFunctionContext<readonly ['hr' 'attendances']>): Promise<Attendance[]> => {
                                           ~~~~~~~~~~~~
