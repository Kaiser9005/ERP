import React, { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip
} from '@mui/material';
import { formatCurrency } from '../../utils/format';
import { useTheme } from '@mui/material/styles';

interface BudgetAnalysis {
  total_prevu: number;
  total_realise: number;
  categories: {
    [key: string]: {
      prevu: number;
      realise: number;
      ecart: number;
      ecart_percentage: number;
    };
  };
  weather_impact: {
    score: number;
    factors: string[];
    projections: {
      [key: string]: string;
    };
  };
  recommendations: string[];
}

const BudgetAnalysisComponent: React.FC = () => {
  const [analysis, setAnalysis] = useState<BudgetAnalysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  const currentPeriod = new Date().toISOString().slice(0, 7); // YYYY-MM

  useEffect(() => {
    const fetchAnalysis = async () => {
      try {
        const response = await fetch(`/api/finance/budgets/analysis/${currentPeriod}`);
        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des données');
        }
        const data = await response.json();
        setAnalysis(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Une erreur est survenue');
      } finally {
        setLoading(false);
      }
    };

    fetchAnalysis();
  }, [currentPeriod]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">{error}</Alert>;
  }

  if (!analysis) {
    return <Alert severity="info">Aucune donnée disponible</Alert>;
  }

  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Analyse Budgétaire - {currentPeriod}
      </Typography>

      {/* Résumé Global */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Budget Total
              </Typography>
              <Typography variant="h4">
                {formatCurrency(analysis.total_prevu)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Réalisé
              </Typography>
              <Typography variant="h4">
                {formatCurrency(analysis.total_realise)}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Impact Météo
              </Typography>
              <Typography variant="h4">
                {analysis.weather_impact.score}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Tableau Détaillé */}
      <TableContainer component={Paper} sx={{ mb: 4 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Catégorie</TableCell>
              <TableCell align="right">Budget</TableCell>
              <TableCell align="right">Réalisé</TableCell>
              <TableCell align="right">Écart</TableCell>
              <TableCell align="right">%</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {Object.entries(analysis.categories).map(([category, data]) => (
              <TableRow key={category}>
                <TableCell>{category}</TableCell>
                <TableCell align="right">{formatCurrency(data.prevu)}</TableCell>
                <TableCell align="right">{formatCurrency(data.realise)}</TableCell>
                <TableCell align="right">{formatCurrency(data.ecart)}</TableCell>
                <TableCell align="right">
                  <Chip
                    label={`${data.ecart_percentage}%`}
                    color={data.ecart_percentage < 0 ? 'error' : 'success'}
                    size="small"
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Impact Météo */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Impact Météorologique
          </Typography>
          <Box sx={{ mb: 2 }}>
            {analysis.weather_impact.factors.map((factor, index) => (
              <Chip
                key={index}
                label={factor}
                sx={{ mr: 1, mb: 1 }}
                color="primary"
              />
            ))}
          </Box>
          <Typography variant="subtitle1" gutterBottom>
            Projections par catégorie :
          </Typography>
          {Object.entries(analysis.weather_impact.projections).map(([category, projection]) => (
            <Typography key={category} color="textSecondary" paragraph>
              <strong>{category}:</strong> {projection}
            </Typography>
          ))}
        </CardContent>
      </Card>

      {/* Recommandations */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recommandations
          </Typography>
          {analysis.recommendations.map((recommendation, index) => (
            <Alert key={index} severity="info" sx={{ mb: 1 }}>
              {recommendation}
            </Alert>
          ))}
        </CardContent>
      </Card>
    </Box>
  );
};

export default BudgetAnalysisComponent;
