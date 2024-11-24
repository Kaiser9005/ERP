import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider, CircularProgress } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { productionService } from '../../services/production';
import type { ProductionEvent } from '../../types/production';

const RecentActivities: React.FC = () => {
  const { data: activities, isLoading } = useQuery<ProductionEvent[]>({
    queryKey: ['production', 'events', 'all'],
    queryFn: () => productionService.getProductionEvents('all'),
    select: (data) => data.slice(0, 5), // Prendre les 5 plus récents
    staleTime: 1000 * 60 * 1, // 1 minute
    refetchInterval: 1000 * 60 * 2 // 2 minutes
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (!activities || activities.length === 0) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Activités Récentes
          </Typography>
          <Typography color="textSecondary">
            Aucune activité récente
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activités Récentes
        </Typography>
        <List>
          {activities.map((activity, index) => (
            <React.Fragment key={activity.id}>
              <ListItem>
                <ListItemText
                  primary={activity.type}
                  secondary={
                    <>
                      <Typography component="span" variant="body2" color="textPrimary">
                        {new Date(activity.date_debut).toLocaleDateString('fr-FR')}
                      </Typography>
                      {' - '}
                      {activity.description || 'Aucune description'}
                    </>
                  }
                />
              </ListItem>
              {index < activities.length - 1 && <Divider />}
            </React.Fragment>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default RecentActivities;
