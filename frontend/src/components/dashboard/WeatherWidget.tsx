import React from 'react';
import { Card, CardContent, Typography, Grid, Box, CircularProgress } from '@mui/material';
import { WbSunny, Opacity, Speed } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { weatherService } from '../../services/weather';
import { queryKeys } from '../../config/queryClient';
import type { WeatherData } from '../../types/production';

const WeatherWidget: React.FC = () => {
  const { data: weatherData, isLoading } = useQuery<WeatherData>({
    queryKey: queryKeys.weather.current(),
    queryFn: () => weatherService.getCurrentWeather(),
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

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Conditions Météorologiques
          {weatherData.cached_at && (
            <Typography variant="caption" color="textSecondary" component="span" sx={{ ml: 1 }}>
              (Mis à jour {new Date(weatherData.cached_at).toLocaleTimeString()})
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
                {weatherData.temperature}°C
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
                {weatherData.humidity}%
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
                {weatherData.precipitation}mm
              </Typography>
            </Box>
          </Grid>
        </Grid>
        {weatherData.risks?.level === 'HIGH' && (
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
