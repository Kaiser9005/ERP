import { RouteObject } from 'react-router-dom';
import InventoryPage from '../components/inventory/InventoryPage';
import ProductForm from '../components/inventory/ProductForm';
import ProductDetails from '../components/inventory/ProductDetails';

export const inventoryRoutes: RouteObject[] = [
  {
    path: 'inventory',
    children: [
      {
        index: true,
        element: <InventoryPage />
      },
      {
        path: 'products/new',
        element: <ProductForm />
      },
      {
        path: 'products/:id',
        element: <ProductDetails />
      },
      {
        path: 'products/:id/edit',
        element: <ProductForm />
      }
    ]
  }
];