import React from 'react';
import { Box, Typography, Grid, Paper } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';
import { useQuery } from 'react-query';
import { getFinanceOverview } from '../../services/finance';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);

const FinanceOverview: React.FC = () => {
  const { data: financeData } = useQuery('finance-overview', getFinanceOverview);

  const options: ChartOptions<'bar'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
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
    labels: financeData?.labels || [],
    datasets: [
      {
        label: 'Revenus',
        data: financeData?.revenues || [],
        backgroundColor: 'rgba(46, 125, 50, 0.5)',
      },
      {
        label: 'Dépenses',
        data: financeData?.expenses || [],
        backgroundColor: 'rgba(211, 47, 47, 0.5)',
      }
    ]
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Aperçu Financier
      </Typography>
      <Box sx={{ height: 300 }}>
        <Bar options={options} data={data} />
      </Box>
    </Box>
  );
};

export default FinanceOverview;