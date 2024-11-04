import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import ProductionStats from './ProductionStats';
import InventoryStats from './InventoryStats';
import FinanceStats from './FinanceStats';
import HRStats from './HRStats';
import WeatherWidget from './WeatherWidget';
import RecentActivities from './RecentActivities';
import ProductionChart from './ProductionChart';
import CashFlowChart from './CashFlowChart';

const DashboardPage: React.FC = () => {
  return (
    <>
      <PageHeader
        title="Tableau de Bord"
        subtitle="Vue d'ensemble des opérations de FOFAL"
      />

      <Grid container spacing={3}>
        {/* Statistiques de production */}
        <Grid item xs={12} lg={3}>
          <ProductionStats />
        </Grid>

        {/* Statistiques d'inventaire */}
        <Grid item xs={12} lg={3}>
          <InventoryStats />
        </Grid>

        {/* Statistiques financières */}
        <Grid item xs={12} lg={3}>
          <FinanceStats />
        </Grid>

        {/* Statistiques RH */}
        <Grid item xs={12} lg={3}>
          <HRStats />
        </Grid>

        {/* Graphique de production */}
        <Grid item xs={12} lg={8}>
          <ProductionChart />
        </Grid>

        {/* Widget météo */}
        <Grid item xs={12} lg={4}>
          <WeatherWidget />
        </Grid>

        {/* Graphique des flux financiers */}
        <Grid item xs={12} lg={8}>
          <CashFlowChart />
        </Grid>

        {/* Activités récentes */}
        <Grid item xs={12} lg={4}>
          <RecentActivities />
        </Grid>
      </Grid>
    </>
  );
};

export default DashboardPage;