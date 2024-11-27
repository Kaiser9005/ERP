import React, { useState } from 'react';
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
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
  Tooltip,
  IconButton,
  InputAdornment,
} from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from 'react-query';
import { creerProduit, modifierProduit, getProduit, verifierCodeUnique } from '../../services/inventaire';
import PageHeader from '../layout/PageHeader';
import { LoadingButton } from '@mui/lab';
import { Info, Help } from '@mui/icons-material';
import { CategoryProduit, UniteMesure } from '../../types/inventaire';

interface ProduitFormData {
  code: string;
  nom: string;
  categorie: CategoryProduit;
  description?: string;
  unite_mesure: UniteMesure;
  seuil_alerte: number;
  prix_unitaire: number;
  specifications?: Record<string, unknown>;
}

const schema = yup.object({
  code: yup.string()
    .required('Le code est requis')
    .min(3, 'Le code doit contenir au moins 3 caractères')
    .matches(/^[A-Z0-9-]+$/, 'Le code ne doit contenir que des majuscules, chiffres et tirets')
    .test('unique', 'Ce code existe déjà', async (value, context) => {
      if (!value) return true;
      const isEdit = context.options.context?.isEdit;
      const currentId = context.options.context?.currentId;
      if (isEdit && currentId) {
        const product = await getProduit(currentId);
        if (product.code === value) return true;
      }
      return await verifierCodeUnique(value);
    }),
  nom: yup.string()
    .required('Le nom est requis')
    .min(2, 'Le nom doit contenir au moins 2 caractères'),
  categorie: yup.mixed<CategoryProduit>()
    .oneOf(Object.values(CategoryProduit))
    .required('La catégorie est requise'),
  description: yup.string()
    .max(500, 'La description ne doit pas dépasser 500 caractères'),
  unite_mesure: yup.mixed<UniteMesure>()
    .oneOf(Object.values(UniteMesure))
    .required('L\'unité de mesure est requise'),
  seuil_alerte: yup.number()
    .required('Le seuil d\'alerte est requis')
    .positive('Le seuil doit être positif')
    .transform((value) => (isNaN(value) ? undefined : value)),
  prix_unitaire: yup.number()
    .required('Le prix unitaire est requis')
    .positive('Le prix doit être positif')
    .transform((value) => (isNaN(value) ? undefined : value)),
  specifications: yup.object().optional()
}).required();

const UNITES_MESURE = [
  { value: UniteMesure.KG, label: 'Kilogramme' },
  { value: UniteMesure.L, label: 'Litre' },
  { value: UniteMesure.UNITE, label: 'Unité' },
  { value: UniteMesure.CARTON, label: 'Carton' }
];

