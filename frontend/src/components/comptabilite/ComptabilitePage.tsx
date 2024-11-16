import React, { useState } from 'react';
import { Grid, Box, Tabs, Tab, Typography } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import ComptesList from './ComptesList';
import EcrituresForm from './EcrituresForm';
import JournauxList from './JournauxList';
import GrandLivre from './rapports/GrandLivre';
import Balance from './rapports/Balance';
import Bilan from './rapports/Bilan';
import CompteResultat from './rapports/CompteResultat';
import BudgetOverview from './BudgetOverview';
import FinanceStats from './FinanceStats';
import CashFlowChart from './CashFlowChart';
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
      id={`comptabilite-tabpanel-${index}`}
      aria-labelledby={`comptabilite-tab-${index}`}
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

const a11yProps = (index: number) => {
  return {
    id: `comptabilite-tab-${index}`,
    'aria-controls': `comptabilite-tabpanel-${index}`,
  };
};

const ComptabilitePage: React.FC = () => {
  const navigate = useNavigate();
  const [currentTab, setCurrentTab] = useState(0);

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setCurrentTab(newValue);
  };

  return (
    <>
      <PageHeader
        title="Comptabilité"
        subtitle="Gestion comptable et rapports financiers"
        action={{
          label: "Nouvelle Écriture",
          onClick: () => navigate('/comptabilite/ecritures/new'),
          icon: <Add />
        }}
      />

      {/* Vue d'ensemble */}
      <Box sx={{ mb: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <FinanceStats />
          </Grid>
          <Grid item xs={12} md={8}>
            <CashFlowChart />
          </Grid>
          <Grid item xs={12} md={4}>
            <BudgetOverview />
          </Grid>
        </Grid>
      </Box>

      {/* Navigation par onglets */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs
          value={currentTab}
          onChange={handleTabChange}
          aria-label="Onglets de comptabilité"
          variant="scrollable"
          scrollButtons="auto"
          sx={{
            '& .MuiTabs-flexContainer': {
              gap: 2
            }
          }}
        >
          <Tab label="Plan Comptable" {...a11yProps(0)} />
          <Tab label="Saisie d'Écritures" {...a11yProps(1)} />
          <Tab label="Journaux" {...a11yProps(2)} />
          <Tab label="Grand Livre" {...a11yProps(3)} />
          <Tab label="Balance" {...a11yProps(4)} />
          <Tab label="Bilan" {...a11yProps(5)} />
          <Tab label="Compte de Résultat" {...a11yProps(6)} />
        </Tabs>
      </Box>

      {/* Contenu des onglets */}
      <TabPanel value={currentTab} index={0}>
        <ComptesList />
      </TabPanel>

      <TabPanel value={currentTab} index={1}>
        <EcrituresForm />
      </TabPanel>

      <TabPanel value={currentTab} index={2}>
        <JournauxList />
      </TabPanel>

      <TabPanel value={currentTab} index={3}>
        <GrandLivre />
      </TabPanel>

      <TabPanel value={currentTab} index={4}>
        <Balance />
      </TabPanel>

      <TabPanel value={currentTab} index={5}>
        <Bilan />
      </TabPanel>

      <TabPanel value={currentTab} index={6}>
        <CompteResultat />
      </TabPanel>
    </>
  );
};

export default ComptabilitePage;
