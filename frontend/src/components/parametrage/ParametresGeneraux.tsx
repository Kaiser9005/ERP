import React from 'react';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  Typography,
  Box,
  Button,
  FormControlLabel,
  Switch
} from '@mui/material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { Parametre } from '../../types/parametrage';
import { api } from '../../services/api';

const ParametresGeneraux: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: parametres, isLoading } = useQuery<Parametre[]>(
    'parametres-generaux',
    async () => {
      const response = await api.get('/api/v1/parametrage/general');
      return response.data;
    }
  );

  const updateParametre = useMutation(
    async (params: { id: string; valeur: any }) => {
      await api.put(`/api/v1/parametrage/${params.id}`, {
        valeur: params.valeur
      });
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('parametres-generaux');
      }
    }
  );

  const handleChange = (parametre: Parametre) => (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const value = event.target.type === 'checkbox' 
      ? event.target.checked 
      : event.target.value;

    updateParametre.mutate({
      id: parametre.id,
      valeur: value
    });
  };

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Grid container spacing={3}>
      {parametres?.map((parametre) => (
        <Grid item xs={12} md={6} key={parametre.id}>
          <Card>
            <CardContent>
              <Box mb={2}>
                <Typography variant="subtitle1" gutterBottom>
                  {parametre.libelle}
                </Typography>
                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {parametre.description}
                </Typography>
              </Box>

              {typeof parametre.valeur === 'boolean' ? (
                <FormControlLabel
                  control={
                    <Switch
                      checked={parametre.valeur}
                      onChange={handleChange(parametre)}
                      disabled={!parametre.modifiable}
                    />
                  }
                  label={parametre.valeur ? 'Activé' : 'Désactivé'}
                />
              ) : (
                <TextField
                  fullWidth
                  value={parametre.valeur}
                  onChange={handleChange(parametre)}
                  disabled={!parametre.modifiable}
                  size="small"
                  variant="outlined"
                  type={typeof parametre.valeur === 'number' ? 'number' : 'text'}
                />
              )}
            </CardContent>
          </Card>
        </Grid>
      ))}

      <Grid item xs={12}>
        <Box display="flex" justifyContent="flex-end" mt={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => queryClient.invalidateQueries('parametres-generaux')}
          >
            Actualiser
          </Button>
        </Box>
      </Grid>
    </Grid>
  );
};

export default ParametresGeneraux;
