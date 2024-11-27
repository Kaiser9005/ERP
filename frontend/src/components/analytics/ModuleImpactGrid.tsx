import { FC } from 'react';
import {
  Grid,
  Paper,
  Typography,
  List,
  ListItem,
  ListItemText,
  useTheme
} from '@mui/material';
import type { CrossModuleAnalytics } from '../../types/analytics_cross_module';

interface ModuleImpactGridProps {
  modules: CrossModuleAnalytics['modules'];
}

export const ModuleImpactGrid: FC<ModuleImpactGridProps> = ({ modules }) => {
  const theme = useTheme();

  const renderImpactSection = (title: string, impacts: any) => (
    <Paper sx={{ p: 2, height: '100%' }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <List dense>
        {Object.entries(impacts).map(([key, value]: [string, any]) => (
          <ListItem key={key}>
            <ListItemText
              primary={key.split('_').map(word => 
                word.charAt(0).toUpperCase() + word.slice(1)
              ).join(' ')}
              secondary={
                typeof value === 'number' 
                  ? `${(value * 100).toFixed(1)}%`
                  : Array.isArray(value)
                  ? value.join(', ')
                  : JSON.stringify(value)
              }
            />
          </ListItem>
        ))}
      </List>
    </Paper>
  );

  return (
    <Grid container spacing={2}>
      {/* RH Impact */}
      <Grid item xs={12} md={6} lg={3}>
        {renderImpactSection('Impact RH', {
          'Formation': modules.hr.analytics.training_completion_rate,
          'Productivité': modules.hr.production_impact.productivity.current_rate,
          'Coûts': modules.hr.finance_impact.labor_costs.total,
          'Météo': modules.hr.weather_impact.score
        })}
      </Grid>

      {/* Production Impact */}
      <Grid item xs={12} md={6} lg={3}>
        {renderImpactSection('Impact Production', {
          'Efficacité': modules.production.analytics.efficiency_rate,
          'Charge RH': modules.production.hr_impact.workload.current_load,
          'Coûts': modules.production.finance_impact.production_costs.total,
          'Météo': modules.production.weather_impact.score
        })}
      </Grid>

      {/* Finance Impact */}
      <Grid item xs={12} md={6} lg={3}>
        {renderImpactSection('Impact Finance', {
          'Budget RH': modules.finance.hr_impact.budget_constraints.current_usage,
          'Investissements': modules.finance.production_impact.investment_capacity.available,
          'Cash Flow': modules.finance.analytics.cash_flow,
          'Météo': modules.finance.weather_impact.score
        })}
      </Grid>

      {/* Inventory Impact */}
      <Grid item xs={12} md={6} lg={3}>
        {renderImpactSection('Impact Inventaire', {
          'Stock': modules.inventory.analytics.total_items,
          'Production': modules.inventory.production_impact.stock_availability.rate,
          'Valeur': modules.inventory.finance_impact.stock_value.total,
          'Météo': modules.inventory.weather_impact.score
        })}
      </Grid>

      {/* Weather Impact */}
      <Grid item xs={12}>
        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Impact Météo Global
          </Typography>
          <Grid container spacing={2}>
            {Object.entries(modules.weather.impact).map(([module, impact]) => (
              <Grid item xs={12} sm={6} md={3} key={module}>
                <Paper 
                  sx={{ 
                    p: 2, 
                    bgcolor: theme.palette.grey[50],
                    height: '100%'
                  }}
                >
                  <Typography variant="subtitle1" gutterBottom>
                    {module.charAt(0).toUpperCase() + module.slice(1)}
                  </Typography>
                  <List dense>
                    <ListItem>
                      <ListItemText 
                        primary="Score d'impact"
                        secondary={`${(impact.score * 100).toFixed(1)}%`}
                      />
                    </ListItem>
                    <ListItem>
                      <ListItemText 
                        primary="Facteurs"
                        secondary={impact.facteurs.join(', ')}
                      />
                    </ListItem>
                  </List>
                </Paper>
              </Grid>
            ))}
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default ModuleImpactGrid;
