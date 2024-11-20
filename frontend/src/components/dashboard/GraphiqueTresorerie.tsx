import React from 'react';
import { Card, CardContent, Typography, Box } from '@mui/material';
import { useQuery } from 'react-query';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';

interface DonneeTresorerie {
  date: string;
  solde: number;
  entrees: number;
  sorties: number;
}

const getDonneesTresorerie = async (): Promise<DonneeTresorerie[]> => {
  const response = await fetch('/api/v1/finance/tresorerie/evolution');
  return response.json();
};

const formatMontant = (montant: number) => {
  return new Intl.NumberFormat('fr-FR', {
    style: 'currency',
    currency: 'XAF',
    maximumFractionDigits: 0
  }).format(montant);
};

const formatDate = (date: string) => {
  return format(new Date(date), 'd MMM', { locale: fr });
};

const GraphiqueTresorerie: React.FC = () => {
  const { data: donnees = [], isLoading } = useQuery(
    'donnees-tresorerie',
    getDonneesTresorerie
  );

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Typography color="text.secondary">
            Chargement des données de trésorerie...
          </Typography>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Évolution de la Trésorerie
        </Typography>

        <Box sx={{ width: '100%', height: 300 }}>
          <ResponsiveContainer>
            <AreaChart
              data={donnees}
              margin={{
                top: 10,
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
                tickFormatter={formatMontant}
                label={{ 
                  value: 'Montant (XAF)', 
                  angle: -90, 
                  position: 'insideLeft',
                  style: { textAnchor: 'middle' }
                }}
              />
              <Tooltip
                labelFormatter={(value) => format(new Date(value), 'dd MMMM yyyy', { locale: fr })}
                formatter={(value: number) => [formatMontant(value)]}
              />
              <Legend />
              <Area
                type="monotone"
                dataKey="solde"
                name="Solde"
                stroke="#8884d8"
                fill="#8884d8"
                fillOpacity={0.3}
              />
              <Area
                type="monotone"
                dataKey="entrees"
                name="Entrées"
                stroke="#82ca9d"
                fill="#82ca9d"
                fillOpacity={0.3}
              />
              <Area
                type="monotone"
                dataKey="sorties"
                name="Sorties"
                stroke="#ffc658"
                fill="#ffc658"
                fillOpacity={0.3}
              />
            </AreaChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
};

export default GraphiqueTresorerie;
