import React from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Switch,
  FormControlLabel,
  Grid,
  IconButton,
  Chip
} from '@mui/material';
import { Settings } from '@mui/icons-material';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { getModulesConfiguration, updateModuleConfiguration } from '../../services/parametrage';
import { ConfigurationModule } from '../../types/parametrage';

const ConfigurationModules: React.FC = () => {
  const queryClient = useQueryClient();

  const { data: modules, isLoading } = useQuery(
    'modules-configuration',
    getModulesConfiguration
  );

  const updateMutation = useMutation(updateModuleConfiguration, {
    onSuccess: () => {
      queryClient.invalidateQueries('modules-configuration');
    }
  });

  const handleModuleActivation = (module: ConfigurationModule) => {
    updateMutation.mutate({
      module: module.module,
      actif: !module.actif
    });
  };

  if (isLoading) {
    return <div>Chargement...</div>;
  }

  return (
    <Box>
      <Grid container spacing={3}>
        {modules?.map((module) => (
          <Grid item xs={12} md={6} key={module.id}>
            <Card>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="center">
                  <Typography variant="h6" gutterBottom>
                    {module.module}
                  </Typography>
                  <IconButton>
                    <Settings />
                  </IconButton>
                </Box>

                <Box display="flex" alignItems="center" gap={2} mb={2}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={module.actif}
                        onChange={() => handleModuleActivation(module)}
                      />
                    }
                    label={module.actif ? 'Activé' : 'Désactivé'}
                  />
                </Box>

                <Box display="flex" gap={1} flexWrap="wrap">
                  {module.roles_autorises?.map((role) => (
                    <Chip key={role} label={role} size="small" />
                  ))}
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export default ConfigurationModules;