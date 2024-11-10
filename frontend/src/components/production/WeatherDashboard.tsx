import React, { useEffect, useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Grid,
  Typography,
  CircularProgress,
  Alert,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  useTheme
} from '@mui/material';
import {
  WbSunny,
  Opacity,
  Air,
  Warning,
  CheckCircle,
  Info
} from '@mui/icons-material';
import { weatherService } from '../../services/weather';

interface WeatherData {
  current_conditions: {
    temperature: number;
    humidity: number;
    precipitation: number;
    wind_speed: number;
    conditions: string;
    uv_index: number;
    cloud_cover: number;
  };
  risks: {
    precipitation: {
      level: 'LOW' | 'MEDIUM' | 'HIGH';
      message: string;
    };
    temperature: {
      level: 'LOW' | 'MEDIUM' | 'HIGH';
      message: string;
    };
    level: 'LOW' | 'MEDIUM' | 'HIGH';
  };
  recommendations: string[];
}

const WeatherDashboard: React.FC = () => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  useEffect(() => {
    const fetchWeatherData = async () => {
      try {
        const data = await weatherService.getAgriculturalMetrics();
        setWeatherData(data);
        setError(null);
      } catch (err) {
        setError("Erreur lors de la récupération des données météo");
        console.error('Weather fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchWeatherData();
    // Rafraîchir toutes les 30 minutes
    const interval = setInterval(fetchWeatherData, 30 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!weatherData) {
    return <Alert severity="info">Aucune donnée météo disponible</Alert>;
  }

  const getRiskColor = (level: 'LOW' | 'MEDIUM' | 'HIGH') => {
    switch (level) {
      case 'HIGH':
        return theme.palette.error.main;
      case 'MEDIUM':
        return theme.palette.warning.main;
      case 'LOW':
        return theme.palette.success.main;
    }
  };

  const getRiskIcon = (level: 'LOW' | 'MEDIUM' | 'HIGH') => {
    switch (level) {
      case 'HIGH':
        return <Warning color="error" />;
      case 'MEDIUM':
        return <Info color="warning" />;
      case 'LOW':
        return <CheckCircle color="success" />;
    }
  };

  return (
    <Grid container spacing={3}>
      {/* Conditions actuelles */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Conditions Météorologiques Actuelles
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Box display="flex" alignItems="center" mb={1}>
                  <WbSunny sx={{ mr: 1 }} />
                  <Typography>
                    {weatherData.current_conditions.temperature}°C
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box display="flex" alignItems="center" mb={1}>
                  <Opacity sx={{ mr: 1 }} />
                  <Typography>
                    {weatherData.current_conditions.humidity}%
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Box display="flex" alignItems="center">
                  <Air sx={{ mr: 1 }} />
                  <Typography>
                    {weatherData.current_conditions.wind_speed} km/h
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2" color="textSecondary">
                  {weatherData.current_conditions.conditions}
                </Typography>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* Risques */}
      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Alertes et Risques
            </Typography>
            <Box mb={2}>
              <Typography
                variant="subtitle2"
                sx={{ color: getRiskColor(weatherData.risks.level) }}
              >
                Niveau de risque global: {weatherData.risks.level}
              </Typography>
            </Box>
            <Grid container spacing={2}>
              <Grid item xs={12}>
                <Box display="flex" alignItems="center" mb={1}>
                  {getRiskIcon(weatherData.risks.precipitation.level)}
                  <Typography sx={{ ml: 1 }}>
                    {weatherData.risks.precipitation.message}
                  </Typography>
                </Box>
              </Grid>
              <Grid item xs={12}>
                <Box display="flex" alignItems="center">
                  {getRiskIcon(weatherData.risks.temperature.level)}
                  <Typography sx={{ ml: 1 }}>
                    {weatherData.risks.temperature.message}
                  </Typography>
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Grid>

      {/* Recommandations */}
      <Grid item xs={12}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recommandations
            </Typography>
            <List>
              {weatherData.recommendations.map((recommendation, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <Info color="primary" />
                  </ListItemIcon>
                  <ListItemText primary={recommendation} />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default WeatherDashboard;
