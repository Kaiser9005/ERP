import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { useQuery } from '@tanstack/react-query';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface DonneeProduction {
  date: string;
  parcelle_a: number;
  parcelle_b: number;
  parcelle_c: number;
  parcelle_d: number;
}

const getDonneesProduction = async (): Promise<DonneeProduction[]> => {
  const response = await fetch('/api/v1/production/graphique');
  return response.json();
};

const formatDate = (date: string) => {
  return format(new Date(date), 'd MMM', { locale: fr });
};

const GraphiqueProduction: React.FC = () => {
  const { data: donnees = [], isLoading } = useQuery({
    queryKey: ['donnees-production'],
    queryFn: getDonneesProduction
  });

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography color="text.secondary">
            Chargement des données de production...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Production par Parcelle
        </Typography>

        <Box sx={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <LineChart
              data={donnees}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                tickFormatter={formatDate}
                interval="preserveEnd"
              />
              <YAxis
                label={{ 
                  value: 'Production (kg)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
              />
              <Tooltip
                labelFormatter={(value) => format(new Date(value), 'dd MMMM yyyy', { locale: fr })}
                formatter={(value: number) => [`${value} kg`]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey="parcelle_a"
                name="Parcelle A"
                stroke="#8884d8"
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="parcelle_b"
                name="Parcelle B"
                stroke="#82ca9d"
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="parcelle_c"
                name="Parcelle C"
                stroke="#ffc658"
                activeDot={{ r: 8 }}
              />
              <Line
                type="monotone"
                dataKey="parcelle_d"
                name="Parcelle D"
                stroke="#ff7300"
                activeDot={{ r: 8 }}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GraphiqueProduction;
