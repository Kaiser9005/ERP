import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js';
import { useQuery } from '@tanstack/react-query';
import { getDonneesTresorerie } from '../../services/finance';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

interface ChartData {
  labels: string[];
  recettes: number[];
  depenses: number[];
}

const GraphiqueTresorerie: React.FC = () => {
  const { data: chartData } = useQuery({
    queryKey: ['tresorerie'],
    queryFn: async (): Promise<ChartData> => {
      const tresorerieData = await getDonneesTresorerie();
      const labels = tresorerieData.historique.map(item => item.date);
      const recettes = tresorerieData.historique.map(item => (item.variation.type === 'increase' ? item.variation.value : 0));
      const depenses = tresorerieData.historique.map(item => (item.variation.type === 'decrease' ? item.variation.value : 0));
      
      return { labels, recettes, depenses };
    }
  });

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
      title: {
        display: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'Montant (FCFA)'
        }
      }
    }
  };

  const data = {
    labels: chartData?.labels || [],
    datasets: [
      {
        label: 'Recettes',
        data: chartData?.recettes || [],
        borderColor: 'rgb(46, 125, 50)',
        backgroundColor: 'rgba(46, 125, 50, 0.5)',
        tension: 0.3
      },
      {
        label: 'Dépenses',
        data: chartData?.depenses || [],
        borderColor: 'rgb(211, 47, 47)',
        backgroundColor: 'rgba(211, 47, 47, 0.5)',
        tension: 0.3
      }
    ]
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Flux de Trésorerie
        </Typography>
        <div style={{ height: '300px' }}>
          <Line options={options} data={data} />
        </div>
      </CardContent>
    </Card>
  );
};

export default GraphiqueTresorerie;
