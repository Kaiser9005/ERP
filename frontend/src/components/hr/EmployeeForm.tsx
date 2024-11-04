import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Card,
  CardContent,
  Grid,
  TextField,
  MenuItem,
  Button,
  Box,
  Alert
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { createEmployee, updateEmployee, getEmployee } from '../../services/hr';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  matricule: yup.string().required('Le matricule est requis'),
  nom: yup.string().required('Le nom est requis'),
  prenom: yup.string().required('Le prénom est requis'),
  date_naissance: yup.date().required('La date de naissance est requise'),
  sexe: yup.string().required('Le sexe est requis'),
  departement: yup.string().required('Le département est requis'),
  poste: yup.string().required('Le poste est requis'),
  date_embauche: yup.date().required('La date d\'embauche est requise'),
  type_contrat: yup.string().required('Le type de contrat est requis'),
  salaire_base: yup.number()
    .required('Le salaire est requis')
    .positive('Le salaire doit être positif')
}).required();

const EmployeeForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: employee, isLoading: isLoadingEmployee } = useQuery(
    ['employee', id],
    () => getEmployee(id!),
    { enabled: isEdit }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: employee || {
      matricule: '',
      nom: '',
      prenom: '',
      date_naissance: null,
      sexe: '',
      departement: '',
      poste: '',
      date_embauche: null,
      type_contrat: '',
      salaire_base: ''
    }
  });

  const mutation = useMutation(
    (data: any) => isEdit ? updateEmployee(id!, data) : createEmployee(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('employees');
        navigate('/hr');
      }
    }
  );

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingEmployee) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier l\'Employé' : 'Nouvel Employé'}
        subtitle={isEdit ? `Modification de ${employee?.prenom} ${employee?.nom}` : 'Création d\'un nouvel employé'}
      />

      <Card>
        <CardContent>
          {mutation.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Une erreur est survenue
            </Alert>
          )}

          <form onSubmit={handleSubmit(onSubmit)}>
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
                  name="date_naissance"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      {...field}
                      label="Date de Naissance"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date_naissance,
                          helperText: errors.date_naissance?.message
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
                      <MenuItem value="PRODUCTION">Production</MenuItem>
                      <MenuItem value="MAINTENANCE">Maintenance</MenuItem>
                      <MenuItem value="ADMINISTRATION">Administration</MenuItem>
                      <MenuItem value="FINANCE">Finance</MenuItem>
                      <MenuItem value="LOGISTIQUE">Logistique</MenuItem>
                      <MenuItem value="QUALITE">Qualité</MenuItem>
                      <MenuItem value="RH">RH</MenuItem>
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
                  name="date_embauche"
                  control={control}
                  render={({ field }) => (
                    <DatePicker
                      {...field}
                      label="Date d'Embauche"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date_embauche,
                          helperText: errors.date_embauche?.message
                        }
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="type_contrat"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Type de Contrat"
                      fullWidth
                      error={!!errors.type_contrat}
                      helperText={errors.type_contrat?.message}
                    >
                      <MenuItem value="CDI">CDI</MenuItem>
                      <MenuItem value="CDD">CDD</MenuItem>
                      <MenuItem value="STAGE">Stage</MenuItem>
                      <MenuItem value="TEMPORAIRE">Temporaire</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="salaire_base"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Salaire de Base"
                      type="number"
                      fullWidth
                      error={!!errors.salaire_base}
                      helperText={errors.salaire_base?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate('/hr')}
                  >
                    Annuler
                  </Button>
                  <LoadingButton
                    variant="contained"
                    type="submit"
                    loading={mutation.isLoading}
                  >
                    {isEdit ? 'Modifier' : 'Créer'}
                  </LoadingButton>
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>
    </>
  );
};

export default EmployeeForm;