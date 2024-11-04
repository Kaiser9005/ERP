# Module Projets - Documentation API

## Projets

### GET /api/v1/projects
Récupère la liste des projets.

**Paramètres de requête:**
- `statut` (optionnel): Filtre par statut
- `skip` (optionnel): Pagination
- `limit` (optionnel): Limite de résultats

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "PRJ001",
    "nom": "Extension Palmiers",
    "description": "Extension de la zone de culture",
    "date_debut": "2024-01-20",
    "date_fin_prevue": "2024-06-20",
    "statut": "EN_COURS",
    "budget": 50000000,
    "responsable_id": "uuid",
    "objectifs": [
      "Augmenter la surface cultivée de 20 hectares",
      "Installer le système d'irrigation"
    ]
  }
]
```

### POST /api/v1/projects
Crée un nouveau projet.

### GET /api/v1/projects/{project_id}
Récupère les détails d'un projet.

### PUT /api/v1/projects/{project_id}
Met à jour un projet existant.

## Tâches

### GET /api/v1/projects/{project_id}/tasks
Récupère les tâches d'un projet.

### POST /api/v1/projects/tasks
Crée une nouvelle tâche.

### PUT /api/v1/projects/tasks/{task_id}
Met à jour une tâche existante.

## Commentaires

### POST /api/v1/projects/tasks/{task_id}/comments
Ajoute un commentaire à une tâche.

## Documents

### POST /api/v1/projects/{project_id}/documents
Upload un document pour un projet.

**Corps de la requête:**
- Multipart form data avec le fichier
- `type` (optionnel): Type de document