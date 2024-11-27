import React from 'react';
import { useQuery } from 'react-query';
import {
  Box,
  Grid,
  Paper,
  Typography,
  CircularProgress,
  Alert
} from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';

import { getHRAnalytics } from '../../../services/hr_analytics';
import StatCard from '../../common/StatCard';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

export const HRAnalyticsDashboard: React.FC = () => {
  const { data: analytics, isLoading, error } = useQuery(
    'hr-analytics',
    getHRAnalytics,
    {
      refetchInterval: 5 * 60 * 1000, // Rafraîchit toutes les 5 minutes
      staleTime: 4 * 60 * 1000 // Considère les données comme périmées après 4 minutes
    }
  );

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Une erreur est survenue lors du chargement des analytics
      </Alert>
    );
  }

  if (!analytics) {
    return null;
  }

  const {
    employee_stats,
    formation_analytics,
    contract_analytics,
    payroll_analytics
  } = analytics;

  const formationTypeData = Object.entries(formation_analytics.formations_by_type)
    .map(([type, count]) => ({ name: type, value: count }));

  const contractTypeData = Object.entries(contract_analytics.contracts_by_type)
    .map(([type, count]) => ({ name: type, value: count }));

  const payrollTrendData = Object.entries(payroll_analytics.payroll_trends)
    .map(([date, amount]) => ({ date, amount }));

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Tableau de Bord RH
      </Typography>

      <Grid container spacing={3}>
        {/* Statistiques générales */}
        <Grid item xs={12} md={3}>
          <StatCard
            title="Employés Total"
            value={employee_stats.total_employees}
            icon="people"
            color="primary"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Contrats Actifs"
            value={employee_stats.active_contracts}
            icon="description"
            color="success"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Formations Complétées"
            value={employee_stats.formations_completed}
            icon="school"
            color="warning"
          />
        </Grid>
        <Grid item xs={12} md={3}>
          <StatCard
            title="Taux de Complétion"
            value={parseFloat((employee_stats.formation_completion_rate * 100).toFixed(1))}
            icon="trending_up"
            color="info"
          />
        </Grid>

        {/* Graphiques */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Types de Formation
            </Typography>
            <PieChart width={400} height={300}>
              <Pie
                data={formationTypeData}
                cx={200}
                cy={150}
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {formationTypeData.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Types de Contrat
            </Typography>
            <BarChart
              width={400}
              height={300}
              data={contractTypeData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Évolution des Salaires
            </Typography>
            <LineChart
              width={900}
              height={300}
              data={payrollTrendData}
              margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="amount" stroke="#8884d8" />
            </LineChart>
          </Paper>
        </Grid>

        {/* Statistiques détaillées */}
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Statistiques des Formations
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="subtitle2">Total Formations</Typography>
                <Typography variant="h6">{formation_analytics.total_formations}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="subtitle2">Total Participations</Typography>
                <Typography variant="h6">{formation_analytics.total_participations}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2">Taux de Complétion</Typography>
                <Typography variant="h6">
                  {(formation_analytics.completion_rate * 100).toFixed(1)}%
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Statistiques des Contrats
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <Typography variant="subtitle2">Total Contrats</Typography>
                <Typography variant="h6">{contract_analytics.total_contracts}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="subtitle2">Taux de Renouvellement</Typography>
                <Typography variant="h6">
                  {(contract_analytics.contract_renewal_rate * 100).toFixed(1)}%
                </Typography>
              </Grid>
              <Grid item xs={12}>
                <Typography variant="subtitle2">Durée Moyenne (jours)</Typography>
                <Typography variant="h6">
                  {contract_analytics.contract_duration_stats.average.toFixed(0)}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>

        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Statistiques des Salaires
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={4}>
                <Typography variant="subtitle2">Total Masse Salariale</Typography>
                <Typography variant="h6">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'EUR'
                  }).format(payroll_analytics.total_payroll)}
                </Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="subtitle2">Salaire Moyen</Typography>
                <Typography variant="h6">
                  {new Intl.NumberFormat('fr-FR', {
                    style: 'currency',
                    currency: 'EUR'
                  }).format(payroll_analytics.average_salary)}
                </Typography>
              </Grid>
              <Grid item xs={4}>
                <Typography variant="subtitle2">Distribution Salaires</Typography>
                <Typography variant="body2">
                  {Object.entries(payroll_analytics.salary_distribution)
                    .map(([range, count]) => `${range}: ${count}`)
                    .join(' | ')}
                </Typography>
              </Grid>
            </Grid>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};
