import React from 'react';
import { Grid } from '@mui/material';
import CarteStatistique from '../common/CarteStatistique';
import { People, EventAvailable, Sick, School } from '@mui/icons-material';
import { useQuery } from '@tanstack/react-query';
import { getEmployeeStats } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';
import { EmployeeStats as EmployeeStatsType } from '../../types/hr';

type VariationType = 'hausse' | 'baisse';

const formatVariation = (value: number): { valeur: number; type: VariationType } => ({
  valeur: Math.abs(value),
  type: value >= 0 ? 'hausse' : 'baisse'
});

const EmployeeStats: React.FC = () => {
  const { data: stats, isLoading } = useQuery<EmployeeStatsType>({
    queryKey: queryKeys.hr.stats(),
    queryFn: getEmployeeStats
  });

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} sm={6} md={3}>
        <CarteStatistique
          titre="Effectif Total"
          valeur={stats?.totalEmployees || 0}
          variation={stats?.employeesVariation ? formatVariation(stats.employeesVariation) : undefined}
          icone={<People />}
          couleur="primary"
          chargement={isLoading}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <CarteStatistique
          titre="Présents Aujourd'hui"
          valeur={stats?.presentToday || 0}
          variation={stats?.presenceVariation ? formatVariation(stats.presenceVariation) : undefined}
          icone={<EventAvailable />}
          couleur="success"
          chargement={isLoading}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <CarteStatistique
          titre="En Congé"
          valeur={stats?.onLeave || 0}
          variation={stats?.leaveVariation ? formatVariation(stats.leaveVariation) : undefined}
          icone={<Sick />}
          couleur="warning"
          chargement={isLoading}
        />
      </Grid>

      <Grid item xs={12} sm={6} md={3}>
        <CarteStatistique
          titre="En Formation"
          valeur={stats?.inTraining || 0}
          variation={stats?.trainingVariation ? formatVariation(stats.trainingVariation) : undefined}
          icone={<School />}
          couleur="info"
          chargement={isLoading}
        />
      </Grid>
    </Grid>
  );
};

export default EmployeeStats;
