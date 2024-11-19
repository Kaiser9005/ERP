import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { TrendingUp, AccountBalance, MonetizationOn, Receipt } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getFinanceStats, FinanceStats as FinanceStatsType } from '../../services/finance';

const FinanceStats: React.FC = () => {
  const { data: stats } = useQuery<FinanceStatsType>(['finance-stats'], getFinanceStats);

  if (!stats) {
    return null;
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Chiffre d'Affaires"
          value={stats.revenue}
          unit="FCFA"
          variation={{
            valeur: stats.revenueVariation?.value || 0,
            type: stats.revenueVariation?.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<TrendingUp />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Bénéfice"
          value={stats.profit}
          unit="FCFA"
          variation={{
            valeur: stats.profitVariation?.value || 0,
            type: stats.profitVariation?.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<AccountBalance />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Trésorerie"
          value={stats.cashflow}
          unit="FCFA"
          variation={{
            valeur: stats.cashflowVariation?.value || 0,
            type: stats.cashflowVariation?.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<MonetizationOn />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Dépenses"
          value={stats.expenses}
          unit="FCFA"
          variation={{
            valeur: stats.expensesVariation?.value || 0,
            type: stats.expensesVariation?.type === 'increase' ? 'hausse' : 'baisse'
          }}
          icon={<Receipt />}
          color="warning"
        />
      </Grid>
    </Grid>
  );
};

export default FinanceStats;
