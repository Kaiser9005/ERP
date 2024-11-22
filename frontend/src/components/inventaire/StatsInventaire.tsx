import React from 'react';
import { useQuery } from '@tanstack/react-query';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  LinearProgress
} from '@mui/material';
import {
  Inventory as InventoryIcon,
  MonetizationOn as MoneyIcon,
  Warning as WarningIcon,
  Sync as SyncIcon,
  TrendingUp as TrendingUpIcon
} from '@mui/icons-material';
import { getStatsInventaire } from '../../services/inventaire';
import type { StatsInventaire as StatsInventaireType, Variation } from '../../types/inventaire';
import StatCard from '../common/StatCard';

const formatVariation = (variation: Variation | undefined) => {
  if (!variation) return undefined;
  return {
    value: Math.abs(variation.value),
    type: variation.type
  };
};

const StatsInventaire: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery<StatsInventaireType>(
    ['stats-inventaire'],
    () => getStatsInventaire()
  );

  if (isLoading) {
    return <LinearProgress />;
  }

  if (error || !stats) {
    return (
      <Typography color="error">
        Erreur lors du chargement des statistiques
      </Typography>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6} lg={3}>
        <StatCard
          title="Valeur Totale"
          value={stats.valeur_totale}
          unit="XAF"
          variation={formatVariation(stats.valueVariation)}
          icon={<MoneyIcon />}
          color="primary"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <StatCard
          title="Rotation Stock"
          value={stats.turnoverRate || 0}
          unit="jours"
          variation={formatVariation(stats.turnoverVariation)}
          icon={<TrendingUpIcon />}
          color="success"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <StatCard
          title="Produits Sous Seuil"
          value={stats.produits_sous_seuil}
          unit="produits"
          variation={formatVariation(stats.alertsVariation)}
          icon={<WarningIcon />}
          color="warning"
        />
      </Grid>
      <Grid item xs={12} md={6} lg={3}>
        <StatCard
          title="Mouvements Récents"
          value={stats.mouvements_recents}
          unit="mouvements"
          variation={formatVariation(stats.movementsVariation)}
          icon={<SyncIcon />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Répartition par Catégorie
            </Typography>
            {Object.entries(stats.repartition_categories).map(([categorie, nombre]) => (
              <div key={categorie}>
                <Typography variant="body2" color="textSecondary">
                  {categorie}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={(nombre / stats.total_produits) * 100}
                  sx={{ mb: 1, height: 8, borderRadius: 4 }}
                />
              </div>
            ))}
          </CardContent>
        </Card>
      </Grid>

      <Grid item xs={12} md={6}>
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Évolution du Stock
            </Typography>
            {stats.evolution_stock.map((point, index) => (
              <div key={index}>
                <Typography variant="body2" color="textSecondary">
                  {new Date(point.date).toLocaleDateString()}
                </Typography>
                <Typography variant="body1">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'XAF'
                  }).format(point.valeur)}
                </Typography>
              </div>
            ))}
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
};

export default StatsInventaire;
