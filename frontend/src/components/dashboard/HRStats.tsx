import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useQuery } from 'react-query';
import { getEmployeeStats } from '../../services/hr';

const HRStats: React.FC = () => {
  const { data: stats } = useQuery('employee-stats', getEmployeeStats);

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
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip
            label={`${stats?.en_conge || 0} En congé`}
            color="warning"
            size="small"
          />
          <Chip
            label={`${stats?.presents || 0} Présents`}
            color="success"
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default HRStats;