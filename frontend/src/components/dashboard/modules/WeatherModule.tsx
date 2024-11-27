import React from 'react';
import { Grid, Typography, Box, Alert } from '@mui/material';
import { WeatherSummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import WbSunnyIcon from '@mui/icons-material/WbSunny';
import OpacityIcon from '@mui/icons-material/Opacity';
import AirIcon from '@mui/icons-material/Air';
import WarningIcon from '@mui/icons-material/Warning';

interface WeatherModuleProps {
  data: WeatherSummary;
}

const WeatherModule: React.FC<WeatherModuleProps> = ({ data }) => {
  const { current_conditions, daily_forecast, alerts, production_impact } = data;

  const getAlertSeverityColor = (severity: 'low' | 'medium' | 'high'): 'success' | 'warning' | 'error' => {
    switch (severity) {
      case 'high':
        return 'error';
      case 'medium':
        return 'warning';
      default:
        return 'success';
    }
  };

  return (
    <Box>
      {/* Conditions Actuelles */}
      <Grid container spacing={2}>
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Température"
            value={current_conditions.temperature}
            unit="°C"
            icon={<WbSunnyIcon />}
            color="warning"
            loading={false}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <StatCard
            title="Humidité"
            value={current_conditions.humidity}
            unit="%"
            icon={<OpacityIcon />}
            color="info"
            loading={false}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <StatCard
            title="Précipitations"
            value={current_conditions.precipitation}
            unit="mm"
            icon={<OpacityIcon />}
            color="primary"
            loading={false}
          />
        </Grid>

        <Grid item xs={12} sm={6}>
          <StatCard
            title="Vitesse du Vent"
            value={current_conditions.wind_speed}
            unit="km/h"
            icon={<AirIcon />}
            color="success"
            loading={false}
          />
        </Grid>
      </Grid>

      {/* Alertes Météo */}
      {alerts.length > 0 && (
        <Box mt={3}>
          <Typography variant="h6" gutterBottom>
            Alertes Météorologiques
          </Typography>
          {alerts.map((alert) => (
            <Alert
              key={alert.id}
              severity={getAlertSeverityColor(alert.severity)}
              icon={<WarningIcon />}
              sx={{ mb: 1 }}
            >
              <Typography variant="subtitle2">
                {alert.type}
              </Typography>
              <Typography variant="body2">
                {alert.description}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                {new Date(alert.start_time).toLocaleString()} - {new Date(alert.end_time).toLocaleString()}
              </Typography>
            </Alert>
          ))}
        </Box>
      )}

      {/* Impact sur la Production */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Impact sur la Production
        </Typography>
        <Alert
          severity={getAlertSeverityColor(production_impact.risk_level)}
          sx={{ mb: 2 }}
        >
          <Typography variant="subtitle2">
            Niveau de Risque: {production_impact.risk_level.toUpperCase()}
          </Typography>
          <Typography variant="body2">
            Zones affectées: {production_impact.affected_areas.join(', ')}
          </Typography>
        </Alert>
        <Box sx={{ mt: 1 }}>
          {production_impact.recommendations.map((recommendation, index) => (
            <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
              • {recommendation}
            </Typography>
          ))}
        </Box>
      </Box>

      {/* Prévisions */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Prévisions
        </Typography>
        <Grid container spacing={1}>
          {daily_forecast.map((forecast, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Box
                sx={{
                  p: 1,
                  borderRadius: 1,
                  bgcolor: 'background.paper',
                  border: 1,
                  borderColor: 'divider'
                }}
              >
                <Typography variant="subtitle2">
                  {new Date(forecast.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body2">
                  {forecast.temperature_high}°C / {forecast.temperature_low}°C
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  {forecast.condition}
                </Typography>
                <Typography variant="body2" color={
                  forecast.precipitation_chance > 70 ? 'error.main' :
                  forecast.precipitation_chance > 30 ? 'warning.main' : 'success.main'
                }>
                  {forecast.precipitation_chance}% de précipitations
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Box>
  );
};

export default WeatherModule;
