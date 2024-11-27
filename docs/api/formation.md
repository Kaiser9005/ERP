# API Formation

Cette API permet de gérer les formations, les sessions de formation, les participations et les évaluations.

## Formations

### GET /api/v1/hr/formation/formations/

Liste toutes les formations.

**Paramètres de requête :**
- `skip` (optionnel) : Nombre d'éléments à sauter (pagination)
- `limit` (optionnel) : Nombre maximum d'éléments à retourner
- `type` (optionnel) : Filtrer par type de formation (technique, securite, agricole)

**Réponse :** `200 OK`
```json
[
  {
    "id": "uuid",
    "titre": "Formation Sécurité",
    "description": "Description de la formation",
    "type": "securite",
    "duree": 8,
    "competences_requises": {},
    "competences_acquises": {},
    "materiel_requis": {},
    "conditions_meteo": {},
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### POST /api/v1/hr/formation/formations/

Crée une nouvelle formation.

**Corps de la requête :**
```json
{
  "titre": "Formation Sécurité",
  "description": "Description de la formation",
  "type": "securite",
  "duree": 8,
  "competences_requises": {},
  "competences_acquises": {},
  "materiel_requis": {},
  "conditions_meteo": {}
}
```

**Réponse :** `201 Created`

### GET /api/v1/hr/formation/formations/{formation_id}

Récupère les détails d'une formation.

**Réponse :** `200 OK`

### PUT /api/v1/hr/formation/formations/{formation_id}

Met à jour une formation.

**Corps de la requête :**
```json
{
  "titre": "Formation Sécurité Mise à Jour",
  "description": "Nouvelle description"
}
```

**Réponse :** `200 OK`

### DELETE /api/v1/hr/formation/formations/{formation_id}

Supprime une formation.

**Réponse :** `204 No Content`

## Sessions de Formation

### GET /api/v1/hr/formation/sessions/

Liste toutes les sessions de formation.

**Paramètres de requête :**
- `skip` (optionnel)
- `limit` (optionnel)
- `formation_id` (optionnel)
- `statut` (optionnel)
- `date_debut` (optionnel)

**Réponse :** `200 OK`
```json
[
  {
    "id": "uuid",
    "formation_id": "uuid",
    "date_debut": "2024-01-01T09:00:00Z",
    "date_fin": "2024-01-01T17:00:00Z",
    "lieu": "Salle de formation",
    "formateur": "Jean Dupont",
    "statut": "planifie",
    "nb_places": 10,
    "notes": "Notes sur la session",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "formation": {}
  }
]
```

### POST /api/v1/hr/formation/sessions/

Crée une nouvelle session de formation.

**Corps de la requête :**
```json
{
  "formation_id": "uuid",
  "date_debut": "2024-01-01T09:00:00Z",
  "date_fin": "2024-01-01T17:00:00Z",
  "lieu": "Salle de formation",
  "formateur": "Jean Dupont",
  "nb_places": 10,
  "notes": "Notes sur la session"
}
```

**Réponse :** `201 Created`

### GET /api/v1/hr/formation/sessions/{session_id}

Récupère les détails d'une session.

**Réponse :** `200 OK`

### PUT /api/v1/hr/formation/sessions/{session_id}

Met à jour une session.

**Réponse :** `200 OK`

### DELETE /api/v1/hr/formation/sessions/{session_id}

Supprime une session.

**Réponse :** `204 No Content`

## Participations

### GET /api/v1/hr/formation/participations/

Liste toutes les participations.

**Paramètres de requête :**
- `skip` (optionnel)
- `limit` (optionnel)
- `session_id` (optionnel)
- `employee_id` (optionnel)
- `statut` (optionnel)

**Réponse :** `200 OK`
```json
[
  {
    "id": "uuid",
    "session_id": "uuid",
    "employee_id": "uuid",
    "statut": "inscrit",
    "note": 85,
    "commentaires": "Très bonne participation",
    "certification_obtenue": true,
    "date_certification": "2024-01-01T17:00:00Z",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "session": {}
  }
]
```

### POST /api/v1/hr/formation/participations/

Crée une nouvelle participation.

**Corps de la requête :**
```json
{
  "session_id": "uuid",
  "employee_id": "uuid",
  "statut": "inscrit"
}
```

**Réponse :** `201 Created`

### GET /api/v1/hr/formation/participations/{participation_id}

Récupère les détails d'une participation.

**Réponse :** `200 OK`

### PUT /api/v1/hr/formation/participations/{participation_id}

Met à jour une participation.

**Réponse :** `200 OK`

### DELETE /api/v1/hr/formation/participations/{participation_id}

Supprime une participation.

**Réponse :** `204 No Content`

## Évaluations

### GET /api/v1/hr/formation/evaluations/

Liste toutes les évaluations.

**Paramètres de requête :**
- `skip` (optionnel)
- `limit` (optionnel)
- `employee_id` (optionnel)
- `evaluateur_id` (optionnel)
- `type` (optionnel)
- `statut` (optionnel)
- `date_debut` (optionnel)
- `date_fin` (optionnel)

**Réponse :** `200 OK`
```json
[
  {
    "id": "uuid",
    "employee_id": "uuid",
    "evaluateur_id": "uuid",
    "date_evaluation": "2024-01-01T14:00:00Z",
    "type": "formation",
    "periode_debut": "2024-01-01T09:00:00Z",
    "periode_fin": "2024-01-01T17:00:00Z",
    "competences": {},
    "objectifs": {},
    "performances": {},
    "points_forts": "Points forts notés",
    "points_amelioration": "Points à améliorer",
    "plan_action": "Plan d'action proposé",
    "note_globale": 85,
    "statut": "valide",
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
]
```

### POST /api/v1/hr/formation/evaluations/

Crée une nouvelle évaluation.

**Corps de la requête :**
```json
{
  "employee_id": "uuid",
  "evaluateur_id": "uuid",
  "date_evaluation": "2024-01-01T14:00:00Z",
  "type": "formation",
  "competences": {},
  "objectifs": {},
  "performances": {},
  "note_globale": 85
}
```

**Réponse :** `201 Created`

### GET /api/v1/hr/formation/evaluations/{evaluation_id}

Récupère les détails d'une évaluation.

**Réponse :** `200 OK`

### PUT /api/v1/hr/formation/evaluations/{evaluation_id}

Met à jour une évaluation.

**Réponse :** `200 OK`

### DELETE /api/v1/hr/formation/evaluations/{evaluation_id}

Supprime une évaluation.

**Réponse :** `204 No Content`

## Statistiques et Rapports

### GET /api/v1/hr/formation/employee/{employee_id}/formations

Récupère l'historique des formations d'un employé.

**Paramètres de requête :**
- `statut` (optionnel)
- `type` (optionnel)

**Réponse :** `200 OK`
```json
[
  {
    "formation": {},
    "session": {},
    "participation": {}
  }
]
```

### GET /api/v1/hr/formation/employee/{employee_id}/evaluations/summary

Récupère un résumé des évaluations d'un employé.

**Paramètres de requête :**
- `date_debut` (optionnel)
- `date_fin` (optionnel)

**Réponse :** `200 OK`
```json
{
  "nombre_evaluations": 5,
  "moyenne_globale": 85.5,
  "progression": 10,
  "points_forts": ["Point fort 1", "Point fort 2"],
  "points_amelioration": ["Point à améliorer 1", "Point à améliorer 2"]
}
```

### GET /api/v1/hr/formation/formations/{formation_id}/statistics

Récupère les statistiques d'une formation.

**Réponse :** `200 OK`
```json
{
  "nombre_sessions": 10,
  "nombre_participants": 50,
  "taux_reussite": 85.5,
  "note_moyenne": 82.3
}
