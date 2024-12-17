# Erreurs de type TS2305

Ce fichier liste les erreurs de type TS2305 rencontrées lors du build du frontend.

## Description de l'erreur

TS2305: Module ... has no exported member ...

## Liste des erreurs

- src/components/finance/__tests__/FormulaireTransaction.test.tsx:11:28 - error TS2305: Module '"../../../types/finance"' has no exported member 'Compte'.

  11 import type { Transaction Compte } from '../../../types/finance';
                                ~~~~~~

- src/components/inventaire/__tests__/DetailsProduit.test.tsx:7:22 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'getProductMovements'.

  7 import { getProduit getProductMovements } from '../../../services/inventaire';
                         ~~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/FormulaireProduit.test.tsx:7:53 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'verifierCodeUnique'.

  7 import { creerProduit modifierProduit getProduit verifierCodeUnique } from '../../../services/inventaire';
                                                        ~~~~~~~~~~~~~~~~~~

- src/components/inventaire/__tests__/HistoriqueMouvements.test.tsx:6:25 - error TS2305: Module '"../../../services/inventaire"' has no exported member 'getTendances'.

  6 import { getMouvements getTendances } from '../../../services/inventaire';
                            ~~~~~~~~~~~~

- src/components/projects/__tests__/TasksOverview.test.tsx:5:10 - error TS2305: Module '"../../../services/projects"' has no exported member 'getRecentTasks'.

  5 import { getRecentTasks } from '../../../services/projects';
             ~~~~~~~~~~~~~~
