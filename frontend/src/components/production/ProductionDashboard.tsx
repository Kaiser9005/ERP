import React, { useEffect, useState } from 'react';
import { Grid, Paper, Typography, Box, Tab, Tabs } from '@mui/material';
import ParcelleMap from './ParcelleMap';
import ProductionCalendar from './ProductionCalendar';
import TableauMeteoParcelleaire from './TableauMeteoParcelleaire';
import HarvestQualityForm from './HarvestQualityForm';
import { Parcelle } from '../../types/production';
import { productionService } from '../../services/production';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

const TabPanel = (props: TabPanelProps) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`production-tabpanel-${index}`}
      aria-labelledby={`production-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const ProductionDashboard: React.FC = () => {
  const [selectedParcelle, setSelectedParcelle] = useState<Parcelle | undefined>(undefined);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  useEffect(() => {
    const loadInitialData = async () => {
      try {
        setLoading(true);
        // Les données seront chargées par les composants enfants
        setLoading(false);
      } catch (err) {
        setError('Erreur lors du chargement des données');
        setLoading(false);
      }
    };

    loadInitialData();
  }, []);

  const handleParcelleSelect = async (parcelle: Parcelle) => {
    try {
      setSelectedParcelle(parcelle);
      // Charger les données détaillées de la parcelle si nécessaire
      await productionService.getParcelle(parcelle.id);
    } catch (err) {
      setError('Erreur lors du chargement des détails de la parcelle');
    }
  };

  const handleTabChange = (_event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Chargement du tableau de bord...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1, p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord de Production
      </Typography>

      <Grid container spacing={3}>
        {/* Carte des parcelles */}
        <Grid item xs={12}>
          <Paper elevation={3} sx={{ p: 2, height: '500px' }}>
            <ParcelleMap onParcelleSelect={handleParcelleSelect} />
          </Paper>
        </Grid>

        {/* Informations détaillées */}
        <Grid item xs={12}>
          <Paper elevation={3}>
            <Tabs
              value={tabValue}
              onChange={handleTabChange}
              variant="scrollable"
              scrollButtons="auto"
              aria-label="production dashboard tabs"
            >
              <Tab label="Météo" />
              <Tab label="Calendrier" />
              <Tab label="Récolte" />
            </Tabs>

            <TabPanel value={tabValue} index={0}>
              <TableauMeteoParcelleaire parcelle={selectedParcelle} />
            </TabPanel>

            <TabPanel value={tabValue} index={1}>
              <ProductionCalendar parcelle={selectedParcelle} />
            </TabPanel>

            <TabPanel value={tabValue} index={2}>
              <HarvestQualityForm
                parcelle={selectedParcelle}
                onSubmit={() => {
                  // Recharger les données si nécessaire
                }}
              />
            </TabPanel>
          </Paper>
        </Grid>

        {/* Informations de la parcelle sélectionnée */}
        {selectedParcelle && (
          <Grid item xs={12}>
            <Paper elevation={3} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Détails de la Parcelle: {selectedParcelle.code}
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} md={3}>
                  <Typography variant="body1">
                    Type de culture: {selectedParcelle.culture_type}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body1">
                    Surface: {selectedParcelle.surface_hectares} ha
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body1">
                    Statut: {selectedParcelle.statut}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={3}>
                  <Typography variant="body1">
                    Date de plantation: {new Date(selectedParcelle.date_plantation).toLocaleDateString()}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          </Grid>
        )}
      </Grid>
    </Box>
  );
};

export default ProductionDashboard;
