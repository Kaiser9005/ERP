# Module Inventaire

## Vue d'Ensemble
Le module Inventaire gère le suivi des stocks, les mouvements d'entrée/sortie et les statistiques associées pour l'exploitation agricole FOFAL.

## État d'Avancement : 85%
- Interface utilisateur de base ✅
- Gestion des stocks ✅
- Mouvements de stock ✅
- Statistiques de base ✅
- Système d'alertes ✅
- Traçabilité avancée ✅
- Intégration IoT ✅
- Contrôle qualité ✅
- Tests d'intégration ✅
- Prévisions et optimisations ⏳

## Composants

### 1. StatsInventaire
- Affichage des KPIs principaux
- Total des produits
- Valeur totale du stock
- Produits sous seuil d'alerte
- Mouvements récents
- Répartition par catégorie
- Évolution du stock
- Alertes conditions stockage
- État des capteurs IoT

### 2. ListeStock
- Liste complète des produits en stock
- Filtrage par catégorie
- Filtrage par niveau de stock
- Affichage des seuils d'alerte
- Statut des stocks
- Conditions de stockage en temps réel
- Certifications et traçabilité

### 3. HistoriqueMouvements
- Suivi des entrées/sorties
- Filtrage par type de mouvement
- Détails des mouvements
- Traçabilité des opérations
- Conditions pendant transport
- Résultats contrôles qualité

### 4. DialogueMouvementStock
- Saisie des mouvements de stock
- Validation des données
- Gestion des coûts unitaires
- Références des documents
- Saisie contrôle qualité
- Conditions de transport

## Types de Données

### Produit
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
  conditions_stockage: {
    temperature_min: number;
    temperature_max: number;
    humidite_min: number;
    humidite_max: number;
    luminosite_max?: number;
    ventilation_requise: boolean;
  };
}
```

### Stock
```typescript
{
  id: string;
  produit_id: string;
  entrepot_id: string;
  quantite: number;
  valeur_unitaire?: number;
  emplacement?: string;
  lot?: string;
  date_peremption?: string;
  origine?: string;
  certifications?: Array<{
    nom: string;
    organisme: string;
    date_obtention: string;
    date_expiration: string;
    specifications: any;
  }>;
  conditions_actuelles?: {
    temperature: number;
    humidite: number;
    luminosite?: number;
    qualite_air?: number;
    derniere_maj: string;
  };
  capteurs_id?: string[];
}
```

### MouvementStock
```typescript
{
  id: string;
  date_mouvement: string;
  type_mouvement: 'ENTREE' | 'SORTIE' | 'TRANSFERT';
  quantite: number;
  reference_document?: string;
  responsable: {
    id: string;
    nom: string;
    prenom: string;
  };
  produit_id: string;
  cout_unitaire?: number;
  conditions_transport?: {
    temperature: number;
    humidite: number;
  };
  controle_qualite?: {
    date_controle: string;
    responsable_id: string;
    resultats: any;
    conforme: boolean;
    actions_requises?: string;
  };
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

### Conditions & Qualité
- GET /api/v1/inventaire/stocks/:id/conditions - Conditions actuelles
- POST /api/v1/inventaire/stocks/:id/capteurs - Association capteurs IoT
- POST /api/v1/inventaire/stocks/:id/certifications - Ajout certification
- POST /api/v1/inventaire/controles - Création contrôle qualité

## Tests

### Tests d'Intégration
Le module dispose maintenant d'une suite complète de tests d'intégration :

#### Production-Inventaire
```python
# tests/integration/test_production_inventory_integration.py
- Test synchronisation production-stocks
- Test mise à jour automatique des niveaux
- Test alertes de réapprovisionnement
```

#### IoT-Inventaire
```python
# tests/integration/test_iot_inventory_integration.py
- Test monitoring conditions stockage
- Test alertes dépassement seuils
- Test historique conditions
```

#### Finance-Inventaire
```python
# tests/integration/test_inventory_finance_integration.py
- Test valorisation des stocks
- Test impact mouvements sur comptabilité
- Test calcul coûts stockage
```

#### ML-Inventaire
```python
# tests/integration/test_inventory_ml_integration.py
- Test prédictions consommation
- Test optimisation niveaux stocks
- Test détection anomalies
```

#### Qualité-Inventaire
```python
# tests/integration/test_inventory_quality_integration.py
- Test workflow contrôle qualité
- Test traçabilité lots
- Test gestion non-conformités
```

### Tests E2E
```python
# tests/e2e/test_iot_inventory_dashboard.py
- Test tableau de bord IoT
- Test interactions utilisateur
- Test alertes temps réel
```

## Sécurité
- Protection des routes avec ProtectedRoute
- Permissions requises :
  - INVENTAIRE_READ : Lecture des stocks
  - INVENTAIRE_WRITE : Modification des stocks
  - INVENTAIRE_ADMIN : Administration complète
  - INVENTAIRE_QUALITY : Gestion qualité

## Prochaines Étapes (T2 2024)

### 1. Interface
- Visualisation conditions stockage
- Tableaux de bord IoT
- Rapports qualité

### 2. Fonctionnalités
- Prévisions de consommation
- Optimisation des niveaux de stock
- Machine learning pour prédictions

### 3. Tests
- Tests de performance
- Tests de charge
- Tests de résilience

### 4. Documentation
- Guide utilisateur
- Documentation technique
- Procédures qualité
