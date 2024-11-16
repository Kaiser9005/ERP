import React, { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  Grid,
  Typography,
  LinearProgress,
  Box,
  IconButton,
  Tooltip,
  Chip,
} from '@mui/material';
import { Info, TrendingUp, TrendingDown } from '@mui/icons-material';
import { formatCurrency } from '../../utils/format';

interface BudgetData {
  categorie: string;
  prevu: number;
  realise: number;
  ecart: number;
  ecart_percentage: number;
}

interface BudgetAnalysis {
  total_prevu: number;
  total_realise: number;
  categories: Record<string, BudgetData>;
  weather_impact: {
    score: number;
    factors: string[];
    projections: Record<string, string>;
  };
  recommendations: string[];
}

const BudgetOverview: React.FC = () => {
  const [budgetData, setBudgetData] = useState<BudgetAnalysis | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchBudgetData = async () => {
      try {
        const response = await fetch('/api/v1/comptabilite/budget/analysis');
        const data = await response.json();
        setBudgetData(data);
      } catch (error) {
        console.error('Erreur lors du chargement des données budgétaires:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchBudgetData();
  }, []);

  if (loading) {
    return <LinearProgress />;
  }

  if (!budgetData) {
    return (
      <Typography color="textSecondary">
        Aucune donnée budgétaire disponible
      </Typography>
    );
  }

  const globalProgress = (budgetData.total_realise / budgetData.total_prevu) * 100;

  return (
    <Card>
      <CardHeader
        title="Aperçu Budgétaire"
        subheader={`Impact météo: ${budgetData.weather_impact.score}%`}
        action={
          <Tooltip title="Analyse budgétaire en temps réel">
            <IconButton>
              <Info />
            </IconButton>
          </Tooltip>
        }
      />
      <CardContent>
        <Grid container spacing={3}>
          {/* Progression globale */}
          <Grid item xs={12}>
            <Box sx={{ mb: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                <Typography variant="subtitle2">Progression globale</Typography>
                <Typography variant="subtitle2">
                  {globalProgress.toFixed(1)}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={Math.min(globalProgress, 100)}
                sx={{
                  height: 8,
                  borderRadius: 4,
                  backgroundColor: 'action.hover',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 4,
                  },
                }}
              />
            </Box>
          </Grid>

          {/* Totaux */}
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              Budget prévu
            </Typography>
            <Typography variant="h6">
              {formatCurrency(budgetData.total_prevu)}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="subtitle2" color="textSecondary">
              Réalisé
            </Typography>
            <Typography variant="h6">
              {formatCurrency(budgetData.total_realise)}
            </Typography>
          </Grid>

          {/* Catégories principales */}
          <Grid item xs={12}>
            <Typography variant="subtitle1" sx={{ mb: 2 }}>
              Principales catégories
            </Typography>
            {Object.entries(budgetData.categories).map(([categorie, data]) => (
              <Box key={categorie} sx={{ mb: 2 }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                  <Typography variant="body2">{categorie}</Typography>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Typography variant="body2">
                      {formatCurrency(data.realise)} / {formatCurrency(data.prevu)}
                    </Typography>
                    <Chip
                      size="small"
                      icon={data.ecart_percentage >= 0 ? <TrendingUp /> : <TrendingDown />}
                      label={`${Math.abs(data.ecart_percentage).toFixed(1)}%`}
                      color={data.ecart_percentage >= 0 ? 'success' : 'error'}
                    />
                  </Box>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={Math.min((data.realise / data.prevu) * 100, 100)}
                  sx={{
                    height: 4,
                    borderRadius: 2,
                  }}
                />
              </Box>
            ))}
          </Grid>

          {/* Impact météo */}
          {budgetData.weather_impact.factors.length > 0 && (
            <Grid item xs={12}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>
                Facteurs météorologiques
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {budgetData.weather_impact.factors.map((factor, index) => (
                  <Chip
                    key={index}
                    label={factor}
                    size="small"
                    color="primary"
                    variant="outlined"
                  />
                ))}
              </Box>
            </Grid>
          )}

          {/* Recommandations */}
          {budgetData.recommendations.length > 0 && (
            <Grid item xs={12}>
              <Typography variant="subtitle1" sx={{ mb: 1 }}>
                Recommandations
              </Typography>
              {budgetData.recommendations.map((recommendation, index) => (
                <Typography
                  key={index}
                  variant="body2"
                  color="textSecondary"
                  sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 0.5 }}
                >
                  • {recommendation}
                </Typography>
              ))}
            </Grid>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};

export default BudgetOverview;
