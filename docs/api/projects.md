# API Gestion de Projets

## Vue d'Ensemble
API REST pour la gestion des projets dans l'ERP FOFAL.

## Endpoints

### Projets

#### Créer un projet
```http
POST /api/v1/projects/
```

**Corps de la requête**
```json
{
  "code": "PROJ-2024-001",
  "nom": "Expansion Parcelle Sud",
  "description": "Extension de la zone de culture de palmiers",
  "date_debut": "2024-03-01",
  "date_fin_prevue": "2024-06-30",
  "responsable_id": "uuid",
  "budget_prevu": 5000000,
  "metadata": {
    "priorite": "HAUTE",
    "zone": "SUD",
    "type": "EXPANSION"
  }
}
```

**Réponse**
```json
{
  "id": "uuid",
  "code": "PROJ-2024-001",
  "nom": "Expansion Parcelle Sud",
  "statut": "PLANIFIE",
  ...
}
```

#### Lister les projets
```http
GET /api/v1/projects/
```

**Paramètres de requête**
- `statut` (optionnel): Filtrer par statut
- `responsable_id` (optionnel): Filtrer par responsable
- `date_debut` (optionnel): Date de début minimum
- `skip` (optionnel): Pagination - nombre d'éléments à sauter
- `limit` (optionnel): Pagination - nombre d'éléments à retourner

**Réponse**
```json
{
  "total": 45,
  "items": [
    {
      "id": "uuid",
      "code": "PROJ-2024-001",
      "nom": "Expansion Parcelle Sud",
      ...
    },
    ...
  ]
}
```

### Tâches

#### Créer une tâche
```http
POST /api/v1/projects/{project_id}/tasks/
```

**Corps de la requête**
```json
{
  "titre": "Préparation du terrain",
  "description": "Nettoyage et nivellement de la parcelle",
  "date_debut": "2024-03-01",
  "date_fin_prevue": "2024-03-15",
  "priorite": "HAUTE",
  "responsable_id": "uuid",
  "metadata": {
    "equipement_requis": ["tracteur", "niveleuse"],
    "surface": "5ha"
  }
}
```

#### Mettre à jour le statut d'une tâche
```http
PATCH /api/v1/projects/{project_id}/tasks/{task_id}/status
```

**Corps de la requête**
```json
{
  "statut": "EN_COURS",
  "notes": "Démarrage des travaux de nettoyage"
}
```

### Ressources

#### Affecter une ressource
```http
POST /api/v1/projects/{project_id}/resources/
```

**Corps de la requête**
```json
{
  "ressource_id": "uuid",
  "type_ressource": "EMPLOYE",
  "date_debut": "2024-03-01",
  "date_fin": "2024-03-15",
  "cout": 150000,
  "notes": "Affectation à temps plein"
}
```

### Documents

#### Ajouter un document
```http
POST /api/v1/projects/{project_id}/documents/
```

**Corps de la requête**
```json
{
  "nom": "Plan_Parcelle_Sud.pdf",
  "type": "PLAN",
  "description": "Plan détaillé de la nouvelle parcelle",
  "url": "https://storage.fofal.com/documents/plan_parcelle_sud.pdf"
}
```

## Modèles de Données

### Projet
```typescript
interface Projet {
  id: string;
  code: string;
  nom: string;
  description: string;
  date_debut: Date;
  date_fin_prevue: Date;
  date_fin_reelle?: Date;
  statut: 'PLANIFIE' | 'EN_COURS' | 'EN_PAUSE' | 'TERMINE' | 'ANNULE';
  responsable_id: string;
  budget_prevu: number;
  cout_reel: number;
  metadata: Record<string, any>;
}
```

### Tâche
```typescript
interface Tache {
  id: string;
  projet_id: string;
  titre: string;
  description: string;
  date_debut: Date;
  date_fin_prevue: Date;
  date_fin_reelle?: Date;
  priorite: 'BASSE' | 'MOYENNE' | 'HAUTE' | 'CRITIQUE';
  statut: 'A_FAIRE' | 'EN_COURS' | 'EN_REVUE' | 'TERMINE';
  responsable_id: string;
  parent_id?: string;
  ordre: number;
  metadata: Record<string, any>;
}
```

## Codes d'Erreur

| Code | Description |
|------|-------------|
| 400  | Données invalides |
| 401  | Non authentifié |
| 403  | Non autorisé |
| 404  | Ressource non trouvée |
| 409  | Conflit (ex: code projet déjà utilisé) |
| 422  | Erreur de validation |

## Notes d'Implémentation

### Sécurité
- Authentification JWT requise
- Vérification RBAC pour chaque opération
- Validation des données entrantes

### Performance
- Pagination par défaut : 50 éléments
- Cache des données fréquemment accédées
- Optimisation des requêtes imbriquées

### Bonnes Pratiques
- Utilisation des codes HTTP standards
- Versioning de l'API
- Documentation Swagger/OpenAPI
- Logs des opérations importantes
