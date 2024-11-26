import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import {
  TextField,
  Grid,
  Paper,
  Typography,
  Button,
  Box,
  FormControl,
  InputLabel,
  OutlinedInput,
  InputAdornment,
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { CreatePayrollRequest, PayrollSlip } from '../../../types/payroll';

interface PayrollFormProps {
  initialData?: PayrollSlip;
  onSubmit: (data: CreatePayrollRequest) => void;
  onCancel: () => void;
}

export const PayrollForm: React.FC<PayrollFormProps> = ({
  initialData,
  onSubmit,
  onCancel,
}) => {
  const { control, handleSubmit } = useForm<CreatePayrollRequest>({
    defaultValues: initialData ? {
      contract_id: initialData.contract_id,
      period_start: initialData.period_start,
      period_end: initialData.period_end,
      worked_hours: initialData.worked_hours,
      overtime_hours: initialData.overtime_hours,
      overtime_amount: initialData.overtime_amount,
      bonus: initialData.bonus,
      deductions: initialData.deductions,
      bonus_details: initialData.bonus_details,
      deduction_details: initialData.deduction_details,
      employer_contributions: initialData.employer_contributions,
      employee_contributions: initialData.employee_contributions,
    } : {
      contract_id: '',
      period_start: '',
      period_end: '',
      worked_hours: 151.67, // Heures mensuelles standard
      overtime_hours: 0,
      overtime_amount: 0,
      bonus: 0,
      deductions: 0,
      bonus_details: {},
      deduction_details: {},
      employer_contributions: 0,
      employee_contributions: 0,
    }
  });

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        {initialData ? 'Modifier la fiche de paie' : 'Nouvelle fiche de paie'}
      </Typography>

      <form onSubmit={handleSubmit(onSubmit)}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Controller
              name="period_start"
              control={control}
              render={({ field }) => (
                <DatePicker
                  label="Début de période"
                  value={field.value}
                  onChange={field.onChange}
                  format="dd/MM/yyyy"
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      error: false
                    }
                  }}
                />
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="period_end"
              control={control}
              render={({ field }) => (
                <DatePicker
                  label="Fin de période"
                  value={field.value}
                  onChange={field.onChange}
                  format="dd/MM/yyyy"
                  slotProps={{
                    textField: {
                      fullWidth: true,
                      error: false
                    }
                  }}
                />
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="worked_hours"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Heures travaillées"
                  type="number"
                  fullWidth
                  InputProps={{
                    endAdornment: <InputAdornment position="end">h</InputAdornment>,
                  }}
                />
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="overtime_hours"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Heures supplémentaires"
                  type="number"
                  fullWidth
                  InputProps={{
                    endAdornment: <InputAdornment position="end">h</InputAdornment>,
                  }}
                />
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="overtime_amount"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Montant heures sup.</InputLabel>
                  <OutlinedInput
                    {...field}
                    type="number"
                    startAdornment={<InputAdornment position="start">€</InputAdornment>}
                    label="Montant heures sup."
                  />
                </FormControl>
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="bonus"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Primes</InputLabel>
                  <OutlinedInput
                    {...field}
                    type="number"
                    startAdornment={<InputAdornment position="start">€</InputAdornment>}
                    label="Primes"
                  />
                </FormControl>
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="deductions"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Retenues</InputLabel>
                  <OutlinedInput
                    {...field}
                    type="number"
                    startAdornment={<InputAdornment position="start">€</InputAdornment>}
                    label="Retenues"
                  />
                </FormControl>
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="employer_contributions"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Charges patronales</InputLabel>
                  <OutlinedInput
                    {...field}
                    type="number"
                    startAdornment={<InputAdornment position="start">€</InputAdornment>}
                    label="Charges patronales"
                  />
                </FormControl>
              )}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <Controller
              name="employee_contributions"
              control={control}
              render={({ field }) => (
                <FormControl fullWidth>
                  <InputLabel>Charges salariales</InputLabel>
                  <OutlinedInput
                    {...field}
                    type="number"
                    startAdornment={<InputAdornment position="start">€</InputAdornment>}
                    label="Charges salariales"
                  />
                </FormControl>
              )}
            />
          </Grid>
        </Grid>

        <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
          <Button onClick={onCancel} variant="outlined">
            Annuler
          </Button>
          <Button type="submit" variant="contained" color="primary">
            {initialData ? 'Modifier' : 'Créer'}
          </Button>
        </Box>
      </form>
    </Paper>
  );
};
