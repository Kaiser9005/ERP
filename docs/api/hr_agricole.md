# API RH Agricole

## Vue d'ensemble

L'API RH Agricole gère les fonctionnalités spécifiques aux ressources humaines agricoles, notamment :
- Gestion des compétences agricoles
- Suivi des certifications
- Affectations aux parcelles
- Conditions de travail
- Formations spécialisées
- Évaluations agricoles

Base URL : `/api/v1/hr-agricole`

## Endpoints

### Compétences Agricoles

#### Créer une compétence
```http
POST /competences/
```
**Corps de la requête :**
```json
{
  "employe_id": "uuid",
  "specialite": "CULTURE",
  "niveau": "INTERMEDIAIRE",
  "cultures": ["tomates", "salades"],
  "equipements": ["tracteur", "système irrigation"],
  "date_acquisition": "2024-01-15",
  "validite": "2025-01-15",
  "commentaire": "Formation complète"
}
```

#### Récupérer une compétence
```http
GET /competences/{competence_id}
```

#### Récupérer les compétences d'un employé
```http
GET /employes/{employe_id}/competences/
```

#### Mettre à jour une compétence
```http
PUT /competences/{competence_id}
```

### Certifications Agricoles

#### Créer une certification
```http
POST /certifications/
```
**Corps de la requête :**
```json
{
  "competence_id": "uuid",
  "type_certification": "PHYTOSANITAIRE",
  "organisme": "CERTIPHYTO",
  "numero": "CERT-2024-001",
  "date_obtention": "2024-01-15",
  "date_expiration": "2026-01-15",
  "niveau": "Opérateur"
}
```

#### Récupérer une certification
```http
GET /certifications/{certification_id}
```

#### Récupérer les certifications d'une compétence
```http
GET /competences/{competence_id}/certifications/
```

#### Mettre à jour une certification
```http
PUT /certifications/{certification_id}
```

### Affectations Parcelles

#### Créer une affectation
```http
POST /affectations/
```
**Corps de la requête :**
```json
{
  "employe_id": "uuid",
  "parcelle_id": "uuid",
  "date_debut": "2024-01-15",
  "date_fin": "2024-06-15",
  "role": "Chef d'équipe",
  "responsabilites": ["supervision", "planification"],
  "objectifs": {
    "rendement": 85,
    "qualite": 90
  },
  "restrictions_meteo": ["pluie forte", "vent violent"],
  "equipements_requis": ["EPI complet", "radio"]
}
```

#### Récupérer une affectation
```http
GET /affectations/{affectation_id}
```

#### Récupérer les affectations d'un employé
```http
GET /employes/{employe_id}/affectations/
```

#### Récupérer les affectations d'une parcelle
```http
GET /parcelles/{parcelle_id}/affectations/
```

#### Mettre à jour une affectation
```http
PUT /affectations/{affectation_id}
```

### Conditions de Travail

#### Créer une condition de travail
```http
POST /conditions-travail/
```
**Corps de la requête :**
```json
{
  "employe_id": "uuid",
  "date": "2024-01-15",
  "temperature": 25.5,
  "humidite": 65,
  "precipitation": false,
  "vent": 15.2,
  "exposition_soleil": 240,
  "charge_physique": 7,
  "equipements_protection": ["chapeau", "gants", "lunettes"],
  "incidents": [
    {
      "type": "exposition_soleil",
      "duree": 30,
      "mesures_prises": ["pause", "hydratation"]
    }
  ]
}
```

#### Récupérer une condition de travail
```http
GET /conditions-travail/{condition_id}
```

#### Récupérer les conditions de travail d'un employé
```http
GET /employes/{employe_id}/conditions-travail/?date_debut=2024-01-01&date_fin=2024-01-31
```

#### Mettre à jour une condition de travail
```http
PUT /conditions-travail/{condition_id}
```

### Formations Agricoles

#### Créer une formation agricole
```http
POST /formations-agricoles/
```
**Corps de la requête :**
```json
{
  "formation_id": "uuid",
  "specialite": "CULTURE",
  "cultures_concernees": ["tomates", "salades"],
  "equipements_concernes": ["système irrigation", "serre"],
  "conditions_meteo": {
    "temperature_min": 15,
    "temperature_max": 30,
    "conditions_optimales": ["ensoleillé", "peu nuageux"]
  },
  "pratiques_specifiques": ["taille", "tuteurage"],
  "evaluation_terrain": true,
  "resultats_evaluation": {
    "pratique": 85,
    "theorie": 90
  }
}
```

