import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useQuery } from 'react-query';
import { getStatsRH } from '../../services/rh';

const StatsRH: React.FC = () => {
  const { data: stats } = useQuery('stats-rh', getStatsRH);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Ressources Humaines
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Effectif Total
          </Typography>
          <Typography variant="h4">
            {stats?.effectif_total || 0}
          </Typography>
          {stats?.variation_effectif && (
            <Typography
              variant="body2"
              color={stats.variation_effectif.type === 'hausse' ? 'success.main' : 'error.main'}
            >
              {stats.variation_effectif.type === 'hausse' ? '+' : '-'}
              {stats.variation_effectif.valeur}% par rapport au mois dernier
            </Typography>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Chip
            label={`${stats?.absences_jour || 0} Absences`}
            color="error"
            size="small"
          />
          <Chip
            label={`${stats?.conges_en_cours || 0} En congé`}
            color="warning"
            size="small"
          />
          <Chip
            label={`${stats?.evaluations_prevues || 0} Évaluations`}
            color="info"
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatsRH;
