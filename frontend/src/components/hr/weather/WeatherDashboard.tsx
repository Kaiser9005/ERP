import React, { useEffect, useState } from 'react';
import { weatherService } from '../../../services/weather';
import type { WeatherHRMetrics } from '../../../types/weather';
import { Box, Card, Grid, Typography, Alert, Chip } from '@mui/material';
import WeatherStatCard from './WeatherStatCard';

const WeatherDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<WeatherHRMetrics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const data = await weatherService.getHRWeatherMetrics();
        setMetrics(data);
      } catch (err) {
        setError("Erreur lors de la récupération des données météo");
      } finally {
        setLoading(false);
      }
    };

    fetchMetrics();
    // Rafraîchir toutes les 5 minutes
    const interval = setInterval(fetchMetrics, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return <Box>Chargement des données météo...</Box>;
  }

  if (error || !metrics) {
    return <Alert severity="error">{error}</Alert>;
  }

  const { current_conditions, risks, schedule_adjustments, safety_requirements, alerts } = metrics;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord Météo RH
      </Typography>

      {/* Alertes */}
      {alerts.map((alert, index) => (
        <Alert 
          key={index}
          severity={alert.level === 'CRITICAL' ? 'error' : alert.level === 'WARNING' ? 'warning' : 'info'}
          sx={{ mb: 2 }}
        >
          {alert.message}
          <Box sx={{ mt: 1 }}>
            {alert.affected_roles.map(role => (
              <Chip 
                key={role} 
                label={role} 
                size="small" 
                sx={{ mr: 1 }} 
              />
            ))}
          </Box>
        </Alert>
      ))}

      {/* Conditions actuelles */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} md={3}>
          <WeatherStatCard
            title="Température"
            value={`${current_conditions.temperature}°C`}
            status={risks.temperature.level}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <WeatherStatCard
            title="Précipitations"
            value={`${current_conditions.precipitation} mm`}
            status={risks.precipitation.level}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <WeatherStatCard
            title="Vent"
            value={`${current_conditions.wind_speed} km/h`}
            status={risks.wind.level}
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <WeatherStatCard
            title="Niveau de Risque Global"
            value={risks.level}
            status={risks.level}
          />
        </Grid>
      </Grid>

      {/* Ajustements de planning */}
      {schedule_adjustments.length > 0 && (
        <Card sx={{ p: 2, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Ajustements de Planning
          </Typography>
          {schedule_adjustments.map((adjustment, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Typography variant="subtitle1">
                {adjustment.reason}
              </Typography>
              <Typography variant="body2">
                Horaires ajustés : {adjustment.adjusted_schedule.start} - {adjustment.adjusted_schedule.end}
              </Typography>
              <Chip 
                label={adjustment.status} 
                color={
                  adjustment.status === 'APPROVED' ? 'success' :
                  adjustment.status === 'PROPOSED' ? 'warning' : 'default'
                }
                size="small"
                sx={{ mt: 1 }}
              />
            </Box>
          ))}
        </Card>
      )}

      {/* Équipements de sécurité */}
      {safety_requirements.length > 0 && (
        <Card sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Équipements Requis
          </Typography>
          {safety_requirements.map((requirement, index) => (
            <Box key={index} sx={{ mb: 2 }}>
              <Typography variant="subtitle1">
                Condition : {requirement.weather_condition}
              </Typography>
              <Box sx={{ mt: 1 }}>
                {requirement.required_equipment.map(equipment => (
                  <Chip 
                    key={equipment}
                    label={equipment}
                    color="primary"
                    size="small"
                    sx={{ mr: 1, mb: 1 }}
                  />
                ))}
              </Box>
              {requirement.instructions && (
                <Typography variant="body2" sx={{ mt: 1 }}>
                  {requirement.instructions}
                </Typography>
              )}
            </Box>
          ))}
        </Card>
      )}
    </Box>
  );
};

export default WeatherDashboard;
