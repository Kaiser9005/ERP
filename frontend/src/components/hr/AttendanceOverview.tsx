import React from 'react';
import {
  Typography,
  Box,
  Grid,
  Chip,
  Alert,
  CircularProgress
} from '@mui/material';
import {
  PeopleAlt,
  EventBusy,
  School,
  WorkOff
} from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getEmployeeStats } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { EmployeeStats } from '../../types/hr';
import StatCard from './components/StatCard';

const AttendanceOverview: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery<EmployeeStats>({
    queryKey: queryKeys.hr.stats(),
    queryFn: getEmployeeStats
  });

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Une erreur est survenue lors du chargement des statistiques
      </Alert>
    );
  }

  if (!stats) {
    return (
      <Alert severity="info" sx={{ mb: 2 }}>
        Aucune donnée disponible
      </Alert>
    );
  }

  const absents = stats.totalEmployees - stats.presentToday - stats.onLeave - stats.inTraining;

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Vue d'ensemble des Présences
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Présents"
            value={stats.presentToday}
            total={stats.totalEmployees}
            icon={<PeopleAlt sx={{ color: 'primary.main' }} />}
            color="primary"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="En Congé"
            value={stats.onLeave}
            total={stats.totalEmployees}
            icon={<EventBusy sx={{ color: 'info.main' }} />}
            color="info"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="En Formation"
            value={stats.inTraining}
            total={stats.totalEmployees}
            icon={<School sx={{ color: 'warning.main' }} />}
            color="warning"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Absents"
            value={absents}
            total={stats.totalEmployees}
            icon={<WorkOff sx={{ color: 'error.main' }} />}
            color="error"
          />
        </Grid>
      </Grid>

      <Box mt={3}>
        <Typography variant="subtitle1" gutterBottom>
          Tendances
        </Typography>
        <Box display="flex" gap={2}>
          <Chip
            label={`Évolution effectif: ${Math.abs(stats.employeesVariation)}%`}
            color={stats.employeesVariation >= 0 ? 'success' : 'error'}
            size="small"
          />
          <Chip
            label={`Taux de congés: ${Math.abs(stats.leaveVariation)}%`}
            color={stats.leaveVariation <= 0 ? 'success' : 'warning'}
            size="small"
          />
          <Chip
            label={`Taux de formation: ${Math.abs(stats.trainingVariation)}%`}
            color={stats.trainingVariation >= 0 ? 'info' : 'warning'}
            size="small"
          />
        </Box>
      </Box>
    </Box>
  );
};

export default AttendanceOverview;
