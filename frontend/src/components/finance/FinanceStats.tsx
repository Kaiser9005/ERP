import React from 'react';
import { Grid } from '@mui/material';
import StatCard from '../common/StatCard';
import { AccountBalance, TrendingUp, AccountBalanceWallet, Receipt } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getFinanceStats } from '../../services/finance';

const FinanceStats: React.FC = () => {
  const { data: stats, isLoading } = useQuery('finance-stats', getFinanceStats);

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Chiffre d'Affaires"
          value={stats?.revenue || 0}
          unit="FCFA"
          variation={stats?.revenueVariation}
          icon={<AccountBalance />}
          color="primary"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Bénéfice Net"
          value={stats?.profit || 0}
          unit="FCFA"
          variation={stats?.profitVariation}
          icon={<TrendingUp />}
          color="success"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Trésorerie"
          value={stats?.cashflow || 0}
          unit="FCFA"
          variation={stats?.cashflowVariation}
          icon={<AccountBalanceWallet />}
          color="info"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Dépenses"
          value={stats?.expenses || 0}
          unit="FCFA"
          variation={stats?.expensesVariation}
          icon={<Receipt />}
          color="warning"
        />
      </Grid>
    </Grid>
  );
};

export default FinanceStats;