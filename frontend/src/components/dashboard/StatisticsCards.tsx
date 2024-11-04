import React from 'react';
import { Grid } from '@mui/material';
import StatCard from './StatCard';
import { Agriculture, Inventory, AccountBalance, People } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getDashboardStats } from '../../services/dashboard';

const StatisticsCards: React.FC = () => {
  const { data: stats } = useQuery('dashboard-stats', getDashboardStats);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Production"
          value={stats?.production.total || 0}
          unit="tonnes"
          variation={stats?.production.variation}
          icon={<Agriculture />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Stock"
          value={stats?.inventory.value || 0}
          unit="FCFA"
          variation={stats?.inventory.variation}
          icon={<Inventory />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Chiffre d'Affaires"
          value={stats?.finance.revenue || 0}
          unit="FCFA"
          variation={stats?.finance.variation}
          icon={<AccountBalance />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Employés Actifs"
          value={stats?.hr.activeEmployees || 0}
          variation={stats?.hr.variation}
          icon={<People />}
          color="warning"
        />
      </Grid>
    </Grid>
  );
};

export default StatisticsCards;