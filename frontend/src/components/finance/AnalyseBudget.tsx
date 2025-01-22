import React from 'react';
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
import { useQuery } from 'react-query';
import { getAnalyseBudget } from '../../services/finance';
import type { AnalyseBudgetaire } from '../../types/finance';
import { formatCurrency } from '../../utils/format';

interface CategoryData {
  prevu: number;
  realise: number;
  ecart: number;
  ecart_pourcentage: number;
}

interface ImpactMeteo {
    score: number;
    facteurs: string[];
    projections: {
      [key: string]: string;
    };
  }

const AnalyseBudget: React.FC = () => {
  const periodeActuelle = new Date().toISOString().slice(0, 7); // YYYY-MM

  const { data: analyse, isLoading, error } = useQuery<AnalyseBudgetaire>(
    ['analyse-budget', periodeActuelle],
    () => getAnalyseBudget(periodeActuelle)
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Une erreur est survenue lors du chargement des données</Alert>;
  }

  if (!analyse) {
    return <Alert severity="info">Aucune donnée disponible</Alert>;
  }

  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Analyse Budgétaire - {periodeActuelle}
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
                {formatCurrency(analyse.total_prevu)}
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
                {formatCurrency(analyse.total_realise)}
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
                {analyse.impact_meteo.score}%
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
            {Object.entries(analyse.categories).map(([categorie, donnees]: [string, CategoryData]) => (
              <TableRow key={categorie}>
                <TableCell>{categorie}</TableCell>
                <TableCell align="right">{formatCurrency(donnees.prevu)}</TableCell>
                <TableCell align="right">{formatCurrency(donnees.realise)}</TableCell>
                <TableCell align="right">{formatCurrency(donnees.ecart)}</TableCell>
                <TableCell align="right">
                  <Chip
                    label={`${donnees.ecart_pourcentage}%`}
                    color={donnees.ecart_pourcentage < 0 ? 'error' : 'success'}
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
            {analyse.impact_meteo.facteurs.map((facteur, index) => (
              <Chip
                key={index}
                label={facteur}
                sx={{ mr: 1, mb: 1 }}
                color="primary"
              />
            ))}
          </Box>
          <Typography variant="subtitle1" gutterBottom>
            Projections par catégorie :
          </Typography>
          {Object.entries(analyse.impact_meteo.projections).map(([categorie, projection]: [string, string]) => (
            <Typography key={categorie} color="textSecondary" paragraph>
              <strong>{categorie}:</strong> {projection}
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
          {analyse.recommandations.map((recommandation: string, index: number) => (
            <Alert key={index} severity="info" sx={{ mb: 1 }}>
              {recommandation}
            </Alert>
          ))}
        </CardContent>
      </Card>
    </Box>
  );
};

export default AnalyseBudget;
