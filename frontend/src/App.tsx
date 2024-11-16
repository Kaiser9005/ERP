import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { AuthProvider } from './hooks/useAuth';
import { ThemeModeProvider } from './contexts/ThemeModeContext';

// Import des routes
import AppRoutes from './routes/index';
import ComptabilitePage from './components/comptabilite/ComptabilitePage';
import { ProtectedRoute } from './routes/ProtectedRoute';
import { theme } from './theme'; // Assurez-vous d'avoir un fichier theme.ts

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
        <ThemeProvider theme={theme}>
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
        </ThemeProvider>
      </ThemeModeProvider>
    </QueryClientProvider>
  );
};

export default App;
