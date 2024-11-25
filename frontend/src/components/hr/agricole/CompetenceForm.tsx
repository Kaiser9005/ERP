import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
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
  Box,
  Autocomplete,
  FormHelperText,
  CircularProgress
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import {
  CompetenceAgricoleCreate,
  CompetenceAgricoleUpdate,
  CompetenceAgricole
} from '../../../types/hr_agricole';

// Constantes pour les énumérations
const SPECIALITES = [
  'CULTURE',
  'ELEVAGE',
  'MARAICHAGE',
  'ARBORICULTURE',
  'MAINTENANCE',
  'LOGISTIQUE'
] as const;

const NIVEAUX = [
  'DEBUTANT',
  'INTERMEDIAIRE',
  'AVANCE',
  'EXPERT'
] as const;

// Schéma de validation
const competenceSchema = z.object({
  employe_id: z.string().uuid(),
  specialite: z.enum(SPECIALITES),
  niveau: z.enum(NIVEAUX),
  cultures: z.array(z.string()).min(1, 'Au moins une culture doit être sélectionnée'),
  equipements: z.array(z.string()),
  date_acquisition: z.date(),
  date_mise_a_jour: z.date().optional(),
  validite: z.date().optional(),
  commentaire: z.string().optional(),
  donnees_supplementaires: z.record(z.any()).optional()
});

type CompetenceFormData = z.infer<typeof competenceSchema>;

interface CompetenceFormProps {
  open: boolean;
  onClose: () => void;
  onSubmit: (data: CompetenceAgricoleCreate | CompetenceAgricoleUpdate) => Promise<void>;
  competence?: CompetenceAgricole;
  employeId: string;
  isLoading?: boolean;
}

const culturesDisponibles = [
  'Blé',
  'Maïs',
  'Orge',
  'Soja',
  'Tournesol',
  'Colza',
  'Betterave',
  'Pomme de terre',
  'Tomate',
  'Carotte',
  'Salade',
  'Oignon',
  'Poireau',
  'Haricot',
  'Pois',
  'Vigne',
  'Pommier',
  'Poirier',
  'Prunier',
  'Cerisier'
];

const equipementsDisponibles = [
  'Tracteur',
  'Moissonneuse-batteuse',
  'Charrue',
  'Semoir',
  'Pulvérisateur',
  'Épandeur',
  'Système irrigation',
  'Serre',
  'Outils manuels',
  'Station météo',
  'Drone',
  'GPS agricole',
  'Robot de traite',
  'Système ventilation',
  'Système chauffage'
];

const CompetenceForm: React.FC<CompetenceFormProps> = ({
  open,
  onClose,
  onSubmit,
  competence,
  employeId,
  isLoading = false
}) => {
  const {
    control,
    handleSubmit,
    formState: { errors },
    reset
  } = useForm<CompetenceFormData>({
    resolver: zodResolver(competenceSchema),
    defaultValues: competence ? {
      ...competence,
      date_acquisition: new Date(competence.date_acquisition),
      date_mise_a_jour: competence.date_mise_a_jour ? new Date(competence.date_mise_a_jour) : undefined,
      validite: competence.validite ? new Date(competence.validite) : undefined
    } : {
      employe_id: employeId,
      cultures: [],
      equipements: [],
      donnees_supplementaires: {}
    }
  });

  const handleClose = () => {
    reset();
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
      <DialogTitle>
        {competence ? 'Modifier la compétence' : 'Nouvelle compétence'}
      </DialogTitle>
      <form onSubmit={handleSubmit((data) => {
        const formattedData = {
          ...data,
          date_acquisition: data.date_acquisition.toISOString(),
          date_mise_a_jour: data.date_mise_a_jour?.toISOString(),
          validite: data.validite?.toISOString()
        };
        return onSubmit(formattedData);
      })}>
        <DialogContent>
          <Box display="grid" gap={3} gridTemplateColumns="repeat(2, 1fr)">
            <Controller
              name="specialite"
              control={control}
              render={({ field }) => (
                <FormControl error={!!errors.specialite} fullWidth>
                  <InputLabel>Spécialité</InputLabel>
                  <Select {...field} label="Spécialité">
                    {SPECIALITES.map((specialite) => (
                      <MenuItem key={specialite} value={specialite}>
                        {specialite}
                      </MenuItem>
                    ))}
                  </Select>
                  {errors.specialite && (
                    <FormHelperText>{errors.specialite.message}</FormHelperText>
                  )}
                </FormControl>
              )}
            />

            <Controller
              name="niveau"
              control={control}
              render={({ field }) => (
                <FormControl error={!!errors.niveau} fullWidth>
                  <InputLabel>Niveau</InputLabel>
                  <Select {...field} label="Niveau">
                    {NIVEAUX.map((niveau) => (
                      <MenuItem key={niveau} value={niveau}>
                        {niveau}
                      </MenuItem>
                    ))}
                  </Select>
                  {errors.niveau && (
                    <FormHelperText>{errors.niveau.message}</FormHelperText>
                  )}
                </FormControl>
              )}
            />

            <Controller
              name="cultures"
              control={control}
              render={({ field: { onChange, value } }) => (
                <FormControl error={!!errors.cultures} fullWidth>
                  <Autocomplete
                    multiple
                    options={culturesDisponibles}
                    value={value}
                    onChange={(_, newValue) => onChange(newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Cultures"
                        error={!!errors.cultures}
                        helperText={errors.cultures?.message}
                      />
                    )}
                  />
                </FormControl>
              )}
            />

            <Controller
              name="equipements"
              control={control}
              render={({ field: { onChange, value } }) => (
                <FormControl error={!!errors.equipements} fullWidth>
                  <Autocomplete
                    multiple
                    options={equipementsDisponibles}
                    value={value}
                    onChange={(_, newValue) => onChange(newValue)}
                    renderInput={(params) => (
                      <TextField
                        {...params}
                        label="Équipements"
                        error={!!errors.equipements}
                        helperText={errors.equipements?.message}
                      />
                    )}
                  />
                </FormControl>
              )}
            />

            <Controller
              name="date_acquisition"
              control={control}
              render={({ field: { onChange, value } }) => (
                <DatePicker
                  label="Date d'acquisition"
                  value={value}
                  onChange={onChange}
                  format="dd/MM/yyyy"
                  slotProps={{
                    textField: {
                      error: !!errors.date_acquisition,
                      helperText: errors.date_acquisition?.message
                    }
                  }}
                />
              )}
            />

            <Controller
              name="validite"
              control={control}
              render={({ field: { onChange, value } }) => (
                <DatePicker
                  label="Date de validité"
                  value={value}
                  onChange={onChange}
                  format="dd/MM/yyyy"
                  slotProps={{
                    textField: {
                      error: !!errors.validite,
                      helperText: errors.validite?.message
                    }
                  }}
                />
              )}
            />

            <Controller
              name="commentaire"
              control={control}
              render={({ field }) => (
                <TextField
                  {...field}
                  label="Commentaire"
                  multiline
                  rows={4}
                  fullWidth
                  error={!!errors.commentaire}
                  helperText={errors.commentaire?.message}
                />
              )}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleClose}>Annuler</Button>
          <Button
            type="submit"
            variant="contained"
            color="primary"
            disabled={isLoading}
          >
            {isLoading ? (
              <CircularProgress size={24} />
            ) : competence ? (
              'Modifier'
            ) : (
              'Créer'
            )}
          </Button>
        </DialogActions>
      </form>
    </Dialog>
  );
};

export default CompetenceForm;
