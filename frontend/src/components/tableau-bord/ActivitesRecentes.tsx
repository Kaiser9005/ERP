import React from 'react';
import { Card, CardContent, Typography, List, ListItem, ListItemText, Chip, Box } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface Activite {
  id: string;
  type: 'PRODUCTION' | 'FINANCE' | 'INVENTAIRE' | 'RH';
  description: string;
  date: string;
  statut: 'EN_COURS' | 'TERMINE' | 'ANNULE';
}

const getActivites = async (): Promise<Activite[]> => {
  const response = await fetch('/api/v1/activites/recentes');
  return response.json();
};

const getTypeColor = (type: Activite['type']) => {
  switch (type) {
    case 'PRODUCTION':
      return 'success';
    case 'FINANCE':
      return 'primary';
    case 'INVENTAIRE':
      return 'warning';
    case 'RH':
      return 'info';
    default:
      return 'default';
  }
};

const getStatutColor = (statut: Activite['statut']) => {
  switch (statut) {
    case 'EN_COURS':
      return 'warning';
    case 'TERMINE':
      return 'success';
    case 'ANNULE':
      return 'error';
    default:
      return 'default';
  }
};

const ActivitesRecentes: React.FC = () => {
  const { data: activites = [], isLoading } = useQuery({
    queryKey: ['activites-recentes'],
    queryFn: getActivites
  });

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activités Récentes
        </Typography>

        {isLoading ? (
          <Typography color="text.secondary">Chargement des activités...</Typography>
        ) : (
          <List>
            {activites.map((activite) => (
              <ListItem
                key={activite.id}
                divider
                sx={{
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  gap: 1
                }}
              >
                <ListItemText
                  primary={activite.description}
                  secondary={format(new Date(activite.date), "d MMMM yyyy 'à' HH:mm", { locale: fr })}
                />
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Chip
                    label={activite.type}
                    size="small"
                    color={getTypeColor(activite.type)}
                  />
                  <Chip
                    label={activite.statut.replace('_', ' ')}
                    size="small"
                    color={getStatutColor(activite.statut)}
                  />
                </Box>
              </ListItem>
            ))}
          </List>
        )}

        {!isLoading && activites.length === 0 && (
          <Typography color="text.secondary" sx={{ textAlign: 'center', py: 2 }}>
            Aucune activité récente
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default ActivitesRecentes;
