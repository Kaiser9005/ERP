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
import { getMouvements, MouvementStock } from '../../services/inventaire';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';

const HistoriqueMouvements: React.FC = () => {
  const { data: mouvements = [] } = useQuery<MouvementStock[]>('recent-movements', getMouvements);

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
          {mouvements.map((mouvement) => (
            <ListItem key={mouvement.id} divider>
              <ListItemAvatar>
                <Avatar sx={{ bgcolor: `${getMovementColor(mouvement.type_mouvement)}.light` }}>
                  {getMovementIcon(mouvement.type_mouvement)}
                </Avatar>
              </ListItemAvatar>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    {mouvement.produit_id}
                    <Chip
                      size="small"
                      label={mouvement.type_mouvement}
                      color={getMovementColor(mouvement.type_mouvement)}
                    />
                  </Box>
                }
                secondary={
                  <>
                    {mouvement.quantite} - {mouvement.reference_document || 'Sans référence'}
                    <br />
                    {formatDistanceToNow(new Date(mouvement.date_mouvement), {
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

export default HistoriqueMouvements;
