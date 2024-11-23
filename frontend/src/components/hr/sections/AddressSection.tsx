import React from 'react';
import { Grid, TextField } from '@mui/material';
import { Controller } from 'react-hook-form';
import { FormSectionProps } from '../types/formTypes';

/**
 * Composant de gestion de l'adresse dans le formulaire employé
 * Intégré avec react-hook-form pour la gestion du formulaire
 * Utilise les validations définies dans employeeSchema
 */
export const AddressSection: React.FC<FormSectionProps> = ({ control, errors }) => {
  return (
    <Grid container spacing={3}>
      {/* Rue */}
      <Grid item xs={12}>
        <Controller
          name="adresse.rue"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              label="Rue"
              fullWidth
              error={!!errors.adresse?.rue}
              helperText={errors.adresse?.rue?.message}
              placeholder="Entrez l'adresse complète"
            />
          )}
        />
      </Grid>

      {/* Ville */}
      <Grid item xs={12} md={6}>
        <Controller
          name="adresse.ville"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              label="Ville"
              fullWidth
              error={!!errors.adresse?.ville}
              helperText={errors.adresse?.ville?.message}
              placeholder="Entrez la ville"
            />
          )}
        />
      </Grid>

      {/* Code Postal */}
      <Grid item xs={12} md={6}>
        <Controller
          name="adresse.codePostal"
          control={control}
          defaultValue=""
          render={({ field }) => (
            <TextField
              {...field}
              label="Code Postal"
              fullWidth
              error={!!errors.adresse?.codePostal}
              helperText={errors.adresse?.codePostal?.message}
              placeholder="Ex: 75001"
            />
          )}
        />
      </Grid>

      {/* Pays */}
      <Grid item xs={12}>
        <Controller
          name="adresse.pays"
          control={control}
          defaultValue="Cameroun"
          render={({ field }) => (
            <TextField
              {...field}
              label="Pays"
              fullWidth
              error={!!errors.adresse?.pays}
              helperText={errors.adresse?.pays?.message}
            />
          )}
        />
      </Grid>
    </Grid>
  );
};
