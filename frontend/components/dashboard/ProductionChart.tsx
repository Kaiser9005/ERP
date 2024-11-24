import React from 'react';
import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { productionService } from '../../services/production';
import { queryKeys } from '../../config/queryClient';

interface ChartData {
  mois: string;
  quantite: number;
}

const ProductionChart: React.FC = () => {
  const { data, isLoading } = useQuery<ChartData[]>({
    queryKey: queryKeys.production.stats(),
    queryFn: () => productionService.getProductionStats('global'),
    staleTime: 1000 * 60 * 5, // 5 minutes
    refetchInterval: 1000 * 60 * 15 // 15 minutes
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
          <CircularProgress />
        </CardContent>
      </Card>
    );
  }

  if (!data) {
    return (
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Production Mensuelle
          </Typography>
          <Typography color="textSecondary">
            Aucune donnée disponible
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Production Mensuelle
        </Typography>
        <LineChart width={600} height={300} data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="mois" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="quantite" stroke="#8884d8" />
        </LineChart>
      </CardContent>
    </Card>
  );
};

export default ProductionChart;
