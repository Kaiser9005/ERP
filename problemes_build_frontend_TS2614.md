# Erreurs de type TS2614

Ce fichier liste les erreurs de type TS2614 rencontrées lors du build du frontend.

## Description de l'erreur

TS2614: Module ... has no exported member ...

## Liste des erreurs

- src/components/dashboard/__tests__/StatsProduction.test.tsx:6:10 - error TS2614: Module '"../../../services/production"' has no exported member 'getStatsProduction'. Did you mean to use 'import getStatsProduction from "../../../services/production"' instead?

  6 import { getStatsProduction } from '../../../services/production';
             ~~~~~~~~~~~~~~~~~~

- src/components/dashboard/StatisticsCards.tsx:6:10 - error TS2614: Module '"../../services/dashboard"' has no exported member 'getDashboardStats'. Did you mean to use 'import getDashboardStats from "../../services/dashboard"' instead?

  6 import { getDashboardStats } from '../../services/dashboard';
             ~~~~~~~~~~~~~~~~~

- src/components/dashboard/StatsProduction.tsx:4:10 - error TS2614: Module '"../../services/production"' has no exported member 'getStatsProduction'. Did you mean to use 'import getStatsProduction from "../../services/production"' instead?

  4 import { getStatsProduction } from '../../services/production';
             ~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/BudgetOverview.test.tsx:5:10 - error TS2614: Module '"../../../services/finance"' has no exported member 'getBudgetOverview'. Did you mean to use 'import getBudgetOverview from "../../../services/finance"' instead?

  5 import { getBudgetOverview } from '../../../services/finance';
             ~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:28 - error TS2614: Module '"../../../services/finance"' has no exported member 'modifierTransaction'. Did you mean to use 'import modifierTransaction from "../../../services/finance"' instead?

  10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                ~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:65 - error TS2614: Module '"../../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../../services/finance"' instead?

  10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
                                                                     ~~~~~~~~~~

- src/components/finance/__tests__/ListeTransactions.test.tsx:7:44 - error TS2614: Module '"../../../services/finance"' has no exported member 'StatutTransaction'. Did you mean to use 'import StatutTransaction from "../../../services/finance"' instead?

  7 import { getTransactions TypeTransaction StatutTransaction } from '../../../services/finance';
                                               ~~~~~~~~~~~~~~~~~

- src/components/finance/AnalyseBudget.tsx:20:28 - error TS2614: Module '"../../services/finance"' has no exported member 'AnalyseBudgetaire'. Did you mean to use 'import AnalyseBudgetaire from "../../services/finance"' instead?

  20 import { getAnalyseBudget AnalyseBudgetaire } from '../../services/finance';
                                ~~~~~~~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:28 - error TS2614: Module '"../../services/finance"' has no exported member 'modifierTransaction'. Did you mean to use 'import modifierTransaction from "../../services/finance"' instead?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                ~~~~~~~~~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:65 - error TS2614: Module '"../../services/finance"' has no exported member 'getComptes'. Did you mean to use 'import getComptes from "../../services/finance"' instead?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                     ~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:107 - error TS2614: Module '"../../services/finance"' has no exported member 'StatutTransaction'. Did you mean to use 'import StatutTransaction from "../../services/finance"' instead?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                                               ~~~~~~~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:126 - error TS2614: Module '"../../services/finance"' has no exported member 'Compte'. Did you mean to use 'import Compte from "../../services/finance"' instead?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                                                                  ~~~~~~
