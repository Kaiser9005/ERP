# Module Comptabilité (75%) - Partie 2 : Technique et Intégration

## Tests et Validation

### Tests Unitaires
```typescript
describe('ComptabiliteService', () => {
  describe('Écritures', () => {
    it('valide une écriture équilibrée', async () => {
      const ecriture = {
        lignes: [
          { compte_id: '1', debit: 1000, credit: 0 },
          { compte_id: '2', debit: 0, credit: 1000 }
        ]
      };
      const result = await service.validerEcriture(ecriture);
      expect(result.statut).toBe('VALIDEE');
    });

    it('rejette une écriture non équilibrée', async () => {
      const ecriture = {
        lignes: [
          { compte_id: '1', debit: 1000, credit: 0 },
          { compte_id: '2', debit: 0, credit: 900 }
        ]
      };
      await expect(service.validerEcriture(ecriture))
        .rejects.toThrow('Écriture non équilibrée');
    });
  });

  describe('Clôture', () => {
    it('effectue la clôture mensuelle', async () => {
      const result = await service.clotureMensuelle('2024-01');
      expect(result.statut).toBe('CLOTURE');
      expect(result.ecritures_cloturees).toBeGreaterThan(0);
    });
  });
});
```

### Tests d'Intégration
```typescript
describe('Intégration Finance-Comptabilité', () => {
  it('génère les écritures depuis une transaction', async () => {
    // Création transaction
    const transaction = await financeService.createTransaction({
      type: 'RECETTE',
      montant: 1000,
      compte_destination_id: 'COMPTE1'
    });

    // Vérification écritures générées
    const ecritures = await comptaService.getEcrituresForTransaction(transaction.id);
    expect(ecritures).toHaveLength(2);
    expect(ecritures[0].debit).toBe(1000);
    expect(ecritures[1].credit).toBe(1000);
  });
});
```

## Workflow de Clôture

### Clôture Mensuelle
```typescript
interface ClotureMensuelle {
  etapes: {
    verification: {
      controles: [
        'Équilibre des journaux',
        'Séquence des pièces',
        'Lettrage complet',
        'Rapprochement bancaire'
      ];
      actions: [
        'Validation écritures en attente',
        'Génération écritures automatiques',
        'Calcul des totaux'
      ];
    };
    execution: {
      actions: [
        'Gel des écritures',
        'Reports à nouveau',
        'Génération états',
        'Archivage documents'
      ];
    };
    validation: {
      controles: [
        'Vérification balances',
        'Contrôle des reports',
        'Validation états'
      ];
    };
  };
  roles_requis: ['COMPTABLE', 'RESPONSABLE_COMPTA'];
  documents_generes: [
    'Balance mensuelle',
    'Grand livre',
    'États de synthèse',
    'Journal centralisateur'
  ];
}
```

### Clôture Annuelle
```typescript
interface ClotureAnnuelle extends ClotureMensuelle {
  etapes_supplementaires: {
    preparation: {
      actions: [
        'Inventaire physique',
        'Provisions',
        'Régularisations',
        'Amortissements'
      ];
    };
    fiscalite: {
      actions: [
        'Calcul résultat fiscal',
        'Détermination impôts',
        'États fiscaux',
        'Liasse fiscale'
      ];
    };
    ouverture: {
      actions: [
        'Reports à nouveau',
        'Reprise provisions',
        'Ouverture exercice',
        'Migration soldes'
      ];
    };
  };
  roles_requis: ['RESPONSABLE_COMPTA', 'DIRECTION'];
  documents_supplementaires: [
    'Bilan',
    'Compte résultat',
    'Annexes légales',
    'Liasse fiscale'
  ];
}
```

## Intégration Météo

### Impact sur les Comptes
```typescript
interface ImpactMeteo {
  provisions: {
    types: [
      'Risques climatiques',
      'Pertes sur récoltes',
      'Dégâts matériels'
    ];
    calcul: {
      facteurs: [
        'Historique météo',
        'Prévisions',
        'Vulnérabilité cultures'
      ];
      methode: 'Statistique' | 'Actuarielle';
    };
  };
  analytique: {
    axes: [
      'Conditions météo',
      'Impact production',
      'Coûts additionnels'
    ];
    ventilation: {
      criteres: [
        'Type événement',
        'Intensité',
        'Zone impact'
      ];
    };
  };
}
```

### Reporting Spécifique
```typescript
interface ReportingMeteo {
  indicateurs: {
    financiers: [
      'Coûts directs intempéries',
      'Pertes de production',
      'Provisions constituées'
    ];
    operationnels: [
      'Jours d\'interruption',
      'Surface impactée',
      'Rendement perdu'
    ];
  };
  analyses: {
    correlation: {
      variables: [
        'Conditions météo',
        'Performance financière',
        'Coûts maintenance'
      ];
      periode: 'mensuel' | 'trimestriel' | 'annuel';
    };
  };
}
```

## Maintenance et Optimisation

### Performance
```typescript
interface OptimisationPerformance {
  cache: {
    niveaux: [
      'Soldes comptes',
      'Totaux journaux',
      'États fréquents'
    ];
    strategie: {
      invalidation: 'temps' | 'événement';
      duree_vie: number;
    };
  };
  indexation: {
    champs: [
      'numero_compte',
      'date_ecriture',
      'journal_code'
    ];
    types: [
      'B-tree',
      'Hash',
      'GiST'
    ];
  };
  partitionnement: {
    criteres: [
      'date',
      'journal',
      'type_compte'
    ];
    strategie: 'range' | 'list' | 'hash';
  };
}
```

### Archivage
```typescript
interface StrategieArchivage {
  criteres: {
    age: 'supérieur à 2 ans';
    statut: 'clôturé';
    type: 'non courant';
  };
  methode: {
    format: 'PDF/A';
    compression: true;
    chiffrement: true;
  };
  retention: {
    legale: '10 ans';
    recommandee: '15 ans';
  };
  restauration: {
    delai: '48h max';
    procedure: string[];
  };
}
```

[Suite dans comptabilite_part3.md]
