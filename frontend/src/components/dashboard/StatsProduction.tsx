import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress } from '@mui/material';
import { useQuery } from 'react-query';
import { getStatsProduction } from '../../services/production';

const StatsProduction: React.FC = () => {
  const { data: stats } = useQuery('stats-production', getStatsProduction);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Production
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Production Totale
          </Typography>
          <Typography variant="h4">
            {stats?.total || 0} T
          </Typography>
          {stats?.variation && (
            <Typography
              variant="body2"
              color={stats.variation.type === 'hausse' ? 'success.main' : 'error.main'}
            >
              {stats.variation.type === 'hausse' ? '+' : '-'}
              {stats.variation.valeur}% par rapport au mois dernier
            </Typography>
          )}
        </Box>

        <Box>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Parcelles Actives: {stats?.parcelles_actives || 0}
          </Typography>
          <LinearProgress
            variant="determinate"
            value={(stats?.parcelles_actives || 0) / 70 * 100}
            color="success"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatsProduction;
