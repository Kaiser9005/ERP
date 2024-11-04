import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../dashboard/StatCard';
import { Assignment, TrendingUp, Warning, CheckCircle } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getProjectStats } from '../../services/projects';

const ProjectStats: React.FC = () => {
  const { data: stats } = useQuery('project-stats', getProjectStats);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Projets Actifs"
          value={stats?.activeProjects || 0}
          variation={stats?.projectsVariation}
          icon={<Assignment />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Taux de Complétion"
          value={stats?.completionRate || 0}
          unit="%"
          variation={stats?.completionVariation}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Tâches en Retard"
          value={stats?.delayedTasks || 0}
          variation={stats?.delayedVariation}
          icon={<Warning />}
          color="error"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Tâches Terminées"
          value={stats?.completedTasks || 0}
          variation={stats?.tasksVariation}
          icon={<CheckCircle />}
          color="info"
        />
      </Grid>
    </Grid>
  );
};

export default ProjectStats;