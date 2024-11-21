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
import { creerTransaction, modifierTransaction, getTransaction, getComptes, Transaction, TypeTransaction, StatutTransaction, Compte } from '../../services/finance';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

interface FormData extends Omit<Transaction, 'id' | 'date'> {
  date: Date;
  compte_source_id?: string;
  compte_destination_id?: string;
}

const schema = yup.object({
  reference: yup.string().required('La référence est requise'),
  date: yup.date().required('La date est requise'),
  type: yup.string().oneOf(['ENTREE', 'SORTIE'], 'Type invalide').required('Le type est requis'),
  montant: yup.number()
    .required('Le montant est requis')
    .positive('Le montant doit être positif'),
  description: yup.string(),
  compte_source_id: yup.string().when('type', {
    is: (val: string) => val === 'SORTIE',
    then: (schema) => schema.required('Le compte source est requis')
  }),
  compte_destination_id: yup.string().when('type', {
    is: (val: string) => val === 'ENTREE',
    then: (schema) => schema.required('Le compte destination est requis')
  })
}).required();

const FormulaireTransaction: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const estModification = Boolean(id);

  const { data: transaction, isLoading: chargementTransaction } = useQuery(
    ['transaction', id],
    () => getTransaction(id!),
    { 
      enabled: estModification,
      select: (data) => ({
        ...data,
        date: new Date(data.date)
      })
    }
  );

  const { data: comptes = [] } = useQuery<Compte[]>('comptes', getComptes);

  const { control, handleSubmit, watch, formState: { errors } } = useForm<FormData>({
    resolver: yupResolver(schema) as any,
    defaultValues: transaction || {
      reference: '',
      date: new Date(),
      type: undefined,
      montant: 0,
      description: '',
      compte_source_id: '',
      compte_destination_id: '',
      statut: 'EN_ATTENTE' as StatutTransaction
    }
  });

  const typeTransaction = watch('type');

  const mutation = useMutation(
    (data: FormData) => {
      const transactionData: Omit<Transaction, 'id'> = {
        ...data,
        date: data.date.toISOString()
      };
      return estModification 
        ? modifierTransaction(id!, transactionData)
        : creerTransaction(transactionData);
    },
    {
      onSuccess: () => {
        queryClient.invalidateQueries('transactions');
        navigate('/finance');
      }
    }
  );

  const onSubmit = (data: FormData) => {
    mutation.mutate(data);
  };

  if (estModification && chargementTransaction) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={estModification ? 'Modifier la Transaction' : 'Nouvelle Transaction'}
        subtitle={estModification ? `Modification de ${transaction?.reference}` : 'Création d\'une nouvelle transaction'}
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
                  name="date"
                  control={control}
                  render={({ field }) => (
                    <DateTimePicker
                      {...field}
                      label="Date de Transaction"
                      slotProps={{
                        textField: {
                          fullWidth: true,
                          error: !!errors.date,
                          helperText: errors.date?.message
                        }
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="type"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Type de Transaction"
                      fullWidth
                      error={!!errors.type}
                      helperText={errors.type?.message}
                    >
                      <MenuItem value="ENTREE">Entrée</MenuItem>
                      <MenuItem value="SORTIE">Sortie</MenuItem>
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

              {typeTransaction === 'SORTIE' && (
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
                        {comptes.map((compte) => (
                          <MenuItem key={compte.id} value={compte.id}>
                            {compte.libelle}
                          </MenuItem>
                        ))}
                      </TextField>
                    )}
                  />
                </Grid>
              )}

              {typeTransaction === 'ENTREE' && (
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
                        {comptes.map((compte) => (
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
                    {estModification ? 'Modifier' : 'Créer'}
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

export default FormulaireTransaction;
