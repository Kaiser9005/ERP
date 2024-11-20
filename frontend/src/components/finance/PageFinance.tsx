import React, { useState } from 'react';
import { Grid, Box, Tabs, Tab } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import StatsFinance from './StatsFinance';
import ListeTransactions from './ListeTransactions';
import GraphiqueTresorerie from './GraphiqueTresorerie';
import VueBudget from './VueBudget';
import AnalyseBudget from './AnalyseBudget';
import ProjectionsFinancieres from './ProjectionsFinancieres';
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

const PageFinance: React.FC = () => {
  const navigate = useNavigate();
  const [ongletActuel, setOngletActuel] = useState(0);

  const handleChangementOnglet = (event: React.SyntheticEvent, nouvelOnglet: number) => {
    setOngletActuel(nouvelOnglet);
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
          <StatsFinance />
        </Grid>
      </Grid>

      {/* Onglets */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs
          value={ongletActuel}
          onChange={handleChangementOnglet}
          aria-label="onglets finance"
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
      <TabPanel value={ongletActuel} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} lg={8}>
            <GraphiqueTresorerie />
          </Grid>
          <Grid item xs={12} lg={4}>
            <VueBudget />
          </Grid>
        </Grid>
      </TabPanel>

      <TabPanel value={ongletActuel} index={1}>
        <AnalyseBudget />
      </TabPanel>

      <TabPanel value={ongletActuel} index={2}>
        <ProjectionsFinancieres />
      </TabPanel>

      <TabPanel value={ongletActuel} index={3}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <ListeTransactions />
          </Grid>
        </Grid>
      </TabPanel>
    </>
  );
};

export default PageFinance;
