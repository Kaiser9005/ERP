import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  WaterDrop as WaterDropIcon,
  Thermostat as ThermostatIcon,
  Air as AirIcon,
  WbSunny as SunIcon
} from '@mui/icons-material';
import { Parcelle } from '../../types/production';
import { productionService } from '../../services/production';

interface WeatherData {
  temperature: number;
  humidite: number;
  precipitation: number;
  ensoleillement: number;
  vent: number;
  previsions: {
    date: string;
    temperature: number;
    precipitation: number;
  }[];
}

interface WeatherDashboardProps {
  parcelle?: Parcelle;
}

const WeatherDashboard: React.FC<WeatherDashboardProps> = ({ parcelle }) => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadWeatherData = async () => {
      if (!parcelle) return;

      try {
        setLoading(true);
        const data = await productionService.getWeatherData(parcelle.id);
        setWeatherData(data);
      } catch (err) {
        setError('Erreur lors du chargement des données météo');
      } finally {
        setLoading(false);
      }
    };

    loadWeatherData();
  }, [parcelle]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Chargement des données météo...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!parcelle || !weatherData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Sélectionnez une parcelle pour voir les données météo</Typography>
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Conditions Météorologiques - {parcelle.code}
      </Typography>

      <Grid container spacing={3}>
        {/* Température */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <ThermostatIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.temperature}°C
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Température
            </Typography>
          </Paper>
        </Grid>

        {/* Humidité */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <WaterDropIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.humidite}%
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Humidité
            </Typography>
          </Paper>
        </Grid>

        {/* Précipitations */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <SunIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.ensoleillement}h
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Ensoleillement
            </Typography>
          </Paper>
        </Grid>

        {/* Vent */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <AirIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.vent} km/h
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Vent
            </Typography>
          </Paper>
        </Grid>

        {/* Prévisions */}
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Prévisions sur 5 jours
            </Typography>
            <Grid container spacing={2}>
              {weatherData.previsions.map((prevision, index) => (
                <Grid item xs={12} sm={2.4} key={index}>
                  <Paper elevation={1} sx={{ p: 1, textAlign: 'center' }}>
                    <Typography variant="body2">
                      {new Date(prevision.date).toLocaleDateString()}
                    </Typography>
                    <Typography variant="body1">
                      {prevision.temperature}°C
                    </Typography>
                    <Typography variant="body2">
                      {prevision.precipitation}mm
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Paper>
  );
};

export default WeatherDashboard;
