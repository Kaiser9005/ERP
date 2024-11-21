import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  LinearProgress,
  Chip
} from '@mui/material';
import {
  Assignment,
  CheckCircle,
  Schedule,
  Warning,
  TrendingUp
} from '@mui/icons-material';
import { useQuery, QueryFunction } from 'react-query';
import { getProjectStats } from '../../services/projects';
import type { ProjectStats as ProjectStatsType } from '../../types/project';

interface StatCardProps {
  title: string;
  value: number;
  total?: number;
  icon: React.ReactNode;
  color: string;
  trend?: {
    value: number;
    isPositive: boolean;
  };
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  total,
  icon,
  color,
  trend
}) => {
  const progress = total ? (value / total) * 100 : undefined;

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
            {title}
          </Typography>
        </Box>

        <Typography variant="h4" gutterBottom>
          {value.toLocaleString()}
          {total && (
            <Typography
              component="span"
              variant="subtitle1"
              color="text.secondary"
              sx={{ ml: 1 }}
            >
              / {total.toLocaleString()}
            </Typography>
          )}
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
              {progress.toFixed(1)}% du total
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

const ProjectStats: React.FC = () => {
  const queryFn: QueryFunction<ProjectStatsType> = async () => {
    const response = await getProjectStats();
    return response as unknown as ProjectStatsType;
  };

  const { data: stats, isLoading } = useQuery<ProjectStatsType>(
    ['project-stats'],
    queryFn,
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      cacheTime: 10 * 60 * 1000 // 10 minutes
    }
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
        Vue d'ensemble des Projets
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Projets Actifs"
            value={stats.projets_actifs}
            total={stats.total_projets}
            icon={<Assignment sx={{ color: 'primary.main' }} />}
            color="primary"
            trend={{
              value: stats.variation_projets_actifs,
              isPositive: stats.variation_projets_actifs > 0
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Tâches Complétées"
            value={stats.taches_completees}
            total={stats.total_taches}
            icon={<CheckCircle sx={{ color: 'success.main' }} />}
            color="success"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Tâches En Retard"
            value={stats.taches_retard}
            icon={<Warning sx={{ color: 'error.main' }} />}
            color="error"
            trend={{
              value: stats.variation_taches_retard,
              isPositive: stats.variation_taches_retard < 0
            }}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Heures Travaillées"
            value={stats.heures_travaillees}
            icon={<Schedule sx={{ color: 'info.main' }} />}
            color="info"
            trend={{
              value: stats.variation_heures,
              isPositive: stats.variation_heures > 0
            }}
          />
        </Grid>
      </Grid>

      <Box mt={3}>
        <Typography variant="subtitle1" gutterBottom>
          Performance des Projets
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>
                  Répartition par Statut
                </Typography>
                <Box display="flex" gap={1} flexWrap="wrap">
                  <Chip
                    label={`En cours (${stats.repartition.en_cours})`}
                    color="primary"
                    size="small"
                  />
                  <Chip
                    label={`En attente (${stats.repartition.en_attente})`}
                    color="warning"
                    size="small"
                  />
                  <Chip
                    label={`Terminés (${stats.repartition.termines})`}
                    color="success"
                    size="small"
                  />
                  <Chip
                    label={`En retard (${stats.repartition.en_retard})`}
                    color="error"
                    size="small"
                  />
                </Box>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} sm={6}>
            <Card>
              <CardContent>
                <Typography variant="subtitle2" gutterBottom>
                  Taux de Complétion
                </Typography>
                <Box>
                  <Typography variant="h3" gutterBottom>
                    {stats.taux_completion}%
                  </Typography>
                  <LinearProgress
                    variant="determinate"
                    value={stats.taux_completion}
                    sx={{ mb: 1, height: 8, borderRadius: 4 }}
                    color="success"
                  />
                  <Typography variant="body2" color="text.secondary">
                    {stats.projets_termines} projets terminés sur {stats.total_projets}
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

export default ProjectStats;
