import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import ProductionStats from './ProductionStats';
import ParcellesList from './ParcellesList';
import ProductionCalendar from './ProductionCalendar';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const ProductionPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Production"
        subtitle="Gestion des parcelles et des récoltes"
        action={{
          label: "Nouvelle Parcelle",
          onClick: () => navigate('/production/parcelles/new'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques de production */}
        <Grid item xs={12}>
          <ProductionStats />
        </Grid>

        {/* Calendrier de production */}
        <Grid item xs={12} lg={8}>
          <ProductionCalendar />
        </Grid>

        {/* Liste des parcelles */}
        <Grid item xs={12} lg={4}>
          <ParcellesList />
        </Grid>
      </Grid>
    </>
  );
};

export default ProductionPage;