import React from 'react';
import { Grid } from '@mui/material';
import PageHeader from '../layout/PageHeader';
import InventoryStats from './InventoryStats';
import StockList from './StockList';
import MovementHistory from './MovementHistory';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const InventoryPage: React.FC = () => {
  const navigate = useNavigate();

  return (
    <>
      <PageHeader
        title="Inventaire"
        subtitle="Gestion des stocks et mouvements"
        action={{
          label: "Nouveau Produit",
          onClick: () => navigate('/inventory/products/new'),
          icon: <Add />
        }}
      />

      <Grid container spacing={3}>
        {/* Statistiques d'inventaire */}
        <Grid item xs={12}>
          <InventoryStats />
        </Grid>

        {/* Liste des stocks */}
        <Grid item xs={12} lg={8}>
          <StockList />
        </Grid>

        {/* Historique des mouvements */}
        <Grid item xs={12} lg={4}>
          <MovementHistory />
        </Grid>
      </Grid>
    </>
  );
};

export default InventoryPage;