# Erreurs de type TS2724

Ce fichier liste les erreurs de type TS2724 rencontrées lors du build du frontend.

## Description de l'erreur

TS2724: ... has no exported member named ... Did you mean ...?

## Liste des erreurs

- src/components/comptabilite/rapports/GrandLivre.tsx:20:32 - error TS2724: '"../../../types/comptabilite"' has no exported member named 'LigneGrandLivre'. Did you mean 'GrandLivre'?

  20 import type { CompteComptable LigneGrandLivre } from '../../../types/comptabilite';
                                    ~~~~~~~~~~~~~~~

- src/components/dashboard/__tests__/MLDashboard.test.tsx:5:10 - error TS2724: '"../../../services/dashboard"' has no exported member named 'dashboardService'. Did you mean 'DashboardService'?

  5 import { dashboardService } from '../../../services/dashboard'
             ~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:10:10 - error TS2724: '"../../../services/finance"' has no exported member named 'creerTransaction'. Did you mean 'createTransaction'?

  10 import { creerTransaction modifierTransaction getTransaction getComptes } from '../../../services/finance';
              ~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/ListeTransactions.test.tsx:7:27 - error TS2724: '"../../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?

  7 import { getTransactions TypeTransaction StatutTransaction } from '../../../services/finance';
                              ~~~~~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:10 - error TS2724: '"../../services/finance"' has no exported member named 'creerTransaction'. Did you mean 'createTransaction'?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
              ~~~~~~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:77 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                 ~~~~~~~~~~~

- src/components/finance/FormulaireTransaction.tsx:18:90 - error TS2724: '"../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?

  18 import { creerTransaction modifierTransaction getTransaction getComptes Transaction TypeTransaction StatutTransaction Compte } from '../../services/finance';
                                                                                              ~~~~~~~~~~~~~~~

- src/components/finance/ListeTransactions.tsx:19:27 - error TS2724: '"../../services/finance"' has no exported member named 'Transaction'. Did you mean 'getTransaction'?

  19 import { getTransactions Transaction TypeTransaction } from '../../services/finance';
                               ~~~~~~~~~~~

- src/components/finance/ListeTransactions.tsx:19:40 - error TS2724: '"../../services/finance"' has no exported member named 'TypeTransaction'. Did you mean 'getTransaction'?

  19 import { getTransactions Transaction TypeTransaction } from '../../services/finance';
                                            ~~~~~~~~~~~~~~~

- src/components/finance/ProjectionsFinancieres.tsx:21:37 - error TS2724: '"../../services/finance"' has no exported member named 'ProjectionsFinancieres'. Did you mean 'getProjectionsFinancieres'?

  21 import { getProjectionsFinancieres ProjectionsFinancieres as IProjectionsFinancieres } from '../../services/finance';
                                         ~~~~~~~~~~~~~~~~~~~~~~

- src/components/finance/StatsFinance.tsx:6:27 - error TS2724: '"../../services/finance"' has no exported member named 'FinanceStats'. Did you mean 'getFinanceStats'?

  6 import { getStatsFinance FinanceStats } from '../../services/finance';
                              ~~~~~~~~~~~~

- src/components/projects/__tests__/TaskList.test.tsx:5:10 - error TS2724: '"../../../services/projects"' has no exported member named 'getProjectTasks'. Did you mean 'getProjectStats'?

  5 import { getProjectTasks } from '../../../services/projects';
             ~~~~~~~~~~~~~~~
