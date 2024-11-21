# Module Inventaire

## Vue d'Ensemble
Le module Inventaire gère le suivi des stocks, les mouvements d'entrée/sortie et les statistiques associées pour l'exploitation agricole FOFAL.

## État d'Avancement : 35%
- Interface utilisateur de base ✅
- Gestion des stocks ✅
- Mouvements de stock ✅
- Statistiques de base ✅
- Système d'alertes ⏳
- Prévisions et optimisations ⏳
- Tests complets ⏳

## Composants

### 1. StatsInventaire
- Affichage des KPIs principaux
- Total des produits
- Valeur totale du stock
- Produits sous seuil d'alerte
- Mouvements récents
- Répartition par catégorie
- Évolution du stock

### 2. ListeStock
- Liste complète des produits en stock
- Filtrage par catégorie
- Filtrage par niveau de stock
- Affichage des seuils d'alerte
- Statut des stocks

### 3. HistoriqueMouvements
- Suivi des entrées/sorties
- Filtrage par type de mouvement
- Détails des mouvements
- Traçabilité des opérations

### 4. DialogueMouvementStock
- Saisie des mouvements de stock
- Validation des données
- Gestion des coûts unitaires
- Références des documents

## Types de Données

### Product
```typescript
{
  id: string;
  code: string;
  nom: string;
  description?: string;
  categorie: string;
  unite_mesure: string;
  prix_unitaire: number;
  seuil_alerte: number;
}
```

### StockMovement
```typescript
{
  id: string;
  date_mouvement: string;
  type_mouvement: 'ENTREE' | 'SORTIE';
  quantite: number;
  reference_document?: string;
  responsable: {
    id: string;
    nom: string;
    prenom: string;
  };
  produit_id: string;
  cout_unitaire?: number;
}
```

## Services API

### Produits
- GET /api/v1/inventaire/produits - Liste des produits
- GET /api/v1/inventaire/produits/:id - Détails d'un produit
- POST /api/v1/inventaire/produits - Création d'un produit
- PUT /api/v1/inventaire/produits/:id - Mise à jour d'un produit
- DELETE /api/v1/inventaire/produits/:id - Suppression d'un produit

### Mouvements
- GET /api/v1/inventaire/mouvements - Liste des mouvements
- POST /api/v1/inventaire/mouvements - Création d'un mouvement
- GET /api/v1/inventaire/produits/:id/mouvements - Mouvements d'un produit

### Statistiques
- GET /api/v1/inventaire/stats - Statistiques globales
- GET /api/v1/inventaire/produits/:id/stock - Niveau de stock d'un produit

## Sécurité
- Protection des routes avec ProtectedRoute
- Permissions requises :
  - INVENTAIRE_READ : Lecture des stocks
  - INVENTAIRE_WRITE : Modification des stocks
  - INVENTAIRE_ADMIN : Administration complète

## Prochaines Étapes (T2 2024)

### 1. Interface
- Gestion des emplacements de stockage
- Traçabilité par lot
- Rapports d'inventaire

### 2. Fonctionnalités
- Système d'alertes de stock
- Prévisions de consommation
- Optimisation des niveaux de stock

### 3. Tests
- Tests unitaires
- Tests d'intégration
- Tests E2E

### 4. Documentation
- Guide utilisateur
- Documentation technique
- Procédures d'inventaire
