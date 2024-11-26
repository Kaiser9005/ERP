import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
    TextField,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    Button,
    Grid,
    Paper,
    Typography,
    Box
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { ContractCreate, ContractUpdate, CONTRACT_TYPES } from '../../types/contract';

interface ContractFormProps {
    initialData?: ContractUpdate;
    employeeId?: string;
    onSubmit: (data: ContractCreate | ContractUpdate) => void;
    onCancel: () => void;
    isLoading?: boolean;
}

export const ContractForm: React.FC<ContractFormProps> = ({
    initialData,
    employeeId,
    onSubmit,
    onCancel,
    isLoading = false
}) => {
    const { control, handleSubmit, formState: { errors } } = useForm({
        defaultValues: {
            type: initialData?.type || '',
            start_date: initialData?.start_date || '',
            end_date: initialData?.end_date || '',
            wage: initialData?.wage || 0,
            position: initialData?.position || '',
            department: initialData?.department || '',
            employee_id: employeeId || ''
        }
    });

    return (
        <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
                {initialData ? 'Modifier le Contrat' : 'Nouveau Contrat'}
            </Typography>

            <form onSubmit={handleSubmit(onSubmit)}>
                <Grid container spacing={3}>
                    <Grid item xs={12} sm={6}>
                        <FormControl fullWidth error={!!errors.type}>
                            <InputLabel>Type de Contrat</InputLabel>
                            <Controller
                                name="type"
                                control={control}
                                rules={{ required: 'Type de contrat requis' }}
                                render={({ field }) => (
                                    <Select {...field} label="Type de Contrat">
                                        {CONTRACT_TYPES.map(type => (
                                            <MenuItem key={type} value={type}>
                                                {type}
                                            </MenuItem>
                                        ))}
                                    </Select>
                                )}
                            />
                        </FormControl>
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name="wage"
                            control={control}
                            rules={{ 
                                required: 'Salaire requis',
                                min: { value: 0, message: 'Le salaire doit être positif' }
                            }}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    label="Salaire"
                                    type="number"
                                    error={!!errors.wage}
                                    helperText={errors.wage?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name="start_date"
                            control={control}
                            rules={{ required: 'Date de début requise' }}
                            render={({ field }) => (
                                <DatePicker
                                    {...field}
                                    label="Date de Début"
                                    slotProps={{
                                        textField: {
                                            fullWidth: true,
                                            error: !!errors.start_date,
                                            helperText: errors.start_date?.message
                                        }
                                    }}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name="end_date"
                            control={control}
                            render={({ field }) => (
                                <DatePicker
                                    {...field}
                                    label="Date de Fin"
                                    slotProps={{
                                        textField: {
                                            fullWidth: true,
                                            error: !!errors.end_date,
                                            helperText: errors.end_date?.message
                                        }
                                    }}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name="position"
                            control={control}
                            rules={{ required: 'Poste requis' }}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    label="Poste"
                                    error={!!errors.position}
                                    helperText={errors.position?.message}
                                />
                            )}
                        />
                    </Grid>

                    <Grid item xs={12} sm={6}>
                        <Controller
                            name="department"
                            control={control}
                            rules={{ required: 'Département requis' }}
                            render={({ field }) => (
                                <TextField
                                    {...field}
                                    fullWidth
                                    label="Département"
                                    error={!!errors.department}
                                    helperText={errors.department?.message}
                                />
                            )}
                        />
                    </Grid>
                </Grid>

                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button onClick={onCancel} disabled={isLoading}>
                        Annuler
                    </Button>
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        disabled={isLoading}
                    >
                        {isLoading ? 'Enregistrement...' : 'Enregistrer'}
                    </Button>
                </Box>
            </form>
        </Paper>
    );
};
