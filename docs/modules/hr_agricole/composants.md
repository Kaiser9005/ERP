# Composants RH Agricole

## CompetencesAgricoles

Composant principal pour la gestion des compétences agricoles.

### Utilisation

```typescript
import { CompetencesAgricoles } from '@components/hr/agricole/CompetencesAgricoles';

<CompetencesAgricoles employeId="123" />
```

### Props

| Prop | Type | Requis | Description |
|------|------|--------|-------------|
| employeId | UUID | Oui | Identifiant de l'employé |

### Fonctionnalités

- Affichage des compétences de l'employé
- Ajout/modification/suppression de compétences
- Validation des compétences
- Suivi des renouvellements

### Exemple

```typescript
import { CompetencesAgricoles } from '@components/hr/agricole/CompetencesAgricoles';
import { useEmploye } from '@hooks/useEmploye';

export const PageCompetences = () => {
  const { employeId } = useEmploye();
  
  return (
    <div>
      <h1>Compétences Agricoles</h1>
      <CompetencesAgricoles employeId={employeId} />
    </div>
  );
};
```

## CompetenceForm

Formulaire pour ajouter ou modifier une compétence.

### Utilisation

```typescript
import { CompetenceForm } from '@components/hr/agricole/CompetenceForm';

<CompetenceForm 
  employeId="123"
  competenceId="456" // optionnel, pour modification
  onSubmit={handleSubmit}
/>
```

### Props

| Prop | Type | Requis | Description |
|------|------|--------|-------------|
| employeId | UUID | Oui | Identifiant de l'employé |
| competenceId | UUID | Non | ID de la compétence (pour modification) |
| onSubmit | (data: CompetenceAgricoleCreate) => void | Oui | Callback de soumission |

### Champs du formulaire

- Nom de la compétence
- Description
- Niveau (débutant, intermédiaire, expert)
- Date d'obtention
- Date d'expiration
- Certifications associées

### Validation

- Nom requis
- Description min 10 caractères
- Niveau valide
- Date d'obtention antérieure à aujourd'hui
- Date d'expiration postérieure à la date d'obtention

### Exemple

```typescript
import { CompetenceForm } from '@components/hr/agricole/CompetenceForm';
import { createCompetence } from '@services/hr_agricole';

export const AjoutCompetence = () => {
  const handleSubmit = async (data) => {
    try {
      await createCompetence(data);
      // Succès
    } catch (error) {
      // Gestion erreur
    }
  };

  return (
    <div>
      <h2>Nouvelle Compétence</h2>
      <CompetenceForm 
        employeId="123"
        onSubmit={handleSubmit}
      />
    </div>
  );
};
```

## CompetencesList

Liste des compétences avec filtrage et tri.

### Utilisation

```typescript
import { CompetencesList } from '@components/hr/agricole/CompetencesList';

<CompetencesList 
  employeId="123"
  filtres={filtres}
  tri={tri}
  pagination={pagination}
/>
```

### Props

| Prop | Type | Requis | Description |
|------|------|--------|-------------|
| employeId | UUID | Oui | Identifiant de l'employé |
| filtres | FiltresRHAgricole | Non | Options de filtrage |
| tri | OptionsTriRHAgricole | Non | Options de tri |
| pagination | PaginationRHAgricole | Non | Options de pagination |

### Fonctionnalités

- Affichage en tableau ou grille
- Filtrage par type, niveau, statut
- Tri par nom, date, niveau
- Pagination
- Actions rapides (voir détails, modifier, supprimer)

### Exemple

```typescript
import { CompetencesList } from '@components/hr/agricole/CompetencesList';

export const ListeCompetences = () => {
  const [filtres, setFiltres] = useState<FiltresRHAgricole>({
    type: 'technique',
    niveau: 'expert',
    statut: 'actif'
  });

  const [tri, setTri] = useState<OptionsTriRHAgricole>({
    champ: 'nom',
    ordre: 'asc'
  });

  const [pagination, setPagination] = useState<PaginationRHAgricole>({
    page: 1,
    limite: 10
  });

  return (
    <div>
      <h2>Liste des Compétences</h2>
      <CompetencesList
        employeId="123"
        filtres={filtres}
        tri={tri}
        pagination={pagination}
      />
    </div>
  );
};
```

## Styles

Les composants utilisent Material-UI et des styles personnalisés :

```typescript
// Thème personnalisé
const theme = {
  colors: {
    primary: '#1976d2',
    secondary: '#dc004e',
    success: '#4caf50',
    warning: '#ff9800',
    error: '#f44336'
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px'
  }
};

// Styles communs
const commonStyles = {
  card: {
    padding: theme.spacing.md,
    marginBottom: theme.spacing.md,
    borderRadius: '4px',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: 500,
    marginBottom: theme.spacing.md
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: theme.spacing.md
  }
};
```

## Accessibilité

- Labels et ARIA labels
- Navigation au clavier
- Messages d'erreur explicites
- Contraste suffisant
- Support lecteur d'écran
