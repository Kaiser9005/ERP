import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import { FinanceStats } from '../../types/finance';
import { formatCurrency } from '../../utils/format';

interface StatsFinanceProps {
  stats: FinanceStats;
}

const StatsFinance: React.FC<StatsFinanceProps> = ({ stats }) => {
  const renderStatWithVariation = (
    label: string,
    value: number | undefined,
    variation?: { valeur: number; type: 'hausse' | 'baisse' }
  ) => (
    <Paper elevation={3} sx={{ p: 2, textAlign: 'center' }}>
      <Typography variant="h6">{label}</Typography>
      <Typography variant="h4">{value !== undefined ? formatCurrency(value) : 'N/A'}</Typography>
      {variation && (
        <Typography
          variant="body2"
          color={variation.type === 'hausse' ? 'success.main' : 'error.main'}
        >
          {variation.type === 'hausse' ? '▲' : '▼'} {variation.valeur}%
        </Typography>
      )}
    </Paper>
  );

  return (
    <Box sx={{ flexGrow: 1, p: 2 }}>
      <Typography variant="h4" gutterBottom>
        Statistiques Financières
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={3}>
          {renderStatWithVariation(
            'Revenus',
            stats.revenue,
            stats.revenueVariation
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderStatWithVariation(
            'Bénéfice',
            stats.profit,
            stats.profitVariation
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderStatWithVariation(
            'Flux de Trésorerie',
            stats.cashflow,
            stats.cashflowVariation
          )}
        </Grid>
        <Grid item xs={12} md={3}>
          {renderStatWithVariation(
            'Dépenses',
            stats.expenses,
            stats.expensesVariation
          )}
        </Grid>
      </Grid>
    </Box>
  );
};

export default StatsFinance;
