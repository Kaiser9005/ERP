import React, { useState } from 'react';
import { Grid, Paper, Box, FormControl, InputLabel, Select, MenuItem, Button, Typography } from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers';
import { useTranslation } from 'react-i18next';
import { CSVLink } from 'react-csv';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
  LineChart, Line, AreaChart, Area
} from 'recharts';
import StatCard from '../common/StatCard';
import { Inventory, TrendingUp, Warning, LocalShipping } from '@mui/icons-material';
import { useQuery } from 'react-query';
import { getStatsInventaire, getMouvements, getStocks, getPrevisions, getFournisseurs } from '../../services/inventaire';
import { CategoryProduit, PeriodeInventaire, SeuilStockType } from '../../types/inventaire';
import { formatNumber, formatDate, formatDateForAPI } from '../../utils/format';

interface Variation {
  valeur: number;
  type: 'hausse' | 'baisse';
}

const StatsInventaire: React.FC = () => {
  const { t } = useTranslation();
  const [periode, setPeriode] = useState<PeriodeInventaire>(PeriodeInventaire.MOIS);
  const [categorie, setCategorie] = useState<CategoryProduit | 'tous'>('tous');
  const [dateDebut, setDateDebut] = useState<Date | null>(null);
  const [dateFin, setDateFin] = useState<Date | null>(null);
  const [fournisseur, setFournisseur] = useState<string>('tous');
  const [seuilStock, setSeuilStock] = useState<SeuilStockType | 'tous'>('tous');

  const { data: fournisseurs = [] } = useQuery('fournisseurs', getFournisseurs);

  const filtres = {
    periode,
    categorie: categorie !== 'tous' ? categorie : undefined,
    dateDebut: dateDebut ? formatDateForAPI(dateDebut) : undefined,
    dateFin: dateFin ? formatDateForAPI(dateFin) : undefined,
    fournisseur: fournisseur !== 'tous' ? fournisseur : undefined,
    seuilStock: seuilStock !== 'tous' ? seuilStock : undefined
  };

  const { data: statsService } = useQuery(
    ['statistiques-inventaire', filtres],
    () => getStatsInventaire(filtres)
  );

  const { data: mouvements } = useQuery(
    ['mouvements-stock', filtres],
    () => getMouvements(filtres)
  );

  const { data: stocks } = useQuery(
    ['stocks', filtres],
    () => getStocks(filtres)
  );

  const { data: previsions } = useQuery(
    ['previsions-stock', filtres],
    () => getPrevisions(filtres)
  );

  const stats = statsService ? {
    valeurTotale: statsService.valeur_totale,
    variationValeur: { valeur: statsService.valeur_stock, type: 'hausse' as const },
    tauxRotation: statsService.total_produits,
    variationRotation: { valeur: statsService.rotation_stock, type: 'hausse' as const },
    alertes: statsService.stock_faible,
    variationAlertes: { valeur: 0, type: 'hausse' as const },
    mouvements: statsService.mouvements.entrees + statsService.mouvements.sorties,
    variationMouvements: { valeur: 0, type: 'hausse' as const }
  } : undefined;

  // Données pour le graphique des mouvements
  const donneesGraphiqueMouvements = mouvements ? [
    { name: t('inventaire.entrees'), value: statsService?.mouvements.entrees || 0 },
    { name: t('inventaire.sorties'), value: statsService?.mouvements.sorties || 0 }
  ] : [];

  // Données pour le graphique des stocks par catégorie
  const donneesStocksParCategorie = stocks ? Object.values(CategoryProduit).map(cat => ({
    name: t(`inventaire.categories.${cat.toLowerCase()}`),
    value: stocks.filter(s => s.produit.categorie === cat).length
  })) : [];

  // Données pour le graphique des tendances
  const donneesTendances = mouvements ? mouvements.map(m => ({
    date: formatDate(m.date_mouvement),
    entrees: m.type_mouvement === 'ENTREE' ? m.quantite : 0,
    sorties: m.type_mouvement === 'SORTIE' ? m.quantite : 0
  })) : [];

  // Données pour le graphique des prévisions
  const donneesPrevisions = previsions ? previsions.map(p => ({
    date: formatDate(p.date),
    reel: p.valeur_reelle,
    prevu: p.valeur_prevue
  })) : [];

  // Données pour l'export CSV
  const donneesExport = stats ? [
    {
      valeurTotale: formatNumber(stats.valeurTotale),
      tauxRotation: stats.tauxRotation,
      alertes: stats.alertes,
      mouvements: stats.mouvements,
      periode: periode,
      dateExport: formatDate(new Date())
    }
  ] : [];

  return (
    <Box sx={{ p: 3 }} role="region" aria-label={t('inventaire.statistiques')}>
      <Box sx={{ mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h5" component="h2">
          {t('inventaire.statistiques')}
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <FormControl size="small">
            <InputLabel id="periode-select-label">{t('commun.periode')}</InputLabel>
            <Select
              labelId="periode-select-label"
              value={periode}
              onChange={(e) => setPeriode(e.target.value as PeriodeInventaire)}
              label={t('commun.periode')}
            >
              {Object.values(PeriodeInventaire).map((p) => (
                <MenuItem key={p} value={p}>
                  {t(`commun.periodes.${p}`)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          {periode === PeriodeInventaire.PERSONNALISE && (
            <>
              <DatePicker
                label={t('commun.dateDebut')}
                value={dateDebut}
                onChange={(date: Date | null) => setDateDebut(date)}
                slotProps={{ textField: { size: 'small' } }}
              />
              <DatePicker
                label={t('commun.dateFin')}
                value={dateFin}
                onChange={(date: Date | null) => setDateFin(date)}
                slotProps={{ textField: { size: 'small' } }}
              />
            </>
          )}

          <FormControl size="small">
            <InputLabel id="categorie-select-label">{t('inventaire.categorie')}</InputLabel>
            <Select
              labelId="categorie-select-label"
              value={categorie}
              onChange={(e) => setCategorie(e.target.value as CategoryProduit | 'tous')}
              label={t('inventaire.categorie')}
            >
              <MenuItem value="tous">{t('commun.tous')}</MenuItem>
              {Object.values(CategoryProduit).map((cat) => (
                <MenuItem key={cat} value={cat}>
                  {t(`inventaire.categories.${cat.toLowerCase()}`)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small">
            <InputLabel id="fournisseur-select-label">{t('inventaire.fournisseur')}</InputLabel>
            <Select
              labelId="fournisseur-select-label"
              value={fournisseur}
              onChange={(e) => setFournisseur(e.target.value)}
              label={t('inventaire.fournisseur')}
            >
              <MenuItem value="tous">{t('commun.tous')}</MenuItem>
              {fournisseurs.map((f) => (
                <MenuItem key={f} value={f}>
                  {f}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <FormControl size="small">
            <InputLabel id="seuil-select-label">{t('inventaire.seuilStock')}</InputLabel>
            <Select
              labelId="seuil-select-label"
              value={seuilStock}
              onChange={(e) => setSeuilStock(e.target.value as SeuilStockType | 'tous')}
              label={t('inventaire.seuilStock')}
            >
              <MenuItem value="tous">{t('commun.tous')}</MenuItem>
              {Object.values(SeuilStockType).map((seuil) => (
                <MenuItem key={seuil} value={seuil}>
                  {t(`inventaire.seuilStock.${seuil}`)}
                </MenuItem>
              ))}
            </Select>
          </FormControl>

          <CSVLink
            data={donneesExport}
            filename={`statistiques_inventaire_${new Date().toISOString()}.csv`}
            style={{ textDecoration: 'none' }}
          >
            <Button variant="outlined" color="primary">
              {t('commun.exporter')}
            </Button>
          </CSVLink>
        </Box>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title={t('inventaire.valeurTotale')}
            value={stats?.valeurTotale || 0}
            unit="FCFA"
            variation={stats?.variationValeur}
            icon={<Inventory />}
            color="primary"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title={t('inventaire.tauxRotation')}
            value={stats?.tauxRotation || 0}
            unit={t('inventaire.produits')}
            variation={stats?.variationRotation}
            icon={<TrendingUp />}
            color="success"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title={t('inventaire.alertes')}
            value={stats?.alertes || 0}
            variation={stats?.variationAlertes}
            icon={<Warning />}
            color="warning"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title={t('inventaire.mouvements')}
            value={stats?.mouvements || 0}
            variation={stats?.variationMouvements}
            icon={<LocalShipping />}
            color="info"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {t('inventaire.graphiques.mouvements')}
            </Typography>
            <Box role="img" aria-label={t('inventaire.graphiques.mouvements')}>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={donneesGraphiqueMouvements}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#2196f3" name={t('inventaire.quantite')} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {t('inventaire.graphiques.stocksParCategorie')}
            </Typography>
            <Box role="img" aria-label={t('inventaire.graphiques.stocksParCategorie')}>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={donneesStocksParCategorie}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#4caf50" name={t('inventaire.nombreProduits')} />
                </BarChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {t('inventaire.graphiques.tendances')}
            </Typography>
            <Box role="img" aria-label={t('inventaire.graphiques.tendances')}>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={donneesTendances}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="entrees" stroke="#2196f3" name={t('inventaire.entrees')} />
                  <Line type="monotone" dataKey="sorties" stroke="#f44336" name={t('inventaire.sorties')} />
                </LineChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              {t('inventaire.graphiques.previsions')}
            </Typography>
            <Box role="img" aria-label={t('inventaire.graphiques.previsions')}>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={donneesPrevisions}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Area type="monotone" dataKey="reel" stackId="1" stroke="#82ca9d" fill="#82ca9d" name={t('inventaire.valeurReelle')} />
                  <Area type="monotone" dataKey="prevu" stackId="1" stroke="#8884d8" fill="#8884d8" name={t('inventaire.valeurPrevue')} />
                </AreaChart>
              </ResponsiveContainer>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default StatsInventaire;