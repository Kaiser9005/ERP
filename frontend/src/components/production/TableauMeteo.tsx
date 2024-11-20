import React from 'react';
import { Card, CardContent, Typography, Box, Grid, Alert, CircularProgress } from '@mui/material';
import { useQuery } from 'react-query';
import { weatherService } from '../../services/weather';

const TableauMeteo: React.FC = () => {
  const { data: metrics, isLoading, error } = useQuery(
    'metriques-agricoles',
    () => weatherService.getAgriculturalMetrics(),
    {
      refetchInterval: 30 * 60 * 1000, // Rafraîchir toutes les 30 minutes
    }
  );

  if (isLoading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !metrics) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        Erreur lors du chargement des données météorologiques
      </Alert>
    );
  }

  const warningMessage = weatherService.getWarningMessage(metrics);
  const cacheAge = weatherService.getCacheAge(metrics.current_conditions.cached_at);

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord Météorologique
      </Typography>

      {cacheAge && (
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          Dernière mise à jour : {cacheAge}
        </Typography>
      )}

      {warningMessage && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          {warningMessage}
        </Alert>
      )}

      <Grid container spacing={3}>
        {/* Conditions actuelles */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Conditions Actuelles
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body1">
                  Température : {metrics.current_conditions.temperature}°C
                </Typography>
                <Typography variant="body1">
                  Humidité : {metrics.current_conditions.humidity}%
                </Typography>
                <Typography variant="body1">
                  Précipitations : {metrics.current_conditions.precipitation} mm
                </Typography>
                <Typography variant="body1">
                  Vitesse du vent : {metrics.current_conditions.wind_speed} km/h
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Risques */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Analyse des Risques
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body1" color={
                  metrics.risks.precipitation.level === 'HIGH' ? 'error.main' :
                  metrics.risks.precipitation.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                }>
                  Précipitations : {metrics.risks.precipitation.message}
                </Typography>
                <Typography variant="body1" color={
                  metrics.risks.temperature.level === 'HIGH' ? 'error.main' :
                  metrics.risks.temperature.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                }>
                  Température : {metrics.risks.temperature.message}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Recommandations */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recommandations
              </Typography>
              <Box sx={{ mt: 2 }}>
                {metrics.recommendations.map((recommendation, index) => (
                  <Typography key={index} variant="body1" sx={{ mb: 1 }}>
                    • {recommendation}
                  </Typography>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default TableauMeteo;
