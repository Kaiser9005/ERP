import { FC } from 'react';
import {
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Paper,
  Chip,
  Box,
  Typography,
  useTheme
} from '@mui/material';
import {
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  Sync as SyncIcon,
  Notifications as NotificationsIcon
} from '@mui/icons-material';
import type { CrossModuleRecommendation } from '../../types/analytics_cross_module';

interface RecommendationsListProps {
  recommendations: CrossModuleRecommendation[];
}

export const RecommendationsList: FC<RecommendationsListProps> = ({ recommendations }) => {
  const theme = useTheme();

  const getIcon = (type: string) => {
    switch (type) {
      case 'CORRELATION':
        return <SyncIcon />;
      case 'ML_PREDICTION':
        return <TrendingUpIcon />;
      case 'OPTIMIZATION':
        return <TrendingUpIcon />;
      case 'ALERT':
        return <WarningIcon />;
      default:
        return <NotificationsIcon />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'HIGH':
        return theme.palette.error.main;
      case 'MEDIUM':
        return theme.palette.warning.main;
      case 'LOW':
        return theme.palette.success.main;
      default:
        return theme.palette.info.main;
    }
  };

  return (
    <Paper sx={{ p: 0 }}>
      <List>
        {recommendations.map((recommendation, index) => (
          <ListItem
            key={index}
            divider={index < recommendations.length - 1}
            sx={{
              '&:hover': {
                backgroundColor: theme.palette.action.hover
              }
            }}
          >
            <ListItemIcon>
              {getIcon(recommendation.type)}
            </ListItemIcon>
            <ListItemText
              primary={
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <Typography variant="subtitle1">
                    {recommendation.description}
                  </Typography>
                  <Chip
                    label={recommendation.priority}
                    size="small"
                    sx={{
                      backgroundColor: getPriorityColor(recommendation.priority),
                      color: 'white'
                    }}
                  />
                </Box>
              }
              secondary={
                <Box>
                  <Box sx={{ mb: 1 }}>
                    <Typography variant="body2" color="textSecondary">
                      Modules concernés:
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                      {recommendation.modules.map((module) => (
                        <Chip
                          key={module}
                          label={module}
                          size="small"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                  </Box>
                  {recommendation.actions.length > 0 && (
                    <Box>
                      <Typography variant="body2" color="textSecondary">
                        Actions recommandées:
                      </Typography>
                      <List dense>
                        {recommendation.actions.map((action, actionIndex) => (
                          <ListItem key={actionIndex} dense>
                            <ListItemText
                              primary={action}
                              sx={{ m: 0 }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  )}
                  {recommendation.expected_impact && (
                    <Box sx={{ mt: 1 }}>
                      <Typography variant="body2" color="textSecondary">
                        Impact attendu:
                      </Typography>
                      {recommendation.expected_impact.savings && (
                        <Typography variant="body2">
                          Économies potentielles: {recommendation.expected_impact.savings.toLocaleString()}€
                        </Typography>
                      )}
                      {recommendation.expected_impact.timeline && (
                        <Typography variant="body2">
                          Délai: {recommendation.expected_impact.timeline}
                        </Typography>
                      )}
                    </Box>
                  )}
                </Box>
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );
};

export default RecommendationsList;
