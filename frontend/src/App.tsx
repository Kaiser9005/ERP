import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CssBaseline from '@mui/material/CssBaseline';
import { ThemeProvider } from '@mui/material/styles';
import { AuthProvider } from './contexts/AuthContext';
import { ThemeModeProvider } from './contexts/ThemeModeContext';

// Import des routes
import PageConnexion from './components/auth/PageConnexion';
import AppRoutes from './routes/index';
import ComptabilitePage from './components/comptabilite/ComptabilitePage';
import RouteProtege from './components/auth/RouteProtege';
import { theme } from './theme';

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
                    <RouteProtege>
                      <ComptabilitePage />
                    </RouteProtege>
                  }
                />
                <Route path="/connexion" element={<PageConnexion />} />
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
