import React from 'react';
import { Card, CardContent, Typography, Grid, Box, CircularProgress } from '@mui/material';
import { WbSunny, Opacity, Speed } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { productionService } from '../../services/production';
import { queryKeys } from '../../config/queryClient';
import type { WeatherData } from '../../types/production';

const WeatherWidget: React.FC = () => {
  const { data: weatherData, isLoading } = useQuery<WeatherData>({
    queryKey: queryKeys.weather.current(),
    queryFn: () => productionService.getWeatherData('current'),
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
      </CardContent>
    </Card>
  );
};

export default WeatherWidget;
