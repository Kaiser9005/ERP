# Module Inventaire

## Vue d'Ensemble
Le module Inventaire gère le suivi des stocks, les mouvements d'entrée/sortie et les statistiques associées pour l'exploitation agricole FOFAL.

## État d'Avancement : 95%
- Interface utilisateur de base ✅
- Gestion des stocks ✅
- Mouvements de stock ✅
- Statistiques de base ✅
- Système d'alertes ✅
- Traçabilité avancée ✅
- Intégration IoT ✅
- Contrôle qualité ✅
- Tests d'intégration ✅
- Prévisions et optimisations ✅
- Machine Learning ✅

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
- Prédictions ML

### 2. ListeStock
- Liste complète des produits en stock
- Filtrage par catégorie
- Filtrage par niveau de stock
- Affichage des seuils d'alerte
- Statut des stocks
- Conditions de stockage en temps réel
- Certifications et traçabilité
- Niveaux optimaux ML

### 3. HistoriqueMouvements
- Suivi des entrées/sorties
- Filtrage par type de mouvement
- Détails des mouvements
- Traçabilité des opérations
- Conditions pendant transport
- Résultats contrôles qualité
- Analyse patterns ML

### 4. DialogueMouvementStock
- Saisie des mouvements de stock
- Validation des données
- Gestion des coûts unitaires
- Références des documents
- Saisie contrôle qualité
- Conditions de transport
- Recommandations ML

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
  ml_config?: {
    modele_prediction: string;
    parametres_optimisation: any;
    seuils_qualite: any;
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
  ml_insights?: {
    niveau_optimal: number;
    risque_qualite: string;
    recommendations: string[];
    derniere_prediction: string;
  };
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
  ml_analyse?: {
    pattern_type: string;
    anomalie: boolean;
    impact_qualite: string;
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

### Machine Learning
- GET /api/v1/inventaire/stocks/:id/predictions - Prédictions ML
- GET /api/v1/inventaire/stocks/:id/optimisation - Niveaux optimaux
- GET /api/v1/inventaire/stocks/:id/qualite/risques - Risques qualité
- GET /api/v1/inventaire/stocks/:id/patterns - Analyse patterns
- POST /api/v1/inventaire/ml/train - Entraînement modèles

## Machine Learning

### Architecture ML
```python
services/inventory_ml/
├── __init__.py
├── base.py           # Modèle ML de base
├── optimization.py   # Optimisation des stocks
├── analysis.py      # Analyse des patterns
└── quality.py       # Prédiction qualité
```

### Fonctionnalités ML

#### 1. Prédiction Stock
```python
def predict_stock_optimal(stock: Stock, mouvements: List[MouvementStock]) -> Dict:
    """
    Prédit le niveau optimal de stock
    Returns:
        Dict contenant:
        - niveau_optimal: float
        - confiance: float
        - date_prediction: str
    """
```

#### 2. Optimisation Dynamique
```python
def optimize_stock_levels(
    stock: Stock,
    mouvements: List[MouvementStock],
    weather_data: Dict
) -> Dict:
    """
    Optimise les niveaux de stock
    Returns:
        Dict contenant:
        - niveau_optimal: float
        - niveau_min: float
        - niveau_max: float
        - ajustements: Dict
        - confiance: float
    """
```

#### 3. Analyse Patterns
```python
def analyze_stock_patterns(
    stock: Stock,
    mouvements: List[MouvementStock]
) -> Dict:
    """
    Analyse les patterns de stock
    Returns:
        Dict contenant:
        - tendance: str
        - force_tendance: float
        - saisonnalite: Dict
        - anomalies: List[Dict]
        - recommendations: List[str]
    """
```

#### 4. Prédiction Qualité
```python
def predict_quality_risk(
    stock: Stock,
    conditions_actuelles: Dict,
    historique_conditions: List[Dict]
) -> Dict:
    """
    Prédit les risques qualité
    Returns:
        Dict contenant:
        - niveau_risque: str
        - probabilite: float
        - facteurs_risque: List[Dict]
        - recommendations: List[str]
    """
```

## Tests

### Tests d'Intégration
Le module dispose d'une suite complète de tests d'intégration :

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
# tests/inventory_ml/
test_base.py          # Tests modèle base
test_optimization.py  # Tests optimisation
test_analysis.py      # Tests analyse patterns
test_quality.py       # Tests prédiction qualité
test_integration.py   # Tests intégration ML
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
  - INVENTAIRE_ML : Gestion ML

## Prochaines Étapes (T2 2024)

### 1. ML Avancé
- Apprentissage continu
- Détection anomalies avancée
- Prédictions multi-variables
- Auto-optimisation modèles

### 2. Interface
- Visualisation ML insights
- Tableaux de bord prédictifs
- Rapports ML personnalisés

### 3. Tests
- Tests ML robustesse
- Tests ML performance
- Tests ML dérive

### 4. Documentation
- Guide ML utilisateur
- Documentation ML technique
- Procédures ML maintenance
