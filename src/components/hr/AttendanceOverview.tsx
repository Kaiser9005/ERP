import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  PeopleAlt,
  EventBusy,
  School,
  WorkOff
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getEmployeeStats, EmployeeStats } from '../../services/hr';

const StatCard: React.FC<{
  title: string;
  value: number;
  total: number;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, total, icon, color }) => {
  const percentage = (value / total) * 100;

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
              borderRadius: '50%',
              p: 1,
              mr: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6" color="text.secondary">
            {title}
          </Typography>
        </Box>

        <Typography variant="h4" gutterBottom>
          {value}
          <Typography
            component="span"
            variant="subtitle1"
            color="text.secondary"
            sx={{ ml: 1 }}
          >
            / {total}
          </Typography>
        </Typography>

        <Box>
          <LinearProgress
            variant="determinate"
            value={percentage}
            sx={{ mb: 1, backgroundColor: `${color}.lighter` }}
            color={color as any}
          />
          <Typography variant="body2" color="text.secondary">
            {percentage.toFixed(1)}% du total
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

const AttendanceOverview: React.FC = () => {
  const { data: stats, isLoading } = useQuery('employee-stats', getEmployeeStats);

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!stats) {
    return <Typography>Aucune donnée disponible</Typography>;
  }

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Vue d'ensemble des Présences
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Employés Actifs"
            value={stats.activeEmployees}
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
            value={stats.totalEmployees - stats.activeEmployees - stats.onLeave - stats.inTraining}
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
            label={`Croissance: ${stats.employeeGrowth.value}%`}
            color={stats.employeeGrowth.type === 'increase' ? 'success' : 'error'}
            size="small"
          />
          <Chip
            label={`Taux de congés: ${stats.leaveRate.value}%`}
            color={stats.leaveRate.type === 'increase' ? 'warning' : 'success'}
            size="small"
          />
          <Chip
            label={`Taux de formation: ${stats.trainingRate.value}%`}
            color={stats.trainingRate.type === 'increase' ? 'info' : 'warning'}
            size="small"
          />
        </Box>
      </Box>
    </Box>
  );
};

export default AttendanceOverview;
