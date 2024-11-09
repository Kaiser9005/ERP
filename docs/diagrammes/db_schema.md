# Schéma de Base de Données FOFAL ERP

## Vue d'Ensemble
Ce document présente la structure complète de la base de données de l'ERP FOFAL, incluant les relations entre les tables et les contraintes principales.

## Modules et Tables

### 1. Module Production

```mermaid
erDiagram
    PARCELLE ||--o{ CYCLE_CULTURE : contient
    PARCELLE ||--o{ RECOLTE : produit
    PARCELLE ||--o{ PRODUCTION_EVENT : enregistre
    PARCELLE {
        UUID id PK
        string code UK
        enum culture_type
        decimal surface_hectares
        date date_plantation
        enum statut
        json coordonnees_gps
        UUID responsable_id FK
        json metadata
    }
    CYCLE_CULTURE {
        UUID id PK
        UUID parcelle_id FK
        date date_debut
        date date_fin
        decimal rendement_prevu
        decimal rendement_reel
        text notes
        json metadata
    }
    RECOLTE {
        UUID id PK
        UUID parcelle_id FK
        UUID cycle_culture_id FK
        datetime date_recolte
        decimal quantite_kg
        enum qualite
        json conditions_meteo
        json equipe_recolte
        text notes
        json metadata
    }
    PRODUCTION_EVENT {
        UUID id PK
        UUID parcelle_id FK
        string type
        datetime date_debut
        datetime date_fin
        text description
        string statut
        UUID responsable_id FK
        json metadata
    }
```

### 2. Module Gestion de Projets

```mermaid
erDiagram
    PROJET ||--o{ TACHE : contient
    PROJET ||--o{ RESSOURCE_PROJET : utilise
    PROJET ||--o{ DOCUMENT_PROJET : possede
    PROJET {
        UUID id PK
        string code UK
        string nom
        text description
        date date_debut
        date date_fin_prevue
        date date_fin_reelle
        enum statut
        UUID responsable_id FK
        decimal budget_prevu
        decimal cout_reel
        json metadata
    }
    TACHE {
        UUID id PK
        UUID projet_id FK
        string titre
        text description
        date date_debut
        date date_fin_prevue
        date date_fin_reelle
        enum priorite
        enum statut
        UUID responsable_id FK
        UUID parent_id FK
        int ordre
        json metadata
    }
    RESSOURCE_PROJET {
        UUID id PK
        UUID projet_id FK
        UUID ressource_id FK
        enum type_ressource
        date date_debut
        date date_fin
        decimal cout
        text notes
        json metadata
    }
    DOCUMENT_PROJET {
        UUID id PK
        UUID projet_id FK
        string nom
        string type
        string url
        UUID auteur_id FK
        datetime date_creation
        text description
        json metadata
    }
```

### 3. Module Inventaire

```mermaid
erDiagram
    PRODUIT ||--o{ MOUVEMENT_STOCK : concerne
    PRODUIT ||--o{ STOCK : possede
    PRODUIT {
        UUID id PK
        string code UK
        string nom
        enum categorie
        string description
        enum unite_mesure
        float seuil_alerte
        float prix_unitaire
        json specifications
    }
    MOUVEMENT_STOCK {
        UUID id PK
        UUID produit_id FK
        enum type_mouvement
        float quantite
        UUID entrepot_source_id FK
        UUID entrepot_destination_id FK
        UUID responsable_id FK
        string reference_document
        text notes
        float cout_unitaire
        datetime date_mouvement
    }
    STOCK {
        UUID id PK
        UUID produit_id FK
        UUID entrepot_id FK
        float quantite
        float valeur_unitaire
        string emplacement
        string lot
        datetime date_derniere_maj
    }
```

### 4. Module Finance

```mermaid
erDiagram
    TRANSACTION ||--o{ LIGNE_TRANSACTION : contient
    COMPTE ||--o{ TRANSACTION : enregistre
    TRANSACTION {
        UUID id PK
        string reference UK
        datetime date_transaction
        enum type_transaction
        decimal montant
        string description
        UUID compte_id FK
        string statut
        json metadata
    }
    LIGNE_TRANSACTION {
        UUID id PK
        UUID transaction_id FK
        string description
        decimal montant
        UUID categorie_id FK
        json metadata
    }
    COMPTE {
        UUID id PK
        string numero UK
        string nom
        enum type_compte
        decimal solde
        boolean actif
        json metadata
    }
```

### 5. Module RH

```mermaid
erDiagram
    EMPLOYE ||--o{ PRESENCE : enregistre
    EMPLOYE ||--o{ CONGE : demande
    EMPLOYE {
        UUID id PK
        string matricule UK
        string nom
        string prenom
        date date_embauche
        enum statut
        json contact
        json metadata
    }
    PRESENCE {
        UUID id PK
        UUID employe_id FK
        datetime debut
        datetime fin
        enum type_presence
        text notes
        json metadata
    }
    CONGE {
        UUID id PK
        UUID employe_id FK
        date date_debut
        date date_fin
        enum type_conge
        string statut
        text motif
        json metadata
    }
```

### 6. Paramétrage

```mermaid
erDiagram
    PARAMETRE ||--o{ CONFIG_MODULE : configure
    PARAMETRE {
        UUID id PK
        string code UK
        string libelle
        string description
        enum type_parametre
        enum module
        json valeur
        boolean modifiable
        boolean visible
        int ordre
        string categorie
    }
    CONFIG_MODULE {
        UUID id PK
        enum module
        boolean actif
        json configuration
        int ordre_affichage
        string icone
        string couleur
        json roles_autorises
    }
```

## Notes Techniques

### Conventions
1. Clés Primaires
   - Utilisation d'UUID pour toutes les tables
   - Préfixe 'id_' pour les clés étrangères

2. Types de Données
   - Decimal pour les montants et quantités
   - JSON pour les données flexibles
   - Enum pour les valeurs prédéfinies

### Contraintes
1. Intégrité Référentielle
   - Suppression en cascade désactivée
   - Mise à jour en cascade activée

2. Indexation
   - Index sur les clés étrangères
   - Index sur les colonnes de recherche fréquente

### Optimisation
1. Performance
   - Partitionnement par date pour les grandes tables
   - Indexation adaptée aux requêtes fréquentes

2. Maintenance
   - Backup quotidien
   - Vacuum régulier
   - Monitoring des performances
