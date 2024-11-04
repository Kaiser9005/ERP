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
  Chip,
  Box,
  IconButton
} from '@mui/material';
import { Check, Close } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getLeaveRequests } from '../../services/hr';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const LeaveRequests: React.FC = () => {
  const { data: requests } = useQuery('leave-requests', getLeaveRequests);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'EN_ATTENTE':
        return 'warning';
      case 'APPROUVE':
        return 'success';
      case 'REFUSE':
        return 'error';
      default:
        return 'default';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Demandes de Congés
        </Typography>

        <List>
          {requests?.map((request) => (
            <ListItem
              key={request.id}
              secondaryAction={
                request.statut === 'EN_ATTENTE' && (
                  <Box>
                    <IconButton size="small" color="success">
                      <Check />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <Close />
                    </IconButton>
                  </Box>
                )
              }
            >
              <ListItemAvatar>
                <Avatar>
                  {request.employe.prenom[0]}{request.employe.nom[0]}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    {request.employe.prenom} {request.employe.nom}
                    <Chip
                      size="small"
                      label={request.statut}
                      color={getStatusColor(request.statut)}
                    />
                  </Box>
                }
                secondary={
                  <>
                    {request.type_conge} - {request.nb_jours} jours
                    <br />
                    {formatDistanceToNow(new Date(request.date_debut), {
                      addSuffix: true,
                      locale: fr
                    })}
                  </>
                }
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
};

export default LeaveRequests;