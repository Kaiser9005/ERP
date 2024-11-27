import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Alert,
  Chip
} from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import { weatherService } from '../../services/weather';
import { queryKeys } from '../../config/queryClient';

interface Props {
  projectId?: string;
  startDate?: Date;
  endDate?: Date;
}

export const WeatherAnalytics: React.FC<Props> = ({
  projectId,
  startDate = new Date(),
  endDate = new Date(Date.now() + 7 * 24 * 60 * 60 * 1000) // 7 jours par défaut
}) => {
  const { data: weatherImpact, isLoading, error } = useQuery({
    queryKey: queryKeys.weather.impact(projectId, startDate, endDate),
    queryFn: () => weatherService.getWeatherImpact(projectId, startDate, endDate),
    enabled: !!projectId,
    refetchInterval: 30 * 60 * 1000 // Rafraîchir toutes les 30 minutes
  });

  const { data: iotData } = useQuery({
    queryKey: queryKeys.weather.iot(projectId),
    queryFn: () => weatherService.getIoTData(projectId),
    enabled: !!projectId,
    refetchInterval: 5 * 60 * 1000 // Rafraîchir toutes les 5 minutes
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        Erreur lors du chargement des analyses météo
      </Alert>
    );
  }

  if (!weatherImpact) {
    return null;
  }

  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h5" gutterBottom>
        Analyse Météorologique Avancée
      </Typography>

      <Grid container spacing={3}>
        {/* Score d'impact */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Score d'Impact Global
              </Typography>
              <Box display="flex" alignItems="center" gap={2}>
                <Typography variant="h3">
                  {(weatherImpact.impact_score * 100).toFixed(0)}%
                </Typography>
                <Chip
                  label={weatherImpact.impact_score > 0.7 ? 'ÉLEVÉ' : 
                         weatherImpact.impact_score > 0.4 ? 'MOYEN' : 'FAIBLE'}
                  color={weatherImpact.impact_score > 0.7 ? 'error' :
                         weatherImpact.impact_score > 0.4 ? 'warning' : 'success'}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Données IoT */}
        {iotData && (
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Données Capteurs IoT
                </Typography>
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={iotData.readings}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="timestamp"
                      tickFormatter={(value) => new Date(value).toLocaleTimeString('fr-FR')}
                    />
                    <YAxis yAxisId="temp" orientation="left" label="Température (°C)" />
                    <YAxis yAxisId="humidity" orientation="right" label="Humidité (%)" />
                    <Tooltip 
                      labelFormatter={(value) => new Date(value).toLocaleString('fr-FR')}
                    />
                    <Legend />
                    <Line
                      yAxisId="temp"
                      type="monotone"
                      dataKey="temperature"
                      stroke="#8884d8"
                      name="Température"
                    />
                    <Line
                      yAxisId="humidity"
                      type="monotone"
                      dataKey="humidity"
                      stroke="#82ca9d"
                      name="Humidité"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}

        {/* Périodes à risque */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Périodes à Risque
              </Typography>
              <Box>
                {weatherImpact.risk_periods.map((period, index) => (
                  <Box key={index} sx={{ mb: 2 }}>
                    <Typography variant="subtitle1">
                      {period.period}
                    </Typography>
                    <Box display="flex" gap={1} flexWrap="wrap">
                      {period.conditions.map((condition, idx) => (
                        <Chip
                          key={idx}
                          label={condition}
                          color={period.risk === 'HIGH' ? 'error' : 'warning'}
                          size="small"
                        />
                      ))}
                    </Box>
                  </Box>
                ))}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Tâches affectées */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tâches Impactées et Alternatives
              </Typography>
              <Grid container spacing={2}>
                {weatherImpact.affected_tasks.map((task, index) => (
                  <Grid item xs={12} key={index}>
                    <Box sx={{ p: 2, border: 1, borderColor: 'divider', borderRadius: 1 }}>
                      <Typography variant="subtitle1" gutterBottom>
                        {task.task_id}
                      </Typography>
                      <Box display="flex" gap={1} mb={1}>
                        {task.conditions.map((condition, idx) => (
                          <Chip
                            key={idx}
                            label={condition}
                            color={task.impact === 'HIGH' ? 'error' : 'warning'}
                            size="small"
                          />
                        ))}
                      </Box>
                      {weatherImpact.alternatives.find(alt => alt.task_id === task.task_id) && (
                        <Typography variant="body2" color="success.main">
                          Alternative disponible : {
                            formatDate(weatherImpact.alternatives.find(
                              alt => alt.task_id === task.task_id
                            )?.alternative_date || '')
                          }
                        </Typography>
                      )}
                    </Box>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default WeatherAnalytics;
