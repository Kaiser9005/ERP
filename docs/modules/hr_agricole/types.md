# Types RH Agricole

## Types de Base

```typescript
type UUID = string;
type NiveauCompetence = 'debutant' | 'intermediaire' | 'expert';
type TypeAffectation = 'principale' | 'secondaire' | 'temporaire';
type StatutAffectation = 'active' | 'planifiee' | 'terminee';
```

## Interfaces Compétences

```typescript
interface CompetenceAgricole {
  id: UUID;
  nom: string;
  description: string;
  niveau: NiveauCompetence;
  dateObtention: string;
  dateExpiration: string;
  employeId: UUID;
  certifications: CertificationAgricole[];
  createdAt: string;
  updatedAt: string;
}

interface CompetenceAgricoleCreate {
  nom: string;
  description: string;
  niveau: NiveauCompetence;
  dateObtention: string;
  dateExpiration: string;
  employeId: UUID;
}

interface CompetenceAgricoleUpdate {
  nom?: string;
  description?: string;
  niveau?: NiveauCompetence;
  dateObtention?: string;
  dateExpiration?: string;
}
```

## Interfaces Certifications

```typescript
interface CertificationAgricole {
  id: UUID;
  nom: string;
  organisme: string;
  dateObtention: string;
  dateExpiration: string;
  competenceId: UUID;
  fichiers: string[];
  createdAt: string;
  updatedAt: string;
}

interface CertificationAgricoleCreate {
  nom: string;
  organisme: string;
  dateObtention: string;
  dateExpiration: string;
  competenceId: UUID;
  fichiers?: string[];
}

interface CertificationAgricoleUpdate {
  nom?: string;
  organisme?: string;
  dateObtention?: string;
  dateExpiration?: string;
  fichiers?: string[];
}
```

## Interfaces Affectations

```typescript
interface AffectationParcelle {
  id: UUID;
  employeId: UUID;
  parcelleId: UUID;
  dateDebut: string;
  dateFin: string;
  type: TypeAffectation;
  statut: StatutAffectation;
  createdAt: string;
  updatedAt: string;
}

interface AffectationParcelleCreate {
  employeId: UUID;
  parcelleId: UUID;
  dateDebut: string;
  dateFin: string;
  type: TypeAffectation;
}

interface AffectationParcelleUpdate {
  dateDebut?: string;
  dateFin?: string;
  type?: TypeAffectation;
  statut?: StatutAffectation;
}
```

## Interfaces Statistiques

```typescript
interface StatistiquesCompetences {
  total: number;
  parNiveau: {
    debutant: number;
    intermediaire: number;
    expert: number;
  };
  aRenouveler: number;
  expirees: number;
}

interface StatistiquesCertifications {
  total: number;
  valides: number;
  expirees: number;
  aRenouveler: number;
  parOrganisme: Record<string, number>;
}

interface StatistiquesFormations {
  total: number;
  enCours: number;
  terminees: number;
  planifiees: number;
  tauxReussite: number;
}

interface StatistiquesConditionsTravail {
  totalHeures: number;
  moyenneHeuresParJour: number;
  conditionsMeteo: {
    favorable: number;
    defavorable: number;
  };
  incidents: number;
}
```

## Interfaces Utilitaires

```typescript
interface ValidationCompetence {
  valide: boolean;
  dateExpiration: string;
  joursRestants: number;
  avertissements: string[];
}

interface CompetenceARenouveler {
  id: UUID;
  nom: string;
  dateExpiration: string;
  joursRestants: number;
  employeId: UUID;
  employeNom: string;
}

interface CertificationARenouveler {
  id: UUID;
  nom: string;
  organisme: string;
  dateExpiration: string;
  joursRestants: number;
  competenceId: UUID;
  competenceNom: string;
}
```

## Interfaces Recherche

```typescript
interface FiltresRHAgricole {
  type?: string;
  niveau?: NiveauCompetence;
  statut?: string;
  dateDebut?: string;
  dateFin?: string;
  recherche?: string;
}

interface OptionsTriRHAgricole {
  champ: string;
  ordre: 'asc' | 'desc';
}

interface PaginationRHAgricole {
  page: number;
  limite: number;
}
