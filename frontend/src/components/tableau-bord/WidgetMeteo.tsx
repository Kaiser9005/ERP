import React from 'react';
import { Card, CardContent, Typography, Box, Chip, Alert, CircularProgress } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { weatherService } from '../../services/weather';

const WidgetMeteo: React.FC = () => {
  const { data: metrics, isLoading, error } = useQuery({
    queryKey: ['agricultural-metrics'],
    queryFn: () => weatherService.getAgriculturalMetrics(),
    refetchInterval: 30 * 60 * 1000, // Rafraîchir toutes les 30 minutes
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (error || !metrics) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">
            Erreur lors du chargement des données météo
          </Alert>
        </CardContent>
      </Card>
    );
  }

  const warningMessage = weatherService.getWarningMessage(metrics);
  const cacheAge = weatherService.getCacheAge(metrics.current_conditions.cached_at);

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Conditions Météo
          </Typography>
          {cacheAge && (
            <Typography variant="caption" color="text.secondary">
              Mis à jour {cacheAge}
            </Typography>
          )}
        </Box>

        {warningMessage && (
          <Alert severity="warning" sx={{ mb: 2 }}>
            {warningMessage}
          </Alert>
        )}

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Température
          </Typography>
          <Typography variant="h4">
            {metrics.current_conditions.temperature}°C
          </Typography>
          <Box sx={{ display: 'flex', gap: 1, mt: 1 }}>
            <Chip
              label={`${metrics.current_conditions.humidity}% Humidité`}
              size="small"
              color="primary"
            />
            <Chip
              label={`${metrics.current_conditions.precipitation}mm Précip.`}
              size="small"
              color="info"
            />
          </Box>
        </Box>

        <Box>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Recommandations
          </Typography>
          {metrics.recommendations.map((recommendation, index) => (
            <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
              • {recommendation}
            </Typography>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
};

export default WidgetMeteo;
