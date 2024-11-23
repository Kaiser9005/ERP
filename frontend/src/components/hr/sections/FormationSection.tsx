import React from 'react';
import { Grid, TextField, IconButton, Box, Chip } from '@mui/material';
import { Controller, useFieldArray } from 'react-hook-form';
import { FormSectionProps } from '../types/formTypes';
import { Add as AddIcon } from '@mui/icons-material';

export const FormationSection: React.FC<FormSectionProps> = ({ control, errors }) => {
  const { fields: diplomeFields, append: appendDiplome, remove: removeDiplome } = useFieldArray({
    control,
    name: 'formation.diplomes' as any
  });

  const { fields: certificationFields, append: appendCertification, remove: removeCertification } = useFieldArray({
    control,
    name: 'formation.certifications' as any
  });

  return (
    <Grid container spacing={3}>
      <Grid item xs={12}>
        <Controller
          name="formation.niveau"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Niveau d'études"
              fullWidth
              error={!!errors.formation?.niveau}
              helperText={errors.formation?.niveau?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12}>
        <Box>
          <Box display="flex" alignItems="center" mb={1}>
            <Box flexGrow={1}>Diplômes</Box>
            <IconButton 
              size="small" 
              onClick={() => appendDiplome('')}
              color="primary"
            >
              <AddIcon />
            </IconButton>
          </Box>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {diplomeFields.map((field, index) => (
              <Controller
                key={field.id}
                name={`formation.diplomes.${index}` as const}
                control={control}
                render={({ field: { value, onChange } }) => (
                  <Chip
                    label={value || 'Nouveau diplôme'}
                    onDelete={() => removeDiplome(index)}
                    onClick={() => {
                      const newValue = window.prompt('Modifier le diplôme', value);
                      if (newValue) onChange(newValue);
                    }}
                  />
                )}
              />
            ))}
          </Box>
        </Box>
      </Grid>

      <Grid item xs={12}>
        <Box>
          <Box display="flex" alignItems="center" mb={1}>
            <Box flexGrow={1}>Certifications</Box>
            <IconButton 
              size="small" 
              onClick={() => appendCertification('')}
              color="primary"
            >
              <AddIcon />
            </IconButton>
          </Box>
          <Box display="flex" flexWrap="wrap" gap={1}>
            {certificationFields.map((field, index) => (
              <Controller
                key={field.id}
                name={`formation.certifications.${index}` as const}
                control={control}
                render={({ field: { value, onChange } }) => (
                  <Chip
                    label={value || 'Nouvelle certification'}
                    onDelete={() => removeCertification(index)}
                    onClick={() => {
                      const newValue = window.prompt('Modifier la certification', value);
                      if (newValue) onChange(newValue);
                    }}
                  />
                )}
              />
            ))}
          </Box>
        </Box>
      </Grid>
    </Grid>
  );
};
