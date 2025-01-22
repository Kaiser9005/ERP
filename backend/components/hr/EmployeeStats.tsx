import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { People, EventAvailable, School, TrendingUp } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getEmployeeStats } from '../../services/hr';

interface EmployeeStats {
  totalEmployees: number;
  activeEmployees: number;
  onLeave: number;
  inTraining: number;
  employeeGrowth: {
    value: number;
    type: 'increase' | 'decrease';
  };
  leaveRate: {
    value: number;
    type: 'increase' | 'decrease';
  };
  trainingRate: {
    value: number;
    type: 'increase' | 'decrease';
  };
}

const EmployeeStats: React.FC = () => {
  const { data: stats } = useQuery<EmployeeStats>(['employee-stats'], getEmployeeStats);

  if (!stats) {
    return null;
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Employés Actifs"
          value={stats.activeEmployees}
          variation={{
            valeur: stats.employeeGrowth.value,
            type: stats.employeeGrowth.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<People />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Congé"
          value={stats.onLeave}
          variation={{
            valeur: stats.leaveRate.value,
            type: stats.leaveRate.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<EventAvailable />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Formation"
          value={stats.inTraining}
          variation={{
            valeur: stats.trainingRate.value,
            type: stats.trainingRate.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<School />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Total Employés"
          value={stats.totalEmployees}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>
    </Grid>
  );
};

export default EmployeeStats;
