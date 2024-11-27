import React from 'react';
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
    FormControl,
    FormHelperText,
    InputLabel,
    MenuItem,
    Select,
    TextField,
    Grid
} from '@mui/material';
import { useForm, Controller } from 'react-hook-form';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Formation, FormationCreate, FormationUpdate } from '../../../types/formation';
import { createFormation, updateFormation } from '../../../services/formation';

interface FormationFormProps {
    open: boolean;
    onClose: () => void;
    formation?: Formation;
}

export const FormationForm: React.FC<FormationFormProps> = ({
    open,
    onClose,
    formation
}) => {
    const queryClient = useQueryClient();
    const isEdit = !!formation;

    const { control, handleSubmit, formState: { errors }, reset } = useForm({
        defaultValues: {
            titre: formation?.titre || '',
            description: formation?.description || '',
            type: formation?.type || 'technique',
            duree: formation?.duree || 0,
            competences_requises: formation?.competences_requises || {},
            competences_acquises: formation?.competences_acquises || {},
            materiel_requis: formation?.materiel_requis || {},
            conditions_meteo: formation?.conditions_meteo || {}
        }
    });

    const createMutation = useMutation({
        mutationFn: (data: FormationCreate) => createFormation(data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['formations'] });
            onClose();
            reset();
        }
    });

    const updateMutation = useMutation({
        mutationFn: (data: FormationUpdate) => {
            if (!formation) throw new Error('Formation non trouvée');
            return updateFormation(formation.id, data);
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['formations'] });
            onClose();
        }
    });

    const onSubmit = async (data: FormationCreate) => {
        if (isEdit) {
            await updateMutation.mutateAsync(data);
        } else {
            await createMutation.mutateAsync(data);
        }
    };

    return (
        <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
            <DialogTitle>
                {isEdit ? 'Modifier la formation' : 'Nouvelle formation'}
            </DialogTitle>
            <form onSubmit={handleSubmit(onSubmit)}>
                <DialogContent>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <Controller
                                name="titre"
                                control={control}
                                rules={{ required: 'Le titre est requis' }}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Titre"
                                        fullWidth
                                        error={!!errors.titre}
                                        helperText={errors.titre?.message}
                                    />
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
                                        fullWidth
                                        multiline
                                        rows={3}
                                    />
                                )}
                            />
                        </Grid>

                        <Grid item xs={12} sm={6}>
                            <Controller
                                name="type"
                                control={control}
                                rules={{ required: 'Le type est requis' }}
                                render={({ field }) => (
                                    <FormControl fullWidth error={!!errors.type}>
                                        <InputLabel>Type</InputLabel>
                                        <Select {...field} label="Type">
                                            <MenuItem value="technique">Technique</MenuItem>
                                            <MenuItem value="securite">Sécurité</MenuItem>
                                            <MenuItem value="agricole">Agricole</MenuItem>
                                        </Select>
                                        {errors.type && (
                                            <FormHelperText>{errors.type.message}</FormHelperText>
                                        )}
                                    </FormControl>
                                )}
                            />
                        </Grid>

                        <Grid item xs={12} sm={6}>
                            <Controller
                                name="duree"
                                control={control}
                                rules={{
                                    required: 'La durée est requise',
                                    min: {
                                        value: 1,
                                        message: 'La durée doit être supérieure à 0'
                                    }
                                }}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Durée (heures)"
                                        type="number"
                                        fullWidth
                                        error={!!errors.duree}
                                        helperText={errors.duree?.message}
                                    />
                                )}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <Controller
                                name="competences_requises"
                                control={control}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Compétences requises"
                                        fullWidth
                                        multiline
                                        rows={2}
                                        value={JSON.stringify(field.value, null, 2)}
                                        onChange={(e) => {
                                            try {
                                                field.onChange(JSON.parse(e.target.value));
                                            } catch (error) {
                                                field.onChange(e.target.value);
                                            }
                                        }}
                                    />
                                )}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <Controller
                                name="competences_acquises"
                                control={control}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Compétences acquises"
                                        fullWidth
                                        multiline
                                        rows={2}
                                        value={JSON.stringify(field.value, null, 2)}
                                        onChange={(e) => {
                                            try {
                                                field.onChange(JSON.parse(e.target.value));
                                            } catch (error) {
                                                field.onChange(e.target.value);
                                            }
                                        }}
                                    />
                                )}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <Controller
                                name="materiel_requis"
                                control={control}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Matériel requis"
                                        fullWidth
                                        multiline
                                        rows={2}
                                        value={JSON.stringify(field.value, null, 2)}
                                        onChange={(e) => {
                                            try {
                                                field.onChange(JSON.parse(e.target.value));
                                            } catch (error) {
                                                field.onChange(e.target.value);
                                            }
                                        }}
                                    />
                                )}
                            />
                        </Grid>

                        <Grid item xs={12}>
                            <Controller
                                name="conditions_meteo"
                                control={control}
                                render={({ field }) => (
                                    <TextField
                                        {...field}
                                        label="Conditions météo"
                                        fullWidth
                                        multiline
                                        rows={2}
                                        value={JSON.stringify(field.value, null, 2)}
                                        onChange={(e) => {
                                            try {
                                                field.onChange(JSON.parse(e.target.value));
                                            } catch (error) {
                                                field.onChange(e.target.value);
                                            }
                                        }}
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
                        disabled={createMutation.isPending || updateMutation.isPending}
                    >
                        {isEdit ? 'Modifier' : 'Créer'}
                    </Button>
                </DialogActions>
            </form>
        </Dialog>
    );
};
