import React from 'react';
import { Box, Container, Tabs, Tab } from '@mui/material';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import PageHeader from '../layout/PageHeader';

const ParametrageLayout: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleTabChange = (_: React.SyntheticEvent, value: string) => {
    navigate(value);
  };

  const currentTab = location.pathname.split('/').pop() || 'general';

  return (
    <Box>
      <PageHeader
        title="Paramétrage"
        subtitle="Configuration du système"
      />

      <Container maxWidth="lg">
        <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
          <Tabs
            value={currentTab}
            onChange={handleTabChange}
            aria-label="paramétrage tabs"
          >
            <Tab
              label="Paramètres Généraux"
              value="general"
            />
            <Tab
              label="Configuration des Modules"
              value="modules"
            />
          </Tabs>
        </Box>

        <Box sx={{ py: 2 }}>
          <Outlet />
        </Box>
      </Container>
    </Box>
  );
};

export default ParametrageLayout;
