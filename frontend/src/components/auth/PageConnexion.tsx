import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  TextField,
  Button,
  Typography,
  Alert,
  Container
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../hooks/useAuth';

const PageConnexion: React.FC = () => {
  const naviguer = useNavigate();
  const { connexion } = useAuth();
  const [erreur, setErreur] = useState<string | null>(null);
  const [chargement, setChargement] = useState(false);
  const [donneesFormulaire, setDonneesFormulaire] = useState({
    nomUtilisateur: '',
    motDePasse: ''
  });

  const gererSoumission = async (e: React.FormEvent) => {
    e.preventDefault();
    setErreur(null);
    setChargement(true);

    try {
      await connexion(donneesFormulaire.nomUtilisateur, donneesFormulaire.motDePasse);
      naviguer('/');
    } catch (err) {
      setErreur(err instanceof Error ? err.message : 'Erreur de connexion');
    } finally {
      setChargement(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ 
        minHeight: '100vh', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'center' 
      }}>
        <Card sx={{ width: '100%' }}>
          <CardContent>
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography variant="h4" component="h1" gutterBottom>
                FOFAL ERP
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                Connectez-vous pour accéder à votre espace
              </Typography>
            </Box>

            {erreur && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {erreur}
              </Alert>
            )}

            <form onSubmit={gererSoumission}>
              <TextField
                fullWidth
                label="Nom d'utilisateur"
                variant="outlined"
                margin="normal"
                value={donneesFormulaire.nomUtilisateur}
                onChange={(e) => setDonneesFormulaire({ ...donneesFormulaire, nomUtilisateur: e.target.value })}
                required
              />

              <TextField
                fullWidth
                label="Mot de passe"
                type="password"
                variant="outlined"
                margin="normal"
                value={donneesFormulaire.motDePasse}
                onChange={(e) => setDonneesFormulaire({ ...donneesFormulaire, motDePasse: e.target.value })}
                required
              />

              <Button
                fullWidth
                type="submit"
                variant="contained"
                size="large"
                disabled={chargement}
                sx={{ mt: 3 }}
              >
                {chargement ? 'Connexion en cours...' : 'Se connecter'}
              </Button>
            </form>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default PageConnexion;