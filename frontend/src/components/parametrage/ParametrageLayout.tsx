import React from 'react';
import { Outlet } from 'react-router-dom';
import { Tabs, Tab, Box } from '@mui/material';
import { useLocation, useNavigate } from 'react-router-dom';

const ParametrageLayout: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const handleTabChange = (_: React.SyntheticEvent, newValue: string) => {
    navigate(newValue);
  };

  return (
    <Box sx={{ width: '100%', height: '100%' }}>
      <Tabs
        value={location.pathname}
        onChange={handleTabChange}
        sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}
      >
        <Tab label="Paramètres Généraux" value="/parametrage/general" />
        <Tab label="Modules" value="/parametrage/modules" />
        <Tab label="Système" value="/parametrage/systeme" />
      </Tabs>
      <Box sx={{ p: 3 }}>
        <Outlet />
      </Box>
    </Box>
  );
}

export default ParametrageLayout;