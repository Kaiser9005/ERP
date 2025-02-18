import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { Inventory, TrendingUp, Warning, LocalShipping } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStatsInventaire, StatsInventaire as StatsInventaireService } from '../../services/inventaire';

interface StatistiquesInventaire {
  valeurTotale: number;
  variationValeur: { valeur: number; type: 'hausse' | 'baisse' };
  tauxRotation: number;
  variationRotation: { valeur: number; type: 'hausse' | 'baisse' };
  alertes: number;
  variationAlertes: { valeur: number; type: 'hausse' | 'baisse' };
  mouvements: number;
  variationMouvements: { valeur: number; type: 'hausse' | 'baisse' };
}

const transformStatsInventaire = (stats: StatsInventaireService): StatistiquesInventaire => ({
  valeurTotale: stats.valeur_totale,
  variationValeur: stats.valeur_stock,
  tauxRotation: stats.total_produits,
  variationRotation: stats.rotation_stock,
  alertes: stats.stock_faible,
  variationAlertes: { valeur: 0, type: 'hausse' },
  mouvements: stats.mouvements.entrees,
  variationMouvements: { valeur: 0, type: 'hausse' }
});

const StatsInventaire: React.FC = () => {
  const { data: statsService } = useQuery<StatsInventaireService>('statistiques-inventaire', getStatsInventaire);
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
          variation={stats?.variationAlertes}
          icon={<Warning />}
          color="warning"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Mouvements"
          value={stats?.mouvements || 0}
          variation={stats?.variationMouvements}
          icon={<LocalShipping />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default StatsInventaire;
