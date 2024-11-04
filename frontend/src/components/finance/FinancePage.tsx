import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import FinanceStats from './FinanceStats';
import TransactionsList from './TransactionsList';
import CashFlowChart from './CashFlowChart';
import BudgetOverview from './BudgetOverview';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const FinancePage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Finance"
        subtitle="Gestion financière et trésorerie"
        action={{
          label: "Nouvelle Transaction",
          onClick: () => navigate('/finance/transactions/new'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques financières */}
        <Grid item xs={12}>
          <FinanceStats />
        </Grid>

        {/* Graphique des flux de trésorerie */}
        <Grid item xs={12} lg={8}>
          <CashFlowChart />
        </Grid>

        {/* Aperçu du budget */}
        <Grid item xs={12} lg={4}>
          <BudgetOverview />
        </Grid>

        {/* Liste des transactions */}
        <Grid item xs={12}>
          <TransactionsList />
        </Grid>
      </Grid>
    </>
  );
};

export default FinancePage;