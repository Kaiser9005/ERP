import React from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { createMouvement } from '../../services/inventaire';
import { CreateMouvementStock } from '../../types/inventaire';

interface DialogueMouvementStockProps {
  open: boolean;
  onClose: () => void;
  productId: string | null;
}

export const DialogueMouvementStock: React.FC<DialogueMouvementStockProps> = ({
  open,
  onClose,
  productId
}) => {
  const queryClient = useQueryClient();
  const { control, handleSubmit, reset } = useForm<CreateMouvementStock>();

  const mutation = useMutation({
    mutationFn: createMouvement,
    onSuccess: () => {
      queryClient.invalidateQueries(['mouvements', productId]);
      queryClient.invalidateQueries(['produit', productId]);
      onClose();
      reset();
    }
  });

  const onSubmit = (data: Partial<CreateMouvementStock>) => {
    if (!productId) return;
    
    mutation.mutate({
      ...data,
      produit_id: productId,
      quantite: data.quantite || 0,
      type_mouvement: data.type_mouvement || 'ENTREE'
    } as CreateMouvementStock);
  };

  return (
    <Dialog open={open} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Nouveau Mouvement de Stock</DialogTitle>
      <form onSubmit={handleSubmit(onSubmit)}>
        <DialogContent>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel>Type de Mouvement</InputLabel>
                <Controller
                  name="type_mouvement"
                  control={control}
                  defaultValue="ENTREE"
                  render={({ field }) => (
                    <Select {...field} label="Type de Mouvement">
                      <MenuItem value="ENTREE">Entrée</MenuItem>
                      <MenuItem value="SORTIE">Sortie</MenuItem>
                      <MenuItem value="TRANSFERT">Transfert</MenuItem>
                    </Select>
                  )}
                />
              </FormControl>
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="quantite"
                control={control}
                defaultValue={0}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Quantité"
                    type="number"
                    fullWidth
                    inputProps={{ min: 0, step: 0.01 }}
                  />
                )}
              />
            </Grid>

            <Grid item xs={12}>
              <Controller
                name="cout_unitaire"
                control={control}
                render={({ field }) => (
                  <TextField
                    {...field}
                    label="Coût Unitaire"
                    type="number"
                    fullWidth
                    inputProps={{ min: 0, step: 0.01 }}
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
                    label="Référence Document"
                    fullWidth
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
                    multiline
                    rows={3}
                    fullWidth
                  />
                )}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={onClose}>Annuler</Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={mutation.isLoading}
          >
            {mutation.isLoading ? 'Enregistrement...' : 'Enregistrer'}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default DialogueMouvementStock;
