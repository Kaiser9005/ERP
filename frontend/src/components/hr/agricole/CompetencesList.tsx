import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  IconButton,
  Tooltip,
  Chip,
  Box,
  Typography,
  Alert
} from '@mui/material';
import { Edit as EditIcon, Warning as WarningIcon } from '@mui/icons-material';
import { format } from 'date-fns';
import { fr } from 'date-fns/locale';
import { CompetenceAgricole, NiveauCompetence } from '../../../types/hr_agricole';

interface CompetencesListProps {
  onEdit: (competence: CompetenceAgricole) => void;
  competences: CompetenceAgricole[];
}

const niveauColors: Record<NiveauCompetence, 'default' | 'info' | 'success' | 'warning'> = {
  DEBUTANT: 'default',
  INTERMEDIAIRE: 'info',
  AVANCE: 'success',
  EXPERT: 'warning'
};

const CompetencesList: React.FC<CompetencesListProps> = ({ onEdit, competences }) => {
  if (!competences?.length) {
    return (
      <Alert severity="info">
        Aucune compétence agricole enregistrée pour cet employé
      </Alert>
    );
  }

  return (
    <TableContainer component={Paper}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Spécialité</TableCell>
            <TableCell>Niveau</TableCell>
            <TableCell>Cultures</TableCell>
            <TableCell>Équipements</TableCell>
            <TableCell>Date acquisition</TableCell>
            <TableCell>Validité</TableCell>
            <TableCell>Actions</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {competences.map((competence) => (
            <TableRow key={competence.id}>
              <TableCell>{competence.specialite}</TableCell>
              <TableCell>
                <Chip
                  label={competence.niveau}
                  color={niveauColors[competence.niveau]}
                  size="small"
                />
              </TableCell>
              <TableCell>
                <Box display="flex" gap={0.5} flexWrap="wrap">
                  {competence.cultures.map((culture) => (
                    <Chip
                      key={culture}
                      label={culture}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </TableCell>
              <TableCell>
                <Box display="flex" gap={0.5} flexWrap="wrap">
                  {competence.equipements.map((equipement) => (
                    <Chip
                      key={equipement}
                      label={equipement}
                      size="small"
                      variant="outlined"
                    />
                  ))}
                </Box>
              </TableCell>
              <TableCell>
                {format(new Date(competence.date_acquisition), 'dd MMMM yyyy', { locale: fr })}
              </TableCell>
              <TableCell>
                {competence.validite ? (
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography>
                      {format(new Date(competence.validite), 'dd MMMM yyyy', { locale: fr })}
                    </Typography>
                    {new Date(competence.validite) < new Date() && (
                      <Tooltip title="Compétence expirée">
                        <WarningIcon color="error" fontSize="small" />
                      </Tooltip>
                    )}
                  </Box>
                ) : (
                  'Non applicable'
                )}
              </TableCell>
              <TableCell>
                <Tooltip title="Modifier">
                  <IconButton
                    size="small"
                    onClick={() => onEdit(competence)}
                    color="primary"
                  >
                    <EditIcon />
                  </IconButton>
                </Tooltip>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default CompetencesList;
