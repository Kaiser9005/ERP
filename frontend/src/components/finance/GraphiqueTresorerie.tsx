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
import { useQuery } from 'react-query';
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

const GraphiqueTresorerie: React.FC = () => {
  const { data: tresorerie } = useQuery('tresorerie', getDonneesTresorerie);

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
    labels: tresorerie?.labels || [],
    datasets: [
      {
        label: 'Recettes',
        data: tresorerie?.recettes || [],
        borderColor: 'rgb(46, 125, 50)',
        backgroundColor: 'rgba(46, 125, 50, 0.5)',
        tension: 0.3
      },
      {
        label: 'Dépenses',
        data: tresorerie?.depenses || [],
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
