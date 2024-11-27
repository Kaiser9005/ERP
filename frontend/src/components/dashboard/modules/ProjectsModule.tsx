import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { ProjectsSummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import AssignmentIcon from '@mui/icons-material/Assignment';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import EngineeringIcon from '@mui/icons-material/Engineering';
import TimelineIcon from '@mui/icons-material/Timeline';

interface ProjectsModuleProps {
  data: ProjectsSummary;
}

const ProjectsModule: React.FC<ProjectsModuleProps> = ({ data }) => {
  const { active_projects, completion_predictions, resource_optimization, recent_activities } = data;

  return (
    <Box>
      <Grid container spacing={2}>
        {/* Projets Actifs */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Projets Actifs"
            value={active_projects}
            icon={<AssignmentIcon />}
            color="primary"
            loading={false}
          />
        </Grid>

        {/* Gain d'Efficacité */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Gain d'Efficacité"
            value={resource_optimization.efficiency_gain}
            unit="%"
            icon={<TrendingUpIcon />}
            color="success"
            loading={false}
          />
        </Grid>

        {/* Économies Potentielles */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Économies Potentielles"
            value={resource_optimization.potential_savings}
            unit="€"
            icon={<TimelineIcon />}
            color="info"
            loading={false}
          />
        </Grid>

        {/* Projets à Risque */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Projets à Risque"
            value={completion_predictions.filter(p => p.risk_factors.length > 0).length}
            icon={<EngineeringIcon />}
            color="warning"
            loading={false}
          />
        </Grid>
      </Grid>

      {/* Prédictions de Complétion */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Prédictions de Complétion
        </Typography>
        <Grid container spacing={1}>
          {completion_predictions.map((prediction) => (
            <Grid item xs={12} key={prediction.project_id}>
              <Box
                sx={{
                  p: 1,
                  borderRadius: 1,
                  bgcolor: 'background.paper',
                  border: 1,
                  borderColor: 'divider'
                }}
              >
                <Typography variant="subtitle2">
                  {prediction.project_name}
                </Typography>
                <Typography variant="body2">
                  Complétion prévue : {new Date(prediction.predicted_completion).toLocaleDateString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Confiance : {Math.round(prediction.confidence * 100)}%
                </Typography>
                {prediction.risk_factors.length > 0 && (
                  <Typography variant="body2" color="warning.main">
                    Facteurs de risque : {prediction.risk_factors.join(', ')}
                  </Typography>
                )}
              </Box>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Recommandations d'Optimisation */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Recommandations d'Optimisation
        </Typography>
        <Box>
          {resource_optimization.recommendations.map((recommendation, index) => (
            <Typography key={index} variant="body2" sx={{ mb: 0.5 }}>
              • {recommendation}
            </Typography>
          ))}
        </Box>
      </Box>

      {/* Activités Récentes */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Activités Récentes
        </Typography>
        {recent_activities.map((activity) => (
          <Box
            key={activity.id}
            sx={{
              p: 1,
              mb: 1,
              borderRadius: 1,
              bgcolor: 'background.paper',
              border: 1,
              borderColor: 'divider',
              '&:hover': {
                bgcolor: 'action.hover'
              }
            }}
          >
            <Typography variant="body2" color="textSecondary">
              {new Date(activity.timestamp).toLocaleString()}
            </Typography>
            <Typography>{activity.description}</Typography>
            <Typography variant="body2" color="primary">
              {activity.user} - {activity.status}
            </Typography>
          </Box>
        ))}
      </Box>
    </Box>
  );
};

export default ProjectsModule;
