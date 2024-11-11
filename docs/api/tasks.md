# API Gestion des Tâches

## Vue d'ensemble

Cette API fournit des endpoints pour gérer les tâches du projet, incluant la création, la mise à jour, la suppression et le suivi des tâches. Elle intègre également des fonctionnalités spécifiques pour la gestion des ressources et l'analyse des conditions météorologiques.

## Endpoints

### POST /api/v1/tasks

Crée une nouvelle tâche avec ses ressources et dépendances associées.

#### Corps de la requête

```json
{
    "title": "Plantation palmiers zone A",
    "description": "Planter 50 palmiers dans la zone A",
    "status": "A_FAIRE",
    "priority": "HAUTE",
    "category": "PLANTATION",
    "start_date": "2024-02-01T08:00:00Z",
    "due_date": "2024-02-03T17:00:00Z",
    "project_id": 1,
    "assigned_to": 2,
    "parcelle_id": 3,
    "weather_dependent": true,
    "min_temperature": 20,
    "max_temperature": 35,
    "max_wind_speed": 20,
    "max_precipitation": 5,
    "estimated_hours": 16,
    "resources": [
        {
            "resource_id": 1,
            "quantity_required": 50
        }
    ],
    "dependencies": [
        {
            "dependent_on_id": 2,
            "dependency_type": "finish_to_start"
        }
    ]
}
```

#### Réponse

```json
{
    "id": 1,
    "title": "Plantation palmiers zone A",
    "description": "Planter 50 palmiers dans la zone A",
    "status": "A_FAIRE",
    "priority": "HAUTE",
    "category": "PLANTATION",
    "start_date": "2024-02-01T08:00:00Z",
    "due_date": "2024-02-03T17:00:00Z",
    "project_id": 1,
    "assigned_to": 2,
    "parcelle_id": 3,
    "weather_dependent": true,
    "min_temperature": 20,
    "max_temperature": 35,
    "max_wind_speed": 20,
    "max_precipitation": 5,
    "estimated_hours": 16,
    "created_at": "2024-01-20T10:30:00Z",
    "updated_at": "2024-01-20T10:30:00Z"
}
```

### GET /api/v1/tasks/{task_id}

Récupère les détails d'une tâche spécifique.

#### Paramètres de chemin

- `task_id`: ID de la tâche à récupérer

#### Réponse

```json
{
    "id": 1,
    "title": "Plantation palmiers zone A",
    "status": "EN_COURS",
    "completion_percentage": 30,
    ...
}
```

### GET /api/v1/tasks/{task_id}/weather

Récupère une tâche avec analyse des conditions météo actuelles.

#### Paramètres de chemin

- `task_id`: ID de la tâche à analyser

#### Réponse

```json
{
    "id": 1,
    "title": "Plantation palmiers zone A",
    "weather_suitable": true,
    "weather_conditions": {
        "temperature": 25,
        "humidity": 70,
        "wind_speed": 15,
        "precipitation": 0
    },
    "weather_warnings": []
}
```

### PUT /api/v1/tasks/{task_id}

Met à jour une tâche existante.

#### Paramètres de chemin

- `task_id`: ID de la tâche à mettre à jour

#### Corps de la requête

```json
{
    "status": "EN_COURS",
    "completion_percentage": 50,
    "actual_hours": 8
}
```

### DELETE /api/v1/tasks/{task_id}

Supprime une tâche et libère ses ressources.

#### Paramètres de chemin

- `task_id`: ID de la tâche à supprimer

### GET /api/v1/projects/{project_id}/tasks

Récupère les tâches d'un projet avec pagination et filtres.

#### Paramètres de requête

- `page`: Numéro de page (défaut: 1)
- `size`: Taille de la page (défaut: 20, max: 100)
- `status`: Filtre par statut (optionnel)
- `category`: Filtre par catégorie (optionnel)

#### Réponse

```json
{
    "tasks": [
        {
            "id": 1,
            "title": "Plantation palmiers zone A",
            ...
        }
    ],
    "total": 45,
    "page": 1,
    "size": 20,
    "total_pages": 3
}
```

### POST /api/v1/tasks/{task_id}/comments

Ajoute un commentaire à une tâche.

#### Corps de la requête

```json
{
    "content": "Travaux commencés ce matin",
    "user_id": 1
}
```

### PUT /api/v1/tasks/{task_id}/resources/{resource_id}

Met à jour l'utilisation d'une ressource pour une tâche.

#### Paramètres de requête

- `quantity_used`: Quantité utilisée de la ressource

### GET /api/v1/tasks/{task_id}/dependencies

Récupère toutes les tâches qui dépendent de la tâche spécifiée.

### GET /api/v1/tasks/weather-dependent

Récupère toutes les tâches dépendantes de la météo avec leur statut actuel.

## Codes d'erreur

- `400 Bad Request`: Données invalides ou contraintes non respectées
- `404 Not Found`: Ressource non trouvée
- `409 Conflict`: Conflit avec l'état actuel des ressources

## Notes d'utilisation

- Les tâches météo-dépendantes sont automatiquement analysées avec les conditions météo actuelles
- La suppression d'une tâche libère automatiquement les ressources associées
- Les dépendances circulaires sont automatiquement détectées et empêchées
- La mise à jour du statut à "TERMINEE" met automatiquement le pourcentage de complétion à 100%

## Exemples d'utilisation

### Création d'une tâche avec ressources

```bash
curl -X POST "http://api.example.com/api/v1/tasks" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Plantation palmiers zone A",
         "category": "PLANTATION",
         "project_id": 1,
         "resources": [{"resource_id": 1, "quantity_required": 50}]
     }'
```

### Récupération des tâches météo-dépendantes

```bash
curl "http://api.example.com/api/v1/tasks/weather-dependent"
