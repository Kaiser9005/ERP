import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Box
} from '@mui/material';
import { Edit, Visibility } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getParcelles } from '../../services/production';
import { useNavigate } from 'react-router-dom';

const ParcellesList: React.FC = () => {
  const navigate = useNavigate();
  const { data: parcelles, isLoading } = useQuery('parcelles', getParcelles);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE':
        return 'success';
      case 'EN_REPOS':
        return 'warning';
      case 'EN_PREPARATION':
        return 'info';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Parcelles
        </Typography>

        <List>
          {parcelles?.map((parcelle) => (
            <ListItem key={parcelle.id} divider>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    {parcelle.code}
                    <Chip
                      size="small"
                      label={parcelle.culture_type}
                      color="primary"
                    />
                  </Box>
                }
                secondary={
                  <>
                    <Chip
                      size="small"
                      label={parcelle.statut}
                      color={getStatusColor(parcelle.statut)}
                      sx={{ mr: 1 }}
                    />
                    {parcelle.surface_hectares} ha
                  </>
                }
              />
              <ListItemSecondaryAction>
                <IconButton
                  edge="end"
                  onClick={() => navigate(`/production/parcelles/${parcelle.id}`)}
                  sx={{ mr: 1 }}
                  data-testid="view-button"
                >
                  <Visibility />
                </IconButton>
                <IconButton
                  edge="end"
                  onClick={() => navigate(`/production/parcelles/${parcelle.id}/edit`)}
                  data-testid="edit-button"
                >
                  <Edit />
                </IconButton>
              </ListItemSecondaryAction>
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default ParcellesList;