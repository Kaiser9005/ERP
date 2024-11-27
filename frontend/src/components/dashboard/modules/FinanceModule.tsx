import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { FinanceSummary } from '../../../types/dashboard';
import StatCard from '../../../components/common/StatCard';
import MonetizationOnIcon from '@mui/icons-material/MonetizationOn';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AssignmentIcon from '@mui/icons-material/Assignment';

interface FinanceModuleProps {
  data: FinanceSummary;
}

const FinanceModule: React.FC<FinanceModuleProps> = ({ data }) => {
  const getBudgetStatusColor = (status: string): 'success' | 'warning' | 'primary' | 'info' => {
    switch (status) {
      case 'under':
        return 'success';
      case 'over':
        return 'warning';
      default:
        return 'info';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('fr-FR', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(amount);
  };

  return (
    <Box>
      <Grid container spacing={2}>
        {/* Revenus Journaliers */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Revenus Journaliers"
            value={data.daily_revenue}
            unit="€"
            icon={<MonetizationOnIcon />}
            color="success"
            loading={false}
          />
        </Grid>

        {/* Dépenses Mensuelles */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Dépenses Mensuelles"
            value={data.monthly_expenses}
            unit="€"
            icon={<AccountBalanceIcon />}
            color="warning"
            loading={false}
          />
        </Grid>

        {/* Flux de Trésorerie */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Flux de Trésorerie"
            value={data.cash_flow}
            unit="€"
            icon={<TrendingUpIcon />}
            color="primary"
            loading={false}
          />
        </Grid>

        {/* Statut Budget */}
        <Grid item xs={12} sm={6}>
          <StatCard
            title="Statut Budget"
            value={Math.abs(data.budget_status.variance)}
            unit="%"
            icon={<AssignmentIcon />}
            color={getBudgetStatusColor(data.budget_status.status)}
            loading={false}
          />
        </Grid>
      </Grid>

      {/* Détails du Budget */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Détails du Budget
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Budget Actuel
              </Typography>
              <Typography variant="h6" color="primary.main">
                {formatCurrency(data.budget_status.current)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Budget Prévu
              </Typography>
              <Typography variant="h6" color="info.main">
                {formatCurrency(data.budget_status.planned)}
              </Typography>
            </Box>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Box
              sx={{
                p: 2,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider'
              }}
            >
              <Typography variant="subtitle2" color="textSecondary">
                Variance
              </Typography>
              <Typography
                variant="h6"
                color={data.budget_status.variance >= 0 ? 'success.main' : 'warning.main'}
              >
                {formatCurrency(data.budget_status.variance)}
              </Typography>
            </Box>
          </Grid>
        </Grid>
      </Box>

      {/* Transactions Récentes */}
      <Box mt={3}>
        <Typography variant="h6" gutterBottom>
          Transactions Récentes
        </Typography>
        <Box>
          {data.recent_transactions.map((transaction) => (
            <Box
              key={transaction.id}
              sx={{
                p: 1,
                mb: 1,
                borderRadius: 1,
                bgcolor: 'background.paper',
                border: 1,
                borderColor: 'divider',
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
            >
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Box>
                  <Typography variant="body2" color="textSecondary">
                    {new Date(transaction.timestamp).toLocaleString()}
                  </Typography>
                  <Typography>{transaction.description}</Typography>
                  <Typography variant="body2" color="primary">
                    {transaction.category}
                  </Typography>
                </Box>
                <Typography
                  variant="h6"
                  color={transaction.type === 'income' ? 'success.main' : 'warning.main'}
                >
                  {transaction.type === 'income' ? '+' : '-'}
                  {formatCurrency(transaction.amount)}
                </Typography>
              </Box>
            </Box>
          ))}
        </Box>
      </Box>
    </Box>
  );
};

export default FinanceModule;