const FormulaireProduit: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [formData, setFormData] = useState<ProduitFormData | null>(null);

  const { data: product, isLoading: isLoadingProduct } = useQuery(
    ['product', id],
    () => getProduit(id!),
    { 
      enabled: isEdit,
      onSuccess: (data) => {
        reset(data);
      }
    }
  );

  const { control, handleSubmit, formState: { errors, isValid, isDirty }, reset, watch } = useForm<ProduitFormData>({
    resolver: yupResolver(schema),
    context: { isEdit, currentId: id },
    mode: 'onChange',
    defaultValues: {
      code: '',
      nom: '',
      categorie: CategoryProduit.INTRANT,
      description: '',
      unite_mesure: UniteMesure.KG,
      seuil_alerte: 0,
      prix_unitaire: 0,
      specifications: {}
    }
  });

  const mutation = useMutation(
    (data: ProduitFormData) => isEdit ? modifierProduit(id!, data) : creerProduit(data),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('products');
        navigate('/inventaire', {
          state: { 
            notification: {
              type: 'success',
              message: `Produit ${isEdit ? 'modifié' : 'créé'} avec succès`
            }
          }
        });
      },
      onError: (error: Error) => {
        setSubmitError(error.message);
      }
    }
  );

  const onSubmit = (data: ProduitFormData) => {
    if (isEdit && isDirty) {
      setFormData(data);
      setConfirmOpen(true);
    } else {
      handleConfirm(data);
    }
  };

  const handleConfirm = (data: ProduitFormData) => {
    setSubmitError(null);
    mutation.mutate(data);
  };

  const handleCancel = () => {
    if (isDirty) {
      setConfirmOpen(true);
    } else {
      navigate('/inventaire');
    }
  };

  if (isLoadingProduct) {
    return (
      <Box 
        display="flex" 
        justifyContent="center" 
        alignItems="center" 
        minHeight="200px"
        role="status"
        aria-label="Chargement des données du produit"
      >
        <Typography>Chargement...</Typography>
      </Box>
    );
  }

  const watchUniteMesure = watch('unite_mesure');

  return (
    <>
      <PageHeader
        title={isEdit ? 'Modifier le Produit' : 'Nouveau Produit'}
        subtitle={isEdit ? `Modification de ${product?.nom}` : 'Création d\'un nouveau produit'}
      />

      <Card>
        <CardContent>
          {submitError && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {submitError}
            </Alert>
          )}
         
          <form onSubmit={handleSubmit(onSubmit)} aria-label="Formulaire produit">
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
                      InputProps={{
                        endAdornment: (
                          <Tooltip title="Code unique du produit (majuscules, chiffres et tirets uniquement)">
                            <IconButton size="small" sx={{ mr: 1 }}>
                              <Help fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Code du produit',
                        'aria-describedby': 'code-helper'
                      }}
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
                      inputProps={{
                        'aria-label': 'Nom du produit',
                        'aria-describedby': 'nom-helper'
                      }}
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
                      InputProps={{
                        endAdornment: (
                          <Tooltip title="Type de produit">
                            <IconButton size="small" sx={{ mr: 1 }}>
                              <Info fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Catégorie du produit',
                        'aria-describedby': 'categorie-helper'
                      }}
                    >
                      {Object.entries(CategoryProduit).map(([key, value]) => (
                        <MenuItem key={key} value={value}>
                          {value}
                        </MenuItem>
                      ))}
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
                      InputProps={{
                        endAdornment: (
                          <Tooltip title="Unité de mesure pour le stock">
                            <IconButton size="small" sx={{ mr: 1 }}>
                              <Info fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Unité de mesure',
                        'aria-describedby': 'unite-mesure-helper'
                      }}
                    >
                      {UNITES_MESURE.map(({ value, label }) => (
                        <MenuItem key={value} value={value}>
                          {label}
                        </MenuItem>
                      ))}
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
                      inputProps={{
                        'aria-label': 'Description du produit',
                        'aria-describedby': 'description-helper',
                        maxLength: 500
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="seuil_alerte"
                  control={control}
                  render={({ field: { onChange, value, ...field } }) => (
                    <TextField
                      {...field}
                      label="Seuil d'Alerte"
                      type="number"
                      fullWidth
                      value={value}
                      onChange={(e) => onChange(Number(e.target.value))}
                      error={!!errors.seuil_alerte}
                      helperText={errors.seuil_alerte?.message}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            {watchUniteMesure && (
                              <Typography variant="caption">
                                {UNITES_MESURE.find(u => u.value === watchUniteMesure)?.label}
                              </Typography>
                            )}
                            <Tooltip title="Niveau de stock minimum avant alerte">
                              <IconButton size="small">
                                <Info fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </InputAdornment>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Seuil d\'alerte',
                        'aria-describedby': 'seuil-alerte-helper',
                        min: 0,
                        step: 0.01
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12} md={6}>
                <Controller
                  name="prix_unitaire"
                  control={control}
                  render={({ field: { onChange, value, ...field } }) => (
                    <TextField
                      {...field}
                      label="Prix Unitaire"
                      type="number"
                      fullWidth
                      value={value}
                      onChange={(e) => onChange(Number(e.target.value))}
                      error={!!errors.prix_unitaire}
                      helperText={errors.prix_unitaire?.message}
                      InputProps={{
                        endAdornment: (
                          <InputAdornment position="end">
                            <Typography variant="caption" sx={{ mr: 1 }}>
                              XAF
                            </Typography>
                            <Tooltip title="Prix unitaire en Francs CFA">
                              <IconButton size="small">
                                <Info fontSize="small" />
                              </IconButton>
                            </Tooltip>
                          </InputAdornment>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Prix unitaire',
                        'aria-describedby': 'prix-unitaire-helper',
                        min: 0,
                        step: 0.01
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
                  <Button
                    variant="outlined"
                    onClick={handleCancel}
                    aria-label="Annuler"
                  >
                    Annuler
                  </Button>
                  <LoadingButton
                    variant="contained"
                    type="submit"
                    loading={mutation.isLoading}
                    disabled={!isValid}
                    aria-label={isEdit ? 'Modifier le produit' : 'Créer le produit'}
                  >
                    {isEdit ? 'Modifier' : 'Créer'}
                  </LoadingButton>
                </Box>
              </Grid>
            </Grid>
          </form>
        </CardContent>
      </Card>

      <Dialog
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        aria-labelledby="confirm-dialog-title"
      >
        <DialogTitle id="confirm-dialog-title">
          Confirmer les modifications
        </DialogTitle>
        <DialogContent>
          <Typography>
            Voulez-vous vraiment {isEdit ? 'modifier' : 'quitter sans sauvegarder'} ce produit ?
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setConfirmOpen(false)}
            aria-label="Annuler la confirmation"
          >
            Annuler
          </Button>
          <Button
            onClick={() => {
              setConfirmOpen(false);
              if (formData) {
                handleConfirm(formData);
              } else {
                navigate('/inventaire');
              }
            }}
            variant="contained"
            color="primary"
            aria-label="Confirmer"
          >
            Confirmer
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default FormulaireProduit;
