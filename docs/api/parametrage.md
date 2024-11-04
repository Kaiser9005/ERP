# Module Paramétrage - Documentation API

## Paramètres Système

### GET /api/v1/parametrage/parametres
Récupère la liste des paramètres système.

**Paramètres de requête:**
- `module` (optionnel): Filtre par module
- `categorie` (optionnel): Filtre par catégorie

**Réponse:**
```json
[
  {
    "id": "uuid",
    "code": "DEVISE_DEFAUT",
    "libelle": "Devise par défaut",
    "description": "Devise utilisée par défaut dans le système",
    "type_parametre": "GENERAL",
    "module": null,
    "valeur": {
      "code": "XAF",
      "symbole": "FCFA"
    },
    "modifiable": true,
    "visible": true,
    "ordre": 1,
    "categorie": "FINANCE"
  }
]
```

### POST /api/v1/parametrage/parametres
Crée un nouveau paramètre.

### PUT /api/v1/parametrage/parametres/{parametre_id}
Met à jour un paramètre existant.

## Configuration des Modules

### GET /api/v1/parametrage/modules/configuration
Récupère la configuration de tous les modules.

### PUT /api/v1/parametrage/modules/{module}/configuration
Met à jour la configuration d'un module spécifique.

**Corps de la requête:**
```json
{
  "actif": true,
  "configuration": {
    "options": {
      "feature1": true,
      "feature2": false
    }
  },
  "ordre_affichage": 1,
  "icone": "agriculture",
  "couleur": "#4CAF50",
  "roles_autorises": ["ADMIN", "MANAGER"]
}
```