import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { AccountBalance, TrendingUp, AccountBalanceWallet, Receipt } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStatsFinance, FinanceStats } from '../../services/finance';

const StatsFinance: React.FC = () => {
  const { data: stats, isLoading } = useQuery<FinanceStats>('finance-stats', getStatsFinance);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Chiffre d'Affaires"
          value={stats?.revenue || 0}
          unit="FCFA"
          variation={{
            value: stats?.revenueVariation?.value || 0,
            type: stats?.revenueVariation?.type || 'increase'
          }}
          icon={<AccountBalance />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Bénéfice Net"
          value={stats?.profit || 0}
          unit="FCFA"
          variation={{
            value: stats?.profitVariation?.value || 0,
            type: stats?.profitVariation?.type || 'increase'
          }}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Trésorerie"
          value={stats?.cashflow || 0}
          unit="FCFA"
          variation={{
            value: stats?.cashflowVariation?.value || 0,
            type: stats?.cashflowVariation?.type || 'increase'
          }}
          icon={<AccountBalanceWallet />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Dépenses"
          value={stats?.expenses || 0}
          unit="FCFA"
          variation={{
            value: stats?.expensesVariation?.value || 0,
            type: stats?.expensesVariation?.type || 'increase'
          }}
          icon={<Receipt />}
          color="warning"
        />
      </Grid>
    </Grid>
  );
};

export default StatsFinance;
