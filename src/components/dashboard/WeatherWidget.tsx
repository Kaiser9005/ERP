import React from 'react';
import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import { WbSunny, Opacity, Speed } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { productionService } from '../../services/production';

const WeatherWidget: React.FC = () => {
  const { data: weatherData, isLoading } = useQuery(
    ['weather', 'current'],
    () => productionService.getWeatherData('current')
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!weatherData) {
    return null;
  }

  const { conditions_meteo } = weatherData;

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
                {conditions_meteo?.temperature}°C
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
                {conditions_meteo?.humidite}%
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
                {conditions_meteo?.precipitation}mm
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default WeatherWidget;
