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
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createEmployee, updateEmployee, getEmployee, Employee } from '../../services/hr';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

type EmployeeFormData = Omit<Employee, 'id'>;

const schema = yup.object({
  matricule: yup.string().required('Le matricule est requis'),
  nom: yup.string().required('Le nom est requis'),
  prenom: yup.string().required('Le prénom est requis'),
  date_naissance: yup.string().required('La date de naissance est requise'),
  sexe: yup.string().oneOf(['M', 'F']).required('Le sexe est requis'),
  email: yup.string().email('Email invalide').required('L\'email est requis'),
  telephone: yup.string().required('Le téléphone est requis'),
  departement: yup.string().required('Le département est requis'),
  poste: yup.string().required('Le poste est requis'),
  date_embauche: yup.string().required('La date d\'embauche est requise'),
  type_contrat: yup.string()
    .oneOf(['CDI', 'CDD', 'STAGE', 'TEMPORAIRE'])
    .required('Le type de contrat est requis'),
  salaire_base: yup.number()
    .required('Le salaire est requis')
    .positive('Le salaire doit être positif'),
  statut: yup.string()
    .oneOf(['ACTIF', 'CONGE', 'FORMATION', 'INACTIF'])
    .default('ACTIF')
}).required();

const EmployeeForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: employee, isLoading: isLoadingEmployee } = useQuery({
    queryKey: ['employees', id],
    queryFn: () => getEmployee(id!),
    enabled: isEdit
  });

  const defaultValues: EmployeeFormData = {
    matricule: '',
    nom: '',
    prenom: '',
    date_naissance: new Date().toISOString(),
    sexe: 'M',
    email: '',
    telephone: '',
    departement: '',
    poste: '',
    date_embauche: new Date().toISOString(),
    type_contrat: 'CDI',
    salaire_base: 0,
    statut: 'ACTIF'
  };

  const { control, handleSubmit, formState: { errors } } = useForm<EmployeeFormData>({
    resolver: yupResolver(schema),
    defaultValues: employee || defaultValues
  });

  const mutation = useMutation(
    {
      mutationFn: (data: EmployeeFormData) => {
        const employeeData = {
          ...data,
          date_naissance: new Date(data.date_naissance).toISOString(),
          date_embauche: new Date(data.date_embauche).toISOString()
        };
        return isEdit ? updateEmployee(id!, employeeData) : createEmployee(employeeData);
      },
      onSuccess: () => {
        queryClient.invalidateQueries({ queryKey: ['employees'] });
        navigate('/hr');
      }
    }
  );

  const onSubmit = (data: EmployeeFormData) => {
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
          {mutation.error instanceof Error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {mutation.error.message || 'Une erreur est survenue'}
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
                      <MenuItem value="ACTIF">Actif</MenuItem>
                      <MenuItem value="CONGE">En congé</MenuItem>
                      <MenuItem value="FORMATION">En formation</MenuItem>
                      <MenuItem value="INACTIF">Inactif</MenuItem>
                    </TextField>
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
                    loading={mutation.isloading}
                  
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
