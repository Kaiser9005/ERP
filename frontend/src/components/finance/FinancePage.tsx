import React, { useState } from 'react';
import { Grid, Box, Tabs, Tab } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import FinanceStats from './FinanceStats';
import TransactionsList from './TransactionsList';
import CashFlowChart from './CashFlowChart';
import BudgetOverview from './BudgetOverview';
import BudgetAnalysis from './BudgetAnalysis';
import FinancialProjections from './FinancialProjections';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`finance-tabpanel-${index}`}
      aria-labelledby={`finance-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ py: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const FinancePage: React.FC = () => {
  const navigate = useNavigate();
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

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

      {/* Vue d'ensemble - Toujours visible */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12}>
          <FinanceStats />
        </Grid>
      </Grid>

      {/* Onglets */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="finance tabs"
          variant="scrollable"
          scrollButtons="auto"
        >
          <Tab label="Tableau de Bord" id="finance-tab-0" />
          <Tab label="Analyse Budgétaire" id="finance-tab-1" />
          <Tab label="Projections" id="finance-tab-2" />
          <Tab label="Transactions" id="finance-tab-3" />
        </Tabs>
      </Box>

      {/* Contenu des onglets */}
      <TabPanel value={currentTab} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <CashFlowChart />
          </Grid>
          <Grid item xs={12} lg={4}>
            <BudgetOverview />
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={currentTab} index={1}>
        <BudgetAnalysis />
      </TabPanel>

      <TabPanel value={currentTab} index={2}>
        <FinancialProjections />
      </TabPanel>

      <TabPanel value={currentTab} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TransactionsList />
          </Grid>
        </Grid>
      </TabPanel>
    </>
  );
};

export default FinancePage;
