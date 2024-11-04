import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { Doughnut } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  ChartOptions
} from 'chart.js';

ChartJS.register(ArcElement, Tooltip, Legend);

interface AttendanceStats {
  presents: number;
  absents: number;
  retards: number;
  conges: number;
}

interface AttendanceChartProps {
  data?: AttendanceStats;
}

const AttendanceChart: React.FC<AttendanceChartProps> = ({ data }) => {
  const chartData = {
    labels: ['Présents', 'Absents', 'Retards', 'Congés'],
    datasets: [
      {
        data: [
          data?.presents || 0,
          data?.absents || 0,
          data?.retards || 0,
          data?.conges || 0
        ],
        backgroundColor: [
          'rgba(46, 125, 50, 0.8)',  // success
          'rgba(211, 47, 47, 0.8)',  // error
          'rgba(237, 108, 2, 0.8)',  // warning
          'rgba(2, 136, 209, 0.8)'   // info
        ],
        borderColor: [
          'rgb(46, 125, 50)',
          'rgb(211, 47, 47)',
          'rgb(237, 108, 2)',
          'rgb(2, 136, 209)'
        ],
        borderWidth: 1
      }
    ]
  };

  const options: ChartOptions<'doughnut'> = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom' as const
      }
    },
    cutout: '70%'
  };

  const total = (data?.presents || 0) + 
                (data?.absents || 0) + 
                (data?.retards || 0) + 
                (data?.conges || 0);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Répartition des Présences
        </Typography>
        <Box sx={{ position: 'relative', height: 300 }}>
          <Doughnut data={chartData} options={options} />
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              textAlign: 'center'
            }}
          >
            <Typography variant="h4">{total}</Typography>
            <Typography variant="body2" color="text.secondary">
              Total
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default AttendanceChart;