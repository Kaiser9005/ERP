import React from 'react';
import { Grid, Paper, Typography, Box } from '@mui/material';
import {
  WaterDrop as WaterDropIcon,
  Thermostat as ThermostatIcon,
  Air as AirIcon,
  WbSunny as SunIcon
} from '@mui/icons-material';
import { Parcelle } from '../../types/production';
import { weatherService } from '../../services/weather';
import { useQuery } from 'react-query';

interface TableauMeteoParcelleaireProps {
  parcelle?: Parcelle;
}

const TableauMeteoParcelleaire: React.FC<TableauMeteoParcelleaireProps> = ({ parcelle }) => {
  const { data: metrics, isLoading, error } = useQuery(
    ['agricultural-metrics', parcelle?.id],
    () => weatherService.getAgriculturalMetrics(),
    {
      enabled: !!parcelle,
      refetchInterval: 30 * 60 * 1000 // Rafraîchir toutes les 30 minutes
    }
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Chargement des données météo...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography color="error">Erreur lors du chargement des données météo</Typography>
      </Box>
    );
  }

  if (!parcelle || !metrics) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Sélectionnez une parcelle pour voir les données météo</Typography>
      </Box>
    );
  }

  const { current_conditions: weather } = metrics;

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
              {weather.temperature}°C
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
              {weather.humidity}%
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
              {weather.uv_index}
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
              {weather.wind_speed} km/h
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Vent
            </Typography>
          </Paper>
        </Grid>

        {/* Risques et Recommandations */}
        <Grid item xs={12}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="subtitle1" gutterBottom>
              Analyse des Risques
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="body1" color={
                  metrics.risks.precipitation.level === 'HIGH' ? 'error.main' :
                  metrics.risks.precipitation.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                }>
                  Précipitations : {metrics.risks.precipitation.message}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="body1" color={
                  metrics.risks.temperature.level === 'HIGH' ? 'error.main' :
                  metrics.risks.temperature.level === 'MEDIUM' ? 'warning.main' : 'success.main'
                }>
                  Température : {metrics.risks.temperature.message}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {metrics.recommendations && metrics.recommendations.length > 0 && (
          <Grid item xs={12}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="subtitle1" gutterBottom>
                Recommandations
              </Typography>
              {metrics.recommendations.map((recommendation, index) => (
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
