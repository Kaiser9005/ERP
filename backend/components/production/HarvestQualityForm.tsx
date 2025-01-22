import React, { useState } from 'react';
import {
  Paper,
  Typography,
  Box,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Grid,
  SelectChangeEvent
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DateTimePicker } from '@mui/x-date-pickers';
import { fr } from 'date-fns/locale';
import { Parcelle, QualiteRecolte, Recolte } from '../../types/production';
import { productionService } from '../../services/production';

interface HarvestQualityFormProps {
  parcelle?: Parcelle;
  onSubmit?: () => void;
}

interface FormData {
  date_recolte: Date;
  quantite_kg: number;
  qualite: QualiteRecolte;
  conditions_meteo: {
    temperature: number;
    humidite: number;
    precipitation: number;
  };
  notes: string;
}

const initialFormData: FormData = {
  date_recolte: new Date(),
  quantite_kg: 0,
  qualite: QualiteRecolte.B,
  conditions_meteo: {
    temperature: 0,
    humidite: 0,
    precipitation: 0
  },
  notes: ''
};

const HarvestQualityForm: React.FC<HarvestQualityFormProps> = ({ parcelle, onSubmit }) => {
  const [formData, setFormData] = useState<FormData>(initialFormData);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDateChange = (date: Date | null) => {
    if (date) {
      setFormData(prev => ({ ...prev, date_recolte: date }));
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    if (name.startsWith('meteo_')) {
      const meteoField = name.replace('meteo_', '');
      setFormData(prev => ({
        ...prev,
        conditions_meteo: {
          ...prev.conditions_meteo,
          [meteoField]: Number(value)
        }
      }));
    } else {
      setFormData(prev => ({ ...prev, [name]: value }));
    }
  };

  const handleQualityChange = (e: SelectChangeEvent) => {
    setFormData(prev => ({
      ...prev,
      qualite: e.target.value as QualiteRecolte
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!parcelle) return;

    try {
      setLoading(true);
      setError(null);

      // Créer l'objet de récolte avec la date convertie en ISO string
      const recolteData: Partial<Recolte> = {
        parcelle_id: parcelle.id,
        date_recolte: formData.date_recolte.toISOString(),
        quantite_kg: formData.quantite_kg,
        qualite: formData.qualite,
        conditions_meteo: formData.conditions_meteo,
        notes: formData.notes
      };

      // Envoyer les données au serveur
      await productionService.createRecolte(recolteData);

      // Réinitialiser le formulaire
      setFormData(initialFormData);

      // Notifier le parent
      if (onSubmit) {
        onSubmit();
      }
    } catch (err) {
      setError('Erreur lors de l\'enregistrement de la récolte');
    } finally {
      setLoading(false);
    }
  };

  if (!parcelle) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="200px">
        <Typography>Sélectionnez une parcelle pour enregistrer une récolte</Typography>
      </Box>
    );
  }

  return (
    <Paper elevation={3} sx={{ p: 3 }}>
      <Typography variant="h6" gutterBottom>
        Enregistrement de Récolte - {parcelle.code}
      </Typography>

      <form onSubmit={handleSubmit}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <LocalizationProvider dateAdapter={AdapterDateFns} adapterLocale={fr}>
              <DateTimePicker
                label="Date et heure de récolte"
                value={formData.date_recolte}
                onChange={handleDateChange}
                slotProps={{ textField: { fullWidth: true } }}
              />
            </LocalizationProvider>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Quantité (kg)"
              name="quantite_kg"
              type="number"
              value={formData.quantite_kg}
              onChange={handleInputChange}
              InputProps={{ inputProps: { min: 0 } }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel>Qualité</InputLabel>
              <Select
                value={formData.qualite}
                label="Qualité"
                onChange={handleQualityChange}
              >
                <MenuItem value={QualiteRecolte.A}>Qualité A (Supérieure)</MenuItem>
                <MenuItem value={QualiteRecolte.B}>Qualité B (Standard)</MenuItem>
                <MenuItem value={QualiteRecolte.C}>Qualité C (Inférieure)</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Température (°C)"
              name="meteo_temperature"
              type="number"
              value={formData.conditions_meteo.temperature}
              onChange={handleInputChange}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Humidité (%)"
              name="meteo_humidite"
              type="number"
              value={formData.conditions_meteo.humidite}
              onChange={handleInputChange}
              InputProps={{ inputProps: { min: 0, max: 100 } }}
            />
          </Grid>

          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              label="Précipitations (mm)"
              name="meteo_precipitation"
              type="number"
              value={formData.conditions_meteo.precipitation}
              onChange={handleInputChange}
              InputProps={{ inputProps: { min: 0 } }}
            />
          </Grid>

          <Grid item xs={12}>
            <TextField
              fullWidth
              label="Notes"
              name="notes"
              multiline
              rows={4}
              value={formData.notes}
              onChange={handleInputChange}
            />
          </Grid>

          {error && (
            <Grid item xs={12}>
              <Typography color="error">{error}</Typography>
            </Grid>
          )}

          <Grid item xs={12}>
            <Button
              type="submit"
              variant="contained"
              color="primary"
              disabled={loading}
              fullWidth
            >
              {loading ? 'Enregistrement...' : 'Enregistrer la récolte'}
            </Button>
          </Grid>
        </Grid>
      </form>
    </Paper>
  );
};

export default HarvestQualityForm;
