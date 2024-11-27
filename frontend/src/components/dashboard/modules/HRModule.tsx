import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { HRSummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import PeopleIcon from '@mui/icons-material/People';
import WorkIcon from '@mui/icons-material/Work';
import SchoolIcon from '@mui/icons-material/School';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';

interface HRModuleProps {
  data: HRSummary;
}

const HRModule: React.FC<HRModuleProps> = ({ data }) => {
  return (
    <Box>
      <Grid container spacing={2}>
        {/* Employés */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Employés"
            value={data.total_employees}
            icon={<PeopleIcon />}
            color="primary"
            loading={false}
          />
        </Grid>

        {/* Contrats Actifs */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Contrats Actifs"
            value={data.active_contracts}
            icon={<WorkIcon />}
            color="success"
            loading={false}
          />
        </Grid>

        {/* Formations Complétées */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Formations Complétées"
            value={data.completed_trainings}
            icon={<SchoolIcon />}
            color="info"
            loading={false}
          />
        </Grid>

        {/* Taux de Complétion */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Taux de Complétion"
            value={Math.round(data.training_completion_rate * 100)}
            unit="%"
            icon={<TrendingUpIcon />}
            color="warning"
            loading={false}
          />
        </Grid>
      </Grid>

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

export default HRModule;
