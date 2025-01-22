import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { useQuery } from 'react-query';
import { getFinanceStats } from '../../services/finance';

const FinanceStats: React.FC = () => {
  const { data: stats } = useQuery('finance-stats', getFinanceStats);

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'XAF',
      maximumFractionDigits: 0
    }).format(value);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Finance
        </Typography>

        <Box sx={{ mb: 2 }}>
          <Typography variant="subtitle2" color="text.secondary">
            Chiffre d'Affaires
          </Typography>
          <Typography variant="h4">
            {formatCurrency(stats?.recettes || 0)}
          </Typography>
          {stats?.variation && (
            <Typography
              variant="body2"
              color={stats.variation.type === 'increase' ? 'success.main' : 'error.main'}
            >
              {stats.variation.type === 'increase' ? '+' : '-'}
              {stats.variation.value}% ce mois
            </Typography>
          )}
        </Box>

        <Box>
          <Typography variant="subtitle2" color="text.secondary">
            Solde
          </Typography>
          <Typography
            variant="h6"
            color={stats?.solde && stats.solde >= 0 ? 'success.main' : 'error.main'}
          >
            {formatCurrency(stats?.solde || 0)}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default FinanceStats;