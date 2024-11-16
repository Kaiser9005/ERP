import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  Skeleton,
  IconButton,
  Tooltip,
  Chip,
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  AccountBalance,
  Payment,
  Receipt,
  Calculate,
  Info,
} from '@mui/icons-material';
import { formatCurrency } from '../../utils/format';

interface Variation {
  value: number;
  type: 'increase' | 'decrease';
}

interface FinanceStatsData {
  revenue: number;
  revenueVariation: Variation;
  profit: number;
  profitVariation: Variation;
  cashflow: number;
  cashflowVariation: Variation;
  expenses: number;
  expensesVariation: Variation;
}

const StatCard: React.FC<{
  title: string;
  value: number;
  variation: Variation;
  icon: React.ReactNode;
  info?: string;
}> = ({ title, value, variation, icon, info }) => (
  <Card sx={{ height: '100%' }}>
    <CardContent>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Box sx={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'center',
            width: 40,
            height: 40,
            borderRadius: '50%',
            backgroundColor: 'primary.light',
            color: 'primary.main'
          }}>
            {icon}
          </Box>
          <Typography variant="subtitle1" color="textSecondary">
            {title}
          </Typography>
        </Box>
        {info && (
          <Tooltip title={info}>
            <IconButton size="small">
              <Info fontSize="small" />
            </IconButton>
          </Tooltip>
        )}
      </Box>

      <Typography variant="h4" component="div" sx={{ mb: 1 }}>
        {formatCurrency(value)}
      </Typography>

      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Chip
          size="small"
          icon={variation.type === 'increase' ? <TrendingUp /> : <TrendingDown />}
          label={`${variation.value}%`}
          color={variation.type === 'increase' ? 'success' : 'error'}
          variant="outlined"
        />
        <Typography variant="body2" color="textSecondary">
          vs mois précédent
        </Typography>
      </Box>
    </CardContent>
  </Card>
);

const FinanceStats: React.FC = () => {
  const [stats, setStats] = useState<FinanceStatsData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('/api/v1/comptabilite/stats');
        const data = await response.json();
        setStats(data);
      } catch (error) {
        console.error('Erreur lors du chargement des statistiques:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (loading) {
    return (
      <Grid container spacing={3}>
        {[...Array(4)].map((_, index) => (
          <Grid item xs={12} sm={6} md={3} key={index}>
            <Card>
              <CardContent>
                <Skeleton variant="rectangular" height={40} sx={{ mb: 2 }} />
                <Skeleton variant="text" height={60} />
                <Skeleton variant="text" width="60%" />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    );
  }

  if (!stats) {
    return (
      <Typography color="textSecondary">
        Aucune donnée statistique disponible
      </Typography>
    );
  }

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Chiffre d'affaires"
          value={stats.revenue}
          variation={stats.revenueVariation}
          icon={<Receipt />}
          info="Chiffre d'affaires total du mois en cours"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Bénéfice"
          value={stats.profit}
          variation={stats.profitVariation}
          icon={<Calculate />}
          info="Bénéfice net après déduction des charges"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Trésorerie"
          value={stats.cashflow}
          variation={stats.cashflowVariation}
          icon={<AccountBalance />}
          info="Solde de trésorerie disponible"
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <StatCard
          title="Charges"
          value={stats.expenses}
          variation={stats.expensesVariation}
          icon={<Payment />}
          info="Total des charges du mois en cours"
        />
      </Grid>
    </Grid>
  );
};

export default FinanceStats;
