import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { ProductionSummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import FactoryIcon from '@mui/icons-material/Factory';
import SpeedIcon from '@mui/icons-material/Speed';
import SensorsIcon from '@mui/icons-material/Sensors';
import AssessmentIcon from '@mui/icons-material/Assessment';

interface ProductionModuleProps {
  data: ProductionSummary;
}

const ProductionModule: React.FC<ProductionModuleProps> = ({ data }) => {
  return (
    <Box>
      <Grid container spacing={2}>
        {/* Production Journalière */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Production Journalière"
            value={data.daily_production}
            icon={<FactoryIcon />}
            color="primary"
            loading={false}
          />
        </Grid>

        {/* Taux d'Efficacité */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Taux d'Efficacité"
            value={Math.round(data.efficiency_rate * 100)}
            unit="%"
            icon={<SpeedIcon />}
            color="success"
            loading={false}
          />
        </Grid>

        {/* Capteurs Actifs */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Capteurs Actifs"
            value={data.active_sensors}
            icon={<SensorsIcon />}
            color="info"
            loading={false}
          />
        </Grid>

        {/* Score Qualité */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Score Qualité"
            value={Math.round(data.quality_metrics.overall_score * 100)}
            unit="%"
            icon={<AssessmentIcon />}
            color="warning"
            loading={false}
          />
        </Grid>
      </Grid>

      {/* Métriques de Qualité Détaillées */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Métriques de Qualité
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Taux de Défauts
              </Typography>
              <Typography variant="h6" color="error">
                {(data.quality_metrics.defect_rate * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Taux de Conformité
              </Typography>
              <Typography variant="h6" color="success.main">
                {(data.quality_metrics.compliance_rate * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Score d'Efficience
              </Typography>
              <Typography variant="h6" color="primary">
                {(data.quality_metrics.efficiency_score * 100).toFixed(1)}%
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* Activités Récentes */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Activités Récentes
        </Typography>
        <Box>
          {data.recent_activities.map((activity) => (
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
    </Box>
  );
};

export default ProductionModule;
