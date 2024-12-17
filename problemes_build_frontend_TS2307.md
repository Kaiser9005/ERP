# Erreurs de type TS2307

Ce fichier liste les erreurs de type TS2307 rencontrées lors du build du frontend.

## Description de l'erreur

TS2307: Cannot find module ... or its corresponding type declarations.

## Liste des erreurs

- src/components/dashboard/__tests__/MLDashboard.test.tsx:4:25 - error TS2307: Cannot find module '../MLDashboard' or its corresponding type declarations.

  4 import MLDashboard from '../MLDashboard'
                            ~~~~~~~~~~~~~~~~

- src/components/documents/DocumentUploadDialog.tsx:14:29 - error TS2307: Cannot find module 'react-dropzone' or its corresponding type declarations.

  14 import { useDropzone } from 'react-dropzone';
                                 ~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/BudgetOverview.test.tsx:4:28 - error TS2307: Cannot find module '../BudgetOverview' or its corresponding type declarations.

  4 import BudgetOverview from '../BudgetOverview';
                               ~~~~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/FinancePage.test.tsx:5:25 - error TS2307: Cannot find module '../FinancePage' or its corresponding type declarations.

  5 import FinancePage from '../FinancePage';
                            ~~~~~~~~~~~~~~~~

- src/components/finance/__tests__/TransactionList.test.tsx:5:29 - error TS2307: Cannot find module '../TransactionList' or its corresponding type declarations.

  5 import TransactionList from '../TransactionList';
                                ~~~~~~~~~~~~~~~~~~~~

- src/components/production/ParcelleMap.tsx:6:21 - error TS2307: Cannot find module '/home/user/ERP/src/services/api' or its corresponding type declarations.

  6 import { api } from "/home/user/ERP/src/services/api"
                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/routes/inventory.tsx:2:27 - error TS2307: Cannot find module '../components/inventory/InventoryPage' or its corresponding type declarations.

  2 import InventoryPage from '../components/inventory/InventoryPage';
                              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/routes/inventory.tsx:3:25 - error TS2307: Cannot find module '../components/inventory/ProductForm' or its corresponding type declarations.

  3 import ProductForm from '../components/inventory/ProductForm';
                            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- src/routes/inventory.tsx:4:28 - error TS2307: Cannot find module '../components/inventory/ProductDetails' or its corresponding type declarations.

  4 import ProductDetails from '../components/inventory/ProductDetails';
                               ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
