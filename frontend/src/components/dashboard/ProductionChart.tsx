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
import { getProductionHistory } from '../../services/production';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const ProductionChart: React.FC = () => {
  const { data: history } = useQuery('production-history', getProductionHistory);

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
          text: 'Production (tonnes)'
        }
      }
    }
  };

  const data = {
    labels: history?.labels || [],
    datasets: [
      {
        label: 'Palmier à huile',
        data: history?.palmier || [],
        borderColor: 'rgb(46, 125, 50)',
        backgroundColor: 'rgba(46, 125, 50, 0.5)',
        tension: 0.3
      },
      {
        label: 'Papaye',
        data: history?.papaye || [],
        borderColor: 'rgb(255, 160, 0)',
        backgroundColor: 'rgba(255, 160, 0, 0.5)',
        tension: 0.3
      }
    ]
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Production par Culture
        </Typography>
        <div style={{ height: '300px' }}>
          <Line options={options} data={data} />
        </div>
      </CardContent>
    </Card>
  );
};

export default ProductionChart;