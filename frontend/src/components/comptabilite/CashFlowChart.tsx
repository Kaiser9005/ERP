import React, { useState } from 'react';
import {
  Card,
  CardContent,
  CardHeader,
  Box,
  IconButton,
  Tooltip,
  FormControl,
  Select,
  MenuItem,
  SelectChangeEvent,
  Typography,
  LinearProgress,
} from '@mui/material';
import { Info } from '@mui/icons-material';
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as ChartTooltip,
  Legend,
  Area,
} from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { formatCurrency } from '../../utils/format';
import * as comptabiliteService from '../../services/comptabilite';
import type { CashFlowData } from '../../types/comptabilite';

const PERIODE_OPTIONS = [
  { value: '30', label: '30 jours' },
  { value: '90', label: '90 jours' },
  { value: '180', label: '6 mois' },
  { value: '365', label: '1 an' },
];

const CustomTooltip: React.FC<any> = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <Box
        sx={{
          bgcolor: 'background.paper',
          p: 2,
          border: 1,
          borderColor: 'divider',
          borderRadius: 1,
          boxShadow: 1,
        }}
      >
        <Typography variant="subtitle2" sx={{ mb: 1 }}>
          {label}
        </Typography>
        {payload.map((entry: any, index: number) => (
          <Box key={index} sx={{ mb: 0.5 }}>
            <Typography
              variant="body2"
              sx={{ color: entry.color, display: 'flex', alignItems: 'center', gap: 1 }}
            >
              <Box
                component="span"
                sx={{
                  width: 12,
                  height: 12,
                  bgcolor: entry.color,
                  borderRadius: '50%',
                }}
              />
              {entry.name}: {formatCurrency(entry.value)}
            </Typography>
          </Box>
        ))}
      </Box>
    );
  }
  return null;
};

const CashFlowChart: React.FC = () => {
  const [periode, setPeriode] = useState('30');

  const { data, isLoading } = useQuery<CashFlowData[]>({
    queryKey: ['comptabilite', 'cashflow', periode],
    queryFn: () => comptabiliteService.getCashFlow(Number(periode)),
    staleTime: 1000 * 60 * 5, // 5 minutes
  });

  const handlePeriodeChange = (event: SelectChangeEvent) => {
    setPeriode(event.target.value);
  };

  if (isLoading) {
    return <LinearProgress />;
  }

  if (!data) {
    return (
      <Typography color="textSecondary">
        Aucune donnée de trésorerie disponible
      </Typography>
    );
  }

  return (
    <Card>
      <CardHeader
        title="Évolution de la Trésorerie"
        action={
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
            <FormControl size="small">
              <Select value={periode} onChange={handlePeriodeChange}>
                {PERIODE_OPTIONS.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            <Tooltip title="Analyse de trésorerie avec impact météorologique">
              <IconButton>
                <Info />
              </IconButton>
            </Tooltip>
          </Box>
        }
      />
      <CardContent>
        <Box sx={{ width: '100%', height: 400 }}>
          <ResponsiveContainer>
            <ComposedChart
              data={data}
              margin={{ top: 20, right: 20, bottom: 20, left: 20 }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                scale="point"
                padding={{ left: 20, right: 20 }}
              />
              <YAxis
                yAxisId="left"
                orientation="left"
                tickFormatter={(value) => formatCurrency(value)}
              />
              <YAxis
                yAxisId="right"
                orientation="right"
                tickFormatter={(value) => `${value}%`}
              />
              <ChartTooltip content={<CustomTooltip />} />
              <Legend />

              {/* Barres pour les entrées et sorties */}
              <Bar
                yAxisId="left"
                dataKey="entrees"
                name="Entrées"
                fill="#4caf50"
                opacity={0.8}
                barSize={20}
              />
              <Bar
                yAxisId="left"
                dataKey="sorties"
                name="Sorties"
                fill="#f44336"
                opacity={0.8}
                barSize={20}
              />

              {/* Ligne pour le solde */}
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="solde"
                name="Solde"
                stroke="#2196f3"
                strokeWidth={2}
                dot={{ r: 4 }}
              />

              {/* Zone pour les prévisions */}
              <Area
                yAxisId="left"
                type="monotone"
                dataKey="prevision"
                name="Prévision"
                stroke="#9c27b0"
                fill="#9c27b0"
                fillOpacity={0.1}
                strokeDasharray="5 5"
              />

              {/* Ligne pour l'impact météo */}
              <Line
                yAxisId="right"
                type="monotone"
                dataKey="impact_meteo"
                name="Impact Météo"
                stroke="#ff9800"
                strokeWidth={1}
                dot={{ r: 3 }}
              />
            </ComposedChart>
          </ResponsiveContainer>
        </Box>

        {/* Légende des indicateurs */}
        <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 2 }}>
          <Typography variant="body2" color="textSecondary">
            • Les barres représentent les entrées et sorties de trésorerie
          </Typography>
          <Typography variant="body2" color="textSecondary">
            • La ligne bleue montre l'évolution du solde
          </Typography>
          <Typography variant="body2" color="textSecondary">
            • La zone violette indique les prévisions
          </Typography>
          <Typography variant="body2" color="textSecondary">
            • La ligne orange représente l'impact météorologique
          </Typography>
        </Box>
      </CardContent>
    </Card>
  );
};

export default CashFlowChart;
