import React from 'react';
import { Card, CardContent, Typography, Grid, Box } from '@mui/material';
import { WbSunny, Opacity, Air } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getWeatherData } from '../../services/weather';

const WeatherWidget: React.FC = () => {
  const { data: weather } = useQuery('weather', getWeatherData);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Météo
        </Typography>

        <Grid container spacing={2}>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <WbSunny color="warning" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h5">
                {weather?.temperature || '--'}°C
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Température
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Opacity color="info" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h5">
                {weather?.humidite || '--'}%
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Humidité
              </Typography>
            </Box>
          </Grid>

          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center' }}>
              <Air color="primary" sx={{ fontSize: 40, mb: 1 }} />
              <Typography variant="h5">
                {weather?.vent || '--'} km/h
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Vent
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default WeatherWidget;