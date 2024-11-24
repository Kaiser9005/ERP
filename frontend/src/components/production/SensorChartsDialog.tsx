import React, { useMemo } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  Box,
  Typography,
  Grid,
  Paper,
  CircularProgress,
  Alert,
} from '@mui/material';
import { Close as CloseIcon } from '@mui/icons-material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';
import { format, subDays } from 'date-fns';
import { fr } from 'date-fns/locale';

import { useSensor, useSensorReadings, useSensorStats } from '../../services/iot';
import { SENSOR_TYPE_LABELS, SENSOR_UNITS } from '../../types/iot';

interface SensorChartsDialogProps {
  open: boolean;
  onClose: () => void;
  sensorId: string;
}

export const SensorChartsDialog: React.FC<SensorChartsDialogProps> = ({
  open,
  onClose,
  sensorId,
}) => {
  // Récupération des données du capteur
  const { data: sensor, isLoading: sensorLoading } = useSensor(sensorId);

  // Récupération des lectures des 7 derniers jours
  const startDate = subDays(new Date(), 7);
  const {
    data: readings,
    isLoading: readingsLoading,
    error: readingsError,
  } = useSensorReadings(sensorId, {
    start_date: format(startDate, "yyyy-MM-dd'T'HH:mm:ss"),
    end_date: format(new Date(), "yyyy-MM-dd'T'HH:mm:ss"),
  });

  // Récupération des statistiques
  const {
    data: stats,
    isLoading: statsLoading,
    error: statsError,
  } = useSensorStats(sensorId, {
    start_date: format(startDate, "yyyy-MM-dd'T'HH:mm:ss"),
    end_date: format(new Date(), "yyyy-MM-dd'T'HH:mm:ss"),
  });

  // Formatage des données pour le graphique
  const chartData = useMemo(() => {
    if (!readings) return [];
    return readings.map((reading) => ({
      timestamp: new Date(reading.timestamp),
      valeur: reading.valeur,
    }));
  }, [readings]);

  const isLoading = sensorLoading || readingsLoading || statsLoading;
  const error = readingsError || statsError;

  if (error) {
    return (
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogTitle>
          Erreur
          <IconButton
            aria-label="close"
            onClick={onClose}
            sx={{ position: 'absolute', right: 8, top: 8 }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent>
          <Alert severity="error">
            Une erreur est survenue lors du chargement des données
          </Alert>
        </DialogContent>
      </Dialog>
    );
  }

  if (!sensor || isLoading) {
    return (
      <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
        <DialogContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
            <CircularProgress />
          </Box>
        </DialogContent>
      </Dialog>
    );
  }

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {sensor.code} - {SENSOR_TYPE_LABELS[sensor.type]}
        <IconButton
          aria-label="close"
          onClick={onClose}
          sx={{ position: 'absolute', right: 8, top: 8 }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>

      <DialogContent>
        <Grid container spacing={2}>
          {/* Statistiques */}
          <Grid item xs={12}>
            <Grid container spacing={2}>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Moyenne
                  </Typography>
                  <Typography variant="h6">
                    {stats?.moyenne.toFixed(2)} {SENSOR_UNITS[sensor.type]}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Minimum
                  </Typography>
                  <Typography variant="h6">
                    {stats?.minimum.toFixed(2)} {SENSOR_UNITS[sensor.type]}
                  </Typography>
                </Paper>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Paper sx={{ p: 2, textAlign: 'center' }}>
                  <Typography variant="body2" color="text.secondary">
                    Maximum
                  </Typography>
                  <Typography variant="h6">
                    {stats?.maximum.toFixed(2)} {SENSOR_UNITS[sensor.type]}
                  </Typography>
                </Paper>
              </Grid>
            </Grid>
          </Grid>

          {/* Graphique */}
          <Grid item xs={12}>
            <Paper sx={{ p: 2, height: 400 }}>
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis
                    dataKey="timestamp"
                    tickFormatter={(value) => format(value, 'dd/MM HH:mm', { locale: fr })}
                  />
                  <YAxis
                    unit={SENSOR_UNITS[sensor.type]}
                    domain={['auto', 'auto']}
                  />
                  <Tooltip
                    labelFormatter={(value) => format(value as Date, 'dd/MM/yyyy HH:mm', { locale: fr })}
                    formatter={(value: number) => [
                      `${value.toFixed(2)} ${SENSOR_UNITS[sensor.type]}`,
                      'Valeur',
                    ]}
                  />
                  <Line
                    type="monotone"
                    dataKey="valeur"
                    stroke="#2196f3"
                    dot={false}
                    name="Valeur"
                  />
                </LineChart>
              </ResponsiveContainer>
            </Paper>
          </Grid>

          {/* Seuils */}
          <Grid item xs={12}>
            <Typography variant="subtitle2" gutterBottom>
              Seuils configurés :
            </Typography>
            <Grid container spacing={2}>
              {Object.entries(sensor.seuils_alerte).map(([key, value]) => (
                <Grid item xs={12} sm={6} md={3} key={key}>
                  <Paper sx={{ p: 1, textAlign: 'center' }}>
                    <Typography variant="body2" color="text.secondary">
                      Seuil {key}
                    </Typography>
                    <Typography variant="body1">
                      {value} {SENSOR_UNITS[sensor.type]}
                    </Typography>
                  </Paper>
                </Grid>
              ))}
            </Grid>
          </Grid>
        </Grid>
      </DialogContent>
    </Dialog>
  );
};
