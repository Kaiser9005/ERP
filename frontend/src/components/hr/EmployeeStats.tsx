import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../dashboard/StatCard';
import { People, EventAvailable, Sick, School } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getEmployeeStats } from '../../services/hr';

const EmployeeStats: React.FC = () => {
  const { data: stats } = useQuery('employee-stats', getEmployeeStats);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Effectif Total"
          value={stats?.totalEmployees || 0}
          variation={stats?.employeesVariation}
          icon={<People />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Présents Aujourd'hui"
          value={stats?.presentToday || 0}
          variation={stats?.presenceVariation}
          icon={<EventAvailable />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Congé"
          value={stats?.onLeave || 0}
          variation={stats?.leaveVariation}
          icon={<Sick />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="En Formation"
          value={stats?.inTraining || 0}
          variation={stats?.trainingVariation}
          icon={<School />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default EmployeeStats;