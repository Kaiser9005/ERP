# Journal des modifications

## 25/12/2024 02:08

### Mise à jour des tests de ListeTransactions
- Fichier modifié : frontend/src/components/finance/__tests__/ListeTransactions.test.tsx
- Correction des imports pour utiliser les types depuis le fichier types/finance.ts
- Mise à jour des données mockées pour correspondre à l'interface TransactionListResponse
- Mise à jour des types de transactions pour utiliser les valeurs de l'enum TypeTransaction
- Mise à jour des types de statuts pour utiliser les valeurs de l'enum StatutTransaction
- Cette modification corrige les erreurs TS2345 dans ListeTransactions.test.tsx

## 25/12/2024 02:05

### Déplacement et mise à jour du test BudgetOverview
- Fichiers modifiés :
  - Déplacement de frontend/src/components/finance/__tests__/BudgetOverview.test.tsx vers frontend/src/components/comptabilite/__tests__/BudgetOverview.test.tsx
  - Mise à jour des imports pour utiliser getBudgetAnalysis du service comptabilite
  - Adaptation des tests pour correspondre à l'interface BudgetAnalysis
  - Cette modification corrige les erreurs TS2307 et TS2614 dans BudgetOverview.test.tsx

## 25/12/2024 02:02

### Mise à jour du composant GraphiqueTresorerie et ses tests
- Fichiers modifiés :
  - frontend/src/components/finance/GraphiqueTresorerie.tsx
  - frontend/src/components/finance/__tests__/GraphiqueTresorerie.test.tsx
- Adaptation du composant pour utiliser les propriétés de l'interface DonneesTresorerie
- Mise à jour des tests pour vérifier l'affichage des données de trésorerie
- Ajout de l'attente asynchrone dans les tests
- Cette modification corrige les erreurs TS2339 et TS7006 dans GraphiqueTresorerie.tsx

## 25/12/2024 01:46

### Mise à jour du composant PageFinance
- Fichier modifié : frontend/src/components/finance/PageFinance.tsx
- Correction de l'erreur TS6133 en renommant le paramètre 'event' en '_' dans handleChangementOnglet
- Ajout de la gestion des stats avec useState et useEffect
- Correction du passage des props au composant StatsFinance
- Cette modification corrige les erreurs TS6133 et TS2741 dans PageFinance.tsx

## 25/12/2024 00:34

### Mise à jour du composant StatsFinance et ses tests
- Fichiers modifiés :
  - frontend/src/components/dashboard/StatsFinance.tsx
  - frontend/src/components/dashboard/__tests__/StatsFinance.test.tsx
- Ajout de la gestion des valeurs manquantes avec affichage de 'N/A'
- Correction de l'utilisation de 'hausse' au lieu de 'increase'
- Correction de l'accès à 'valeur' au lieu de 'value'
- Ajout d'un test pour le cas où toutes les valeurs sont manquantes
- Amélioration de l'affichage conditionnel des Chips

## 25/12/2024 00:22

### Mise à jour du composant DocumentList et du service documents
- Fichiers modifiés :
  - frontend/src/services/documents.ts
  - frontend/src/components/documents/DocumentList.tsx
- Ajout des types et interfaces pour la gestion des documents
- Implémentation des fonctions getDocuments et deleteDocument
- Correction de la mutation de suppression pour passer les bons paramètres
- Cette modification corrige l'erreur TS2345 dans DocumentList.tsx

## 25/12/2024 00:21

### Mise à jour du composant DialogueMouvementStock
- Fichier modifié : frontend/src/components/inventaire/DialogueMouvementStock.tsx
- Ajout de l'import de useAuth
- Ajout de la vérification de l'utilisateur connecté
- Ajout du responsable_id dans la mutation de création de mouvement
- Cette modification corrige l'erreur TS2345 dans DialogueMouvementStock.tsx

## 25/12/2024 00:19

### Mise à jour de l'interface Produit
- Fichier modifié : frontend/src/types/inventaire.ts
- Ajout de la propriété quantite_stock de type number optionnel
- Cette modification corrige les erreurs liées à la propriété quantite_stock manquante

## 25/12/2024 00:15

### Mise à jour du composant JournauxList
- Fichier modifié : frontend/src/components/comptabilite/JournauxList.tsx
- Ajout de l'import de getJournalEcritures
- Mise à jour des méthodes handleOpenDialog et handleDateChange pour utiliser getJournalEcritures avec les dates de début et fin
- Cette modification corrige l'erreur TS2345 dans JournauxList.tsx

## 25/12/2024 00:12

### Correction de l'interface JournalComptable
- Fichier modifié : frontend/src/types/comptabilite.ts
- Correction de la propriété ecritures pour qu'elle soit de type EcritureComptable[]
- Suppression de la définition incorrecte de la méthode ecritures
- Cette modification corrige l'erreur TS2345 dans JournauxList.tsx

## 24/12/2024 23:46

### Mise à jour de l'interface Parcelle
- Fichier modifié : src/types/production.ts
- Ajout des propriétés manquantes pour le composant ParcelleMap :
  - code
  - culture_type
  - surface_hectares
  - statut
  - coordonnees_gps (latitude, longitude)
- Suppression des anciennes propriétés non utilisées :
  - nom
  - superficie
  - emplacement
  - type_sol

### Correction des chemins d'import
- Fichier modifié : src/components/production/ParcelleMap.tsx
- Remplacement du chemin absolu par un chemin relatif pour l'import du service api
