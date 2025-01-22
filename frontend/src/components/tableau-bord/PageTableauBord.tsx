import React from 'react';
import { Grid, Typography, Box } from '@mui/material';
import { Agriculture, Inventory, AccountBalance, People } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import CarteStatistique from '../common/CarteStatistique';
import CashFlowChart from '../comptabilite/CashFlowChart';
import GraphiqueProduction from './GraphiqueProduction';
import ActivitesRecentes from './ActivitesRecentes';
import WidgetMeteo from './WidgetMeteo';
import { ServiceTableauBord } from '../../services/tableau-bord';
import type { StatsModule } from '../../types/tableau-bord';

const PageTableauBord: React.FC = () => {
  const { data: stats, isLoading, error } = useQuery<StatsModule>({
    queryKey: ['tableau-bord', 'unifie'],
    queryFn: () => ServiceTableauBord.getTableauBordUnifie(),
    staleTime: 1000 * 60 * 5 // 5 minutes
  });

  if (error) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          Tableau de Bord
        </Typography>
        <Typography color="error">
          Une erreur est survenue lors du chargement des données
        </Typography>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord
      </Typography>

      <Grid container spacing={3}>
        {/* Statistiques principales */}
        <Grid item xs={12} sm={6} md={3}>
          <CarteStatistique
            titre="Production"
            valeur={stats?.modules.production.production_journaliere || 0}
            unite="tonnes"
            icone={<Agriculture />}
            couleur="primary"
            chargement={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CarteStatistique
            titre="Stock"
            valeur={stats?.modules.inventaire.valeur_stock || 0}
            unite="FCFA"
            icone={<Inventory />}
            couleur="success"
            chargement={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CarteStatistique
            titre="Chiffre d'Affaires"
            valeur={stats?.modules.finance.revenu_journalier || 0}
            unite="FCFA"
            icone={<AccountBalance />}
            couleur="info"
            chargement={isLoading}
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <CarteStatistique
            titre="Employés Actifs"
            valeur={stats?.modules.rh.total_employes || 0}
            icone={<People />}
            couleur="warning"
            chargement={isLoading}
          />
        </Grid>

        {/* Graphiques et widgets */}
        <Grid item xs={12} lg={8}>
          <GraphiqueProduction />
        </Grid>

        <Grid item xs={12} lg={4}>
          <WidgetMeteo />
        </Grid>

        <Grid item xs={12} lg={8}>
          <CashFlowChart />
        </Grid>

        <Grid item xs={12} lg={4}>
          <ActivitesRecentes />
        </Grid>
      </Grid>
    </Box>
  );
};

export default PageTableauBord;
