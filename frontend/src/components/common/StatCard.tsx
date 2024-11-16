import React from 'react';
import { 
  Card, 
  CardContent, 
  Typography, 
  Box, 
  Chip, 
  IconButton, 
  Tooltip 
} from '@mui/material';
import { Variation } from '../../types/finance';
import { Info } from '@mui/icons-material';

interface StatCardProps {
  title: string;
  value: number;
  unit: string;
  variation?: Variation;
  icon: React.ReactNode;
  color?: 'primary' | 'secondary' | 'success' | 'error' | 'info' | 'warning';
  'data-testid'?: string;
}

const StatCard: React.FC<StatCardProps> = ({
  title, 
  value, 
  unit, 
  variation, 
  icon, 
  color = 'primary',
  'data-testid': dataTestId
}) => {
  const formatValue = (val: number) => 
    new Intl.NumberFormat('fr-FR', {
      style: 'currency', 
      currency: 'XAF',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0
    }).format(val);

  return (
    <Card 
      variant="outlined" 
      sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
      data-testid={dataTestId}
    >
      <CardContent sx={{ flex: 1 }}>
        <Box 
          display="flex" 
          justifyContent="space-between" 
          alignItems="center" 
          mb={2}
        >
          <Typography variant="subtitle2" color="text.secondary">
            {title}
          </Typography>
          <Tooltip title={`Informations sur ${title}`}>
            <IconButton size="small">
              <Info fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>

        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography variant="h5" component="div">
              {formatValue(value)}
            </Typography>
            {variation && (
              <Chip
                size="small"
                label={`${variation.value.toFixed(1)}%`}
                color={
                  variation.type === 'increase' 
                    ? 'success' 
                    : 'error'
                }
                sx={{ mt: 1 }}
                data-testid={
                  variation.type === 'increase' 
                    ? 'increase-chip' 
                    : 'decrease-chip'
                }
              />
            )}
          </Box>
          
          <Box 
            sx={{ 
              color: `${color}.main`, 
              opacity: 0.7,
              display: 'flex',
              alignItems: 'center'
            }}
          >
            {React.cloneElement(icon as React.ReactElement, { 
              fontSize: 'large' 
            })}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatCard;
