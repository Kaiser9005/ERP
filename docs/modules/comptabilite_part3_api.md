# Module Comptabilité (75%) - Partie 3 : API et Modèles

## API Endpoints

### Plan Comptable
```typescript
// Liste des comptes
GET /api/v1/comptabilite/comptes
Params: {
  type_compte?: TypeCompte;
  actif?: boolean;
  parent_id?: string;
}

// Création compte
POST /api/v1/comptabilite/comptes
Body: {
  numero: string;
  libelle: string;
  type_compte: TypeCompte;
  compte_parent_id?: string;
  description?: string;
}

// Détails compte
GET /api/v1/comptabilite/comptes/:id

// Mise à jour compte
PUT /api/v1/comptabilite/comptes/:id
Body: Partial<CompteComptableFormData>
```

### Écritures Comptables
```typescript
// Liste des écritures
GET /api/v1/comptabilite/ecritures
Params: {
  compte_id?: string;
  journal_id?: string;
  date_debut?: string;
  date_fin?: string;
  statut?: StatutEcriture;
}

// Création écriture
POST /api/v1/comptabilite/ecritures
Body: {
  date_ecriture: string;
  numero_piece: string;
  journal_id: string;
  lignes: Array<{
    compte_id: string;
    libelle: string;
    debit: number;
    credit: number;
  }>;
  piece_jointe?: File;
}

// Validation écriture
POST /api/v1/comptabilite/ecritures/:id/valider
Body: {
  validateur_id: string;
  commentaire?: string;
}

// Annulation écriture
POST /api/v1/comptabilite/ecritures/:id/annuler
Body: {
  motif: string;
  commentaire?: string;
}
```

### Journaux
```typescript
// Liste des journaux
GET /api/v1/comptabilite/journaux
Params: {
  type?: TypeJournal;
  actif?: boolean;
}

// Création journal
POST /api/v1/comptabilite/journaux
Body: {
  code: string;
  libelle: string;
  type_journal: TypeJournal;
  description?: string;
}

// Écritures d'un journal
GET /api/v1/comptabilite/journaux/:id/ecritures
Params: {
  date_debut?: string;
  date_fin?: string;
  statut?: StatutEcriture;
}
```

### États Financiers
```typescript
// Grand livre
GET /api/v1/comptabilite/grand-livre
Params: {
  compte_id?: string;
  date_debut: string;
  date_fin: string;
  format?: 'json' | 'pdf' | 'xlsx';
}

// Balance
GET /api/v1/comptabilite/balance
Params: {
  date_debut: string;
  date_fin: string;
  type_compte?: TypeCompte;
  format?: 'json' | 'pdf' | 'xlsx';
}

// Bilan
GET /api/v1/comptabilite/bilan
Params: {
  date: string;
  format?: 'json' | 'pdf' | 'xlsx';
}

// Compte de résultat
GET /api/v1/comptabilite/compte-resultat
Params: {
  date_debut: string;
  date_fin: string;
  format?: 'json' | 'pdf' | 'xlsx';
}
```

### Clôture
```typescript
// Clôture mensuelle
POST /api/v1/comptabilite/cloture/mensuelle
Body: {
  periode: string; // YYYY-MM
  validateur_id: string;
}

// Clôture annuelle
POST /api/v1/comptabilite/cloture/annuelle
Body: {
  exercice: string; // YYYY
  validateur_id: string;
}

// État clôture
GET /api/v1/comptabilite/cloture/etat
Params: {
  periode?: string;
  exercice?: string;
}
```

## Modèles de Données

### Types de Base
```typescript
type UUID = string;
type DateISO = string; // Format: YYYY-MM-DD
type DateTimeISO = string; // Format: YYYY-MM-DDTHH:mm:ss.sssZ
type Decimal = number; // Précision: 15,2
type JSONObject = Record<string, any>;

enum TypeCompte {
  ACTIF = 'ACTIF',
  PASSIF = 'PASSIF',
  CHARGE = 'CHARGE',
  PRODUIT = 'PRODUIT'
}

enum TypeJournal {
  ACHAT = 'ACHAT',
  VENTE = 'VENTE',
  BANQUE = 'BANQUE',
  CAISSE = 'CAISSE',
  OPERATIONS_DIVERSES = 'OPERATIONS_DIVERSES'
}

enum StatutEcriture {
  BROUILLON = 'BROUILLON',
  VALIDEE = 'VALIDEE',
  ANNULEE = 'ANNULEE'
}
```

### Interfaces Métier
```typescript
interface CompteComptable {
  id: UUID;
  numero: string;
  libelle: string;
  type_compte: TypeCompte;
  compte_parent_id?: UUID;
  solde_debit: Decimal;
  solde_credit: Decimal;
  actif: boolean;
  description?: string;
  metadata?: JSONObject;
}

interface EcritureComptable {
  id: UUID;
  date_ecriture: DateTimeISO;
  numero_piece: string;
  journal_id: UUID;
  lignes: Array<{
    compte_id: UUID;
    libelle: string;
    debit: Decimal;
    credit: Decimal;
  }>;
  statut: StatutEcriture;
  validee_par_id?: UUID;
  date_validation?: DateTimeISO;
  piece_jointe_url?: string;
  metadata?: JSONObject;
}

interface JournalComptable {
  id: UUID;
  code: string;
  libelle: string;
  type_journal: TypeJournal;
  actif: boolean;
  description?: string;
  metadata?: JSONObject;
}

interface LigneGrandLivre {
  date: DateISO;
  piece: string;
  journal: string;
  libelle: string;
  debit: Decimal;
  credit: Decimal;
  solde: Decimal;
}

interface CompteBalance {
  compte: {
    numero: string;
    libelle: string;
    type: TypeCompte;
  };
  debit: Decimal;
  credit: Decimal;
  solde: Decimal;
}

interface Bilan {
  actif: Record<string, {
    libelle: string;
    montant: Decimal;
    details: Array<{
      compte: string;
      montant: Decimal;
    }>;
  }>;
  passif: Record<string, {
    libelle: string;
    montant: Decimal;
    details: Array<{
      compte: string;
      montant: Decimal;
    }>;
  }>;
  total_actif: Decimal;
  total_passif: Decimal;
}
