# Guide de Typage et Formulaires

## Conventions de Typage

### Types de Formulaires

#### 1. Séparation UI/API

Pour les formulaires qui nécessitent une transformation de données avant l'envoi à l'API, nous utilisons deux types distincts :

```typescript
// Type pour le formulaire (UI)
interface LeaveFormInputData {
  dateDebut: Date;        // Type Date pour les datepickers
  dateFin: Date;
  type: LeaveType;
  motif: string;
}

// Type pour l'API
interface LeaveFormData {
  dateDebut: string;      // Type string pour les dates ISO
  dateFin: string;
  type: LeaveType;
  motif: string;
  statut: LeaveStatus;    // Champs additionnels pour l'API
}
```

#### 2. Transformation des Données

La transformation des données se fait dans la mutation :

```typescript
const mutation = useMutation({
  mutationFn: (data: LeaveFormInputData) => createLeave({
    ...data,
    dateDebut: data.dateDebut.toISOString(),
    dateFin: data.dateFin.toISOString(),
    statut: 'en_attente'
  })
});
```

### Champs d'Audit

#### 1. Type de Base

```typescript
interface AuditFields {
  created_at?: string;
  updated_at?: string;
  created_by_id?: UUID;
  updated_by_id?: UUID;
  metadata?: Metadata;
}
```

#### 2. Utilisation avec les Entités

```typescript
type EmployeeFormData = Omit<Employee, 'id'> & Partial<AuditFields>;
```

### Validation avec Yup

#### 1. Schéma de Base

```typescript
const schema = yup.object().shape({
  // Champs requis
  matricule: yup.string().required('Le matricule est requis'),
  nom: yup.string().required('Le nom est requis'),
  
  // Énumérations
  statut: yup.string()
    .oneOf(['actif', 'conge', 'formation', 'inactif'])
    .default('actif'),
    
  // Tableaux
  competences: yup.array().of(yup.string().required()).default([]),
  
  // Objets imbriqués
  adresse: yup.object({
    rue: yup.string().required('L\'adresse est requise'),
    ville: yup.string().required('La ville est requise')
  }).optional()
});
```

#### 2. Validation de Dates

```typescript
const validateDateFin = (dateFin: Date) => {
  if (!dateDebut) return true;
  if (isBefore(dateFin, dateDebut)) {
    return "La date de fin doit être après la date de début";
  }
  return true;
};

const schema = yup.object().shape({
  dateDebut: yup.date()
    .required('La date de début est requise')
    .test('date-future', 'La date doit être dans le futur', 
      value => isAfter(value, new Date())),
  dateFin: yup.date()
    .required('La date de fin est requise')
    .test('date-after-debut', 'La date de fin doit être après la date de début',
      validateDateFin)
});
```

## Bonnes Pratiques

### 1. Types Stricts

- Éviter `any` et `unknown`
- Utiliser des types union pour les énumérations
- Définir des interfaces pour les structures complexes

### 2. Transformation de Données

- Transformer les données au plus près de l'API
- Documenter les transformations complexes
- Valider les données avant transformation

### 3. Validation

- Utiliser des messages d'erreur en français
- Centraliser les schémas de validation
- Réutiliser les validations communes

### 4. React Query

- Typer les clés de requête comme readonly
- Utiliser des types génériques pour les mutations
- Gérer les erreurs de manière typée

## Exemples

### Formulaire Complet

```typescript
// Types
interface FormData {
  date: Date;
  value: number;
}

interface ApiData {
  date: string;
  value: number;
}

// Composant
const MyForm: React.FC = () => {
  const mutation = useMutation({
    mutationFn: (data: FormData): Promise<ApiData> => ({
      ...data,
      date: data.date.toISOString()
    })
  });

  return (
    <form onSubmit={handleSubmit(data => mutation.mutate(data))}>
      {/* Implementation */}
    </form>
  );
};
```

### Requête avec Paramètres

```typescript
type QueryKey = readonly ['resource', string];

const useResource = (id: string) => {
  return useQuery({
    queryKey: ['resource', id] as const,
    queryFn: ({ queryKey }) => getResource(queryKey[1])
  });
};
