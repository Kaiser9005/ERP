import React from 'react';
import { Grid, TextField, MenuItem } from '@mui/material';
import { Controller } from 'react-hook-form';
import { DatePicker } from '@mui/x-date-pickers';
import { FormSectionProps } from '../types/formTypes';
import { DEPARTEMENTS, TYPES_CONTRAT, STATUTS } from '../constants/employeeConstants';

export const MainInfoSection: React.FC<FormSectionProps> = ({ control, errors }) => {
  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={6}>
        <Controller
          name="matricule"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Matricule"
              fullWidth
              error={!!errors.matricule}
              helperText={errors.matricule?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="nom"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Nom"
              fullWidth
              error={!!errors.nom}
              helperText={errors.nom?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="prenom"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Prénom"
              fullWidth
              error={!!errors.prenom}
              helperText={errors.prenom?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="dateNaissance"
          control={control}
          render={({ field }) => (
            <DatePicker
              label="Date de Naissance"
              value={field.value}
              onChange={field.onChange}
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: !!errors.dateNaissance,
                  helperText: errors.dateNaissance?.message
                }
              }}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="sexe"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              select
              label="Sexe"
              fullWidth
              error={!!errors.sexe}
              helperText={errors.sexe?.message}
            >
              <MenuItem value="M">Masculin</MenuItem>
              <MenuItem value="F">Féminin</MenuItem>
            </TextField>
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="email"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Email"
              type="email"
              fullWidth
              error={!!errors.email}
              helperText={errors.email?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="telephone"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Téléphone"
              fullWidth
              error={!!errors.telephone}
              helperText={errors.telephone?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="dateEmbauche"
          control={control}
          render={({ field }) => (
            <DatePicker
              label="Date d'Embauche"
              value={field.value}
              onChange={field.onChange}
              slotProps={{
                textField: {
                  fullWidth: true,
                  error: !!errors.dateEmbauche,
                  helperText: errors.dateEmbauche?.message
                }
              }}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="departement"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              select
              label="Département"
              fullWidth
              error={!!errors.departement}
              helperText={errors.departement?.message}
            >
              {DEPARTEMENTS.map((dept) => (
                <MenuItem key={dept} value={dept}>
                  {dept}
                </MenuItem>
              ))}
            </TextField>
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="poste"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Poste"
              fullWidth
              error={!!errors.poste}
              helperText={errors.poste?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="typeContrat"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              select
              label="Type de Contrat"
              fullWidth
              error={!!errors.typeContrat}
              helperText={errors.typeContrat?.message}
            >
              {TYPES_CONTRAT.map((type) => (
                <MenuItem key={type.value} value={type.value}>
                  {type.label}
                </MenuItem>
              ))}
            </TextField>
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="salaireBase"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              label="Salaire de Base"
              type="number"
              fullWidth
              error={!!errors.salaireBase}
              helperText={errors.salaireBase?.message}
            />
          )}
        />
      </Grid>

      <Grid item xs={12} md={6}>
        <Controller
          name="statut"
          control={control}
          render={({ field }) => (
            <TextField
              {...field}
              select
              label="Statut"
              fullWidth
              error={!!errors.statut}
              helperText={errors.statut?.message}
            >
              {STATUTS.map((statut) => (
                <MenuItem key={statut.value} value={statut.value}>
                  {statut.label}
                </MenuItem>
              ))}
            </TextField>
          )}
        />
      </Grid>
    </Grid>
  );
};
