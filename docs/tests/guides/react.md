# Guide des Tests React et React Query

## Vue d'ensemble

Ce guide détaille les bonnes pratiques et standards pour les tests des composants React, avec un focus particulier sur l'utilisation de React Query.

## Configuration de Base

### Configuration React Testing Library
```typescript
// frontend/src/test/setup.ts
import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

afterEach(() => {
  cleanup()
})
```

### Configuration React Query
```typescript
// frontend/src/test/utils.tsx
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        retry: false,
        cacheTime: 0,
        staleTime: 0
      },
    },
  })
}

export function renderWithClient(ui: React.ReactElement) {
  const testQueryClient = createTestQueryClient()
  return {
    ...render(
      <QueryClientProvider client={testQueryClient}>
        {ui}
      </QueryClientProvider>
    ),
    testQueryClient,
  }
}
```

## Structure des Tests React Query

### Test Complet d'un Composant
```typescript
import { screen, waitFor } from '@testing-library/react'
import { renderWithClient } from '../test/utils'
import { server } from '../test/server'
import { rest } from 'msw'

describe('MonComposant', () => {
  // État de chargement
  it('affiche le chargement initialement', () => {
    renderWithClient(<MonComposant />)
    expect(screen.getByTestId('loading')).toBeInTheDocument()
  })

  // Affichage des données
  it('affiche les données après chargement', async () => {
    const mockData = { id: 1, name: 'Test' }
    server.use(
      rest.get('/api/data', (req, res, ctx) => {
        return res(ctx.json(mockData))
      })
    )

    renderWithClient(<MonComposant />)
    
    expect(await screen.findByText('Test')).toBeInTheDocument()
  })

  // Gestion des erreurs
  it('affiche une erreur en cas d'échec', async () => {
    server.use(
      rest.get('/api/data', (req, res, ctx) => {
        return res(ctx.status(500))
      })
    )

    renderWithClient(<MonComposant />)
    
    expect(await screen.findByTestId('error')).toBeInTheDocument()
  })

  // État sans données
  it('affiche un message quand pas de données', async () => {
    server.use(
      rest.get('/api/data', (req, res, ctx) => {
        return res(ctx.json([]))
      })
    )

    renderWithClient(<MonComposant />)
    
    expect(await screen.findByText('Aucune donnée')).toBeInTheDocument()
  })
})
```

### Test des Mutations
```typescript
import { screen, fireEvent } from '@testing-library/react'
import { renderWithClient } from '../test/utils'

describe('FormulaireProduit', () => {
  it('soumet les données correctement', async () => {
    const mockMutation = vi.fn()
    server.use(
      rest.post('/api/produits', async (req, res, ctx) => {
        mockMutation(await req.json())
        return res(ctx.json({ success: true }))
      })
    )

    renderWithClient(<FormulaireProduit />)
    
    fireEvent.change(screen.getByLabelText('Nom'), {
      target: { value: 'Nouveau Produit' }
    })
    
    fireEvent.click(screen.getByText('Enregistrer'))
    
    await waitFor(() => {
      expect(mockMutation).toHaveBeenCalledWith(
        expect.objectContaining({
          nom: 'Nouveau Produit'
        })
      )
    })
  })
})
```

## Standards de Test

### 1. Sélection des Éléments
```typescript
// ✅ Bon : Utiliser des data-testid
<Button data-testid="submit-button">Envoyer</Button>

// ✅ Bon : Utiliser des labels accessibles
<input aria-label="Recherche" />

// ❌ Mauvais : Sélection par classe CSS
screen.getByClassName('submit-btn')
```

### 2. Assertions
```typescript
// ✅ Bon : Assertions positives
expect(screen.getByText('Titre')).toBeInTheDocument()

// ✅ Bon : Vérification d'état
expect(screen.getByRole('button')).toBeEnabled()

// ❌ Mauvais : Assertions négatives sans attente
expect(screen.queryByText('Erreur')).not.toBeInTheDocument()
```

### 3. Tests Asynchrones
```typescript
// ✅ Bon : Utiliser findBy pour les éléments asynchrones
await screen.findByText('Données chargées')

// ✅ Bon : Utiliser waitFor pour les assertions complexes
await waitFor(() => {
  expect(screen.getByText('Success')).toBeInTheDocument()
})

// ❌ Mauvais : Utiliser getBy pour des éléments asynchrones
screen.getByText('Données chargées')
```

## Bonnes Pratiques

### 1. Organisation des Tests
- Un fichier de test par composant
- Tests groupés par fonctionnalité
- Descriptions claires et explicites

### 2. Mocking
- Mocker uniquement ce qui est nécessaire
- Utiliser MSW pour les requêtes API
- Réinitialiser les mocks après chaque test

### 3. Données de Test
- Utiliser des factories pour les données de test
- Éviter les données en dur dans les tests
- Maintenir des fixtures réutilisables

### 4. Performance
- Minimiser les attentes asynchrones
- Nettoyer après chaque test
- Éviter les tests qui dépendent d'autres tests

## Exemples Courants

### 1. Test d'un Formulaire
```typescript
describe('FormulaireProduit', () => {
  it('valide les champs requis', async () => {
    renderWithClient(<FormulaireProduit />)
    
    fireEvent.click(screen.getByText('Enregistrer'))
    
    expect(await screen.findByText('Le nom est requis')).toBeInTheDocument()
  })
})
```

### 2. Test de Navigation
```typescript
describe('Navigation', () => {
  it('navigue vers la bonne page', async () => {
    renderWithClient(<Navigation />)
    
    fireEvent.click(screen.getByText('Produits'))
    
    expect(mockNavigate).toHaveBeenCalledWith('/produits')
  })
})
```

### 3. Test de Filtre
```typescript
describe('ListeProduits', () => {
  it('filtre les produits', async () => {
    renderWithClient(<ListeProduits />)
    
    fireEvent.change(screen.getByLabelText('Recherche'), {
      target: { value: 'test' }
    })
    
    expect(await screen.findByText('Produit Test')).toBeInTheDocument()
    expect(screen.queryByText('Autre Produit')).not.toBeInTheDocument()
  })
})
```

## Maintenance

### Documentation
- Commenter les cas complexes
- Expliquer les mocks particuliers
- Documenter les fixtures réutilisables

### Mise à Jour
- Revoir les tests lors des changements de composants
- Maintenir les snapshots à jour
- Mettre à jour les mocks si nécessaire

### Performance
- Optimiser les tests lents
- Regrouper les tests similaires
- Utiliser des hooks de test appropriés
