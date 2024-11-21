# API Projets

## Vue d'ensemble
L'API Projets fournit les endpoints nécessaires pour gérer les projets et leurs tâches associées dans l'ERP FOFAL.

## Endpoints

### Statistiques
```http
GET /api/v1/projects/stats
```
Retourne les statistiques globales des projets :
- Nombre de projets actifs
- Taux de complétion
- Répartition par statut
- Tendances et variations

### Projets

#### Liste des projets
```http
GET /api/v1/projects
```
Paramètres :
- `page` (optionnel): Numéro de page (défaut: 1)
- `size` (optionnel): Taille de page (défaut: 10)
- `status` (optionnel): Filtre par statut
- `search` (optionnel): Recherche textuelle

#### Détails d'un projet
```http
GET /api/v1/projects/{id}
```

#### Créer un projet
```http
POST /api/v1/projects
```
Corps de la requête :
```json
{
  "code": "string",
  "nom": "string",
  "description": "string",
  "date_debut": "date",
  "date_fin_prevue": "date",
  "statut": "PLANIFIE|EN_COURS|EN_PAUSE|TERMINE|ANNULE",
  "budget": "number",
  "responsable_id": "string"
}
```

#### Mettre à jour un projet
```http
PUT /api/v1/projects/{id}
```

#### Supprimer un projet
```http
DELETE /api/v1/projects/{id}
```

### Documents

#### Liste des documents
```http
GET /api/v1/projects/{id}/documents
```

#### Ajouter un document
```http
POST /api/v1/projects/{id}/documents
```
Type: `multipart/form-data`
Champs :
- `file`: Fichier
- `type`: Type de document

#### Supprimer un document
```http
DELETE /api/v1/projects/{id}/documents/{documentId}
```

### Statistiques et Rapports

#### Progression du projet
```http
GET /api/v1/projects/{id}/progress
```
Retourne :
- Pourcentage de complétion
- Nombre de tâches complétées
- Heures travaillées vs estimées

#### Timeline du projet
```http
GET /api/v1/projects/{id}/timeline
```
Retourne :
- Dates planifiées et réelles
- Jalons importants
- Progression temporelle

#### Analyse des risques
```http
GET /api/v1/projects/{id}/risks
```
Retourne :
- Nombre total de risques
- Répartition par priorité
- Statut des mitigations

## Modèles de Données

### Project
```typescript
interface Project {
  id: string;
  code: string;
  nom: string;
  description?: string;
  date_debut: string;
  date_fin_prevue: string;
  date_fin_reelle?: string;
  statut: ProjectStatus;
  budget?: number;
  responsable_id: string;
  objectifs?: Array<{
    description: string;
    criteres_succes?: string;
    date_cible?: string;
    statut?: string;
  }>;
  risques?: Array<{
    description: string;
    impact: 'FAIBLE' | 'MOYEN' | 'ELEVE';
    probabilite: 'FAIBLE' | 'MOYENNE' | 'ELEVEE';
    mitigation?: string;
    statut?: string;
  }>;
  created_at: string;
  updated_at: string;
}
```

### ProjectStats
```typescript
interface ProjectStats {
  projets_actifs: number;
  total_projets: number;
  variation_projets_actifs: number;
  taches_completees: number;
  total_taches: number;
  taches_retard: number;
  variation_taches_retard: number;
  heures_travaillees: number;
  variation_heures: number;
  repartition: {
    en_cours: number;
    en_attente: number;
    termines: number;
    en_retard: number;
  };
  taux_completion: number;
  projets_termines: number;
}
```

## Codes d'Erreur
- `400`: Requête invalide
- `401`: Non authentifié
- `403`: Non autorisé
- `404`: Ressource non trouvée
- `409`: Conflit (ex: code projet déjà utilisé)
- `500`: Erreur serveur

## Exemples d'Utilisation

### Créer un nouveau projet
```typescript
const response = await fetch('/api/v1/projects', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    code: 'PROJ-001',
    nom: 'Expansion Palmiers',
    description: 'Extension de la zone de culture',
    date_debut: '2024-01-01',
    date_fin_prevue: '2024-06-30',
    statut: 'PLANIFIE',
    budget: 50000,
    responsable_id: 'user-123'
  })
});
```

### Obtenir les statistiques
```typescript
const stats = await fetch('/api/v1/projects/stats').then(r => r.json());
