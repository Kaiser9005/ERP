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
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { createTransaction, updateTransaction, getTransaction, getComptes } from '../../services/finance';
import { TypeTransaction, StatutTransaction, Compte, Transaction } from '../../types/finance';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

interface TransactionFormData {
  reference: string;
  date_transaction: string;
  type_transaction: TypeTransaction;
  categorie: string;
  montant: number;
  description?: string;
  compte_source?: string;
  compte_destination?: string;
  statut: StatutTransaction;
  fichierJustificatif?: File;
}

const schema = yup.object().shape({
  reference: yup.string().required('La référence est requise'),
  date_transaction: yup.string().required('La date est requise'),
  type_transaction: yup.mixed<TypeTransaction>()
    .oneOf(Object.values(TypeTransaction))
    .required('Le type est requis'),
  categorie: yup.string().required('La catégorie est requise'),
  montant: yup.number()
    .required('Le montant est requis')
    .positive('Le montant doit être positif'),
  description: yup.string().optional(),
  compte_source: yup.string()
    .test('compte-source-required', 'Le compte source est requis', function(value) {
      const type = this.parent.type_transaction;
      if (type === TypeTransaction.DEPENSE || type === TypeTransaction.VIREMENT) {
        return !!value;
      }
      return true;
    }),
  compte_destination: yup.string()
    .test('compte-destination-required', 'Le compte destination est requis', function(value) {
      const type = this.parent.type_transaction;
      if (type === TypeTransaction.RECETTE || type === TypeTransaction.VIREMENT) {
        return !!value;
      }
      return true;
    }),
  statut: yup.mixed<StatutTransaction>()
    .oneOf(Object.values(StatutTransaction))
    .default(StatutTransaction.BROUILLON)
});

const TransactionForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: transaction, isLoading: isLoadingTransaction } = useQuery({
    queryKey: ['transactions', id],
    queryFn: () => getTransaction(id!),
    enabled: isEdit
  });

  const { data: comptes = [] } = useQuery<Compte[]>({
    queryKey: ['comptes'],
    queryFn: getComptes,
    initialData: []
  });

  const defaultValues: TransactionFormData = {
    reference: '',
    date_transaction: new Date().toISOString(),
    type_transaction: TypeTransaction.RECETTE,
    categorie: '',
    montant: 0,
    description: '',
    compte_source: '',
    compte_destination: '',
    statut: StatutTransaction.BROUILLON
  };

  const { control, handleSubmit, watch, formState: { errors } } = useForm<TransactionFormData>({
    resolver: yupResolver(schema),
    defaultValues: transaction || defaultValues
  });

  const typeTransaction = watch('type_transaction');

  const mutation = useMutation<Transaction, Error, TransactionFormData>({
    mutationFn: (data: TransactionFormData) => {
      const transactionData: TransactionFormData = {
        date_transaction: new Date(data.date_transaction).toISOString(),
        montant: data.montant,
        type_transaction: data.type_transaction,
        categorie: data.categorie,
        description: data.description,
        reference: data.reference,
        compte_source: data.compte_source,
        compte_destination: data.compte_destination,
        statut: data.statut || StatutTransaction.BROUILLON,
        fichierJustificatif: data.fichierJustificatif
      };
      return isEdit ? updateTransaction(id!, transactionData) : createTransaction(transactionData);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['transactions'] });
      navigate('/finance');
    }
  });

  const onSubmit = (data: TransactionFormData) => {
    const formData = {
      ...data,
      statut: data.statut || 'BROUILLON'
    };
    mutation.mutate(formData);
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
                    name="compte_source"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Compte Source"
                        fullWidth
                        error={!!errors.compte_source}
                        helperText={errors.compte_source?.message}
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

              {(typeTransaction === 'RECETTE' || typeTransaction === 'VIREMENT') && (
                <Grid item xs={12} md={6}>
                  <Controller
                    name="compte_destination"
                    control={control}
                    render={({ field }) => (
                      <TextField
                        {...field}
                        select
                        label="Compte Destination"
                        fullWidth
                        error={!!errors.compte_destination}
                        helperText={errors.compte_destination?.message}
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
                    loading={mutation.isPending}
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
