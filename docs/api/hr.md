# API RH

## Types

### LeaveFormData
```typescript
interface LeaveFormData {
  type: LeaveType;
  dateDebut: string;
  dateFin: string;
  motif: string;
  statut: LeaveStatus;
}
```

### LeaveFormInputData
```typescript
interface LeaveFormInputData {
  type: LeaveType;
  dateDebut: Date;
  dateFin: Date;
  motif: string;
}
```

### EmployeeFormData
```typescript
type EmployeeFormData = Omit<Employee, 'id'> & {
  competences: string[];
  formation?: Formation & {
    diplomes: string[];
    certifications: string[];
  };
  adresse?: Address;
  metadata?: Metadata;
} & Partial<AuditFields>;
```

## Endpoints

### GET /api/v1/hr/employes
Récupère la liste des employés avec pagination.

**Paramètres**
- search?: string
- departement?: string
- statut?: string
- page?: number
- pageSize?: number

**Réponse**
```typescript
interface EmployeeListResponse {
  items: Employee[];
  total: number;
  page: number;
  pageSize: number;
}
```

### GET /api/v1/hr/employes/:id
Récupère les détails d'un employé.

**Réponse**
```typescript
Employee
```

### POST /api/v1/hr/employes
Crée un nouvel employé.

**Corps de la requête**
```typescript
Omit<Employee, 'id'>
```

**Réponse**
```typescript
Employee
```

### PATCH /api/v1/hr/employes/:id
Met à jour un employé existant.

**Corps de la requête**
```typescript
Partial<Employee>
```

**Réponse**
```typescript
Employee
```

### DELETE /api/v1/hr/employes/:id
Supprime un employé.

### GET /api/v1/hr/conges
Récupère la liste des congés.

**Paramètres**
- employeeId?: UUID
- statut?: LeaveStatus
- dateDebut?: string
- dateFin?: string

**Réponse**
```typescript
Leave[]
```

### POST /api/v1/hr/conges
Crée une nouvelle demande de congé.

**Corps de la requête**
```typescript
LeaveFormData
```

**Réponse**
```typescript
Leave
```

### PATCH /api/v1/hr/conges/:id
Met à jour une demande de congé.

**Corps de la requête**
```typescript
Partial<LeaveFormData>
```

**Réponse**
```typescript
Leave
```

### POST /api/v1/hr/conges/:id/approve
Approuve une demande de congé.

**Réponse**
```typescript
Leave
```

### POST /api/v1/hr/conges/:id/reject
Rejette une demande de congé.

**Corps de la requête**
```typescript
{
  motif: string;
}
```

**Réponse**
```typescript
Leave
```

### GET /api/v1/hr/stats
Récupère les statistiques RH.

**Réponse**
```typescript
EmployeeStats
```

### GET /api/v1/hr/employes/export
Exporte les données des employés.

**Paramètres**
- format: 'csv' | 'xlsx'

**Réponse**
Blob (fichier)

### POST /api/v1/hr/employes/import
Importe des données d'employés.

**Corps de la requête**
FormData avec fichier

**Réponse**
```typescript
{
  imported: number;
  errors: string[];
}
