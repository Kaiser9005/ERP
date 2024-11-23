import React from 'react';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import { Box, Card, CardContent, Typography, Button } from '@mui/material';
import { LoadingButton } from '@mui/lab';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

import { employeeSchema } from './schemas/employeeSchema';
import { defaultEmployeeValues } from './constants/employeeConstants';
import { MainInfoSection } from './sections/MainInfoSection';
import { AddressSection } from './sections/AddressSection';
import { FormationSection } from './sections/FormationSection';
import { EmployeeFormData } from './types/formTypes';
import { createEmployee, updateEmployee, getEmployee } from '../../services/hr';
import { queryKeys } from '../../config/queryClient';

export const EmployeeForm: React.FC = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const isEdit = Boolean(id);

  const { data: employee, isLoading: isLoadingEmployee } = useQuery({
    queryKey: queryKeys.hr.employee(id!),
    queryFn: () => getEmployee(id!),
    enabled: isEdit
  });

  const {
    control,
    handleSubmit,
    formState: { errors }
  } = useForm<EmployeeFormData>({
    resolver: yupResolver(employeeSchema),
    defaultValues: employee || defaultEmployeeValues
  });

  const mutation = useMutation({
    mutationFn: (data: EmployeeFormData) => {
      return isEdit ? updateEmployee(id!, data) : createEmployee(data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: queryKeys.hr.employees() });
      navigate('/hr/employees');
    }
  });

  const onSubmit = (data: EmployeeFormData) => {
    mutation.mutate(data);
  };

  if (isEdit && isLoadingEmployee) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <LoadingButton loading />
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        {isEdit ? 'Modifier l\'Employé' : 'Nouvel Employé'}
      </Typography>
      {isEdit && (
        <Typography variant="subtitle1" color="text.secondary" gutterBottom>
          Modification de {employee?.prenom} {employee?.nom}
        </Typography>
      )}

      <Card>
        <CardContent>
          <form onSubmit={handleSubmit(onSubmit)}>
            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>
                Informations Principales
              </Typography>
              <MainInfoSection control={control} errors={errors} />
            </Box>

            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>
                Adresse
              </Typography>
              <AddressSection control={control} errors={errors} />
            </Box>

            <Box sx={{ mb: 4 }}>
              <Typography variant="h6" gutterBottom>
                Formation
              </Typography>
              <FormationSection control={control} errors={errors} />
            </Box>

            <Box sx={{ display: 'flex', gap: 2, justifyContent: 'flex-end' }}>
              <Button
                variant="outlined"
                onClick={() => navigate('/hr/employees')}
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
          </form>
        </CardContent>
      </Card>
    </Box>
  );
};

export default EmployeeForm;
