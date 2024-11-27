import { FC } from 'react';
import { Box, useTheme } from '@mui/material';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';
import type { ModuleCorrelations } from '../../types/analytics_cross_module';

interface CorrelationsChartProps {
  correlations: ModuleCorrelations;
}

export const CorrelationsChart: FC<CorrelationsChartProps> = ({ correlations }) => {
  const theme = useTheme();

  const data = [
    {
      name: 'RH-Production',
      value: correlations.hr_production,
      fill: theme.palette.primary.main
    },
    {
      name: 'Production-Finance',
      value: correlations.production_finance,
      fill: theme.palette.secondary.main
    },
    {
      name: 'Météo-Global',
      value: correlations.weather_global,
      fill: theme.palette.info.main
    },
    {
      name: 'Inventaire-Finance',
      value: correlations.inventory_finance,
      fill: theme.palette.warning.main
    }
  ];

  return (
    <Box sx={{ width: '100%', height: 300 }}>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            dataKey="name"
            angle={-45}
            textAnchor="end"
            height={70}
            interval={0}
          />
          <YAxis
            domain={[0, 1]}
            tickFormatter={(value) => `${(value * 100).toFixed(0)}%`}
          />
          <Tooltip
            formatter={(value: number) => `${(value * 100).toFixed(1)}%`}
          />
          <Bar
            dataKey="value"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default CorrelationsChart;
