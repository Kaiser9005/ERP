import React, { useState } from 'react';
import { Box, useMediaQuery, useTheme } from '@mui/material';
import { Outlet } from 'react-router-dom';
import TopBar from './TopBar';
import SideBar from './SideBar';
import NotificationCenter from './NotificationCenter';
import BreadcrumbNav from './BreadcrumbNav';
import { useAuth } from '../../hooks/useAuth';

const DashboardLayout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const { user } = useAuth();

  const handleSidebarToggle = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleNotificationsToggle = () => {
    setNotificationsOpen(!notificationsOpen);
  };

  return (
    <Box sx={{ display: 'flex', minHeight: '100vh' }}>
      <TopBar 
        onSidebarToggle={handleSidebarToggle}
        onNotificationsToggle={handleNotificationsToggle}
      />
      
      <SideBar 
        open={sidebarOpen && !isMobile}
        onClose={() => setSidebarOpen(false)}
        user={user}
      />

      <NotificationCenter 
        open={notificationsOpen}
        onClose={() => setNotificationsOpen(false)}
      />

      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          mt: 8,
          ml: { md: sidebarOpen ? '240px' : 0 },
          transition: theme.transitions.create('margin', {
            easing: theme.transitions.easing.sharp,
            duration: theme.transitions.duration.leavingScreen,
          }),
        }}
      >
        <BreadcrumbNav />
        <Outlet />
      </Box>
    </Box>
  );
};

export default DashboardLayout;