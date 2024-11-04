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
import { getBudgetOverview } from '../../services/finance';

const BudgetOverview: React.FC = () => {
  const { data: budgets, isLoading } = useQuery('budget-overview', getBudgetOverview);

  const getProgressColor = (percentage: number) => {
    if (percentage >= 90) return 'error';
    if (percentage >= 75) return 'warning';
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
            const percentage = (budget.spent / budget.allocated) * 100;
            return (
              <ListItem key={budget.category}>
                <ListItemText
                  primary={budget.category}
                  secondary={
                    <Box sx={{ mt: 1 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="body2" color="text.secondary">
                          {new Intl.NumberFormat('fr-FR', {
                            style: 'currency',
                            currency: 'XAF'
                          }).format(budget.spent)}
                        </Typography>
                        <Typography variant="body2" color="text.secondary">
                          {new Intl.NumberFormat('fr-FR', {
                            style: 'currency',
                            currency: 'XAF'
                          }).format(budget.allocated)}
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={Math.min(percentage, 100)}
                        color={getProgressColor(percentage)}
                      />
                      <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5 }}>
                        {percentage.toFixed(1)}% utilisé
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

export default BudgetOverview;