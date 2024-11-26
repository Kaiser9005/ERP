# API Contrats

Cette documentation décrit les endpoints de l'API pour la gestion des contrats.

## Endpoints

### Récupérer tous les contrats actifs

```http
GET /hr/contracts/active
```

Retourne la liste de tous les contrats actifs.

#### Réponse

```json
[
  {
    "id": "string",
    "employee_id": "string",
    "employee_name": "string",
    "type": "string",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "wage": 2500,
    "position": "string",
    "department": "string",
    "is_active": true,
    "created_at": "2024-01-01",
    "updated_at": "2024-01-01"
  }
]
```

### Récupérer un contrat spécifique

```http
GET /hr/contracts/{contract_id}
```

Retourne les détails d'un contrat spécifique.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| contract_id | string | L'identifiant unique du contrat |

#### Réponse

```json
{
  "id": "string",
  "employee_id": "string",
  "employee_name": "string",
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string",
  "is_active": true,
  "created_at": "2024-01-01",
  "updated_at": "2024-01-01"
}
```

### Récupérer les contrats d'un employé

```http
GET /hr/contracts/employee/{employee_id}
```

Retourne tous les contrats associés à un employé spécifique.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| employee_id | string | L'identifiant unique de l'employé |

#### Réponse

```json
[
  {
    "id": "string",
    "employee_id": "string",
    "employee_name": "string",
    "type": "string",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "wage": 2500,
    "position": "string",
    "department": "string",
    "is_active": true,
    "created_at": "2024-01-01",
    "updated_at": "2024-01-01"
  }
]
```

### Créer un nouveau contrat

```http
POST /hr/contracts
```

Crée un nouveau contrat.

#### Corps de la requête

```json
{
  "employee_id": "string",
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string"
}
```

#### Réponse

```json
{
  "id": "string",
  "employee_id": "string",
  "employee_name": "string",
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string",
  "is_active": true,
  "created_at": "2024-01-01",
  "updated_at": "2024-01-01"
}
```

### Mettre à jour un contrat

```http
PATCH /hr/contracts/{contract_id}
```

Met à jour les informations d'un contrat existant.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| contract_id | string | L'identifiant unique du contrat |

#### Corps de la requête

```json
{
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string",
  "is_active": true
}
```

#### Réponse

```json
{
  "id": "string",
  "employee_id": "string",
  "employee_name": "string",
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string",
  "is_active": true,
  "created_at": "2024-01-01",
  "updated_at": "2024-01-01"
}
```

### Terminer un contrat

```http
POST /hr/contracts/{contract_id}/terminate
```

Termine un contrat existant en définissant sa date de fin et en le marquant comme inactif.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| contract_id | string | L'identifiant unique du contrat |

#### Corps de la requête

```json
{
  "end_date": "2024-12-31"
}
```

#### Réponse

```json
{
  "id": "string",
  "employee_id": "string",
  "employee_name": "string",
  "type": "string",
  "start_date": "2024-01-01",
  "end_date": "2024-12-31",
  "wage": 2500,
  "position": "string",
  "department": "string",
  "is_active": false,
  "created_at": "2024-01-01",
  "updated_at": "2024-01-01"
}
```

### Récupérer les contrats qui expirent bientôt

```http
GET /hr/contracts/expiring/{days}
```

Retourne la liste des contrats qui expirent dans le nombre de jours spécifié.

#### Paramètres

| Nom | Type | Description |
|-----|------|-------------|
| days | integer | Nombre de jours avant expiration |

#### Réponse

```json
[
  {
    "id": "string",
    "employee_id": "string",
    "employee_name": "string",
    "type": "string",
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "wage": 2500,
    "position": "string",
    "department": "string",
    "is_active": true,
    "created_at": "2024-01-01",
    "updated_at": "2024-01-01"
  }
]
```

## Codes d'erreur

| Code | Description |
|------|-------------|
| 400 | Requête invalide (données manquantes ou invalides) |
| 404 | Contrat ou employé non trouvé |
| 409 | Conflit (par exemple, tentative de créer un contrat en doublon) |
| 500 | Erreur serveur interne |
