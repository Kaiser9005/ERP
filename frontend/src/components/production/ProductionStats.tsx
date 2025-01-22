import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  LinearProgress,
  Alert
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
import { useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { validate as uuidValidate } from 'uuid';

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
}) => {
  const { t } = useTranslation();
  return (
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
            {t(title)}
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
              {t('production.stats.objectifCompletion', { progress })}
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
};

const ProductionStats: React.FC = () => {
  const { t } = useTranslation();
  const { parcelle_id } = useParams();
  let validatedParcelleId: string | undefined = undefined;
  let isValidUUID = false;
  if (parcelle_id) {
    isValidUUID = uuidValidate(parcelle_id);
    if (isValidUUID) {
      validatedParcelleId = parcelle_id;
    }
  }
  const { data: stats, isLoading } = useQuery(
    ['production-stats', validatedParcelleId],
    () => validatedParcelleId ? productionService.getProductionStats(validatedParcelleId) : Promise.reject('Invalid parcelle_id')
  );

  if (isLoading) {
    return <Typography>{t('commun.chargement')}</Typography>;
  }

  if (!stats) {
    return <Typography>{t('commun.aucuneDonnee')}</Typography>;
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {t('production.stats.titre')}
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="production.stats.palmier"
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
            title="production.stats.papaye"
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
            title="production.stats.rendementMoyen"
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
            title="production.stats.utilisationEau"
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
          {t('production.stats.repartition')}
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>
                  {t(`culture.\${CultureType.PALMIER.toLowerCase()}`)}
                </Typography>
                <Box display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    {t('production.stats.surfaceActive')}
                  </Typography>
                  <Typography>
                    {stats.palmier.surface_active} hectares
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    {t('production.stats.rendement')}
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
                  {t(`culture.\${CultureType.PAPAYE.toLowerCase()}`)}
                </Typography>
                <Box display="flex" justifyContent="space-between" mb={1}>
                  <Typography variant="body2" color="text.secondary">
                    {t('production.stats.surfaceActive')}
                  </Typography>
                  <Typography>
                    {stats.papaye.surface_active} hectares
                  </Typography>
                </Box>
                <Box display="flex" justifyContent="space-between">
                  <Typography variant="body2" color="text.secondary">
                    {t('production.stats.rendement')}
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
