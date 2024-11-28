import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Chip,
  Box,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Alert,
  Tooltip,
  Grid
} from '@mui/material';
import { Add, Remove, SwapHoriz, Search } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getMouvements, getTendances } from '../../services/inventaire';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';
import { useTranslation } from 'react-i18next';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as ChartTooltip, Legend, ResponsiveContainer } from 'recharts';
import { TypeMouvement, FiltresInventaire } from '../../types/inventaire';

const HistoriqueMouvements: React.FC = () => {
  const { t } = useTranslation();
  const [typeMouvement, setTypeMouvement] = useState<TypeMouvement | ''>('');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const filtres: FiltresInventaire = {
    ...(typeMouvement && { type_mouvement: typeMouvement }),
    ...(searchTerm && { recherche: searchTerm })
  };

  const { data: mouvements = [], isLoading, error } = useQuery(
    ['recent-movements', filtres],
    () => getMouvements(filtres)
  );

  const { data: tendances = [] } = useQuery(
    ['tendances-mouvements', filtres],
    () => getTendances(filtres)
  );

  const getMovementIcon = (type: TypeMouvement) => {
    switch (type) {
      case TypeMouvement.ENTREE:
        return <Add />;
      case TypeMouvement.SORTIE:
        return <Remove />;
      default:
        return <SwapHoriz />;
    }
  };

  const getMovementColor = (type: TypeMouvement): 'success' | 'error' | 'info' => {
    switch (type) {
      case TypeMouvement.ENTREE:
        return 'success';
      case TypeMouvement.SORTIE:
        return 'error';
      default:
        return 'info';
    }
  };

  const filteredMouvements = mouvements.filter(mouvement => 
    mouvement.produit.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mouvement.reference_document?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" p={3}>
            <CircularProgress />
            <Typography ml={2}>{t('commun.chargement')}</Typography>
          </Box>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <CardContent>
          <Alert severity="error">
            {t('inventaire.mouvements.erreurChargement')}
          </Alert>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('inventaire.mouvements.titre')}
        </Typography>

        <Grid container spacing={2} mb={3}>
          <Grid item xs={12} md={6}>
            <FormControl fullWidth size="small">
              <InputLabel id="type-mouvement-label">
                {t('inventaire.mouvements.filtres.type')}
              </InputLabel>
              <Select
                labelId="type-mouvement-label"
                value={typeMouvement}
                label={t('inventaire.mouvements.filtres.type')}
                onChange={(e) => setTypeMouvement(e.target.value as TypeMouvement | '')}
              >
                <MenuItem value="">{t('commun.tous')}</MenuItem>
                <MenuItem value={TypeMouvement.ENTREE}>{t('inventaire.mouvements.types.entree')}</MenuItem>
                <MenuItem value={TypeMouvement.SORTIE}>{t('inventaire.mouvements.types.sortie')}</MenuItem>
                <MenuItem value={TypeMouvement.TRANSFERT}>{t('inventaire.mouvements.types.transfert')}</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} md={6}>
            <TextField
              fullWidth
              size="small"
              placeholder={t('inventaire.mouvements.filtres.recherche')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              InputProps={{
                startAdornment: <Search color="action" sx={{ mr: 1 }} />
              }}
            />
          </Grid>
        </Grid>

        {tendances.length > 0 && (
          <Box mb={3} height={300}>
            <Typography variant="subtitle1" gutterBottom>
              {t('inventaire.mouvements.graphiques.titre')}
            </Typography>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={tendances}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <ChartTooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="entrees"
                  name={t('inventaire.mouvements.graphiques.entrees')}
                  stroke="#2e7d32"
                />
                <Line
                  type="monotone"
                  dataKey="sorties"
                  name={t('inventaire.mouvements.graphiques.sorties')}
                  stroke="#d32f2f"
                />
              </LineChart>
            </ResponsiveContainer>
          </Box>
        )}

        {filteredMouvements.length === 0 ? (
          <Typography color="textSecondary">
            {t('inventaire.mouvements.aucunMouvement')}
          </Typography>
        ) : (
          <List>
            {filteredMouvements.map((mouvement) => (
              <ListItem
                key={mouvement.id}
                divider
                aria-label={`${t(`inventaire.mouvements.types.${mouvement.type_mouvement.toLowerCase()}`)} - ${mouvement.produit.nom}`}
              >
                <ListItemAvatar>
                  <Tooltip title={t(`inventaire.mouvements.types.${mouvement.type_mouvement.toLowerCase()}`)}>
                    <Avatar sx={{ bgcolor: `${getMovementColor(mouvement.type_mouvement)}.light` }}>
                      {getMovementIcon(mouvement.type_mouvement)}
                    </Avatar>
                  </Tooltip>
                </ListItemAvatar>
                <ListItemText
                  primary={
                    <Box display="flex" alignItems="center" gap={1}>
                      <Tooltip title={mouvement.produit.code}>
                        <Typography component="span">
                          {mouvement.produit.nom}
                        </Typography>
                      </Tooltip>
                      <Chip
                        size="small"
                        label={t(`inventaire.mouvements.types.${mouvement.type_mouvement.toLowerCase()}`)}
                        color={getMovementColor(mouvement.type_mouvement)}
                      />
                    </Box>
                  }
                  secondary={
                    <>
                      <Tooltip title={t('inventaire.mouvements.colonnes.quantite')}>
                        <Typography component="span" variant="body2">
                          {`${mouvement.quantite} ${mouvement.produit.unite_mesure}`}
                        </Typography>
                      </Tooltip>
                      <br />
                      <Tooltip title={t('inventaire.mouvements.colonnes.reference')}>
                        <Typography component="span" variant="body2">
                          {mouvement.reference_document || t('commun.sansReference')}
                        </Typography>
                      </Tooltip>
                      <br />
                      <Tooltip title={t('inventaire.mouvements.colonnes.date')}>
                        <Typography component="span" variant="body2" color="textSecondary">
                          {formatDistanceToNow(new Date(mouvement.date_mouvement), {
                            addSuffix: true,
                            locale: fr
                          })}
                        </Typography>
                      </Tooltip>
                    </>
                  }
                />
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
};

export default HistoriqueMouvements;
