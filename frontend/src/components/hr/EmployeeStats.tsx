import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { People, EventAvailable, Sick, School } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getEmployeeStats } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { EmployeeStats as EmployeeStatsType } from '../../types/hr';

type VariationType = 'hausse' | 'baisse';

const formatVariation = (value: number): { valeur: number; type: VariationType } => ({
  valeur: Math.abs(value),
  type: value >= 0 ? 'hausse' : 'baisse'
});

const EmployeeStats: React.FC = () => {
  const { data: stats } = useQuery<EmployeeStatsType>({
    queryKey: queryKeys.hr.stats(),
    queryFn: getEmployeeStats
  });

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Effectif Total"
          value={stats?.totalEmployees || 0}
          variation={stats?.employeesVariation ? formatVariation(stats.employeesVariation) : undefined}
          icon={<People />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Présents Aujourd'hui"
          value={stats?.presentToday || 0}
          variation={stats?.presenceVariation ? formatVariation(stats.presenceVariation) : undefined}
          icon={<EventAvailable />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Congé"
          value={stats?.onLeave || 0}
          variation={stats?.leaveVariation ? formatVariation(stats.leaveVariation) : undefined}
          icon={<Sick />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Formation"
          value={stats?.inTraining || 0}
          variation={stats?.trainingVariation ? formatVariation(stats.trainingVariation) : undefined}
          icon={<School />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default EmployeeStats;
