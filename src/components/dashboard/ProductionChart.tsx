import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { productionService } from '../../services/production';

interface ChartData {
  mois: string;
  quantite: number;
}

const ProductionChart: React.FC = () => {
  const [data, setData] = useState<ChartData[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        // On utilise une parcelle "global" pour les statistiques générales
        const stats = await productionService.getProductionStats('global');
        setData(stats);
      } catch (error) {
        console.error('Erreur lors du chargement des données de production:', error);
      } finally {
        setIsLoading(false);
      }
    };

    fetchData();
  }, []);

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
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
