import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { Inventory, TrendingUp, Warning, LocalShipping } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStatsInventaire, StatsInventaire as StatsInventaireType } from '../../services/inventaire';

interface StatistiquesInventaire {
  valeurTotale: number;
  variationValeur: { value: number; type: 'increase' | 'decrease' };
  tauxRotation: number;
  variationRotation: { value: number; type: 'increase' | 'decrease' };
  alertes: number;
  variationAlertes: { value: number; type: 'increase' | 'decrease' };
  mouvements: number;
  variationMouvements: { value: number; type: 'increase' | 'decrease' };
}

const transformStatsInventaire = (stats: StatsInventaireType): StatistiquesInventaire => ({
  valeurTotale: stats.valeur_totale,
  variationValeur: stats.valeur_stock,
  tauxRotation: stats.total_produits,
  variationRotation: stats.rotation_stock,
  alertes: stats.stock_faible,
  variationAlertes: { value: 0, type: 'increase' },
  mouvements: stats.mouvements.entrees,
  variationMouvements: { value: 0, type: 'increase' }
});

const StatsInventaire: React.FC = () => {
  const { data: statsService } = useQuery<StatsInventaireType>('statistiques-inventaire', getStatsInventaire);
  const stats = statsService ? transformStatsInventaire(statsService) : undefined;

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Valeur Totale"
          value={stats?.valeurTotale || 0}
          unit="FCFA"
          variation={stats?.variationValeur}
          icon={<Inventory />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Rotation de Stock"
          value={stats?.tauxRotation || 0}
          unit="produits"
          variation={stats?.variationRotation}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Alertes de Stock"
          value={stats?.alertes || 0}
          unit="alertes"
          variation={stats?.variationAlertes}
          icon={<Warning />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Mouvements"
          value={stats?.mouvements || 0}
          unit="mouvements"
          variation={stats?.variationMouvements}
          icon={<LocalShipping />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default StatsInventaire;
