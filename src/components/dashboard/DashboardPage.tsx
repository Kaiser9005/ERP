import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import StatCard from '../common/StatCard';
import { Agriculture, Inventory, AccountBalance, People } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getDashboardStats } from '../../services/dashboard';
import CashFlowChart from '../finance/CashFlowChart';
import ProductionChart from './ProductionChart';
import RecentActivities from './RecentActivities';
import WeatherWidget from './WeatherWidget';

type ApiVariation = {
  value: number;
  type: 'increase' | 'decrease';
};

type UiVariation = {
  valeur: number;
  type: 'hausse' | 'baisse';
};

// Fonction utilitaire pour convertir le format des variations
const convertirVariation = (variation?: ApiVariation): UiVariation | undefined => {
  if (!variation) return undefined;
  return {
    valeur: variation.value,
    type: variation.type === 'increase' ? 'hausse' as const : 'baisse' as const
  };
};

const DashboardPage: React.FC = () => {
  const { data: stats } = useQuery('dashboard-stats', getDashboardStats);

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord
      </Typography>

      <Grid container spacing={3}>
        {/* Statistiques principales */}
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Production"
            value={stats?.production.total || 0}
            unit="tonnes"
            variation={convertirVariation(stats?.production.variation)}
            icon={<Agriculture />}
            color="primary"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Stock"
            value={stats?.inventory.value || 0}
            unit="FCFA"
            variation={convertirVariation(stats?.inventory.variation)}
            icon={<Inventory />}
            color="success"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Chiffre d'Affaires"
            value={stats?.finance.revenue || 0}
            unit="FCFA"
            variation={convertirVariation(stats?.finance.variation)}
            icon={<AccountBalance />}
            color="info"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Employés Actifs"
            value={stats?.hr.activeEmployees || 0}
            variation={convertirVariation(stats?.hr.variation)}
            icon={<People />}
            color="warning"
          />
        </Grid>

        {/* Graphiques et widgets */}
        <Grid item xs={12} lg={8}>
          <ProductionChart />
        </Grid>

        <Grid item xs={12} lg={4}>
          <WeatherWidget />
        </Grid>

        <Grid item xs={12} lg={8}>
          <CashFlowChart />
        </Grid>

        <Grid item xs={12} lg={4}>
          <RecentActivities />
        </Grid>
      </Grid>
    </Box>
  );
};

export default DashboardPage;
