import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Divider,
} from '@mui/material';
import {
  Dashboard,
  Agriculture,
  Inventory,
  People,
  AccountBalance,
  Assignment,
  Settings,
} from '@mui/icons-material';
import { useNavigate, useLocation } from 'react-router-dom';

interface SideBarProps {
  open: boolean;
  onClose: () => void;
  width: number;
}

const menuItems = [
  { text: 'Tableau de bord', icon: <Dashboard />, path: '/dashboard' },
  { text: 'Production', icon: <Agriculture />, path: '/production' },
  { text: 'Inventaire', icon: <Inventory />, path: '/inventaire' },
  { text: 'Employés', icon: <People />, path: '/employes' },
  { text: 'Finance', icon: <AccountBalance />, path: '/finance' },
  { text: 'Projets', icon: <Assignment />, path: '/projets' },
  { text: 'Paramètres', icon: <Settings />, path: '/parametres' },
];

const SideBar: React.FC<SideBarProps> = ({ open, onClose, width }) => {
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
        width,
        flexShrink: 0,
        '& .MuiDrawer-paper': {
          width,
          boxSizing: 'border-box',
          mt: 8,
        },
      }}
    >
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
      <Divider />
    </Drawer>
  );
};

export default SideBar;