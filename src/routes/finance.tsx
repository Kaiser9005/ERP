import { RouteObject } from 'react-router-dom';
import FinancePage from '../components/finance/FinancePage';
import TransactionForm from '../components/finance/TransactionForm';
import TransactionDetails from '../components/finance/TransactionDetails';

export const financeRoutes: RouteObject[] = [
  {
    path: 'finance',
    children: [
      {
        index: true,
        element: <FinancePage />
      },
      {
        path: 'transactions/new',
        element: <TransactionForm />
      },
      {
        path: 'transactions/:id',
        element: <TransactionDetails />
      },
      {
        path: 'transactions/:id/edit',
        element: <TransactionForm />
      }
    ]
  }
];