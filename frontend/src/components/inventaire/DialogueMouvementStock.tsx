import React from 'react';
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
  Button
} from '@mui/material';
import { useMutation, useQueryClient } from 'react-query';
import { creerMouvement } from '../../services/inventaire';
import { LoadingButton } from '@mui/lab';
import { TypeMouvement } from '../../types/inventaire';

interface MouvementData {
  type_mouvement: TypeMouvement;
  quantite: number;
  reference_document: string;
  cout_unitaire?: number;
  notes?: string;
}

const schema = yup.object({
  type_mouvement: yup.mixed<TypeMouvement>().oneOf(Object.values(TypeMouvement)).required('Le type de mouvement est requis'),
  quantite: yup.number()
    .required('La quantité est requise')
    .positive('La quantité doit être positive'),
  reference_document: yup.string().required('La référence est requise'),
  cout_unitaire: yup.number().positive('Le coût unitaire doit être positif'),
  notes: yup.string()
}).required();

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

  const { control, handleSubmit, formState: { errors } } = useForm<MouvementData>({
    resolver: yupResolver(schema),
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
      onClose();
    }
  });

  const onSubmit = (data: MouvementData) => {
    if (productId) {
      mutation.mutate({
        produit_id: productId,
        ...data
      });
    }
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogTitle>Nouveau Mouvement de Stock</DialogTitle>
        
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
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
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="cout_unitaire"
                control={control}
                render={({ field: { onChange, value, ...field } }) => (
                  <TextField
                    {...field}
                    label="Coût Unitaire (XAF)"
                    type="number"
                    fullWidth
                    value={value || ''}
                    onChange={(e) => onChange(e.target.value ? Number(e.target.value) : undefined)}
                    error={!!errors.cout_unitaire}
                    helperText={errors.cout_unitaire?.message}
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
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>

        <DialogActions>
          <Button onClick={onClose}>
            Annuler
          </Button>
          <LoadingButton
            variant="contained"
            type="submit"
            loading={mutation.isLoading}
          >
            Enregistrer
          </LoadingButton>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default DialogueMouvementStock;
