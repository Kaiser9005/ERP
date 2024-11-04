import React from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Badge,
  Box,
  useTheme,
  Tooltip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications,
  LightMode,
  DarkMode,
} from '@mui/icons-material';
import { useThemeMode } from '../../hooks/useThemeMode';
import UserMenu from './UserMenu';

interface TopBarProps {
  onSidebarToggle: () => void;
  onNotificationsToggle: () => void;
}

const TopBar: React.FC<TopBarProps> = ({
  onSidebarToggle,
  onNotificationsToggle,
}) => {
  const theme = useTheme();
  const { toggleThemeMode, mode } = useThemeMode();

  return (
    <AppBar
      position="fixed"
      sx={{
        zIndex: theme.zIndex.drawer + 1,
        backgroundColor: 'background.paper',
        color: 'text.primary',
      }}
      elevation={1}
    >
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onSidebarToggle}
          sx={{ mr: 2 }}
        >
          <MenuIcon />
        </IconButton>

        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          FOFAL ERP
        </Typography>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Tooltip title="Changer le thème">
            <IconButton color="inherit" onClick={toggleThemeMode}>
              {mode === 'dark' ? <LightMode /> : <DarkMode />}
            </IconButton>
          </Tooltip>

          <Tooltip title="Notifications">
            <IconButton color="inherit" onClick={onNotificationsToggle}>
              <Badge badgeContent={3} color="error">
                <Notifications />
              </Badge>
            </IconButton>
          </Tooltip>

          <UserMenu />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default TopBar;