import React from 'react';
import { Box, Typography, Grid } from '@mui/material';
import StatsInventaire from './StatsInventaire';
import ListeStock from './ListeStock';
import HistoriqueMouvements from './HistoriqueMouvements';

const PageInventaire: React.FC = () => {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Gestion de l'Inventaire
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <StatsInventaire />
        </Grid>

        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            État des Stocks
          </Typography>
          <ListeStock />
        </Grid>

        <Grid item xs={12}>
          <Typography variant="h5" gutterBottom>
            Historique des Mouvements
          </Typography>
          <HistoriqueMouvements />
        </Grid>
      </Grid>
    </Box>
  );
};

export default PageInventaire;
