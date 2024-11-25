import React, { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  Box,
  Button,
  Typography,
  Alert,
  CircularProgress
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { 
  CompetenceAgricole,
  CompetenceAgricoleCreate,
  CompetenceAgricoleUpdate 
} from '../../../types/hr_agricole';
import {
  createCompetence,
  updateCompetence,
  getCompetencesEmploye
} from '../../../services/hr_agricole';
import CompetencesList from './CompetencesList';
import CompetenceForm from './CompetenceForm';

interface CompetencesAgricolesProps {
  employeId: string;
}

const CompetencesAgricoles: React.FC<CompetencesAgricolesProps> = ({ employeId }) => {
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [selectedCompetence, setSelectedCompetence] = useState<CompetenceAgricole | undefined>();
  const queryClient = useQueryClient();

  // Récupération des compétences
  const {
    data: competences,
    isLoading,
    error
  } = useQuery<CompetenceAgricole[], Error>({
    queryKey: ['competences', employeId],
    queryFn: () => getCompetencesEmploye(employeId)
  });

  // Mutation pour créer une compétence
  const createMutation = useMutation<
    CompetenceAgricole,
    Error,
    CompetenceAgricoleCreate,
    unknown
  >({
    mutationFn: (data) => createCompetence(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['competences', employeId] });
      setIsFormOpen(false);
    }
  });

  // Mutation pour mettre à jour une compétence
  const updateMutation = useMutation<
    CompetenceAgricole,
    Error,
    { id: string } & CompetenceAgricoleUpdate,
    unknown
  >({
    mutationFn: ({ id, ...data }) => updateCompetence(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['competences', employeId] });
      setIsFormOpen(false);
      setSelectedCompetence(undefined);
    }
  });

  const handleOpenForm = () => {
    setSelectedCompetence(undefined);
    setIsFormOpen(true);
  };

  const handleCloseForm = () => {
    setIsFormOpen(false);
    setSelectedCompetence(undefined);
  };

  const handleEdit = (competence: CompetenceAgricole) => {
    setSelectedCompetence(competence);
    setIsFormOpen(true);
  };

  const handleSubmit = async (data: CompetenceAgricoleCreate | CompetenceAgricoleUpdate) => {
    if (selectedCompetence) {
      await updateMutation.mutateAsync({
        id: selectedCompetence.id,
        ...data
      });
    } else {
      await createMutation.mutateAsync(data as CompetenceAgricoleCreate);
    }
  };

  if (isLoading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error">
        Une erreur est survenue lors du chargement des compétences
      </Alert>
    );
  }

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h6">Compétences Agricoles</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={handleOpenForm}
        >
          Ajouter une compétence
        </Button>
      </Box>

      <CompetencesList
        onEdit={handleEdit}
        competences={competences || []}
      />

      <CompetenceForm
        open={isFormOpen}
        onClose={handleCloseForm}
        onSubmit={handleSubmit}
        competence={selectedCompetence}
        employeId={employeId}
        isLoading={createMutation.isPending || updateMutation.isPending}
      />
    </Box>
  );
};

export default CompetencesAgricoles;
