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
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { createProduct, updateProduct, getProduct } from '../../services/inventory';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';

const schema = yup.object({
  code: yup.string().required('Le code est requis'),
  nom: yup.string().required('Le nom est requis'),
  categorie: yup.string().required('La catégorie est requise'),
  description: yup.string(),
  unite_mesure: yup.string().required('L\'unité de mesure est requise'),
  seuil_alerte: yup.number()
    .positive('Le seuil doit être positif')
    .required('Le seuil d\'alerte est requis'),
  prix_unitaire: yup.number()
    .positive('Le prix doit être positif')
    .required('Le prix unitaire est requis'),
  specifications: yup.object()
}).required();

const ProductForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: product, isLoading: isLoadingProduct } = useQuery(
    ['product', id],
    () => getProduct(id!),
    { enabled: isEdit }
  );

  const { control, handleSubmit, formState: { errors } } = useForm({
    resolver: yupResolver(schema),
    defaultValues: product || {
      code: '',
      nom: '',
      categorie: '',
      description: '',
      unite_mesure: '',
      seuil_alerte: '',
      prix_unitaire: '',
      specifications: {}
    }
  });

  const mutation = useMutation(
    (data: any) => isEdit ? updateProduct(id!, data) : createProduct(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('products');
        navigate('/inventory');
      }
    }
  );

  const onSubmit = (data: any) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingProduct) {
    return <div>Chargement...</div>;
  }

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier le Produit' : 'Nouveau Produit'}
        subtitle={isEdit ? `Modification de ${product?.nom}` : 'Création d\'un nouveau produit'}
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
                  name="code"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Code"
                      fullWidth
                      error={!!errors.code}
                      helperText={errors.code?.message}
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
                      <MenuItem value="INTRANT">Intrant</MenuItem>
                      <MenuItem value="EQUIPEMENT">Équipement</MenuItem>
                      <MenuItem value="RECOLTE">Récolte</MenuItem>
                      <MenuItem value="EMBALLAGE">Emballage</MenuItem>
                      <MenuItem value="PIECE_RECHANGE">Pièce de rechange</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="unite_mesure"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Unité de Mesure"
                      fullWidth
                      error={!!errors.unite_mesure}
                      helperText={errors.unite_mesure?.message}
                    >
                      <MenuItem value="KG">Kilogramme</MenuItem>
                      <MenuItem value="LITRE">Litre</MenuItem>
                      <MenuItem value="UNITE">Unité</MenuItem>
                      <MenuItem value="TONNE">Tonne</MenuItem>
                      <MenuItem value="METRE">Mètre</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

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

              <Grid item xs={12} md={6}>
                <Controller
                  name="seuil_alerte"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Seuil d'Alerte"
                      type="number"
                      fullWidth
                      error={!!errors.seuil_alerte}
                      helperText={errors.seuil_alerte?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="prix_unitaire"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Prix Unitaire"
                      type="number"
                      fullWidth
                      error={!!errors.prix_unitaire}
                      helperText={errors.prix_unitaire?.message}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={() => navigate('/inventory')}
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

export default ProductForm;