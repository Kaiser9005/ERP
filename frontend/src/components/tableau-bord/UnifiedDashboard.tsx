import React, { useState, useEffect } from 'react';
import { Grid, Container, Typography, Box, CircularProgress } from '@mui/material';
import { ModuleCard } from './ModuleCard';
import { AlertsPanel } from './AlertsPanel';
import { ModuleStats, ModuleType } from '../../types/dashboard';
import DashboardService from '../../services/dashboard';

// Import des composants spécifiques à chaque module
import HRModule from './modules/HRModule';
import ProductionModule from './modules/ProductionModule';
import FinanceModule from './modules/FinanceModule';
import InventoryModule from './modules/InventoryModule';
import ModuleMétéo from './modules/ModuleMétéo';
import ProjectsModule from './modules/ProjectsModule';

const UnifiedDashboard: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [dashboardData, setDashboardData] = useState<ModuleStats | null>(null);
  const [expandedModules, setExpandedModules] = useState<Record<ModuleType, boolean>>({
    hr: true,
    production: true,
    finance: true,
    inventory: true,
    weather: true,
    projects: true
  });

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const data = await DashboardService.getUnifiedDashboard();
      setDashboardData(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Une erreur est survenue');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
    const interval = setInterval(fetchDashboardData, 300000); // Rafraîchissement toutes les 5 minutes
    return () => clearInterval(interval);
  }, []);

  const handleModuleExpand = (module: ModuleType) => {
    setExpandedModules(prev => ({
      ...prev,
      [module]: !prev[module]
    }));
  };

  const handleModuleRefresh = async (module: ModuleType) => {
    try {
      await DashboardService.refreshModule(module);
      await fetchDashboardData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors du rafraîchissement');
    }
  };

  const handleAlertAcknowledge = async (alertId: string) => {
    try {
      await DashboardService.updateAlertStatus(alertId, 'acknowledged');
      await fetchDashboardData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la mise à jour de l\'alerte');
    }
  };

  const handleAlertResolve = async (alertId: string) => {
    try {
      await DashboardService.updateAlertStatus(alertId, 'resolved');
      await fetchDashboardData();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Erreur lors de la résolution de l\'alerte');
    }
  };

  if (loading && !dashboardData) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="100vh">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!dashboardData) {
    return null;
  }

  return (
    <Container maxWidth="xl">
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          Tableau de Bord Unifié
        </Typography>
        <Typography variant="subtitle1" color="textSecondary">
          Dernière mise à jour : {new Date(dashboardData.timestamp).toLocaleString()}
        </Typography>
      </Box>

      <AlertsPanel
        alerts={dashboardData.alerts}
        onAcknowledge={handleAlertAcknowledge}
        onResolve={handleAlertResolve}
      />

      <Grid container spacing={3}>
        {/* Module RH */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Ressources Humaines"
            module="hr"
            expanded={expandedModules.hr}
            onExpand={() => handleModuleExpand('hr')}
            onRefresh={() => handleModuleRefresh('hr')}
            loading={loading}
          >
            <HRModule data={dashboardData.modules.hr} />
          </ModuleCard>
        </Grid>

        {/* Module Production */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Production"
            module="production"
            expanded={expandedModules.production}
            onExpand={() => handleModuleExpand('production')}
            onRefresh={() => handleModuleRefresh('production')}
            loading={loading}
          >
            <ProductionModule data={dashboardData.modules.production} />
          </ModuleCard>
        </Grid>

        {/* Module Finance */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Finance"
            module="finance"
            expanded={expandedModules.finance}
            onExpand={() => handleModuleExpand('finance')}
            onRefresh={() => handleModuleRefresh('finance')}
            loading={loading}
          >
            <FinanceModule data={dashboardData.modules.finance} />
          </ModuleCard>
        </Grid>

        {/* Module Inventaire */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Inventaire"
            module="inventory"
            expanded={expandedModules.inventory}
            onExpand={() => handleModuleExpand('inventory')}
            onRefresh={() => handleModuleRefresh('inventory')}
            loading={loading}
          >
            <InventoryModule data={dashboardData.modules.inventory} />
          </ModuleCard>
        </Grid>

        {/* Module Météo */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Météo"
            module="weather"
            expanded={expandedModules.weather}
            onExpand={() => handleModuleExpand('weather')}
            onRefresh={() => handleModuleRefresh('weather')}
            loading={loading}
          >
            <ModuleMétéo data={dashboardData.modules.weather} />
          </ModuleCard>
        </Grid>

        {/* Module Projets */}
        <Grid item xs={12} md={6}>
          <ModuleCard
            title="Projets"
            module="projects"
            expanded={expandedModules.projects}
            onExpand={() => handleModuleExpand('projects')}
            onRefresh={() => handleModuleRefresh('projects')}
            loading={loading}
          >
            <ProjectsModule data={dashboardData.modules.projects} />
          </ModuleCard>
        </Grid>
      </Grid>
    </Container>
  );
};

export default UnifiedDashboard;
