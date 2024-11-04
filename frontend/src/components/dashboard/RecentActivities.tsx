import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Box
} from '@mui/material';
import {
  Agriculture,
  Inventory,
  AccountBalance,
  Person
} from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getRecentActivities } from '../../services/activities';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const getActivityIcon = (type: string) => {
  switch (type) {
    case 'PRODUCTION':
      return <Agriculture />;
    case 'INVENTORY':
      return <Inventory />;
    case 'FINANCE':
      return <AccountBalance />;
    default:
      return <Person />;
  }
};

const getActivityColor = (type: string) => {
  switch (type) {
    case 'PRODUCTION':
      return 'success.main';
    case 'INVENTORY':
      return 'info.main';
    case 'FINANCE':
      return 'warning.main';
    default:
      return 'primary.main';
  }
};

const RecentActivities: React.FC = () => {
  const { data: activities } = useQuery('recent-activities', getRecentActivities);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activités Récentes
        </Typography>

        <List>
          {activities?.map((activity) => (
            <ListItem key={activity.id}>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: getActivityColor(activity.type) }}>
                  {getActivityIcon(activity.type)}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={activity.titre}
                secondary={
                  <Box>
                    <Typography variant="body2">
                      {activity.description}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">
                      {formatDistanceToNow(new Date(activity.date), {
                        addSuffix: true,
                        locale: fr
                      })}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default RecentActivities;