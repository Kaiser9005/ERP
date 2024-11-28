import React from 'react';
import { Grid, CircularProgress } from '@mui/material';
import { useTranslation } from 'react-i18next';
import { Add } from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';

import PageHeader from '../../components/layout/PageHeader';
import StatsInventaire from './StatsInventaire';
import ListeStock from './ListeStock';
import HistoriqueMouvements from './HistoriqueMouvements';
import ErrorAlert from '../../components/common/ErrorAlert';
import { fetchInventoryPermissions } from '../../services/inventaire';

const PageInventaire: React.FC = () => {
  const { t } = useTranslation();
  const navigate = useNavigate();

  // Vérifier les permissions de l'utilisateur
  const { data: permissions, isLoading, error } = useQuery(
    'inventoryPermissions',
    fetchInventoryPermissions
  );

  if (isLoading) {
    return (
      <Grid container justifyContent="center" alignItems="center" style={{ minHeight: '400px' }}>
        <CircularProgress 
          aria-label={t('common.loading')} 
          role="progressbar"
        />
      </Grid>
    );
  }

  if (error) {
    return <ErrorAlert message={t('inventory.error.loading')} />;
  }

  const headerAction = permissions?.canCreate ? {
    label: t('inventory.actions.newProduct'),
    onClick: () => navigate('/inventaire/produits/nouveau'),
    icon: <Add />,
    'aria-label': t('inventory.actions.newProduct')
  } : undefined;

  return (
    <div role="main" aria-label={t('inventory.page.title')}>
      <PageHeader
        title={t('inventory.page.title')}
        subtitle={t('inventory.page.subtitle')}
        action={headerAction}
      />

      <Grid container spacing={3}>
        {/* Statistiques d'inventaire */}
        <Grid item xs={12}>
          <StatsInventaire />
        </Grid>

        {/* Liste des stocks */}
        <Grid 
          item 
          xs={12} 
          lg={8}
          role="region" 
          aria-label={t('inventory.sections.stockList')}
        >
          <ListeStock />
        </Grid>

        {/* Historique des mouvements */}
        <Grid 
          item 
          xs={12} 
          lg={4}
          role="region" 
          aria-label={t('inventory.sections.movements')}
        >
          <HistoriqueMouvements />
        </Grid>
      </Grid>
    </div>
  );
};

export default PageInventaire;
