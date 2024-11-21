import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../dashboard/StatCard';
import { Inventory, TrendingUp, Warning, LocalShipping } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getInventoryStats, Variation } from '../../services/inventory';

const InventoryStats: React.FC = () => {
  const { data: stats } = useQuery('inventory-stats', getInventoryStats);

  const formatVariation = (variation: Variation | undefined) => {
    if (!variation) return undefined;
    return {
      value: Math.abs(variation.value),
      type: variation.type
    };
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Valeur Totale"
          value={stats?.totalValue || 0}
          unit="FCFA"
          variation={formatVariation(stats?.valueVariation)}
          icon={<Inventory />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Rotation Stock"
          value={stats?.turnoverRate || 0}
          unit="jours"
          variation={formatVariation(stats?.turnoverVariation)}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Alertes Stock"
          value={stats?.alerts || 0}
          variation={formatVariation(stats?.alertsVariation)}
          icon={<Warning />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Mouvements"
          value={stats?.movements || 0}
          variation={formatVariation(stats?.movementsVariation)}
          icon={<LocalShipping />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default InventoryStats;
