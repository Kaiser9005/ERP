import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import StatsInventaire from './StatsInventaire';
import ListeStock from './ListeStock';
import HistoriqueMouvements from './HistoriqueMouvements';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const PageInventaire: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Inventaire"
        subtitle="Gestion des stocks et mouvements"
        action={{
          label: "Nouveau Produit",
          onClick: () => navigate('/inventaire/produits/nouveau'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques d'inventaire */}
        <Grid item xs={12}>
          <StatsInventaire />
        </Grid>

        {/* Liste des stocks */}
        <Grid item xs={12} lg={8}>
          <ListeStock />
        </Grid>

        {/* Historique des mouvements */}
        <Grid item xs={12} lg={4}>
          <HistoriqueMouvements />
        </Grid>
      </Grid>
    </>
  );
};

export default PageInventaire;
