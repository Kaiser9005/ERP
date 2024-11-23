import React from 'react';
import { Grid, Alert } from '@mui/material';
import { TrendingUp, TrendingDown, AccountBalance, Receipt } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getFinanceStats } from '../../services/finance';
import { queryKeys } from '../../config/queryClient';
import StatCard from '../common/StatCard';
import type { FinanceStats as FinanceStatsType } from '../../types/finance';

const FinanceStats: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery<FinanceStatsType>({
    queryKey: queryKeys.finance.stats(),
    queryFn: () => getFinanceStats(),
    staleTime: 1000 * 60 * 5 // 5 minutes
  });

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 3 }}>
        Erreur lors du chargement des statistiques financières
      </Alert>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Revenus"
          value={stats?.revenue ?? 0}
          icon={<TrendingUp />}
          color="primary"
          unit="XAF"
          loading={isLoading}
          variation={stats ? {
            valeur: stats.revenueVariation,
            type: stats.revenueVariation >= 0 ? 'hausse' : 'baisse'
          } : undefined}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Bénéfices"
          value={stats?.profit ?? 0}
          icon={<AccountBalance />}
          color="success"
          unit="XAF"
          loading={isLoading}
          variation={stats ? {
            valeur: stats.profitVariation,
            type: stats.profitVariation >= 0 ? 'hausse' : 'baisse'
          } : undefined}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Trésorerie"
          value={stats?.cashflow ?? 0}
          icon={<Receipt />}
          color="info"
          unit="XAF"
          loading={isLoading}
          variation={stats ? {
            valeur: stats.cashflowVariation,
            type: stats.cashflowVariation >= 0 ? 'hausse' : 'baisse'
          } : undefined}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Dépenses"
          value={stats?.expenses ?? 0}
          icon={<TrendingDown />}
          color="warning"
          unit="XAF"
          loading={isLoading}
          variation={stats ? {
            valeur: -stats.expensesVariation,
            type: stats.expensesVariation <= 0 ? 'hausse' : 'baisse'
          } : undefined}
        />
      </Grid>
    </Grid>
  );
};

export default FinanceStats;
