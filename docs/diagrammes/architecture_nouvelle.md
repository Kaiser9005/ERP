# Nouvelle Architecture FOFAL ERP

## Vue d'Ensemble

```mermaid
graph TB
    subgraph "Frontend (React/TypeScript)"
        A[Components] --> B[Services API]
        A --> C[Types]
        A --> D[Routes]
        A --> E[Utils]
        
        subgraph "Components par Module"
            F[Common]
            G[Dashboard]
            H[Finance]
            I[HR]
            J[Inventory]
            K[Production]
        end
    end

    subgraph "Backend (FastAPI/Python)"
        L[API] --> M[Services]
        L --> N[Models]
        L --> O[Schemas]
        
        subgraph "Services"
            P[Module Services]
            Q[ML Services]
            R[Core Services]
        end
        
        subgraph "ML Services"
            S[Inventory ML]
            T[Production ML]
            U[Projects ML]
        end
    end

    subgraph "Infrastructure"
        V[PostgreSQL]
        W[Redis Cache]
        X[External APIs]
    end

    B -->|API Calls| L
    M --> V
    M --> W
    M --> X
```

## Structure Détaillée

### Frontend

```mermaid
graph TB
    subgraph "src/"
        A[components/] --> B[common/]
        A --> C[dashboard/]
        A --> D[finance/]
        A --> E[hr/]
        A --> F[inventory/]
        A --> G[production/]
        
        H[services/] --> I[API Services]
        H --> J[Utils Services]
        
        K[types/] --> L[Module Types]
        K --> M[Common Types]
        
        N[routes/] --> O[Route Config]
        N --> P[Guards]
        
        Q[utils/] --> R[Helpers]
        Q --> S[Constants]
    end
```

### Backend

```mermaid
graph TB
    subgraph "Services Organization"
        A[services/] --> B[ml/]
        A --> C[module_services/]
        A --> D[core/]
        
        B --> E[inventory_ml/]
        B --> F[production_ml/]
        B --> G[projects_ml/]
        
        C --> H[finance/]
        C --> I[hr/]
        C --> J[inventory/]
        C --> K[production/]
    end

    subgraph "Tests Structure"
        L[tests/] --> M[unit/]
        L --> N[integration/]
        L --> O[e2e/]
        
        M --> P[services/]
        M --> Q[models/]
        
        N --> R[api/]
        N --> S[services/]
        
        O --> T[features/]
    end
```

## Flux de Données

```mermaid
sequenceDiagram
    participant F as Frontend
    participant A as API Layer
    participant S as Services
    participant ML as ML Services
    participant DB as Database
    participant C as Cache
    
    F->>A: API Request
    A->>S: Process Request
    S->>ML: ML Processing (if needed)
    S->>C: Check Cache
    C-->>S: Cache Hit/Miss
    S->>DB: Database Query
    DB-->>S: Query Result
    S->>C: Update Cache
    S-->>A: Service Response
    A-->>F: API Response
```

## Notes Techniques

### 1. Standards de Nommage
- Components: PascalCase (InventoryList, ProductionStats)
- Services: camelCase (inventoryService, productionService)
- Types: PascalCase avec suffixe Type/Interface (InventoryItem, ProductionStats)
- API Endpoints: kebab-case (/api/v1/inventory-items)

### 2. Organisation des Tests
- Unit: Tests isolés des services et modèles
- Integration: Tests des interactions entre composants
- E2E: Tests des flux complets utilisateur

### 3. ML Services
- Modèles standardisés
- Pipeline de données unifié
- Métriques communes
- Cache des prédictions

### 4. Sécurité
- Authentication JWT
- RBAC pour autorisations
- Validation des données
- Rate limiting
- Audit logs
