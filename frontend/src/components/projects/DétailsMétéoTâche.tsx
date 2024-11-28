import React from 'react';
import {
  Box,
  Paper,
  Typography,
  Grid,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import {
  WbSunny as SunIcon,
  Opacity as HumidityIcon,
  Air as WindIcon,
  WaterDrop as RainIcon,
  Warning as WarningIcon
} from '@mui/icons-material';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { TaskWithWeather } from '../../types/task';

const DétailsMétéoTâche: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();

  const { data: taskData, isLoading, error } = useQuery<TaskWithWeather>({
    queryKey: ['task-weather', taskId],
    queryFn: () => 
      fetch(`/api/v1/tasks/${taskId}/weather`)
        .then(res => {
          if (!res.ok) throw new Error('Erreur lors de la récupération des données');
          return res.json();
        }),
    enabled: !!taskId
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error || !taskData) {
    return (
      <Alert severity="error">
        {error instanceof Error ? error.message : "Données non disponibles"}
      </Alert>
    );
  }

  const getWeatherStatusColor = () => {
    if (!taskData.weather_dependent) return 'info';
    return taskData.weather_suitable ? 'success' : 'error';
  };

  const getWeatherStatusText = () => {
    if (!taskData.weather_dependent) return 'Tâche indépendante de la météo';
    return taskData.weather_suitable
      ? 'Conditions météo favorables'
      : 'Conditions météo défavorables';
  };

  return (
    <Box>
      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h5" gutterBottom>
          {taskData.title}
        </Typography>
        <Alert severity={getWeatherStatusColor()} sx={{ mb: 3 }}>
          {getWeatherStatusText()}
        </Alert>

        <Grid container spacing={3}>
          {/* Conditions actuelles */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Conditions Météorologiques Actuelles
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <SunIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Température"
                      secondary={`${taskData.weather_conditions.temperature}°C`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <HumidityIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Humidité"
                      secondary={`${taskData.weather_conditions.humidity}%`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <WindIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Vent"
                      secondary={`${taskData.weather_conditions.wind_speed} km/h`}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon>
                      <RainIcon />
                    </ListItemIcon>
                    <ListItemText
                      primary="Précipitations"
                      secondary={`${taskData.weather_conditions.precipitation} mm`}
                    />
                  </ListItem>
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Contraintes de la tâche */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Contraintes Météorologiques
                </Typography>
                <List>
                  {taskData.min_temperature !== undefined && (
                    <ListItem>
                      <ListItemIcon>
                        <SunIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="Température minimale requise"
                        secondary={`${taskData.min_temperature}°C`}
                      />
                    </ListItem>
                  )}
                  {taskData.max_temperature !== undefined && (
                    <ListItem>
                      <ListItemIcon>
                        <SunIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="Température maximale acceptable"
                        secondary={`${taskData.max_temperature}°C`}
                      />
                    </ListItem>
                  )}
                  {taskData.max_wind_speed !== undefined && (
                    <ListItem>
                      <ListItemIcon>
                        <WindIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="Vitesse du vent maximale"
                        secondary={`${taskData.max_wind_speed} km/h`}
                      />
                    </ListItem>
                  )}
                  {taskData.max_precipitation !== undefined && (
                    <ListItem>
                      <ListItemIcon>
                        <RainIcon />
                      </ListItemIcon>
                      <ListItemText
                        primary="Précipitations maximales"
                        secondary={`${taskData.max_precipitation} mm`}
                      />
                    </ListItem>
                  )}
                </List>
              </CardContent>
            </Card>
          </Grid>

          {/* Alertes */}
          {taskData.weather_warnings.length > 0 && (
            <Grid item xs={12}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Alertes Météorologiques
                  </Typography>
                  <List>
                    {taskData.weather_warnings.map((warning, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <WarningIcon color="error" />
                        </ListItemIcon>
                        <ListItemText primary={warning} />
                      </ListItem>
                    ))}
                  </List>
                </CardContent>
              </Card>
            </Grid>
          )}
        </Grid>
      </Paper>
    </Box>
  );
};

export default DétailsMétéoTâche;
