import React from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from 'react-query';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  List,
  ListItem,
  ListItemText,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import { weatherService } from '../../services/weather';

const DétailsMétéoTâche: React.FC = () => {
  const { taskId } = useParams<{ taskId: string }>();

  const { data: taskData, isLoading, error } = useQuery(
    ['task-weather', taskId],
    () => weatherService.getTaskWeather(taskId as string),
    {
      enabled: !!taskId,
      refetchInterval: 5 * 60 * 1000 // Rafraîchir toutes les 5 minutes
    }
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" p={3}>
        <CircularProgress />
      </Box>
    );
  }

  if (error || !taskData) {
    return (
      <Alert severity="error" sx={{ m: 2 }}>
        Erreur lors du chargement des données météorologiques de la tâche
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
    <Box p={3}>
      <Grid container spacing={3}>
        {/* Statut météo */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center" gap={2}>
                <Chip
                  label={getWeatherStatusText()}
                  color={getWeatherStatusColor()}
                  sx={{ fontSize: '1rem' }}
                />
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {taskData.weather_dependent && (
          <>
            {/* Conditions actuelles */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Conditions Actuelles
                  </Typography>
                  <List>
                    <ListItem>
                      <ListItemText
                        primary="Température"
                        secondary={`${taskData.weather_conditions.temperature}°C`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Humidité"
                        secondary={`${taskData.weather_conditions.humidity}%`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Vent"
                        secondary={`${taskData.weather_conditions.wind_speed} km/h`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText
                        primary="Précipitations"
                        secondary={`${taskData.weather_conditions.precipitation} mm`}
                      />
                    </ListItem>
                  </List>
                </CardContent>
              </Card>
            </Grid>

            {/* Contraintes */}
            <Grid item xs={12} md={6}>
              <Card>
                <CardContent>
                  <Typography variant="h6" gutterBottom>
                    Contraintes Météorologiques
                  </Typography>
                  <List>
                    {taskData.min_temperature && (
                      <ListItem>
                        <ListItemText
                          primary="Température minimale"
                          secondary={`${taskData.min_temperature}°C`}
                        />
                      </ListItem>
                    )}
                    {taskData.max_temperature && (
                      <ListItem>
                        <ListItemText
                          primary="Température maximale"
                          secondary={`${taskData.max_temperature}°C`}
                        />
                      </ListItem>
                    )}
                    {taskData.max_wind_speed && (
                      <ListItem>
                        <ListItemText
                          primary="Vitesse du vent maximale"
                          secondary={`${taskData.max_wind_speed} km/h`}
                        />
                      </ListItem>
                    )}
                    {taskData.max_precipitation && (
                      <ListItem>
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
                      Alertes Météo
                    </Typography>
                    <List>
                      {taskData.weather_warnings.map((warning, index) => (
                        <ListItem key={index}>
                          <Alert severity="warning" sx={{ width: '100%' }}>
                            {warning}
                          </Alert>
                        </ListItem>
                      ))}
                    </List>
                  </CardContent>
                </Card>
              </Grid>
            )}
          </>
        )}
      </Grid>
    </Box>
  );
};

export default DétailsMétéoTâche;
