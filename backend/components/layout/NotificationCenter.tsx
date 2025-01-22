import React from 'react';
import {
  Drawer,
  Box,
  Typography,
  IconButton,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Divider,
} from '@mui/material';
import { Close, Notifications, CheckCircle, Warning, Info } from '@mui/icons-material';

interface NotificationCenterProps {
  open: boolean;
  onClose: () => void;
}

const mockNotifications = [
  {
    id: 1,
    title: 'Alerte Stock',
    message: 'Le stock d\'engrais NPK est bas',
    type: 'warning',
    date: new Date().toISOString(),
  },
  {
    id: 2,
    title: 'Récolte Terminée',
    message: 'La récolte de la parcelle P001 est terminée',
    type: 'success',
    date: new Date().toISOString(),
  },
];

const NotificationCenter: React.FC<NotificationCenterProps> = ({ open, onClose }) => {
  const getNotificationIcon = (type: string) => {
    switch (type) {
      case 'success':
        return <CheckCircle color="success" />;
      case 'warning':
        return <Warning color="warning" />;
      default:
        return <Info color="info" />;
    }
  };

  return (
    <Drawer
      anchor="right"
      open={open}
      onClose={onClose}
      sx={{
        '& .MuiDrawer-paper': {
          width: 320,
          maxWidth: '100%',
        },
      }}
    >
      <Box sx={{ p: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
          <Typography variant="h6" component="div" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Notifications />
            Notifications
          </Typography>
          <IconButton onClick={onClose}>
            <Close />
          </IconButton>
        </Box>

        <Divider />

        <List>
          {mockNotifications.map((notification) => (
            <React.Fragment key={notification.id}>
              <ListItem alignItems="flex-start">
                <ListItemAvatar>
                  <Avatar>{getNotificationIcon(notification.type)}</Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={notification.title}
                  secondary={
                    <React.Fragment>
                      <Typography
                        component="span"
                        variant="body2"
                        color="text.primary"
                      >
                        {notification.message}
                      </Typography>
                      <br />
                      <Typography
                        component="span"
                        variant="caption"
                        color="text.secondary"
                      >
                        {new Date(notification.date).toLocaleString()}
                      </Typography>
                    </React.Fragment>
                  }
                />
              </ListItem>
              <Divider variant="inset" component="li" />
            </React.Fragment>
          ))}
        </List>
      </Box>
    </Drawer>
  );
};

export default NotificationCenter;