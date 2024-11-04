import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { Agriculture, Spa, Timeline, TrendingUp } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getProductionStats } from '../../services/production';

const ProductionStats: React.FC = () => {
  const { data: stats, isLoading } = useQuery('production-stats', getProductionStats);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Production Totale"
          value={stats?.total || 0}
          unit="tonnes"
          variation={stats?.variation}
          icon={<Agriculture />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Rendement Moyen"
          value={stats?.rendement || 0}
          unit="t/ha"
          variation={stats?.rendementVariation}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Parcelles Actives"
          value={stats?.parcellesActives || 0}
          variation={stats?.parcellesVariation}
          icon={<Spa />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Cycles en Cours"
          value={stats?.cyclesEnCours || 0}
          variation={stats?.cyclesVariation}
          icon={<Timeline />}
          color="warning"
        />
      </Grid>
    </Grid>
  );
};

export default ProductionStats;