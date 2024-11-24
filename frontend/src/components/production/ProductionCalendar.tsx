import React, { useEffect, useState } from 'react';
import { Paper, Typography, Box } from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot
} from '@mui/lab';
import { CycleCulture, Parcelle } from '../../types/production';
import { productionService } from '../../services/production';

interface ProductionCalendarProps {
  parcelle?: Parcelle;
}

const ProductionCalendar: React.FC<ProductionCalendarProps> = ({ parcelle }) => {
  const [cycles, setCycles] = useState<CycleCulture[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadCycles = async () => {
      if (!parcelle) return;

      try {
        setLoading(true);
        const cyclesData = await productionService.getCyclesCulture(parcelle.id);
        setCycles(cyclesData);
      } catch (err) {
        setError('Erreur lors du chargement des cycles de culture');
      } finally {
        setLoading(false);
      }
    };

    loadCycles();
  }, [parcelle]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Chargement du calendrier...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography color="error">{error}</Typography>
      </Box>
    );
  }

  if (!parcelle) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Sélectionnez une parcelle pour voir son calendrier</Typography>
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 2 }}>
      <Typography variant="h6" gutterBottom>
        Calendrier de Production - {parcelle.code}
      </Typography>

      <Timeline position="alternate">
        {cycles.map((cycle) => (
          <TimelineItem key={cycle.id}>
            <TimelineSeparator>
              <TimelineDot color="primary" />
              <TimelineConnector />
            </TimelineSeparator>
            <TimelineContent>
              <Paper elevation={2} sx={{ p: 2 }}>
                <Typography variant="subtitle1">
                  Cycle du {new Date(cycle.date_debut).toLocaleDateString()}
                </Typography>
                {cycle.date_fin && (
                  <Typography variant="body2">
                    au {new Date(cycle.date_fin).toLocaleDateString()}
                  </Typography>
                )}
                {cycle.rendement_prevu && (
                  <Typography variant="body2">
                    Rendement prévu: {cycle.rendement_prevu} kg/ha
                  </Typography>
                )}
                {cycle.rendement_reel && (
                  <Typography variant="body2">
                    Rendement réel: {cycle.rendement_reel} kg/ha
                  </Typography>
                )}
                {cycle.notes && (
                  <Typography variant="body2" color="textSecondary">
                    Notes: {cycle.notes}
                  </Typography>
                )}
              </Paper>
            </TimelineContent>
          </TimelineItem>
        ))}
      </Timeline>

      {cycles.length === 0 && (
        <Box display="flex" justifyContent="center" alignItems="center" p={3}>
          <Typography>Aucun cycle de culture enregistré pour cette parcelle</Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ProductionCalendar;
