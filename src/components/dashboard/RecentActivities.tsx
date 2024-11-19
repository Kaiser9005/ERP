import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Divider } from '@mui/material';
import { productionService } from '../../services/production';
import { ProductionEvent } from '../../types/production';

const RecentActivities: React.FC = () => {
  const [activities, setActivities] = useState<ProductionEvent[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchActivities = async () => {
      try {
        // On récupère les événements de production pour toutes les parcelles
        const events = await productionService.getProductionEvents('all');
        // On prend les 5 plus récents
        setActivities(events.slice(0, 5));
      } catch (error) {
        console.error('Erreur lors du chargement des activités récentes:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchActivities();
  }, []);

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
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
