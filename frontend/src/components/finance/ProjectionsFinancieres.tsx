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
  Chip,
  LinearProgress
} from '@mui/material';
import { useQuery } from 'react-query';
import { getProjectionsFinancieres, ProjectionsFinancieres as IProjectionsFinancieres } from '../../services/finance';
import { formatCurrency, formatPercentage } from '../../utils/format';
import { useTheme } from '@mui/material/styles';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

const ProjectionsFinancieres: React.FC = () => {
  const theme = useTheme();

  const { data: projections, isLoading, error } = useQuery<IProjectionsFinancieres>(
    'projections-financieres',
    () => getProjectionsFinancieres(3)
  );

  const calculerTendance = (actuel: number, precedent: number) => {
    const variation = ((actuel - precedent) / precedent) * 100;
    return {
      valeur: Math.abs(variation),
      type: variation >= 0 ? 'hausse' : 'baisse',
      icone: variation >= 0 ? <TrendingUpIcon /> : <TrendingDownIcon />
    };
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return <Alert severity="error">Une erreur est survenue lors du chargement des projections</Alert>;
  }

  if (!projections) {
    return <Alert severity="info">Aucune projection disponible</Alert>;
  }

  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Typography variant="h5" gutterBottom>
        Projections Financières (3 mois)
      </Typography>

      {/* Facteurs Météorologiques */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Facteurs Météorologiques
          </Typography>
          <Box sx={{ mb: 2 }}>
            {projections.facteurs_meteo.map((facteur, index) => (
              <Chip
                key={index}
                label={facteur}
                sx={{ mr: 1, mb: 1 }}
                color="primary"
                variant="outlined"
                data-testid="facteur-meteo"
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Projections des Recettes */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Projections des Recettes
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Période</TableCell>
                  <TableCell align="right">Montant Projeté</TableCell>
                  <TableCell align="right">Impact Météo</TableCell>
                  <TableCell align="right">Tendance</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {projections.recettes.map((projection, index) => {
                  const tendance = index > 0 
                    ? calculerTendance(projection.montant, projections.recettes[index - 1].montant)
                    : null;
                  
                  return (
                    <TableRow key={projection.periode}>
                      <TableCell>{projection.periode}</TableCell>
                      <TableCell align="right">
                        {formatCurrency(projection.montant)}
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress
                            variant="determinate"
                            value={projection.impact_meteo}
                            sx={{ 
                              width: '100px',
                              mr: 1,
                              height: 8,
                              borderRadius: 4
                            }}
                          />
                          {formatPercentage(projection.impact_meteo)}
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {tendance && (
                          <Chip
                            icon={tendance.icone}
                            label={`${formatPercentage(tendance.valeur)}`}
                            color={tendance.type === 'hausse' ? 'success' : 'error'}
                            size="small"
                            data-testid={tendance.type === 'hausse' ? 'success-chip' : 'error-chip'}
                          />
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Projections des Dépenses */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Projections des Dépenses
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Période</TableCell>
                  <TableCell align="right">Montant Projeté</TableCell>
                  <TableCell align="right">Impact Météo</TableCell>
                  <TableCell align="right">Tendance</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {projections.depenses.map((projection, index) => {
                  const tendance = index > 0 
                    ? calculerTendance(projection.montant, projections.depenses[index - 1].montant)
                    : null;
                  
                  return (
                    <TableRow key={projection.periode}>
                      <TableCell>{projection.periode}</TableCell>
                      <TableCell align="right">
                        {formatCurrency(projection.montant)}
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress
                            variant="determinate"
                            value={projection.impact_meteo}
                            sx={{ 
                              width: '100px',
                              mr: 1,
                              height: 8,
                              borderRadius: 4
                            }}
                          />
                          {formatPercentage(projection.impact_meteo)}
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {tendance && (
                          <Chip
                            icon={tendance.icone}
                            label={`${formatPercentage(tendance.valeur)}`}
                            color={tendance.type === 'hausse' ? 'error' : 'success'}
                            size="small"
                            data-testid={tendance.type === 'hausse' ? 'error-chip' : 'success-chip'}
                          />
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
};

export default ProjectionsFinancieres;
