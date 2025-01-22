import { RouteObject } from 'react-router-dom';
import ProductionPage from '../components/production/ProductionPage';
import ParcelleForm from '../components/production/ParcelleForm';
import ParcelleDetails from '../components/production/ParcelleDetails';

export const productionRoutes: RouteObject[] = [
  {
    path: 'production',
    children: [
      {
        index: true,
        element: <ProductionPage />
      },
      {
        path: 'parcelles/new',
        element: <ParcelleForm />
      },
      {
        path: 'parcelles/:id',
        element: <ParcelleDetails />
      },
      {
        path: 'parcelles/:id/edit',
        element: <ParcelleForm />
      }
    ]
  }
];