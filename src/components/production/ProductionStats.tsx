import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  LinearProgress
} from '@mui/material';
import { useQuery } from 'react-query';
import { productionService } from '../../services/production';
import { CultureType } from '../../types/production';
import {
  Agriculture,
  TrendingUp,
  LocalFlorist,
  WaterDrop
} from '@mui/icons-material';

interface StatCardProps {
  title: string;
  value: number;
  unit: string;
  icon: React.ReactNode;
  color: string;
  progress?: number;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  unit,
  icon,
  color,
  progress,
  trend
}) => (
  <Card>
    <CardContent>
      <Box display="flex" alignItems="center" mb={2}>
        <Box
          sx={{
            backgroundColor: `${color}.lighter`,
            borderRadius: '50%',
            p: 1,
            mr: 2,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}
        >
          {icon}
        </Box>
        <Typography variant="subtitle1" color="text.secondary">
          {title}
        </Typography>
      </Box>

      <Typography variant="h4" gutterBottom>
        {value.toLocaleString()}
        <Typography
          component="span"
          variant="subtitle1"
          color="text.secondary"
          sx={{ ml: 1 }}
        >
          {unit}
        </Typography>
      </Typography>

      {progress !== undefined && (
        <Box>
          <LinearProgress
            variant="determinate"
            value={progress}
            sx={{ mb: 1, backgroundColor: `${color}.lighter` }}
            color={color as any}
          />
          <Typography variant="body2" color="text.secondary">
            {progress}% de l'objectif
          </Typography>
        </Box>
      )}

      {trend && (
        <Box display="flex" alignItems="center" mt={1}>
          <TrendingUp
            color={trend.isPositive ? 'success' : 'error'}
            sx={{ mr: 1 }}
          />
          <Typography
            variant="body2"
            color={trend.isPositive ? 'success.main' : 'error.main'}
          >
            {trend.value}% par rapport au mois dernier
          </Typography>
        </Box>
      )}
    </CardContent>
  </Card>
);

const ProductionStats: React.FC = () => {
  const { data: stats, isLoading } = useQuery(
    'production-stats',
    () => productionService.getProductionStats('global')
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!stats) {
    return <Typography>Aucune donnée disponible</Typography>;
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Statistiques de Production
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Production Palmiers"
            value={stats.palmier.production_totale}
            unit="kg"
            icon={<Agriculture sx={{ color: 'primary.main' }} />}
            color="primary"
            progress={stats.palmier.objectif_completion}
            trend={{
              value: stats.palmier.variation_mensuelle,
              isPositive: stats.palmier.variation_mensuelle > 0
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Production Papayes"
            value={stats.papaye.production_totale}
            unit="kg"
            icon={<LocalFlorist sx={{ color: 'success.main' }} />}
            color="success"
            progress={stats.papaye.objectif_completion}
            trend={{
              value: stats.papaye.variation_mensuelle,
              isPositive: stats.papaye.variation_mensuelle > 0
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Rendement Moyen"
            value={stats.rendement_moyen}
            unit="kg/ha"
            icon={<TrendingUp sx={{ color: 'info.main' }} />}
            color="info"
            trend={{
              value: stats.variation_rendement,
              isPositive: stats.variation_rendement > 0
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Utilisation Eau"
            value={stats.utilisation_eau}
            unit="m³"
            icon={<WaterDrop sx={{ color: 'warning.main' }} />}
            color="warning"
            trend={{
              value: stats.variation_eau,
              isPositive: stats.variation_eau < 0
            }}
          />
        </Grid>
      </Grid>

      <Box mt={3}>
        <Typography variant="subtitle1" gutterBottom>
          Répartition par Culture
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>
                  {CultureType.PALMIER}
                </Typography>
                <Box display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Surface Active
                  </Typography>
                  <Typography>
                    {stats.palmier.surface_active} hectares
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Rendement
                  </Typography>
                  <Typography>
                    {stats.palmier.rendement} kg/ha
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>
                  {CultureType.PAPAYE}
                </Typography>
                <Box display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    Surface Active
                  </Typography>
                  <Typography>
                    {stats.papaye.surface_active} hectares
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    Rendement
                  </Typography>
                  <Typography>
                    {stats.papaye.rendement} kg/ha
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default ProductionStats;
