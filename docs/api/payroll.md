# API de Gestion de la Paie

## Vue d'ensemble

L'API de gestion de la paie permet de gérer les fiches de paie des employés, incluant:
- Création et gestion des fiches de paie
- Calcul des salaires et cotisations
- Validation des paiements
- Statistiques et rapports

Base URL: `/api/v1/payroll`

## Endpoints

### Créer une fiche de paie

```http
POST /api/v1/payroll
```

Crée une nouvelle fiche de paie pour un contrat.

**Corps de la requête:**
```json
{
  "contract_id": "string",
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "worked_hours": 151.67,
  "overtime_hours": 10.0,
  "overtime_amount": 250.0,
  "bonus": 100.0,
  "deductions": 50.0,
  "bonus_details": {
    "prime_agricole": 100.0
  },
  "deduction_details": {
    "absence": 50.0
  },
  "employer_contributions": 500.0,
  "employee_contributions": 200.0
}
```

**Réponse:**
```json
{
  "id": "string",
  "contract_id": "string",
  "period_start": "2024-01-01",
  "period_end": "2024-01-31",
  "worked_hours": 151.67,
  "overtime_hours": 10.0,
  "base_salary": 2000.0,
  "overtime_amount": 250.0,
  "bonus": 100.0,
  "deductions": 50.0,
  "bonus_details": {
    "prime_agricole": 100.0
  },
  "deduction_details": {
    "absence": 50.0
  },
  "employer_contributions": 500.0,
  "employee_contributions": 200.0,
  "gross_total": 2300.0,
  "net_total": 2100.0,
  "is_paid": false,
  "payment_date": null,
  "created_at": "2024-01-01",
  "updated_at": "2024-01-01"
}
```

### Récupérer une fiche de paie

```http
GET /api/v1/payroll/{payroll_id}
```

Récupère les détails d'une fiche de paie spécifique.

**Paramètres:**
- `payroll_id`: ID de la fiche de paie

**Réponse:** Même format que la création

### Lister les fiches de paie d'un contrat

```http
GET /api/v1/payroll/contract/{contract_id}
```

Récupère toutes les fiches de paie associées à un contrat.

**Paramètres:**
- `contract_id`: ID du contrat

**Réponse:** Liste de fiches de paie

### Lister les fiches de paie par période

```http
GET /api/v1/payroll/period
```

Récupère les fiches de paie pour une période donnée.

**Paramètres de requête:**
- `start_date`: Date de début (YYYY-MM-DD)
- `end_date`: Date de fin (YYYY-MM-DD)

**Réponse:** Liste de fiches de paie

### Mettre à jour une fiche de paie

```http
PATCH /api/v1/payroll/{payroll_id}
```

Met à jour une fiche de paie existante.

**Corps de la requête:**
```json
{
  "worked_hours": 160.0,
  "overtime_hours": 15.0,
  "overtime_amount": 375.0,
  "bonus": 150.0,
  "deductions": 75.0,
  "bonus_details": {
    "prime_agricole": 150.0
  },
  "deduction_details": {
    "absence": 75.0
  }
}
```

**Réponse:** Fiche de paie mise à jour

### Valider une fiche de paie

```http
POST /api/v1/payroll/{payroll_id}/validate
```

Marque une fiche de paie comme payée.

**Réponse:**
```json
{
  "message": "Fiche de paie validée"
}
```

### Supprimer une fiche de paie

```http
DELETE /api/v1/payroll/{payroll_id}
```

Supprime une fiche de paie.

**Réponse:**
```json
{
  "message": "Fiche de paie supprimée"
}
```

### Statistiques de paie

```http
GET /api/v1/payroll/stats
```

Récupère les statistiques de paie pour une période.

**Paramètres de requête:**
- `start_date`: Date de début (YYYY-MM-DD)
- `end_date`: Date de fin (YYYY-MM-DD)

**Réponse:**
```json
{
  "total_gross": 50000.0,
  "total_net": 40000.0,
  "total_employer_contributions": 15000.0,
  "total_employee_contributions": 10000.0,
  "total_bonus": 2000.0,
  "total_deductions": 1000.0,
  "average_gross": 2500.0,
  "average_net": 2000.0,
  "period_start": "2024-01-01",
  "period_end": "2024-01-31"
}
```

### Calculer les heures supplémentaires

```http
POST /api/v1/payroll/{payroll_id}/calculate-overtime
```

Calcule le montant des heures supplémentaires.

**Paramètres de requête:**
- `hours`: Nombre d'heures supplémentaires

**Réponse:**
```json
{
  "overtime_hours": 10.0,
  "overtime_amount": 250.0
}
```

### Calculer les cotisations

```http
POST /api/v1/payroll/{payroll_id}/calculate-contributions
```

Calcule les cotisations sociales pour une fiche de paie.

**Réponse:**
```json
{
  "employer": 500.0,
  "employee": 200.0
}
```

## Codes d'erreur

- `400 Bad Request`: Données invalides
- `404 Not Found`: Ressource non trouvée
- `500 Internal Server Error`: Erreur serveur

## Notes

- Les montants sont en euros
- Les heures sont décimales (ex: 1h30 = 1.5)
- Le salaire de base est récupéré du contrat associé
- Les cotisations sont calculées automatiquement selon les taux en vigueur
