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
  Box
} from '@mui/material';
import { Add, Remove, SwapHoriz } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getRecentMovements } from '../../services/inventory';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const MovementHistory: React.FC = () => {
  const { data: movements } = useQuery('recent-movements', getRecentMovements);

  const getMovementIcon = (type: string) => {
    switch (type) {
      case 'ENTREE':
        return <Add />;
      case 'SORTIE':
        return <Remove />;
      default:
        return <SwapHoriz />;
    }
  };

  const getMovementColor = (type: string) => {
    switch (type) {
      case 'ENTREE':
        return 'success';
      case 'SORTIE':
        return 'error';
      default:
        return 'info';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Derniers Mouvements
        </Typography>

        <List>
          {movements?.map((movement) => (
            <ListItem key={movement.id} divider>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: `${getMovementColor(movement.type)}.light` }}>
                  {getMovementIcon(movement.type)}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    {movement.product}
                    <Chip
                      size="small"
                      label={movement.type}
                      color={getMovementColor(movement.type)}
                    />
                  </Box>
                }
                secondary={
                  <>
                    {movement.quantity} {movement.unit} - {movement.reference}
                    <br />
                    {formatDistanceToNow(new Date(movement.date), {
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

export default MovementHistory;