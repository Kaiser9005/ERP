import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import StatsProduction from './StatsProduction';
import StatsInventaire from './StatsInventaire';
import StatsFinance from './StatsFinance';
import StatsRH from './StatsRH';
import WidgetMeteo from './WidgetMeteo';
import ActivitesRecentes from './ActivitesRecentes';
import GraphiqueProduction from './GraphiqueProduction';
import GraphiqueTresorerie from './GraphiqueTresorerie';

const TableauBord: React.FC = () => {
  return (
    <>
      <PageHeader
        title="Tableau de Bord"
        subtitle="Vue d'ensemble des opérations de FOFAL"
      />

      <Grid container spacing={3}>
        {/* Statistiques de production */}
        <Grid item xs={12} lg={3}>
          <StatsProduction />
        </Grid>

        {/* Statistiques d'inventaire */}
        <Grid item xs={12} lg={3}>
          <StatsInventaire />
        </Grid>

        {/* Statistiques financières */}
        <Grid item xs={12} lg={3}>
          <StatsFinance />
        </Grid>

        {/* Statistiques RH */}
        <Grid item xs={12} lg={3}>
          <StatsRH />
        </Grid>

        {/* Graphique de production */}
        <Grid item xs={12} lg={8}>
          <GraphiqueProduction />
        </Grid>

        {/* Widget météo */}
        <Grid item xs={12} lg={4}>
          <WidgetMeteo />
        </Grid>

        {/* Graphique des flux financiers */}
        <Grid item xs={12} lg={8}>
          <GraphiqueTresorerie />
        </Grid>

        {/* Activités récentes */}
        <Grid item xs={12} lg={4}>
          <ActivitesRecentes />
        </Grid>
      </Grid>
    </>
  );
};

export default TableauBord;
