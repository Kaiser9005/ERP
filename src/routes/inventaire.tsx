import { RouteObject } from 'react-router-dom';
import ProtectedRoute from './ProtectedRoute';
import PageInventaire from '../components/inventaire/PageInventaire';
import FormulaireProduit from '../components/inventaire/FormulaireProduit';
import StatsInventaire from '../components/inventaire/StatsInventaire';
import ListeStock from '../components/inventaire/ListeStock';
import HistoriqueMouvements from '../components/inventaire/HistoriqueMouvements';
import DetailsProduit from '../components/inventaire/DetailsProduit';

export const inventaireRoutes: RouteObject[] = [
  {
    path: 'inventaire',
    children: [
      {
        index: true,
        element: (
          <ProtectedRoute>
            <PageInventaire />
          </ProtectedRoute>
        )
      },
      {
        path: 'stats',
        element: (
          <ProtectedRoute>
            <StatsInventaire />
          </ProtectedRoute>
        )
      },
      {
        path: 'stock',
        element: (
          <ProtectedRoute>
            <ListeStock />
          </ProtectedRoute>
        )
      },
      {
        path: 'historique',
        element: (
          <ProtectedRoute>
            <HistoriqueMouvements />
          </ProtectedRoute>
        )
      },
      {
        path: 'produits/nouveau',
        element: (
          <ProtectedRoute>
            <FormulaireProduit />
          </ProtectedRoute>
        )
      },
      {
        path: 'produits/:id',
        element: (
          <ProtectedRoute>
            <DetailsProduit />
          </ProtectedRoute>
        )
      },
      {
        path: 'produits/:id/modifier',
        element: (
          <ProtectedRoute>
            <FormulaireProduit />
          </ProtectedRoute>
        )
      }
    ]
  }
];
