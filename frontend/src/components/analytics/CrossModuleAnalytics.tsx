import { useEffect, useState } from 'react';
import { Box, Grid, Paper, Typography } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { 
  Assessment as AssessmentIcon,
  Engineering as EngineeringIcon,
  AccountBalance as AccountBalanceIcon,
  Inventory as InventoryIcon 
} from '@mui/icons-material';
import { useAnalyticsCrossModule } from '../../services/analytics_cross_module';
import type { CrossModuleAnalytics as ICrossModuleAnalytics } from '../../types/analytics_cross_module';
import StatCard from '../../components/common/StatCard';
import CorrelationsChart from './CorrelationsChart';
import RecommendationsList from './RecommendationsList';
import ModuleImpactGrid from './ModuleImpactGrid';
import MLPredictionsChart from './MLPredictionsChart';

export const CrossModuleAnalytics = () => {
  const [dateDebut, setDateDebut] = useState<Date | undefined>(undefined);
  const [dateFin, setDateFin] = useState<Date | undefined>(undefined);
  const [data, setData] = useState<ICrossModuleAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const analytics = useAnalyticsCrossModule();

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const result = await analytics.getUnifiedAnalytics({
          date_debut: dateDebut,
          date_fin: dateFin
        });
        setData(result);
        setError(null);
      } catch (err) {
        setError("Erreur lors de la récupération des données");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [dateDebut, dateFin, analytics]);

  if (loading) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography>Chargement des analytics...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 3 }}>
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!data) {
    return null;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Grid container spacing={3}>
        {/* Filtres de date */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="Date de début"
                  value={dateDebut}
                  onChange={(date) => setDateDebut(date || undefined)}
                  slotProps={{
                    textField: { fullWidth: true }
                  }}
                />
              </Grid>
              <Grid item xs={12} md={6}>
                <DatePicker
                  label="Date de fin"
                  value={dateFin}
                  onChange={(date) => setDateFin(date || undefined)}
                  slotProps={{
                    textField: { fullWidth: true }
                  }}
                />
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        {/* Corrélations */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Corrélations entre modules
            </Typography>
            <CorrelationsChart correlations={data.correlations} />
          </Paper>
        </Grid>

        {/* Prédictions ML */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2, height: '100%' }}>
            <Typography variant="h6" gutterBottom>
              Prédictions ML
            </Typography>
            <MLPredictionsChart predictions={data.predictions} />
          </Paper>
        </Grid>

        {/* Impact des modules */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Impact entre modules
            </Typography>
            <ModuleImpactGrid modules={data.modules} />
          </Paper>
        </Grid>

        {/* Recommandations */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Recommandations
            </Typography>
            <RecommendationsList recommendations={data.recommendations} />
          </Paper>
        </Grid>

        {/* Statistiques clés */}
        <Grid item xs={12}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Impact RH"
                value={Number((data.modules.hr.analytics.training_completion_rate * 100).toFixed(1))}
                unit="%"
                icon={<AssessmentIcon />}
                color="primary"
                variation={{
                  valeur: 10,
                  type: 'hausse'
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Impact Production"
                value={Number((data.modules.production.analytics.efficiency_rate * 100).toFixed(1))}
                unit="%"
                icon={<EngineeringIcon />}
                color="success"
                variation={{
                  valeur: 5,
                  type: 'hausse'
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Impact Finance"
                value={Number(data.modules.finance.analytics.cash_flow)}
                unit="€"
                icon={<AccountBalanceIcon />}
                color="warning"
                variation={{
                  valeur: 2,
                  type: 'baisse'
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <StatCard
                title="Impact Inventaire"
                value={Number(data.modules.inventory.analytics.total_items)}
                icon={<InventoryIcon />}
                color="info"
                variation={{
                  valeur: 3,
                  type: 'hausse'
                }}
              />
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CrossModuleAnalytics;
