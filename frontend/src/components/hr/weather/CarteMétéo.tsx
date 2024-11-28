import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { WbSunny, Opacity, Air } from '@mui/icons-material';

interface CarteMétéoProps {
  title: string;
  value: string;
  status: 'LOW' | 'MEDIUM' | 'HIGH';
}

const getStatusColor = (status: 'LOW' | 'MEDIUM' | 'HIGH') => {
  switch (status) {
    case 'LOW':
      return 'success.main';
    case 'MEDIUM':
      return 'warning.main';
    case 'HIGH':
      return 'error.main';
    default:
      return 'text.secondary';
  }
};

const getStatusIcon = (title: string) => {
  switch (title.toLowerCase()) {
    case 'température':
      return <WbSunny />;
    case 'précipitations':
      return <Opacity />;
    case 'vent':
      return <Air />;
    default:
      return null;
  }
};

const CarteMétéo: React.FC<CarteMétéoProps> = ({
  title,
  value,
  status
}) => {
  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              width: 40,
              height: 40,
              borderRadius: '50%',
              bgcolor: `${getStatusColor(status)}15`,
              color: getStatusColor(status),
              mr: 2
            }}
          >
            {getStatusIcon(title)}
          </Box>
          <Typography variant="h6" color="text.secondary">
            {title}
          </Typography>
        </Box>

        <Typography variant="h4" component="div" gutterBottom>
          {value}
        </Typography>

        <Box display="flex" alignItems="center">
          <Typography
            variant="body2"
            sx={{
              color: getStatusColor(status),
              fontWeight: 'medium'
            }}
          >
            Niveau: {status}
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CarteMétéo;
