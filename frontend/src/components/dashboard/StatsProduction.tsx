import React from 'react';
import { Card, CardContent, Typography, Box, LinearProgress } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { getStatsProduction } from '../../services/production';
import type { ProductionStats } from '../../types/production';

const StatsProduction: React.FC = () => {
  const { data: stats } = useQuery<ProductionStats>({
    queryKey: ['stats-production'],
    queryFn: async () => {
      const response = await getStatsProduction();
      return response as unknown as ProductionStats;
    }
  });

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
              color={stats.variation.type === 'increase' ? 'success.main' : 'error.main'}
            >
              {stats.variation.type === 'increase' ? '+' : '-'}
              {stats.variation.value}% par rapport au mois dernier
            </Typography>
          )}
        </Box>

        <Box>
          <Typography variant="subtitle2" color="text.secondary" gutterBottom>
            Parcelles Actives: {stats?.parcellesActives || 0}
          </Typography>
          <LinearProgress
            variant="determinate"
            value={(stats?.parcellesActives || 0) / 70 * 100}
            color="success"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatsProduction;
