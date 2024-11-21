import React from 'react';
import {
  Card,
  CardContent,
  Grid,
  Typography,
  Box,
  Switch,
  FormControlLabel,
  IconButton,
  Button,
  TextField
} from '@mui/material';
import { Settings } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { ConfigurationModule } from '../../types/parametrage';
import { api } from '../../services/api';

const ConfigurationModules: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: modules, isLoading } = useQuery<ConfigurationModule[]>(
    'configuration-modules',
    async () => {
      const response = await api.get('/api/v1/parametrage/modules');
      return response.data;
    }
  );

  const updateModule = useMutation(
    async (params: { id: string; data: Partial<ConfigurationModule> }) => {
      await api.put(`/api/v1/parametrage/modules/${params.id}`, params.data);
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('configuration-modules');
      }
    }
  );

  const handleToggleModule = (module: ConfigurationModule) => () => {
    updateModule.mutate({
      id: module.id,
      data: { actif: !module.actif }
    });
  };

  if (isLoading) {
    return <Typography>Chargement...</Typography>;
  }

  return (
    <Grid container spacing={3}>
      {modules?.map((module) => (
        <Grid item xs={12} md={6} key={module.id}>
          <Card>
            <CardContent>
              <Box
                display="flex"
                alignItems="center"
                justifyContent="space-between"
                mb={2}
              >
                <Box display="flex" alignItems="center">
                  <Box
                    sx={{
                      width: 40,
                      height: 40,
                      borderRadius: '50%',
                      backgroundColor: module.couleur || 'primary.main',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      mr: 2
                    }}
                  >
                    <Settings sx={{ color: 'white' }} />
                  </Box>
                  <Box>
                    <Typography variant="subtitle1">
                      {module.module}
                    </Typography>
                  </Box>
                </Box>

                <FormControlLabel
                  control={
                    <Switch
                      checked={module.actif}
                      onChange={handleToggleModule(module)}
                    />
                  }
                  label={module.actif ? 'Activé' : 'Désactivé'}
                />
              </Box>

              <Box mb={2}>
                <TextField
                  fullWidth
                  label="Ordre d'affichage"
                  type="number"
                  size="small"
                  value={module.ordre_affichage}
                  onChange={(e) =>
                    updateModule.mutate({
                      id: module.id,
                      data: { ordre_affichage: parseInt(e.target.value, 10) }
                    })
                  }
                />
              </Box>

              <Box>
                <Typography variant="body2" color="text.secondary">
                  Rôles autorisés : {module.roles_autorises.join(', ')}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      ))}

      <Grid item xs={12}>
        <Box display="flex" justifyContent="flex-end" mt={2}>
          <Button
            variant="contained"
            color="primary"
            onClick={() => queryClient.invalidateQueries('configuration-modules')}
          >
            Actualiser
          </Button>
        </Box>
      </Grid>
    </Grid>
  );
};

export default ConfigurationModules;
