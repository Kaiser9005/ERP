import React, { useState, useEffect } from 'react';
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
  Tooltip,
  Grid
} from '@mui/material';
import { Add, Remove, SwapHoriz, Search } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getMouvements, getProduits } from '../../services/inventaire';
import { formatDistanceToNow } from 'date-fns';
import { fr } from 'date-fns/locale';
import { useTranslation } from 'react-i18next';
import { TypeMouvement, FiltresInventaire, MouvementStock, Produit, CategoryProduit, UniteMesure } from '../../types/inventaire';

interface HistoriqueMouvementsProps {
  searchQuery?: string;
}

interface MouvementWithProduit extends MouvementStock {
  produit: Produit;
}

const HistoriqueMouvements: React.FC<HistoriqueMouvementsProps> = ({ searchQuery = '' }) => {
  const { t } = useTranslation();
  const [typeMouvement, setTypeMouvement] = useState<TypeMouvement | ''>('');
  const [searchTerm, setSearchTerm] = useState<string>('');

  // Synchroniser searchTerm avec searchQuery
  useEffect(() => {
    if (searchQuery) {
      setSearchTerm(searchQuery);
    }
  }, [searchQuery]);

  const filtres: FiltresInventaire = {
    ...(typeMouvement && { type_mouvement: typeMouvement }),
    ...(searchTerm && { recherche: searchTerm })
  };

  const { data: mouvements = [], isLoading: isLoadingMouvements } = useQuery(
    ['mouvements', filtres],
    () => getMouvements(filtres)
  );

  const { data: produits = [], isLoading: isLoadingProduits } = useQuery(
    'produits',
    () => getProduits()
  );

  // Combiner les mouvements avec leurs produits
  const mouvementsWithProduits: MouvementWithProduit[] = mouvements.map(mouvement => ({
    ...mouvement,
    produit: produits.find(p => p.id === mouvement.produit_id) || {
      id: mouvement.produit_id,
      code: 'N/A',
      nom: 'Produit inconnu',
      categorie: CategoryProduit.INTRANT,
      unite_mesure: UniteMesure.UNITE,
      description: ''
    }
  }));

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

  const filteredMouvements = mouvementsWithProduits.filter(mouvement => 
    mouvement.produit.nom.toLowerCase().includes(searchTerm.toLowerCase()) ||
    mouvement.reference_document?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  if (isLoadingMouvements || isLoadingProduits) {
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
