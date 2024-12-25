import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useForm, Controller } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as yup from 'yup';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Grid,
  TextField,
  MenuItem,
  Button,
  Alert,
  Tooltip,
  IconButton,
  Typography,
  Box,
  DialogContentText
} from '@mui/material';
import { useMutation, useQueryClient, useQuery } from 'react-query';
import { creerMouvement, getProduit } from '../../services/inventaire';
import { LoadingButton } from '@mui/lab';
import { TypeMouvement } from '../../types/inventaire';
import { Info, Help } from '@mui/icons-material';

interface MouvementData {
  type_mouvement: TypeMouvement;
  quantite: number;
  reference_document: string;
  cout_unitaire?: number;
  notes?: string;
}

const schema = yup.object().shape({
  type_mouvement: yup.mixed<TypeMouvement>()
    .oneOf(Object.values(TypeMouvement))
    .required('Le type de mouvement est requis'),
  quantite: yup.number()
    .required('La quantité est requise')
    .positive('La quantité doit être positive')
    .test('stock-suffisant', 'Stock insuffisant pour cette sortie', function(value) {
      const { type_mouvement } = this.parent;
      const stock = this.options.context?.stock;
      if (type_mouvement === TypeMouvement.SORTIE && typeof stock === 'number') {
        return value <= stock;
      }
      return true;
    }),
  reference_document: yup.string()
    .required('La référence est requise')
    .min(3, 'La référence doit contenir au moins 3 caractères'),
  cout_unitaire: yup.number()
    .transform((value) => (isNaN(value) ? undefined : value))
    .positive('Le coût unitaire doit être positif')
    .optional(),
  notes: yup.string()
    .optional()
});

interface DialogueMouvementStockProps {
  open: boolean;
  onClose: () => void;
  productId: string | null;
}

