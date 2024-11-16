import React, { lazy, Suspense } from 'react';
import { Navigate } from 'react-router-dom';
import { ProtectedRoute } from './ProtectedRoute';
import { CircularProgress, Box } from '@mui/material';

// Lazy loading des composants de comptabilité
const ComptabilitePage = lazy(() => import('../components/comptabilite/ComptabilitePage'));
const ComptesList = lazy(() => import('../components/comptabilite/ComptesList'));
const EcrituresForm = lazy(() => import('../components/comptabilite/EcrituresForm'));
const JournauxList = lazy(() => import('../components/comptabilite/JournauxList'));
const GrandLivre = lazy(() => import('../components/comptabilite/rapports/GrandLivre'));
const Balance = lazy(() => import('../components/comptabilite/rapports/Balance'));
const Bilan = lazy(() => import('../components/comptabilite/rapports/Bilan'));
const CompteResultat = lazy(() => import('../components/comptabilite/rapports/CompteResultat'));

// Composant de chargement
const LoadingComponent = () => (
  <Box 
    sx={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh' 
    }}
  >
    <CircularProgress />
  </Box>
);

const ComptabiliteRoutes = () => {
  return [
    {
      path: '/comptabilite',
      element: (
        <ProtectedRoute>
          <Suspense fallback={<LoadingComponent />}>
            <ComptabilitePage />
          </Suspense>
        </ProtectedRoute>
      ),
      children: [
        {
          index: true,
          element: <Navigate to="dashboard" replace />
        },
        {
          path: 'comptes',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <ComptesList />
            </Suspense>
          )
        },
        {
          path: 'ecritures/new',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <EcrituresForm />
            </Suspense>
          )
        },
        {
          path: 'journaux',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <JournauxList />
            </Suspense>
          )
        },
        {
          path: 'rapports/grand-livre',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <GrandLivre />
            </Suspense>
          )
        },
        {
          path: 'rapports/balance',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <Balance />
            </Suspense>
          )
        },
        {
          path: 'rapports/bilan',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <Bilan />
            </Suspense>
          )
        },
        {
          path: 'rapports/compte-resultat',
          element: (
            <Suspense fallback={<LoadingComponent />}>
              <CompteResultat />
            </Suspense>
          )
        }
      ]
    }
  ];
};

export default ComptabiliteRoutes;
