import React from 'react';
import { Card, CardContent, Typography, Box, Avatar, CircularProgress } from '@mui/material';
import { TrendingUp, TrendingDown } from '@mui/icons-material';

interface StatCardProps {
  title: string;
  value: number;
  unit?: string;
  variation?: {
    valeur: number;
    type: 'hausse' | 'baisse';
  };
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning' | 'info';
  loading?: boolean;
}

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  unit,
  variation,
  icon,
  color,
  loading = false
}) => {
  const formaterValeur = (val: number): string => {
    if (val >= 1000000) {
      return `${(val / 1000000).toFixed(1)}M`;
    }
    if (val >= 1000) {
      return `${(val / 1000).toFixed(1)}k`;
    }
    return val.toString();
  };

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Avatar
            sx={{
              bgcolor: `${color}.light`,
              color: `${color}.main`,
              mr: 2
            }}
          >
            {icon}
          </Avatar>
          <Typography variant="h6" color="text.secondary">
            {title}
          </Typography>
        </Box>

        {loading ? (
          <Box display="flex" justifyContent="center" my={2}>
            <CircularProgress size={24} />
          </Box>
        ) : (
          <>
            <Typography variant="h4" component="div" gutterBottom>
              {formaterValeur(value)}
              {unit && (
                <Typography
                  component="span"
                  variant="subtitle1"
                  color="text.secondary"
                  sx={{ ml: 1 }}
                >
                  {unit}
                </Typography>
              )}
            </Typography>

            {variation && (
              <Box display="flex" alignItems="center">
                {variation.type === 'hausse' ? (
                  <TrendingUp color="success" />
                ) : (
                  <TrendingDown color="error" />
                )}
                <Typography
                  variant="body2"
                  color={variation.type === 'hausse' ? 'success.main' : 'error.main'}
                  sx={{ ml: 1 }}
                >
                  {Math.abs(variation.valeur)}%
                </Typography>
              </Box>
            )}
          </>
        )}
      </CardContent>
    </Card>
  );
};

export default StatCard;
