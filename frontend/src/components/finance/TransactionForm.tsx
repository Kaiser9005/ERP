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
import { DateTimePicker } from '@mui/x-date-pickers';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { createTransaction, updateTransaction, getTransaction, getComptes } from '../../services/finance';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  reference: yup.string().required('La référence est requise'),
  date_transaction: yup.date().required('La date est requise'),
  type_transaction: yup.string().required('Le type est requis'),
  categorie: yup.string().required('La catégorie est requise'),
  montant: yup.number()
    .required('Le montant est requis')
    .positive('Le montant doit être positif'),
  description: yup.string(),
  compte_source_id: yup.string().when('type_transaction', {
    is: (val: string) => val === 'DEPENSE' || val === 'VIREMENT',
    then: yup.string().required('Le compte source est requis')
  }),
  compte_destination_id: yup.string().when('type_transaction', {
    is: (val: string) => val === 'RECETTE' || val === 'VIREMENT',
    then: yup.string().required('Le compte destination est requis')
  })
}).required();

const TransactionForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: transaction, isLoading: isLoadingTransaction } = useQuery(
    ['transaction', id],
    () => getTransaction(id!),
    { enabled: isEdit }
  );

  const { data: comptes } = useQuery('comptes', getComptes);

  const { control, handleSubmit, watch, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: transaction || {
      reference: '',
      date_transaction: new Date(),
      type_transaction: '',
      categorie: '',
      montant: '',
      description: '',
      compte_source_id: '',
      compte_destination_id: ''
    }
  });

  const typeTransaction = watch('type_transaction');

  const mutation = useMutation(
    (data: any) => isEdit ? updateTransaction(id!, data) : createTransaction(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('transactions');
        navigate('/finance');
      }
    }
  );

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingTransaction) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier la Transaction' : 'Nouvelle Transaction'}
        subtitle={isEdit ? `Modification de ${transaction?.reference}` : 'Création d\'une nouvelle transaction'}
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
                  name="reference"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Référence"
                      fullWidth
                      error={!!errors.reference}
                      helperText={errors.reference?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="date_transaction"
                  control={control}
                  render={({ field }) => (
                    <DateTimePicker
                      {...field}
                      label="Date de Transaction"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date_transaction,
                          helperText: errors.date_transaction?.message
                        }
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="type_transaction"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Type de Transaction"
                      fullWidth
                      error={!!errors.type_transaction}
                      helperText={errors.type_transaction?.message}
                    >
                      <MenuItem value="RECETTE">Recette</MenuItem>
                      <MenuItem value="DEPENSE">Dépense</MenuItem>
                      <MenuItem value="VIREMENT">Virement</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="categorie"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Catégorie"
                      fullWidth
                      error={!!errors.categorie}
                      helperText={errors.categorie?.message}
                    >
                      <MenuItem value="VENTE">Vente</MenuItem>
                      <MenuItem value="ACHAT_INTRANT">Achat d'intrants</MenuItem>
                      <MenuItem value="SALAIRE">Salaire</MenuItem>
                      <MenuItem value="MAINTENANCE">Maintenance</MenuItem>
                      <MenuItem value="TRANSPORT">Transport</MenuItem>
                      <MenuItem value="AUTRE">Autre</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="montant"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Montant"
                      type="number"
                      fullWidth
                      error={!!errors.montant}
                      helperText={errors.montant?.message}
                    />
                  )}
                />
              </Grid>

              {(typeTransaction === 'DEPENSE' || typeTransaction === 'VIREMENT') && (
                <Grid item xs={12} md={6}>
                  <Controller
                    name="compte_source_id"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Compte Source"
                        fullWidth
                        error={!!errors.compte_source_id}
                        helperText={errors.compte_source_id?.message}
                      >
                        {comptes?.map((compte) => (
                          <MenuItem key={compte.id} value={compte.id}>
                            {compte.libelle}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
              )}

              {(typeTransaction === 'RECETTE' || typeTransaction === 'VIREMENT') && (
                <Grid item xs={12} md={6}>
                  <Controller
                    name="compte_destination_id"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Compte Destination"
                        fullWidth
                        error={!!errors.compte_destination_id}
                        helperText={errors.compte_destination_id?.message}
                      >
                        {comptes?.map((compte) => (
                          <MenuItem key={compte.id} value={compte.id}>
                            {compte.libelle}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
              )}

              <Grid item xs={12}>
                <Controller
                  name="description"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Description"
                      multiline
                      rows={4}
                      fullWidth
                      error={!!errors.description}
                      helperText={errors.description?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate('/finance')}
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

export default TransactionForm;