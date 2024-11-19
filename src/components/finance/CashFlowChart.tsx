import React from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';
import { useQuery } from '@tanstack/react-query';
import { getCashFlowData, CashFlowData } from '../../services/finance';

const CashFlowChart: React.FC = () => {
  const { data: cashflowData, isLoading } = useQuery<CashFlowData>(
    ['cashflow'],
    getCashFlowData
  );

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  if (!cashflowData) {
    return null;
  }

  const chartData = cashflowData.labels.map((label, index) => ({
    name: label,
    recettes: cashflowData.recettes[index],
    depenses: cashflowData.depenses[index],
    solde: cashflowData.solde?.[index],
    previsions: cashflowData.previsions?.[index],
    impact_meteo: cashflowData.impact_meteo?.[index]
  }));

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Flux de Trésorerie
        </Typography>
        <LineChart width={800} height={400} data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="recettes" stroke="#4caf50" name="Recettes" />
          <Line type="monotone" dataKey="depenses" stroke="#f44336" name="Dépenses" />
          {cashflowData.solde && (
            <Line type="monotone" dataKey="solde" stroke="#2196f3" name="Solde" />
          )}
          {cashflowData.previsions && (
            <Line
              type="monotone"
              dataKey="previsions"
              stroke="#9c27b0"
              name="Prévisions"
              strokeDasharray="5 5"
            />
          )}
          {cashflowData.impact_meteo && (
            <Line
              type="monotone"
              dataKey="impact_meteo"
              stroke="#ff9800"
              name="Impact Météo"
              strokeDasharray="3 3"
            />
          )}
        </LineChart>
      </CardContent>
    </Card>
  );
};

export default CashFlowChart;
