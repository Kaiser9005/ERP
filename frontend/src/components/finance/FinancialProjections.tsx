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
  Chip,
  LinearProgress
} from '@mui/material';
import { formatCurrency, formatPercentage } from '../../utils/format';
import { useTheme } from '@mui/material/styles';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';

interface Projection {
  period: string;
  amount: number;
  weather_impact: number;
}

interface FinancialProjections {
  revenue: Projection[];
  expenses: Projection[];
  weather_factors: string[];
}

const FinancialProjectionsComponent: React.FC = () => {
  const [projections, setProjections] = useState<FinancialProjections | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const theme = useTheme();

  useEffect(() => {
    const fetchProjections = async () => {
      try {
        const response = await fetch('/api/finance/projections?months_ahead=3');
        if (!response.ok) {
          throw new Error('Erreur lors de la récupération des projections');
        }
        const data = await response.json();
        setProjections(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Une erreur est survenue');
      } finally {
        setLoading(false);
      }
    };

    fetchProjections();
  }, []);

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

  if (!projections) {
    return <Alert severity="info">Aucune projection disponible</Alert>;
  }

  const calculateTrend = (current: number, previous: number) => {
    const variation = ((current - previous) / previous) * 100;
    return {
      value: Math.abs(variation),
      type: variation >= 0 ? 'increase' : 'decrease',
      icon: variation >= 0 ? <TrendingUpIcon /> : <TrendingDownIcon />
    };
  };

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
            {projections.weather_factors.map((factor, index) => (
              <Chip
                key={index}
                label={factor}
                sx={{ mr: 1, mb: 1 }}
                color="primary"
                variant="outlined"
              />
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Projections des Revenus */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Projections des Revenus
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
                {projections.revenue.map((projection, index) => {
                  const trend = index > 0 
                    ? calculateTrend(projection.amount, projections.revenue[index - 1].amount)
                    : null;
                  
                  return (
                    <TableRow key={projection.period}>
                      <TableCell>{projection.period}</TableCell>
                      <TableCell align="right">
                        {formatCurrency(projection.amount)}
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress
                            variant="determinate"
                            value={projection.weather_impact}
                            sx={{ 
                              width: '100px',
                              mr: 1,
                              height: 8,
                              borderRadius: 4
                            }}
                          />
                          {formatPercentage(projection.weather_impact)}
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {trend && (
                          <Chip
                            icon={trend.icon}
                            label={`${formatPercentage(trend.value)}`}
                            color={trend.type === 'increase' ? 'success' : 'error'}
                            size="small"
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
                {projections.expenses.map((projection, index) => {
                  const trend = index > 0 
                    ? calculateTrend(projection.amount, projections.expenses[index - 1].amount)
                    : null;
                  
                  return (
                    <TableRow key={projection.period}>
                      <TableCell>{projection.period}</TableCell>
                      <TableCell align="right">
                        {formatCurrency(projection.amount)}
                      </TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          <LinearProgress
                            variant="determinate"
                            value={projection.weather_impact}
                            sx={{ 
                              width: '100px',
                              mr: 1,
                              height: 8,
                              borderRadius: 4
                            }}
                          />
                          {formatPercentage(projection.weather_impact)}
                        </Box>
                      </TableCell>
                      <TableCell align="right">
                        {trend && (
                          <Chip
                            icon={trend.icon}
                            label={`${formatPercentage(trend.value)}`}
                            color={trend.type === 'increase' ? 'error' : 'success'}
                            size="small"
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

export default FinancialProjectionsComponent;
