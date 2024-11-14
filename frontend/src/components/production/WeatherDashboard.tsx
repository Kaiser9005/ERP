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
  useTheme,
  Snackbar,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  WbSunny,
  Opacity,
  Air,
  Warning,
  CheckCircle,
  Info,
  Cached,
  CloudOff,
  Refresh
} from '@mui/icons-material';
import { weatherService } from '../../services/weather';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

interface WeatherData {
  current_conditions: {
    temperature: number;
    humidity: number;
    precipitation: number;
    wind_speed: number;
    conditions: string;
    uv_index: number;
    cloud_cover: number;
    cached_at?: string;
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

const MAX_RETRIES = 3;
const RETRY_DELAY = 5000; // 5 secondes

const WeatherDashboard: React.FC = () => {
  const [weatherData, setWeatherData] = useState<WeatherData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [retryCount, setRetryCount] = useState(0);
  const [retrying, setRetrying] = useState(false);
  const [notification, setNotification] = useState<string | null>(null);
  const theme = useTheme();

  const fetchWeatherData = async (retry = 0) => {
    try {
      setRetrying(retry > 0);
      const data = await weatherService.getAgriculturalMetrics();
      setWeatherData(data);
      setError(null);
      setRetryCount(0);
      
      // Vérifier les risques élevés pour les notifications
      if (data.risks.level === 'HIGH') {
        const messages: string[] = [];
        if (data.risks.precipitation.level === 'HIGH') {
          messages.push(data.risks.precipitation.message);
        }
        if (data.risks.temperature.level === 'HIGH') {
          messages.push(data.risks.temperature.message);
        }
        setNotification(`ALERTE MÉTÉO: ${messages.join(' - ')}`);
      }
    } catch (err) {
      console.error('Weather fetch error:', err);
      if (retry < MAX_RETRIES) {
        setRetryCount(retry + 1);
        setTimeout(() => fetchWeatherData(retry + 1), RETRY_DELAY);
      } else {
        setError("Erreur lors de la récupération des données météo");
        setRetrying(false);
      }
    } finally {
      if (retry === 0 || retry === MAX_RETRIES) {
        setLoading(false);
      }
    }
  };

  useEffect(() => {
    fetchWeatherData();
    // Rafraîchir toutes les 30 minutes
    const interval = setInterval(() => fetchWeatherData(), 30 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const handleRefresh = () => {
    setLoading(true);
    fetchWeatherData();
  };

  if (loading && !retrying) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box>
        <Alert 
          severity="error" 
          action={
            <Chip
              icon={<Refresh />}
              label="Réessayer"
              onClick={handleRefresh}
              color="primary"
              variant="outlined"
            />
          }
        >
          {error}
        </Alert>
        {weatherData && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Affichage des dernières données disponibles
          </Alert>
        )}
      </Box>
    );
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
    <>
      {retrying && (
        <Box sx={{ width: '100%', mb: 2 }}>
          <Alert severity="info" icon={<Cached />}>
            Tentative de reconnexion... ({retryCount}/{MAX_RETRIES})
          </Alert>
          <LinearProgress />
        </Box>
      )}

      {weatherData.current_conditions.cached_at && (
        <Box sx={{ mb: 2 }}>
          <Chip
            icon={<Cached />}
            label={`Dernière mise à jour ${formatDistanceToNow(
              new Date(weatherData.current_conditions.cached_at),
              { addSuffix: true, locale: fr }
            )}`}
            variant="outlined"
            color="primary"
          />
        </Box>
      )}

      <Grid container spacing={3}>
        {/* Conditions actuelles */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                <Typography variant="h6">
                  Conditions Météorologiques Actuelles
                </Typography>
                <Chip
                  icon={<Refresh />}
                  label="Actualiser"
                  onClick={handleRefresh}
                  variant="outlined"
                  size="small"
                />
              </Box>
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

      <Snackbar
        open={!!notification}
        autoHideDuration={6000}
        onClose={() => setNotification(null)}
        anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setNotification(null)} 
          severity="error" 
          sx={{ width: '100%' }}
        >
          {notification}
        </Alert>
      </Snackbar>
    </>
  );
};

export default WeatherDashboard;
