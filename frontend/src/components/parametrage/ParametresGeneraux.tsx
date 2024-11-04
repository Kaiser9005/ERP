import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Grid,
  Alert,
  CircularProgress
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getParametres, updateParametre } from '../../services/parametrage';
import { Parametre } from '../../types/parametrage';

const ParametresGeneraux: React.FC = () => {
  const queryClient = useQueryClient();
  const [error, setError] = useState<string | null>(null);

  const { data: parametres, isLoading } = useQuery(
    'parametres-generaux',
    () => getParametres('GENERAL')
  );

  const updateMutation = useMutation(updateParametre, {
    onSuccess: () => {
      queryClient.invalidateQueries('parametres-generaux');
      setError(null);
    },
    onError: (error: Error) => {
      setError(error.message);
    }
  });

  const handleParametreChange = (parametre: Parametre, newValue: any) => {
    updateMutation.mutate({
      id: parametre.id,
      valeur: { ...parametre.valeur, value: newValue }
    });
  };

  if (isLoading) {
    return <CircularProgress />;
  }

  return (
    <Box>
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Grid container spacing={3}>
        {parametres?.map((parametre) => (
          <Grid item xs={12} md={6} key={parametre.id}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {parametre.libelle}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {parametre.description}
                </Typography>
                
                <TextField
                  fullWidth
                  label="Valeur"
                  value={parametre.valeur.value}
                  onChange={(e) => handleParametreChange(parametre, e.target.value)}
                  disabled={!parametre.modifiable}
                  margin="normal"
                />
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ParametresGeneraux;