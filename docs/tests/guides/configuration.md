# Configuration des Tests FOFAL ERP

## Prérequis

### Python
```bash
# Installation des dépendances
pip install -r requirements.txt

# Principales dépendances
pytest==7.4.0
pytest-cov==4.1.0
pytest-asyncio==0.21.1
pytest-playwright==0.4.0
```

### Node.js (Frontend)
```bash
# Installation des dépendances
cd frontend && npm install

# Principales dépendances
vitest
@testing-library/react
@testing-library/jest-dom
@testing-library/user-event
msw
```

## Configuration des Tests

### pytest.ini
```ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    asyncio: mark test as async
    e2e: mark test as end-to-end
    integration: mark test as integration test
```

### conftest.py
Le fichier `tests/conftest.py` contient les fixtures partagées :
- `test_session` : Session de base de données de test
- `test_client` : Client FastAPI de test
- `auth_token` : Token JWT pour l'authentification

### Configuration E2E

Les tests E2E nécessitent :
1. Playwright installé et configuré
2. Un serveur de développement en cours d'exécution
3. Une base de données de test

```bash
# Installation de Playwright
playwright install

# Configuration dans tests/e2e/conftest.py
@pytest.fixture
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1280,
            "height": 720
        }
    }
```

### Configuration React Query

```typescript
// frontend/src/test/setup.ts
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { render } from '@testing-library/react'

const createTestQueryClient = () => new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

export function renderWithClient(ui: React.ReactElement) {
  const testQueryClient = createTestQueryClient()
  return {
    ...render(
      <QueryClientProvider client={testQueryClient}>{ui}</QueryClientProvider>
    ),
    testQueryClient,
  }
}
```

### Configuration MSW (Mock Service Worker)

```typescript
// frontend/src/test/server.ts
import { setupServer } from 'msw/node'
import { rest } from 'msw'

export const server = setupServer(
  rest.get('/api/data', (req, res, ctx) => {
    return res(ctx.json({ data: 'mocked' }))
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
```

## Exécution des Tests

### Tests Python
```bash
# Tous les tests
pytest

# Tests avec couverture
pytest --cov=app

# Tests spécifiques
pytest tests/test_dashboard.py

# Tests E2E
pytest tests/e2e/

# Tests ML
pytest tests/test_projects_ml_service.py
pytest tests/integration/test_projects_ml_integration.py

# Tests Inventaire
pytest tests/integration/test_inventory_*.py
```

### Tests Frontend
```bash
# Tests unitaires
cd frontend && npm test

# Tests avec couverture
cd frontend && npm test -- --coverage

# Tests E2E
cd frontend && npm run test:e2e
```

## Environnements de Test

### Base de données de test
- Base PostgreSQL dédiée aux tests
- Migrations automatiques avant les tests
- Nettoyage après chaque test

### Variables d'environnement
```bash
# .env.test
DATABASE_URL=postgresql://user:pass@localhost:5432/test_db
JWT_SECRET=test_secret
ENVIRONMENT=test
```

### Cache Redis de test
```python
# tests/conftest.py
@pytest.fixture
def redis_client():
    return FakeRedis()
```

## Intégration Continue

### GitHub Actions
```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## Maintenance

### Couverture de Code
- Objectif : > 80% de couverture
- Rapport détaillé avec `pytest --cov-report=html`
- Vérification dans CI/CD

### Performance
- Optimisation des fixtures volumineuses
- Utilisation du cache de test
- Parallélisation avec `pytest-xdist`

### Documentation
- Mise à jour de ce guide
- Documentation des nouveaux tests
- Maintenance des exemples
