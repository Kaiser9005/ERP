# Module Authentification - Documentation API

## Authentification

### POST /api/v1/auth/token
Authentification et obtention du token JWT.

**Corps de la requête:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Réponse:**
```json
{
  "access_token": "string",
  "token_type": "bearer"
}
```

## Utilisateurs

### POST /api/v1/auth/users
Création d'un nouvel utilisateur.

**Corps de la requête:**
```json
{
  "email": "user@example.com",
  "username": "string",
  "password": "string",
  "nom": "string",
  "prenom": "string",
  "role_id": "uuid"
}
```

### GET /api/v1/auth/users/me
Récupère les informations de l'utilisateur connecté.

## Rôles

### POST /api/v1/auth/roles
Création d'un nouveau rôle.

**Corps de la requête:**
```json
{
  "nom": "string",
  "description": "string",
  "type": "ADMIN",
  "permissions": ["PERMISSION_CODE1", "PERMISSION_CODE2"]
}
```

### GET /api/v1/auth/roles
Liste tous les rôles disponibles.

## Permissions

### POST /api/v1/auth/permissions
Création d'une nouvelle permission.

**Corps de la requête:**
```json
{
  "code": "string",
  "description": "string",
  "module": "string",
  "actions": {
    "create": true,
    "read": true,
    "update": true,
    "delete": false
  }
}
```