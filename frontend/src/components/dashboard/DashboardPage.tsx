import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { Agriculture, Inventory, AccountBalance, People } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import StatCard from '../common/StatCard';
import CashFlowChart from '../comptabilite/CashFlowChart';
import ProductionChart from './ProductionChart';
import RecentActivities from './RecentActivities';
import WidgetMeteo from './WidgetMeteo';
import { DashboardService } from '../../services/dashboard';
import type { ModuleStats } from '../../types/dashboard';

const DashboardPage: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery<ModuleStats>({
    queryKey: ['dashboard', 'unified'],
    queryFn: () => DashboardService.getUnifiedDashboard(),
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
            value={stats?.modules.production.daily_production || 0}
            unit="tonnes"
            icon={<Agriculture />}
            color="primary"
            loading={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Stock"
            value={stats?.modules.inventory.stock_value || 0}
            unit="FCFA"
            icon={<Inventory />}
            color="success"
            loading={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Chiffre d'Affaires"
            value={stats?.modules.finance.daily_revenue || 0}
            unit="FCFA"
            icon={<AccountBalance />}
            color="info"
            loading={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Employés Actifs"
            value={stats?.modules.hr.total_employees || 0}
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
          <WidgetMeteo />
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
