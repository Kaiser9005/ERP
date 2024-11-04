import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
  Box,
  Typography,
  Avatar,
} from '@mui/material';
import {
  Dashboard,
  Agriculture,
  Inventory,
  People,
  AccountBalance,
  Settings,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

const DRAWER_WIDTH = 240;

interface SideBarProps {
  open: boolean;
  onClose: () => void;
  user: any;
}

const menuItems = [
  { text: 'Tableau de bord', icon: <Dashboard />, path: '/dashboard' },
  { text: 'Production', icon: <Agriculture />, path: '/production' },
  { text: 'Inventaire', icon: <Inventory />, path: '/inventaire' },
  { text: 'Employés', icon: <People />, path: '/employes' },
  { text: 'Finance', icon: <AccountBalance />, path: '/finance' },
  { text: 'Paramètres', icon: <Settings />, path: '/parametrage/general' },
];

const SideBar: React.FC<SideBarProps> = ({ open, onClose, user }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const handleNavigation = (path: string) => {
    navigate(path);
    onClose();
  };

  return (
    <Drawer
      variant="persistent"
      anchor="left"
      open={open}
      sx={{
        width: DRAWER_WIDTH,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width: DRAWER_WIDTH,
          boxSizing: 'border-box',
          mt: 8,
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
          <Avatar>{user?.prenom?.[0]}</Avatar>
          <Box>
            <Typography variant="subtitle1">
              {user?.prenom} {user?.nom}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {user?.role?.nom}
            </Typography>
          </Box>
        </Box>
        <Divider />
      </Box>

      <List>
        {menuItems.map((item) => (
          <ListItem key={item.text} disablePadding>
            <ListItemButton
              selected={location.pathname.startsWith(item.path)}
              onClick={() => handleNavigation(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default SideBar;