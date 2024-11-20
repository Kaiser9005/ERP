import React from 'react';
import { Card, CardContent, Typography, Box, Chip } from '@mui/material';
import { useQuery } from 'react-query';
import { getStatsFinance } from '../../services/finance';

const StatsFinance: React.FC = () => {
  const { data: stats } = useQuery('stats-finance', getStatsFinance);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Finance
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Trésorerie
          </Typography>
          <Typography variant="h4">
            {new Intl.NumberFormat('fr-FR', {
              style: 'currency',
              currency: 'XAF',
              maximumFractionDigits: 0
            }).format(stats?.tresorerie || 0)}
          </Typography>
          {stats?.variation_tresorerie && (
            <Typography
              variant="body2"
              color={stats.variation_tresorerie.type === 'hausse' ? 'success.main' : 'error.main'}
            >
              {stats.variation_tresorerie.type === 'hausse' ? '+' : '-'}
              {stats.variation_tresorerie.valeur}% par rapport au mois dernier
            </Typography>
          )}
        </Box>

        <Box sx={{ display: 'flex', gap: 1 }}>
          <Chip
            label={`${stats?.factures_impayees || 0} Factures impayées`}
            color="warning"
            size="small"
          />
          <Chip
            label={`${stats?.paiements_prevus || 0} Paiements prévus`}
            color="info"
            size="small"
          />
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatsFinance;
