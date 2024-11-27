import React from 'react';
import { Box, Grid, Typography, CircularProgress, Alert } from '@mui/material';
import { School, Description, AccountBalance } from '@mui/icons-material';
import { useHRAnalytics } from '../../../services/hr_analytics';
import StatCard from '../components/StatCard';
import EmployeeStats from '../EmployeeStats';
import { queryKeys } from '../../../config/queryClient';

const HRAnalyticsDashboard: React.FC = () => {
  const { data: analytics, isLoading: isLoadingAnalytics, error: analyticsError } = useHRAnalytics();

  if (isLoadingAnalytics) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (analyticsError) {
    return (
      <Alert severity="error">
        Une erreur est survenue lors du chargement des analytics RH
      </Alert>
    );
  }

  if (!analytics) {
    return (
      <Alert severity="info">
        Aucune donnée disponible
      </Alert>
    );
  }

  const { formation_analytics, contract_analytics, payroll_analytics } = analytics;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord RH
      </Typography>

      {/* Statistiques des employés */}
      <Box mb={4}>
        <EmployeeStats />
      </Box>

      {/* Statistiques supplémentaires */}
      <Grid container spacing={3}>
        {/* Formations */}
        <Grid item xs={12} md={4}>
          <StatCard
            title="Formations"
            value={formation_analytics?.total_formations || 0}
            variation={formation_analytics?.completion_rate ? {
              valeur: formation_analytics.completion_rate * 100,
              type: formation_analytics.completion_rate >= 0 ? 'hausse' : 'baisse'
            } : undefined}
            icon={<School />}
            color="info"
            format="number"
          />
        </Grid>

        {/* Contrats */}
        <Grid item xs={12} md={4}>
          <StatCard
            title="Contrats"
            value={contract_analytics?.total_contracts || 0}
            variation={contract_analytics?.contract_renewal_rate ? {
              valeur: contract_analytics.contract_renewal_rate * 100,
              type: contract_analytics.contract_renewal_rate >= 0 ? 'hausse' : 'baisse'
            } : undefined}
            icon={<Description />}
            color="success"
            format="number"
          />
        </Grid>

        {/* Masse salariale */}
        <Grid item xs={12} md={4}>
          <StatCard
            title="Masse Salariale"
            value={payroll_analytics?.total_payroll || 0}
            variation={payroll_analytics?.payroll_trends ? {
              valeur: Object.values(payroll_analytics.payroll_trends)[0],
              type: Object.values(payroll_analytics.payroll_trends)[0] >= 0 ? 'hausse' : 'baisse'
            } : undefined}
            icon={<AccountBalance />}
            color="warning"
            format="currency"
          />
        </Grid>
      </Grid>
    </Box>
  );
};

export default HRAnalyticsDashboard;
