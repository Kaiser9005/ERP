# Module Finance (70%) - Documentation API - Modèles de Données

## Schéma Base de Données

### Table Transactions
```typescript
interface TransactionSchema {
  colonnes: {
    id: 'uuid PRIMARY KEY',
    reference: 'varchar(50) NOT NULL',
    type_transaction: 'transaction_type NOT NULL',
    montant: 'decimal(15,2) NOT NULL',
    devise: 'char(3) NOT NULL',
    date_transaction: 'timestamp NOT NULL',
    statut: 'transaction_status NOT NULL',
    description: 'text',
    compte_source_id: 'uuid REFERENCES comptes(id)',
    compte_destination_id: 'uuid REFERENCES comptes(id)',
    piece_jointe_url: 'varchar(255)',
    metadata: 'jsonb'
  };
  index: [
    'CREATE INDEX idx_transactions_reference ON transactions(reference)',
    'CREATE INDEX idx_transactions_date ON transactions(date_transaction)',
    'CREATE INDEX idx_transactions_type ON transactions(type_transaction)',
    'CREATE INDEX idx_transactions_statut ON transactions(statut)'
  ];
  contraintes: [
    'ALTER TABLE transactions ADD CONSTRAINT unique_reference UNIQUE (reference)',
    'ALTER TABLE transactions ADD CONSTRAINT check_montant CHECK (montant > 0)',
    'ALTER TABLE transactions ADD CONSTRAINT check_devise CHECK (devise ~ \'^[A-Z]{3}$\')'
  ];
}
```

### Table Comptes
```typescript
interface CompteSchema {
  colonnes: {
    id: 'uuid PRIMARY KEY',
    numero: 'varchar(20) NOT NULL',
    libelle: 'varchar(100) NOT NULL',
    type_compte: 'compte_type NOT NULL',
    devise: 'char(3) NOT NULL',
    solde: 'decimal(15,2) NOT NULL DEFAULT 0',
    actif: 'boolean NOT NULL DEFAULT true',
    date_ouverture: 'date NOT NULL',
    date_fermeture: 'date',
    metadata: 'jsonb'
  };
  index: [
    'CREATE INDEX idx_comptes_numero ON comptes(numero)',
    'CREATE INDEX idx_comptes_type ON comptes(type_compte)',
    'CREATE INDEX idx_comptes_actif ON comptes(actif) WHERE actif = true'
  ];
  contraintes: [
    'ALTER TABLE comptes ADD CONSTRAINT unique_numero UNIQUE (numero)',
    'ALTER TABLE comptes ADD CONSTRAINT check_devise CHECK (devise ~ \'^[A-Z]{3}$\')',
    'ALTER TABLE comptes ADD CONSTRAINT check_dates CHECK (date_fermeture IS NULL OR date_fermeture > date_ouverture)'
  ];
}
```

### Table Mouvements
```typescript
interface MouvementSchema {
  colonnes: {
    id: 'uuid PRIMARY KEY',
    transaction_id: 'uuid NOT NULL REFERENCES transactions(id)',
    compte_id: 'uuid NOT NULL REFERENCES comptes(id)',
    type_mouvement: 'mouvement_type NOT NULL',
    montant: 'decimal(15,2) NOT NULL',
    date_mouvement: 'timestamp NOT NULL',
    solde_avant: 'decimal(15,2) NOT NULL',
    solde_apres: 'decimal(15,2) NOT NULL',
    metadata: 'jsonb'
  };
  index: [
    'CREATE INDEX idx_mouvements_transaction ON mouvements(transaction_id)',
    'CREATE INDEX idx_mouvements_compte ON mouvements(compte_id)',
    'CREATE INDEX idx_mouvements_date ON mouvements(date_mouvement)'
  ];
  contraintes: [
    'ALTER TABLE mouvements ADD CONSTRAINT check_montant CHECK (montant > 0)',
    'ALTER TABLE mouvements ADD CONSTRAINT check_soldes CHECK (solde_apres = solde_avant + CASE WHEN type_mouvement = \'CREDIT\' THEN montant ELSE -montant END)'
  ];
}
```

## Types et Énumérations

### Types de Base
```typescript
type UUID = string;
type DateISO = string; // Format: YYYY-MM-DD
type DateTimeISO = string; // Format: YYYY-MM-DDTHH:mm:ss.sssZ
type Decimal = number; // Précision: 15,2
type JSONObject = Record<string, any>;

enum TypeTransaction {
  RECETTE = 'RECETTE',
  DEPENSE = 'DEPENSE',
  VIREMENT = 'VIREMENT'
}

enum StatutTransaction {
  EN_ATTENTE = 'EN_ATTENTE',
  VALIDEE = 'VALIDEE',
  REJETEE = 'REJETEE',
  ANNULEE = 'ANNULEE'
}

enum TypeCompteFinancier {
  BANQUE = 'BANQUE',
  CAISSE = 'CAISSE',
  EPARGNE = 'EPARGNE',
  CREDIT = 'CREDIT'
}

enum TypeMouvement {
  CREDIT = 'CREDIT',
  DEBIT = 'DEBIT'
}
```

### Interfaces Métier
```typescript
interface Transaction {
  id: UUID;
  reference: string;
  type_transaction: TypeTransaction;
  montant: Decimal;
  devise: string;
  date_transaction: DateTimeISO;
  statut: StatutTransaction;
  description?: string;
  compte_source_id?: UUID;
  compte_destination_id?: UUID;
  piece_jointe_url?: string;
  metadata?: JSONObject;
}

interface CompteFinancier {
  id: UUID;
  numero: string;
  libelle: string;
  type_compte: TypeCompteFinancier;
  devise: string;
  solde: Decimal;
  actif: boolean;
  date_ouverture: DateISO;
  date_fermeture?: DateISO;
  metadata?: JSONObject;
}

interface Mouvement {
  id: UUID;
  transaction_id: UUID;
  compte_id: UUID;
  type_mouvement: TypeMouvement;
  montant: Decimal;
  date_mouvement: DateTimeISO;
  solde_avant: Decimal;
  solde_apres: Decimal;
  metadata?: JSONObject;
}
