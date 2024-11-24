import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { Agriculture, Inventory, AccountBalance, People } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import StatCard from '../common/StatCard';
import CashFlowChart from '../comptabilite/CashFlowChart';
import ProductionChart from './ProductionChart';
import RecentActivities from './RecentActivities';
import WeatherWidget from './WeatherWidget';
import { getDashboardStats } from '../../services/dashboard';

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
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['dashboard', 'stats'],
    queryFn: getDashboardStats,
    staleTime: 1000 * 60 * 5 // 5 minutes
  });

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Tableau de Bord
        </Typography>
        <Typography color="error">
          Une erreur est survenue lors du chargement des données
        </Typography>
      </Box>
    );
  }

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
            loading={isLoading}
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
            loading={isLoading}
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
            loading={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Employés Actifs"
            value={stats?.hr.activeEmployees || 0}
            variation={convertirVariation(stats?.hr.variation)}
            icon={<People />}
            color="warning"
            loading={isLoading}
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
