import React from 'react';
import {
  Box,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Typography,
  Chip,
  Paper,
  IconButton,
  Tooltip
} from '@mui/material';
import ErrorIcon from '@mui/icons-material/Error';
import WarningIcon from '@mui/icons-material/Warning';
import InfoIcon from '@mui/icons-material/Info';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DoneIcon from '@mui/icons-material/Done';
import { Alert } from '../../types/dashboard';

interface AlertsPanelProps {
  alerts: Alert[];
  onAcknowledge: (alertId: string) => void;
  onResolve: (alertId: string) => void;
}

const getSeverityIcon = (severity: 'low' | 'medium' | 'high') => {
  switch (severity) {
    case 'high':
      return <ErrorIcon color="error" />;
    case 'medium':
      return <WarningIcon color="warning" />;
    case 'low':
      return <InfoIcon color="info" />;
  }
};

const getSeverityColor = (severity: 'low' | 'medium' | 'high') => {
  switch (severity) {
    case 'high':
      return 'error';
    case 'medium':
      return 'warning';
    case 'low':
      return 'info';
  }
};

const getStatusColor = (status: 'active' | 'acknowledged' | 'resolved') => {
  switch (status) {
    case 'active':
      return 'error';
    case 'acknowledged':
      return 'warning';
    case 'resolved':
      return 'success';
  }
};

export const AlertsPanel: React.FC<AlertsPanelProps> = ({
  alerts,
  onAcknowledge,
  onResolve
}) => {
  const sortedAlerts = [...alerts].sort((a, b) => b.priority - a.priority);

  return (
    <Paper sx={{ p: 2, mb: 2 }}>
      <Typography variant="h6" gutterBottom>
        Alertes Critiques
      </Typography>
      {alerts.length === 0 ? (
        <Typography color="success.main" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <CheckCircleIcon />
          Aucune alerte critique
        </Typography>
      ) : (
        <List>
          {sortedAlerts.map((alert) => (
            <ListItem
              key={alert.id}
              sx={{
                mb: 1,
                border: 1,
                borderColor: 'divider',
                borderRadius: 1,
                '&:hover': {
                  bgcolor: 'action.hover'
                }
              }}
              secondaryAction={
                <Box>
                  {alert.status === 'active' && (
                    <Tooltip title="Accuser réception">
                      <IconButton
                        edge="end"
                        onClick={() => onAcknowledge(alert.id)}
                        size="small"
                        sx={{ mr: 1 }}
                      >
                        <DoneIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                  {alert.status !== 'resolved' && (
                    <Tooltip title="Marquer comme résolu">
                      <IconButton
                        edge="end"
                        onClick={() => onResolve(alert.id)}
                        size="small"
                      >
                        <CheckCircleIcon />
                      </IconButton>
                    </Tooltip>
                  )}
                </Box>
              }
            >
              <ListItemIcon>
                {getSeverityIcon(alert.severity)}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    {alert.message}
                    <Chip
                      label={alert.module}
                      size="small"
                      color="primary"
                      variant="outlined"
                    />
                    <Chip
                      label={alert.status}
                      size="small"
                      color={getStatusColor(alert.status) as any}
                      variant="outlined"
                    />
                  </Box>
                }
                secondary={new Date(alert.timestamp).toLocaleString()}
              />
            </ListItem>
          ))}
        </List>
      )}
    </Paper>
  );
};

export default AlertsPanel;