const DialogueMouvementStock: React.FC<DialogueMouvementStockProps> = ({
  open,
  onClose,
  productId
}) => {
  const queryClient = useQueryClient();
  const { user } = useAuth();
  const [confirmOpen, setConfirmOpen] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  const { data: product } = useQuery(
    ['product', productId],
    () => productId ? getProduit(productId) : Promise.reject('No ID provided'),
    {
      enabled: !!productId
    }
  );

  const { control, handleSubmit, watch, formState: { errors, isValid }, reset } = useForm<MouvementData>({
    resolver: yupResolver(schema),
    context: { stock: product?.quantite_stock },
    mode: 'onChange',
    defaultValues: {
      type_mouvement: TypeMouvement.ENTREE,
      quantite: 0,
      reference_document: '',
      cout_unitaire: undefined,
      notes: ''
    }
  });

  const mutation = useMutation(creerMouvement, {
    onSuccess: () => {
      queryClient.invalidateQueries('stocks');
      queryClient.invalidateQueries('recent-movements');
      queryClient.invalidateQueries(['product', productId]);
      queryClient.invalidateQueries(['product-movements', productId]);
      reset();
      onClose();
    },
    onError: (error: Error) => {
      setSubmitError(error.message);
    }
  });

  const watchType = watch('type_mouvement');
  const watchQuantite = watch('quantite');

  const handleConfirm = (data: MouvementData) => {
    if (productId) {
      setSubmitError(null);
      if (!user?.id) {
        setSubmitError("Utilisateur non connecté");
        return;
      }
      
      mutation.mutate({
        produit_id: productId,
        responsable_id: user.id,
        ...data
      });
    }
  };

  const onSubmit = (data: MouvementData) => {
    if (data.type_mouvement === TypeMouvement.SORTIE && product) {
      setConfirmOpen(true);
    } else {
      handleConfirm(data);
    }
  };

  const handleCancel = () => {
    reset();
    onClose();
  };

  return (
    <>
      <Dialog 
        open={open} 
        onClose={handleCancel}
        maxWidth="sm" 
        fullWidth
        aria-labelledby="mouvement-dialog-title"
        aria-describedby="mouvement-dialog-description"
      >
        <form onSubmit={handleSubmit(onSubmit)}>
          <DialogTitle id="mouvement-dialog-title">
            Nouveau Mouvement de Stock
          </DialogTitle>
          
          <DialogContent>
            <DialogContentText id="mouvement-dialog-description" sx={{ mb: 3 }}>
              {product && (
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle1">
                    Produit: {product.code} - {product.nom}
                  </Typography>
                  <Typography variant="subtitle2">
                    Stock actuel: {product.quantite_stock ?? 0} {product.unite_mesure}
                  </Typography>
                </Box>
              )}
            </DialogContentText>

            {submitError && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {submitError}
              </Alert>
            )}

            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Controller
                  name="type_mouvement"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      select
                      label="Type de Mouvement"
                      fullWidth
                      error={!!errors.type_mouvement}
                      helperText={errors.type_mouvement?.message}
                      InputProps={{
                        endAdornment: (
                          <Tooltip title="Choisissez le type d'opération à effectuer">
                            <IconButton size="small" sx={{ mr: 1 }}>
                              <Help fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Type de mouvement',
                        'aria-describedby': 'type-mouvement-helper'
                      }}
                    >
                      <MenuItem value={TypeMouvement.ENTREE}>Entrée</MenuItem>
                      <MenuItem value={TypeMouvement.SORTIE}>Sortie</MenuItem>
                      <MenuItem value={TypeMouvement.TRANSFERT}>Transfert</MenuItem>
                    </TextField>
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="quantite"
                  control={control}
                  render={({ field: { onChange, value, ...field } }) => (
                    <TextField
                      {...field}
                      label="Quantité"
                      type="number"
                      fullWidth
                      value={value}
                      onChange={(e) => onChange(Number(e.target.value))}
                      error={!!errors.quantite}
                      helperText={errors.quantite?.message}
                      InputProps={{
                        endAdornment: product && (
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            {product.unite_mesure}
                          </Typography>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Quantité',
                        'aria-describedby': 'quantite-helper',
                        min: 0,
                        step: 0.01
                      }}
                    />
                  )}
                />
                {watchType === TypeMouvement.SORTIE && product && (
                  <Typography variant="caption" color="textSecondary">
                    Stock disponible: {product.quantite_stock ?? 0} {product.unite_mesure}
                  </Typography>
                )}
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="cout_unitaire"
                  control={control}
                  render={({ field: { onChange, value, ...field } }) => (
                    <TextField
                      {...field}
                      label="Coût Unitaire"
                      type="number"
                      fullWidth
                      value={value ?? ''}
                      onChange={(e) => onChange(e.target.value ? Number(e.target.value) : undefined)}
                      error={!!errors.cout_unitaire}
                      helperText={errors.cout_unitaire?.message}
                      InputProps={{
                        endAdornment: (
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            XAF
                          </Typography>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Coût unitaire',
                        'aria-describedby': 'cout-unitaire-helper',
                        min: 0,
                        step: 0.01
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="reference_document"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Référence"
                      fullWidth
                      error={!!errors.reference_document}
                      helperText={errors.reference_document?.message}
                      InputProps={{
                        endAdornment: (
                          <Tooltip title="Numéro du document justificatif (bon de commande, facture, etc.)">
                            <IconButton size="small" sx={{ mr: 1 }}>
                              <Info fontSize="small" />
                            </IconButton>
                          </Tooltip>
                        )
                      }}
                      inputProps={{
                        'aria-label': 'Référence du document',
                        'aria-describedby': 'reference-helper'
                      }}
                    />
                  )}
                />
              </Grid>

              <Grid item xs={12}>
                <Controller
                  name="notes"
                  control={control}
                  render={({ field }) => (
                    <TextField
                      {...field}
                      label="Notes"
                      fullWidth
                      multiline
                      rows={3}
                      error={!!errors.notes}
                      helperText={errors.notes?.message}
                      inputProps={{
                        'aria-label': 'Notes additionnelles',
                        'aria-describedby': 'notes-helper'
                      }}
                    />
                  )}
                />
              </Grid>
            </Grid>
          </DialogContent>

          <DialogActions>
            <Button 
              onClick={handleCancel}
              aria-label="Annuler le mouvement"
            >
              Annuler
            </Button>
            <LoadingButton
              variant="contained"
              type="submit"
              loading={mutation.isLoading}
              disabled={!isValid}
              aria-label="Enregistrer le mouvement"
            >
              Enregistrer
            </LoadingButton>
          </DialogActions>
        </form>
      </Dialog>

      <Dialog
        open={confirmOpen}
        onClose={() => setConfirmOpen(false)}
        aria-labelledby="confirm-dialog-title"
      >
        <DialogTitle id="confirm-dialog-title">
          Confirmer la sortie de stock
        </DialogTitle>
        <DialogContent>
          <DialogContentText>
            Voulez-vous vraiment effectuer une sortie de {watchQuantite} {product?.unite_mesure} ?
            {product && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2">
                  Stock actuel: {product.quantite_stock ?? 0} {product.unite_mesure}
                </Typography>
                <Typography variant="body2">
                  Stock après opération: {(product.quantite_stock ?? 0) - (watchQuantite || 0)} {product.unite_mesure}
                </Typography>
              </Box>
            )}
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setConfirmOpen(false)}
            aria-label="Annuler la confirmation"
          >
            Annuler
          </Button>
          <Button
            onClick={handleSubmit(handleConfirm)}
            variant="contained"
            color="primary"
            aria-label="Confirmer la sortie"
          >
            Confirmer
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default DialogueMouvementStock;
