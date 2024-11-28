import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  WaterDrop as WaterDropIcon,
  Thermostat as ThermostatIcon,
  Air as AirIcon,
  WbSunny as SunIcon
} from '@mui/icons-material';
import { Parcelle, WeatherData } from '../../types/production';
import { productionService } from '../../services/production';

interface TableauMeteoParcelleaireProps {
  parcelle?: Parcelle;
}

const TableauMeteoParcelleaire: React.FC<TableauMeteoParcelleaireProps> = ({ parcelle }) => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadWeatherData = async () => {
      if (!parcelle) return;

      try {
        setLoading(true);
        const data = await productionService.getWeatherData("current");
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
              {weatherData.humidity}%
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Humidité
            </Typography>
          </Paper>
        </Grid>

        {/* Ensoleillement */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <SunIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.uv_index}
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Indice UV
            </Typography>
          </Paper>
        </Grid>

        {/* Vent */}
        <Grid item xs={12} sm={6} md={3}>
          <Paper elevation={2} sx={{ p: 2, textAlign: 'center' }}>
            <AirIcon color="primary" sx={{ fontSize: 40 }} />
            <Typography variant="h6">
              {weatherData.wind_speed} km/h
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Vent
            </Typography>
          </Paper>
        </Grid>

        {/* Risques et Recommandations */}
        {weatherData.risks && (
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Analyse des Risques
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1" color={
                    weatherData.risks.precipitation.level === 'HIGH' ? 'error.main' :
                    weatherData.risks.precipitation.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                  }>
                    Précipitations : {weatherData.risks.precipitation.message}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body1" color={
                    weatherData.risks.temperature.level === 'HIGH' ? 'error.main' :
                    weatherData.risks.temperature.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                  }>
                    Température : {weatherData.risks.temperature.message}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}

        {weatherData.recommendations && weatherData.recommendations.length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Recommandations
              </Typography>
              {weatherData.recommendations.map((recommendation, index) => (
                <Typography key={index} variant="body1" sx={{ mb: 1 }}>
                  • {recommendation}
                </Typography>
              ))}
            </Paper>
          </Grid>
        )}
      </Grid>
    </Paper>
  );
};

export default TableauMeteoParcelleaire;
