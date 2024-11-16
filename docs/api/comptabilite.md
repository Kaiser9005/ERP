# API Comptabilité

## Vue d'ensemble

L'API de comptabilité fournit des endpoints pour la gestion complète de la comptabilité, incluant :
- Gestion des comptes et écritures comptables
- Statistiques financières et analyses budgétaires
- Suivi de trésorerie avec impact météorologique
- Rapports comptables (Grand Livre, Balance, Bilan, Compte de Résultat)

## Endpoints

### Statistiques et Analyses

#### GET /api/v1/comptabilite/stats

Récupère les statistiques financières actuelles.

**Réponse**
```json
{
  "revenue": 150000.00,
  "revenueVariation": {
    "value": 5.2,
    "type": "increase"
  },
  "expenses": 120000.00,
  "expensesVariation": {
    "value": 3.1,
    "type": "decrease"
  },
  "profit": 30000.00,
  "profitVariation": {
    "value": 8.5,
    "type": "increase"
  },
  "cashflow": 45000.00,
  "cashflowVariation": {
    "value": 4.2,
    "type": "increase"
  }
}
```

#### GET /api/v1/comptabilite/budget/analysis

Analyse détaillée du budget avec impact météorologique.

**Paramètres**
- `periode` (string, required) : Période d'analyse (format: YYYY-MM)

**Réponse**
```json
{
  "total_prevu": 250000.00,
  "total_realise": 245000.00,
  "categories": {
    "601": {
      "libelle": "Achats matières premières",
      "prevu": 100000.00,
      "realise": 98000.00
    }
  },
  "weather_impact": {
    "score": 25,
    "factors": ["Fortes précipitations", "Températures élevées"],
    "projections": {
      "TRANSPORT": "Augmentation probable des coûts"
    }
  },
  "recommendations": [
    "Optimisation des coûts de transport recommandée"
  ]
}
```

#### GET /api/v1/comptabilite/cashflow

Données de trésorerie avec prévisions et impact météo.

**Paramètres**
- `days` (integer, optional) : Nombre de jours d'historique (défaut: 30, max: 365)

**Réponse**
```json
[
  {
    "date": "2024-01-15",
    "entrees": 25000.00,
    "sorties": 20000.00,
    "solde": 5000.00,
    "prevision": 5200.00,
    "impact_meteo": 4.0
  }
]
```

### Comptes Comptables

#### GET /api/v1/comptabilite/comptes

Liste les comptes comptables.

**Paramètres**
- `type_compte` (string, optional) : Filtre par type de compte
- `actif` (boolean, optional) : Filtre par statut actif/inactif

#### POST /api/v1/comptabilite/comptes

Crée un nouveau compte comptable.

**Corps de la requête**
```json
{
  "numero": "601000",
  "libelle": "Achats matières premières",
  "type_compte": "CHARGE",
  "description": "Compte pour les achats de matières premières"
}
```

### Écritures Comptables

#### POST /api/v1/comptabilite/ecritures

Crée une nouvelle écriture comptable.

**Corps de la requête**
```json
{
  "date_ecriture": "2024-01-15",
  "numero_piece": "FAC2024-001",
  "compte_id": "uuid",
  "libelle": "Achat matières premières",
  "debit": 1000.00,
  "credit": 0.00,
  "journal_id": "uuid"
}
```

#### POST /api/v1/comptabilite/ecritures/{id}/valider

Valide une écriture comptable.

**Paramètres**
- `validee_par_id` (UUID, required) : ID de l'utilisateur validant l'écriture

### Rapports

#### GET /api/v1/comptabilite/grand-livre

Génère le grand livre.

**Paramètres**
- `compte_id` (UUID, optional) : Filtre par compte
- `date_debut` (date, optional) : Date de début
- `date_fin` (date, optional) : Date de fin

#### GET /api/v1/comptabilite/balance

Génère la balance générale.

**Paramètres**
- `date_debut` (date, optional) : Date de début
- `date_fin` (date, optional) : Date de fin

#### GET /api/v1/comptabilite/bilan

Génère le bilan comptable.

**Paramètres**
- `date_fin` (date, required) : Date de fin pour le bilan

#### GET /api/v1/comptabilite/compte-resultat

Génère le compte de résultat.

**Paramètres**
- `date_debut` (date, required) : Date de début de l'exercice
- `date_fin` (date, required) : Date de fin de l'exercice

## Intégration avec le Service Météo

Le module comptabilité intègre les données météorologiques pour :
1. Ajuster les prévisions de trésorerie
2. Analyser l'impact sur les coûts
3. Générer des recommandations adaptées

L'impact météo est calculé en prenant en compte :
- Les précipitations
- Les températures
- Les événements météorologiques exceptionnels

## Sécurité

Tous les endpoints nécessitent une authentification JWT et appliquent un contrôle d'accès basé sur les rôles (RBAC).

## Gestion des Erreurs

L'API utilise les codes d'erreur HTTP standards :
- 400 : Requête invalide
- 401 : Non authentifié
- 403 : Non autorisé
- 404 : Ressource non trouvée
- 500 : Erreur serveur

## Bonnes Pratiques

1. Validation des écritures :
   - Vérifier l'équilibre débit/crédit
   - Contrôler les dates d'exercice
   - Valider les références des comptes

2. Performance :
   - Utilisation du cache Redis
   - Pagination des résultats
   - Optimisation des requêtes

3. Intégration météo :
   - Mise à jour régulière des données
   - Calcul intelligent des impacts
   - Recommandations contextuelles
