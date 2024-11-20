import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  LinearProgress,
  Box
} from '@mui/material';
import { useQuery } from 'react-query';
import { getVueBudget } from '../../services/finance';

const VueBudget: React.FC = () => {
  const { data: budgets } = useQuery('vue-budget', getVueBudget);

  const getCouleurProgression = (pourcentage: number) => {
    if (pourcentage >= 90) return 'error';
    if (pourcentage >= 75) return 'warning';
    return 'success';
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Suivi Budgétaire
        </Typography>

        <List>
          {budgets?.map((budget) => {
            const pourcentage = (budget.depense / budget.alloue) * 100;
            return (
              <ListItem key={budget.categorie}>
                <ListItemText
                  primary={budget.categorie}
                  secondary={
                    <Box sx={{ mt: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2" color="text.secondary">
                          {new Intl.NumberFormat('fr-FR', {
                            style: 'currency',
                            currency: 'XAF'
                          }).format(budget.depense)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {new Intl.NumberFormat('fr-FR', {
                            style: 'currency',
                            currency: 'XAF'
                          }).format(budget.alloue)}
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={Math.min(pourcentage, 100)}
                        color={getCouleurProgression(pourcentage)}
                      />
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                        {pourcentage.toFixed(1)}% utilisé
                      </Typography>
                    </Box>
                  }
                />
              </ListItem>
            );
          })}
        </List>
      </CardContent>
    </Card>
  );
};

export default VueBudget;