#### Récupérer une formation agricole
```http
GET /formations-agricoles/{formation_id}
```

#### Récupérer les détails agricoles d'une formation
```http
GET /formations/{formation_id}/details-agricoles/
```

#### Mettre à jour une formation agricole
```http
PUT /formations-agricoles/{formation_id}
```

### Évaluations Agricoles

#### Créer une évaluation agricole
```http
POST /evaluations-agricoles/
```
**Corps de la requête :**
```json
{
  "evaluation_id": "uuid",
  "performances_cultures": {
    "tomates": {
      "rendement": 85,
      "qualite": 90,
      "techniques": ["taille", "tuteurage"]
    }
  },
  "maitrise_equipements": {
    "tracteur": "AVANCE",
    "irrigation": "EXPERT"
  },
  "respect_securite": {
    "epi": 95,
    "procedures": 90
  },
  "adaptabilite_meteo": {
    "pluie": "EXPERT",
    "chaleur": "AVANCE"
  },
  "gestion_ressources": {
    "eau": 85,
    "intrants": 90
  },
  "qualite_travail": {
    "precision": 85,
    "rapidite": 80
  }
}
```

#### Récupérer une évaluation agricole
```http
GET /evaluations-agricoles/{evaluation_id}
```

#### Récupérer les détails agricoles d'une évaluation
```http
GET /evaluations/{evaluation_id}/details-agricoles/
```

#### Mettre à jour une évaluation agricole
```http
PUT /evaluations-agricoles/{evaluation_id}
```

### Utilitaires

#### Vérifier la validité d'une compétence
```http
GET /competences/{competence_id}/validite/
```
**Réponse :**
```json
{
  "valide": true
}
```

#### Récupérer les compétences à renouveler
```http
GET /competences/a-renouveler/?delai_jours=30
```

#### Récupérer les certifications à renouveler
```http
GET /certifications/a-renouveler/?delai_jours=30
```

## Codes d'erreur

| Code | Description |
|------|-------------|
| 400  | Requête invalide |
| 404  | Ressource non trouvée |
| 422  | Erreur de validation |
| 500  | Erreur serveur |

## Types énumérés

### SpecialiteAgricole
- CULTURE
- ELEVAGE
- MARAICHAGE
- ARBORICULTURE
- MAINTENANCE
- LOGISTIQUE

### NiveauCompetence
- DEBUTANT
- INTERMEDIAIRE
- AVANCE
- EXPERT

### TypeCertification
- PHYTOSANITAIRE
- SECURITE
- CONDUITE_ENGINS
- BIO
- QUALITE

## Exemples d'utilisation

### Créer une compétence avec certification
```python
# 1. Créer la compétence
competence = requests.post("/api/v1/hr-agricole/competences/", json={
    "employe_id": "123e4567-e89b-12d3-a456-426614174000",
    "specialite": "CULTURE",
    "niveau": "AVANCE",
    "cultures": ["tomates", "salades"],
    "date_acquisition": "2024-01-15"
})

# 2. Ajouter une certification
certification = requests.post("/api/v1/hr-agricole/certifications/", json={
    "competence_id": competence.json()["id"],
    "type_certification": "PHYTOSANITAIRE",
    "organisme": "CERTIPHYTO",
    "date_obtention": "2024-01-15"
})
```

### Affecter un employé à une parcelle
```python
# Créer l'affectation
affectation = requests.post("/api/v1/hr-agricole/affectations/", json={
    "employe_id": "123e4567-e89b-12d3-a456-426614174000",
    "parcelle_id": "987fcdeb-51d3-12d3-a456-426614174000",
    "date_debut": "2024-01-15",
    "role": "Chef d'équipe"
})
```

### Suivre les conditions de travail
```python
# Enregistrer les conditions
conditions = requests.post("/api/v1/hr-agricole/conditions-travail/", json={
    "employe_id": "123e4567-e89b-12d3-a456-426614174000",
    "date": "2024-01-15",
    "temperature": 25.5,
    "humidite": 65,
    "charge_physique": 7
})
