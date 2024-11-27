import React from 'react';
import { Card, CardContent, Typography, Grid, Box, CircularProgress } from '@mui/material';
import { WbSunny, Opacity, Speed } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { weatherService } from '../../services/weather';
import { queryKeys } from '../../config/queryClient';
import type { AgriculturalMetrics } from '../../types/weather';

const WeatherWidget: React.FC = () => {
  const { data: weatherData, isLoading } = useQuery({
    queryKey: queryKeys.weather.current(),
    queryFn: () => weatherService.getAgriculturalMetrics(),
    staleTime: 1000 * 60 * 30, // 30 minutes
    refetchInterval: 1000 * 60 * 30, // Rafraîchir toutes les 30 minutes
    retry: 3
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

  if (!weatherData) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Conditions Météorologiques
          </Typography>
          <Typography color="textSecondary">
            Données météo non disponibles
          </Typography>
        </CardContent>
      </Card>
    );
  }

  const { current_conditions: conditions } = weatherData;

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Conditions Météorologiques
          {conditions.cached_at && (
            <Typography variant="caption" color="textSecondary" component="span" sx={{ ml: 1 }}>
              (Mis à jour {new Date(conditions.cached_at).toLocaleTimeString()})
            </Typography>
          )}
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Box display="flex" alignItems="center" flexDirection="column">
              <WbSunny color="primary" />
              <Typography variant="body2" color="textSecondary">
                Température
              </Typography>
              <Typography variant="h6">
                {conditions.temperature}°C
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box display="flex" alignItems="center" flexDirection="column">
              <Opacity color="primary" />
              <Typography variant="body2" color="textSecondary">
                Humidité
              </Typography>
              <Typography variant="h6">
                {conditions.humidity}%
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box display="flex" alignItems="center" flexDirection="column">
              <Speed color="primary" />
              <Typography variant="body2" color="textSecondary">
                Précipitations
              </Typography>
              <Typography variant="h6">
                {conditions.precipitation}mm
              </Typography>
            </Box>
          </Grid>
        </Grid>
        {weatherData.risks.level === 'HIGH' && (
          <Box mt={2} p={1} bgcolor="error.light" borderRadius={1}>
            <Typography color="error.dark" variant="body2">
              {weatherData.risks.precipitation.level === 'HIGH' && weatherData.risks.precipitation.message}
              {weatherData.risks.temperature.level === 'HIGH' && (
                <>
                  {weatherData.risks.precipitation.level === 'HIGH' && ' - '}
                  {weatherData.risks.temperature.message}
                </>
              )}
            </Typography>
          </Box>
        )}
        {weatherData.recommendations && weatherData.recommendations.length > 0 && (
          <Box mt={2}>
            <Typography variant="subtitle2" color="textSecondary">
              Recommandations :
            </Typography>
            <Typography variant="body2" color="textSecondary">
              {weatherData.recommendations[0]}
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default WeatherWidget;
