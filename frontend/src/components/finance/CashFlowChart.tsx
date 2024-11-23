import React from 'react';
import { Card, CardContent, Typography, CircularProgress } from '@mui/material';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import { useQuery } from '@tanstack/react-query';
import { getCashFlowData } from '../../services/finance';
import { queryKeys } from '../../config/queryClient';
import type { CashFlowData } from '../../types/finance';
import type { ChartOptions } from 'chart.js';

// Enregistrer les composants Chart.js nécessaires
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const CashFlowChart: React.FC = () => {
  const { data: cashflowData, isLoading, error } = useQuery<CashFlowData>({
    queryKey: queryKeys.finance.cashflow(),
    queryFn: () => getCashFlowData(),
    staleTime: 1000 * 60 * 5 // 5 minutes
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

  if (error || !cashflowData) {
    return (
      <Card>
        <CardContent sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 400 }}>
          <Typography color="error">
            Erreur lors du chargement des données de trésorerie
          </Typography>
        </CardContent>
      </Card>
    );
  }

  const chartData = {
    labels: cashflowData.labels,
    datasets: [
      {
        label: 'Recettes',
        data: cashflowData.recettes,
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.1)',
        fill: true,
        tension: 0.1
      },
      {
        label: 'Dépenses',
        data: cashflowData.depenses,
        borderColor: 'rgb(255, 99, 132)',
        backgroundColor: 'rgba(255, 99, 132, 0.1)',
        fill: true,
        tension: 0.1
      },
      {
        label: 'Solde',
        data: cashflowData.solde,
        borderColor: 'rgb(54, 162, 235)',
        backgroundColor: 'rgba(54, 162, 235, 0.1)',
        fill: true,
        tension: 0.1,
        borderDash: [5, 5]
      },
      {
        label: 'Prévisions',
        data: cashflowData.previsions,
        borderColor: 'rgb(153, 102, 255)',
        backgroundColor: 'rgba(153, 102, 255, 0.1)',
        fill: true,
        tension: 0.1,
        borderDash: [10, 5]
      },
      {
        label: 'Impact Météo',
        data: cashflowData.impact_meteo,
        borderColor: 'rgb(255, 159, 64)',
        backgroundColor: 'rgba(255, 159, 64, 0.1)',
        fill: true,
        tension: 0.1,
        borderDash: [15, 5]
      }
    ]
  };

  const options: ChartOptions<'line'> = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        align: 'center'
      },
      title: {
        display: true,
        text: 'Flux de Trésorerie',
        font: {
          size: 16
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
        callbacks: {
          label: (context) => {
            const value = context.raw as number;
            return `${context.dataset.label}: ${value.toLocaleString('fr-FR', {
              style: 'currency',
              currency: 'XAF'
            })}`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        }
      },
      y: {
        beginAtZero: true,
        grid: {
          color: 'rgba(0, 0, 0, 0.1)'
        },
        ticks: {
          callback: (value) => {
            return (value as number).toLocaleString('fr-FR', {
              style: 'currency',
              currency: 'XAF',
              maximumFractionDigits: 0
            });
          }
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    }
  };

  return (
    <Card>
      <CardContent sx={{ height: 400 }}>
        <Line data={chartData} options={options} />
      </CardContent>
    </Card>
  );
};

export default CashFlowChart;
