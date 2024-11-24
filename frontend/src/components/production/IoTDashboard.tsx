import React, { useState } from 'react';
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert,
  Chip,
  IconButton,
  Tooltip,
  Button,
} from '@mui/material';
import {
  Add as AddIcon,
  Refresh as RefreshIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  ShowChart as ShowChartIcon,
} from '@mui/icons-material';

import { useCheckAllSensorsHealth, useParcelleSensors } from '../../services/iot';
import { SensorStatus, SENSOR_TYPE_LABELS, SENSOR_STATUS_LABELS } from '../../types/iot';
import { AddSensorDialog } from './AddSensorDialog';
import { SensorChartsDialog } from './SensorChartsDialog';

interface IoTDashboardProps {
  parcelleId: string;
}

export const IoTDashboard: React.FC<IoTDashboardProps> = ({ parcelleId }) => {
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [selectedSensorId, setSelectedSensorId] = useState<string | null>(null);

  const {
    data: sensors,
    isLoading: sensorsLoading,
    error: sensorsError,
  } = useParcelleSensors(parcelleId);

  const {
    data: healthData,
    isLoading: healthLoading,
    error: healthError,
    refetch: refetchHealth,
  } = useCheckAllSensorsHealth(parcelleId);

  const getStatusIcon = (status: SensorStatus) => {
    switch (status) {
      case SensorStatus.ACTIF:
        return <CheckCircleIcon color="success" />;
      case SensorStatus.MAINTENANCE:
        return <WarningIcon color="warning" />;
      case SensorStatus.ERREUR:
        return <ErrorIcon color="error" />;
      default:
        return <ErrorIcon color="disabled" />;
    }
  };

  const getStatusColor = (status: SensorStatus) => {
    switch (status) {
      case SensorStatus.ACTIF:
        return 'success.main';
      case SensorStatus.MAINTENANCE:
        return 'warning.main';
      case SensorStatus.ERREUR:
        return 'error.main';
      default:
        return 'text.disabled';
    }
  };

  if (sensorsLoading || healthLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight={400}>
        <CircularProgress />
      </Box>
    );
  }

  if (sensorsError || healthError) {
    return (
      <Alert severity="error">
        Une erreur est survenue lors du chargement des données des capteurs
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5" component="h2">
          Capteurs IoT
        </Typography>
        <Box>
          <Tooltip title="Rafraîchir l'état des capteurs">
            <IconButton onClick={() => refetchHealth()} size="small" sx={{ mr: 1 }}>
              <RefreshIcon />
            </IconButton>
          </Tooltip>
          <Tooltip title="Ajouter un capteur">
            <IconButton
              onClick={() => setShowAddDialog(true)}
              color="primary"
              size="small"
            >
              <AddIcon />
            </IconButton>
          </Tooltip>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {sensors?.map((sensor) => {
          const health = healthData?.find((h) => h.sensor_id === sensor.id)?.health;

          return (
            <Grid item xs={12} sm={6} md={4} key={sensor.id}>
              <Paper
                sx={{
                  p: 2,
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  position: 'relative',
                  borderLeft: 4,
                  borderColor: health ? getStatusColor(health.status) : 'divider',
                }}
              >
                <Box
                  position="absolute"
                  top={8}
                  right={8}
                  display="flex"
                  alignItems="center"
                  gap={1}
                >
                  <Tooltip title="Voir les graphiques">
                    <IconButton
                      size="small"
                      onClick={() => setSelectedSensorId(sensor.id)}
                    >
                      <ShowChartIcon />
                    </IconButton>
                  </Tooltip>
                  {health && getStatusIcon(health.status)}
                </Box>

                <Typography variant="h6" gutterBottom>
                  {sensor.code}
                </Typography>

                <Chip
                  label={SENSOR_TYPE_LABELS[sensor.type]}
                  size="small"
                  sx={{ alignSelf: 'flex-start', mb: 2 }}
                />

                {health && (
                  <>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      État: {SENSOR_STATUS_LABELS[health.status]}
                    </Typography>

                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      {health.message}
                    </Typography>

                    {health.battery_level !== undefined && (
                      <Typography variant="body2" color="text.secondary">
                        Batterie: {health.battery_level}%
                      </Typography>
                    )}

                    {health.signal_quality !== undefined && (
                      <Typography variant="body2" color="text.secondary">
                        Signal: {health.signal_quality}%
                      </Typography>
                    )}

                    {health.last_reading && (
                      <Box mt={2}>
                        <Typography variant="body2" color="text.secondary">
                          Dernière lecture:
                        </Typography>
                        <Typography variant="h6">
                          {health.last_reading.valeur} {health.last_reading.unite}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {new Date(health.last_reading.timestamp).toLocaleString()}
                        </Typography>
                      </Box>
                    )}
                  </>
                )}

                {!health && (
                  <Typography variant="body2" color="text.secondary">
                    Aucune donnée disponible
                  </Typography>
                )}
              </Paper>
            </Grid>
          )}
        )}

        {sensors?.length === 0 && (
          <Grid item xs={12}>
            <Paper sx={{ p: 3, textAlign: 'center' }}>
              <Typography variant="body1" color="text.secondary" gutterBottom>
                Aucun capteur n'est installé sur cette parcelle
              </Typography>
              <Button
                startIcon={<AddIcon />}
                variant="contained"
                onClick={() => setShowAddDialog(true)}
                sx={{ mt: 2 }}
              >
                Ajouter un capteur
              </Button>
            </Paper>
          </Grid>
        )}
      </Grid>

      <AddSensorDialog
        open={showAddDialog}
        onClose={() => setShowAddDialog(false)}
        parcelleId={parcelleId}
      />

      {selectedSensorId && (
        <SensorChartsDialog
          open={!!selectedSensorId}
          onClose={() => setSelectedSensorId(null)}
          sensorId={selectedSensorId}
        />
      )}
    </Box>
  );
};
