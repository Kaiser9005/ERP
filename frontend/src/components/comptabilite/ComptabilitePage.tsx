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

const TABS = [
  { label: 'Plan Comptable', component: ComptesList },
  { label: 'Saisie d\'Écritures', component: EcrituresForm },
  { label: 'Journaux', component: JournauxList },
  { label: 'Grand Livre', component: GrandLivre },
  { label: 'Balance', component: Balance },
  { label: 'Bilan', component: Bilan },
  { label: 'Compte de Résultat', component: CompteResultat }
];

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
          {TABS.map((tab, index) => (
            <Tab 
              key={index}
              label={tab.label}
              {...a11yProps(index)}
              sx={{
                minHeight: 48,
                textTransform: 'none',
                fontSize: '0.875rem',
                fontWeight: 'medium'
              }}
            />
          ))}
        </Tabs>
      </Box>

      {/* Contenu des onglets */}
      {TABS.map((tab, index) => (
        <TabPanel key={index} value={currentTab} index={index}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              {React.createElement(tab.component)}
            </Grid>
          </Grid>
        </TabPanel>
      ))}
    </>
  );
};

export default ComptabilitePage;
