import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CssBaseline from '@mui/material/CssBaseline';
import { AuthProvider } from './hooks/useAuth';
import { ThemeModeProvider } from './contexts/ThemeModeContext';

// Import des routes
import AppRoutes from './routes/index';
import ComptabilitePage from './components/comptabilite/ComptabilitePage';
import { ProtectedRoute } from './routes/ProtectedRoute';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

const App: React.FC = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeModeProvider>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <Routes>
              {/* Route pour la comptabilité */}
              <Route
                path="/comptabilite/*"
                element={
                  <ProtectedRoute>
                    <ComptabilitePage />
                  </ProtectedRoute>
                }
              />
              
              {/* Autres routes de l'application */}
              <Route path="/*" element={<AppRoutes />} />
            </Routes>
          </Router>
        </AuthProvider>
      </ThemeModeProvider>
    </QueryClientProvider>
  );
};

export default App;
