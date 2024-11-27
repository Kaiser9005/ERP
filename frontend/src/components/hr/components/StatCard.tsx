import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  useTheme
} from '@mui/material';
import { TrendingUp, TrendingDown } from '@mui/icons-material';
import { StatVariation } from '../../../types/hr';

interface StatCardProps {
  title: string;
  value: number;
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning' | 'error' | 'info';
  variation?: StatVariation;
  format?: 'number' | 'currency' | 'percentage';
}

const formatValue = (value: number, format?: string): string => {
  switch (format) {
    case 'currency':
      return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'EUR'
      }).format(value);
    case 'percentage':
      return `${value.toFixed(1)}%`;
    default:
      return new Intl.NumberFormat('fr-FR').format(value);
  }
};

const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  icon,
  color,
  variation,
  format = 'number'
}) => {
  const theme = useTheme();

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: theme.palette[color].light,
              borderRadius: '50%',
              p: 1,
              mr: 2,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center'
            }}
          >
            {icon}
          </Box>
          <Typography variant="h6" color="text.secondary">
            {title}
          </Typography>
        </Box>

        <Box display="flex" alignItems="baseline" mb={1}>
          <Typography variant="h4" component="span">
            {formatValue(value, format)}
          </Typography>
          
          {variation && (
            <Chip
              icon={variation.type === 'hausse' ? <TrendingUp /> : <TrendingDown />}
              label={`${variation.valeur.toFixed(1)}%`}
              size="small"
              color={variation.type === 'hausse' ? 'success' : 'error'}
              sx={{ ml: 1 }}
            />
          )}
        </Box>

        {variation && (
          <Typography variant="body2" color="text.secondary">
            {variation.type === 'hausse' ? 'Augmentation' : 'Diminution'} par rapport à la période précédente
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

export default StatCard;
