import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress
} from '@mui/material';

interface StatCardProps {
  title: string;
  value: number;
  total: number;
  icon: React.ReactNode;
  color: 'primary' | 'success' | 'warning' | 'error' | 'info';
}

const StatCard: React.FC<StatCardProps> = ({ title, value, total, icon, color }) => {
  const percentage = (value / total) * 100;

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" mb={2}>
          <Box
            sx={{
              backgroundColor: `${color}.light`,
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

        <Typography variant="h4" gutterBottom>
          {value}
          <Typography
            component="span"
            variant="subtitle1"
            color="text.secondary"
            sx={{ ml: 1 }}
          >
            / {total}
          </Typography>
        </Typography>

        <Box>
          <LinearProgress
            variant="determinate"
            value={percentage}
            sx={{ mb: 1, backgroundColor: `${color}.lighter` }}
            color={color}
          />
          <Typography variant="body2" color="text.secondary">
            {percentage.toFixed(1)}% du total
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default StatCard;
