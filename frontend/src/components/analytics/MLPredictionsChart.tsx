import { FC } from 'react';
import { Box, useTheme } from '@mui/material';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer
} from 'recharts';
import type { ModulePredictions } from '../../types/analytics_cross_module';

interface MLPredictionsChartProps {
  predictions: ModulePredictions;
}

export const MLPredictionsChart: FC<MLPredictionsChartProps> = ({ predictions }) => {
  const theme = useTheme();

  // Transformer les prédictions en données pour le graphique
  const data = [
    {
      name: 'RH',
      confidence: predictions.hr.confidence,
      risk: predictions.hr.risk_level,
    },
    {
      name: 'Production',
      confidence: predictions.production.confidence,
      risk: predictions.production.risk_level,
    },
    {
      name: 'Finance',
      confidence: predictions.finance.confidence,
      risk: predictions.finance.risk_level,
    },
    {
      name: 'Inventaire',
      confidence: predictions.inventory.confidence,
      risk: predictions.inventory.risk_level,
    }
  ];

  return (
    <Box sx={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis
            domain={[0, 1]}
            tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
          />
          <Tooltip
            formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
          />
          <Legend />
          <Line
            type="monotone"
            dataKey="confidence"
            name="Confiance"
            stroke={theme.palette.primary.main}
            strokeWidth={2}
          />
          <Line
            type="monotone"
            dataKey="risk"
            name="Risque"
            stroke={theme.palette.error.main}
            strokeWidth={2}
          />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default MLPredictionsChart;
