# Module Comptabilité (75%) - Partie 1 : Fondamentaux

## Vue d'ensemble

Le module Comptabilité gère la comptabilité générale et analytique de FOFAL, notamment :
- Plan comptable
- Écritures comptables
- Grand livre et balance
- États financiers réglementaires
- Rapports comptables

## Architecture

### Composants Principaux

#### 1. Plan Comptable
- Structure hiérarchique des comptes
- Gestion des comptes généraux
- Comptes auxiliaires
- Paramétrage comptable
- Règles de validation

#### 2. Écritures Comptables
- Saisie des écritures
- Validation et contrôles
- Lettrage automatique et manuel
- Gestion des pièces justificatives
- Historique des modifications

#### 3. Journaux
- Journal des achats
- Journal des ventes
- Journal de banque
- Journal des opérations diverses
- Contrôles de cohérence

#### 4. États Financiers
- Grand livre
- Balance âgée
- Bilan
- Compte de résultat
- Annexes réglementaires

## Implémentation Technique

### Services
```typescript
// Service comptabilité
const comptabiliteService = {
  // Plan comptable
  getComptes(): Promise<CompteComptable[]>;
  createCompte(data: CompteComptableFormData): Promise<CompteComptable>;
  updateCompte(id: string, data: Partial<CompteComptable>): Promise<CompteComptable>;
  
  // Écritures
  getEcritures(params?: ComptabiliteFilters): Promise<EcritureComptable[]>;
  createEcriture(data: EcritureComptableFormData): Promise<EcritureComptable>;
  validerEcriture(id: string, validateur_id: string): Promise<EcritureComptable>;
  
  // États
  getGrandLivre(params: GrandLivreParams): Promise<LigneGrandLivre[]>;
  getBalance(params: BalanceParams): Promise<CompteBalance[]>;
  getBilan(date: string): Promise<Bilan>;
  getCompteResultat(debut: string, fin: string): Promise<CompteResultat>;
}
```

### Composants React
```typescript
// Composants principaux
const ComptabilitePage: React.FC = () => {
  // Page principale comptabilité
};

const PlanComptable: React.FC = () => {
  // Gestion du plan comptable
};

const SaisieEcriture: React.FC = () => {
  // Saisie des écritures comptables
};

const GrandLivre: React.FC = () => {
  // Consultation du grand livre
};

const Balance: React.FC = () => {
  // Balance des comptes
};

const Bilan: React.FC = () => {
  // États financiers
};
```

## Intégration avec la Finance

### Réception des Transactions
- Conversion automatique en écritures
- Contrôles de cohérence
- Validation comptable
- Traçabilité complète

### Rapprochement
- Rapprochement bancaire
- Lettrage automatique
- Gestion des écarts
- Historique des rapprochements

## Impact Météorologique

### Traitement Comptable
- Provisions pour risques météo
- Ventilation analytique
- Impact sur les résultats
- Indicateurs spécifiques

### Reporting Spécifique
- Annexes dédiées
- Analyses d'impact
- Indicateurs météo
- Recommandations

## Sécurité et Contrôles

### Droits d'Accès
```typescript
enum PermissionComptabilite {
  LECTURE = 'comptabilite:lecture',
  SAISIE = 'comptabilite:saisie',
  VALIDATION = 'comptabilite:validation',
  CLOTURE = 'comptabilite:cloture',
  ADMIN = 'comptabilite:admin'
}

interface RoleComptabilite {
  code: string;
  permissions: PermissionComptabilite[];
  limites?: {
    montant_max?: number;
    validation_requise?: boolean;
    journaux_autorises?: string[];
  };
}
```

### Contrôles Automatiques
```typescript
interface ControleComptable {
  type: 'equilibre' | 'sequence' | 'compte' | 'montant';
  niveau: 'warning' | 'error';
  message: string;
  condition: (data: any) => boolean;
}

const controles: ControleComptable[] = [
  {
    type: 'equilibre',
    niveau: 'error',
    message: 'L\'écriture doit être équilibrée',
    condition: (ecriture) => ecriture.debit === ecriture.credit
  },
  // ...autres contrôles
];
```

[Suite dans comptabilite_part2.md]