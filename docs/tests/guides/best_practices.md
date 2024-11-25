# Guide des Bonnes Pratiques de Test

## Principes Généraux

### 1. Tests Indépendants
- Chaque test doit être autonome
- Pas de dépendances entre les tests
- État initial propre pour chaque test
- Nettoyage après chaque test

### 2. Tests Lisibles
```python
# ✅ Bon : Nom explicite et description claire
def test_product_creation_with_valid_data():
    """Vérifie la création d'un produit avec des données valides."""
    
# ❌ Mauvais : Nom peu clair et pas de description
def test_prod_1():
```

### 3. Tests Maintenables
```python
# ✅ Bon : Utilisation de fixtures et constantes
@pytest.fixture
def valid_product_data():
    return {
        "name": "Test Product",
        "price": Decimal("99.99"),
        "category": ProductCategory.ELECTRONICS
    }

# ❌ Mauvais : Données en dur dans les tests
def test_product():
    product = create_product("Test", "99.99", "ELECTRONICS")
```

### 4. Tests Fiables
```python
# ✅ Bon : Assertions précises
assert response.status_code == 201
assert response.json()["name"] == expected_name

# ❌ Mauvais : Assertions trop générales
assert response.status_code >= 200
assert "name" in response.json()
```

## Organisation du Code

### 1. Structure des Tests
```
tests/
├── conftest.py              # Fixtures partagées
├── unit/                    # Tests unitaires
├── integration/            # Tests d'intégration
└── e2e/                    # Tests end-to-end
```

### 2. Fixtures Partagées
```python
# conftest.py
@pytest.fixture
def db_session():
    """Session de base de données pour les tests."""
    engine = create_test_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    yield session
    
    session.rollback()
    session.close()

@pytest.fixture
def auth_client(db_session):
    """Client HTTP authentifié."""
    client = TestClient(app)
    client.headers["Authorization"] = f"Bearer {create_test_token()}"
    return client
```

### 3. Helpers de Test
```python
# helpers.py
def create_test_product(session, **kwargs):
    """Crée un produit de test avec des valeurs par défaut."""
    defaults = {
        "name": "Test Product",
        "price": Decimal("99.99"),
        "category": ProductCategory.ELECTRONICS
    }
    data = {**defaults, **kwargs}
    product = Product(**data)
    session.add(product)
    session.commit()
    return product

def assert_product_equals(product, expected_data):
    """Compare un produit avec des données attendues."""
    assert product.name == expected_data["name"]
    assert product.price == Decimal(expected_data["price"])
    assert product.category == expected_data["category"]
```

## Standards par Type de Test

### 1. Tests Unitaires
```python
def test_calculate_total_price():
    """Test unitaire d'une fonction de calcul."""
    # Arrangement
    items = [
        {"price": Decimal("10.00"), "quantity": 2},
        {"price": Decimal("15.00"), "quantity": 1}
    ]
    
    # Action
    total = calculate_total_price(items)
    
    # Assertion
    assert total == Decimal("35.00")
```

### 2. Tests d'Intégration
```python
async def test_order_creation_workflow(db_session):
    """Test d'intégration du workflow de commande."""
    # Création du produit
    product = await create_test_product(db_session)
    
    # Création du client
    customer = await create_test_customer(db_session)
    
    # Création de la commande
    order = await create_order(customer.id, [(product.id, 2)])
    
    # Vérifications
    assert order.status == OrderStatus.PENDING
    assert len(order.items) == 1
    assert order.total_price == product.price * 2
```

### 3. Tests E2E
```python
def test_checkout_process(authenticated_page: Page):
    """Test E2E du processus d'achat."""
    # Navigation
    authenticated_page.goto("/products")
    
    # Ajout au panier
    authenticated_page.click("[data-testid='add-to-cart']")
    
    # Vérification du panier
    expect(authenticated_page.locator("[data-testid='cart-count']")
          ).to_have_text("1")
    
    # Processus de paiement
    authenticated_page.click("[data-testid='checkout']")
    authenticated_page.fill("[data-testid='card-number']", "4242424242424242")
    authenticated_page.click("[data-testid='pay-button']")
    
    # Vérification finale
    expect(authenticated_page.locator("[data-testid='success-message']")
          ).to_be_visible()
```

## Gestion des Données de Test

### 1. Données de Test
```python
# test_data.py
TEST_PRODUCTS = [
    {
        "name": "Test Product 1",
        "price": Decimal("99.99"),
        "category": ProductCategory.ELECTRONICS
    },
    {
        "name": "Test Product 2",
        "price": Decimal("149.99"),
        "category": ProductCategory.ELECTRONICS
    }
]

TEST_CUSTOMERS = [
    {
        "email": "test1@example.com",
        "name": "Test User 1"
    }
]
```

### 2. Factories
```python
# factories.py
class ProductFactory:
    @staticmethod
    def create(**kwargs):
        """Crée un produit de test."""
        defaults = {
            "name": f"Product {uuid4()}",
            "price": Decimal("99.99"),
            "category": ProductCategory.ELECTRONICS
        }
        return Product(**{**defaults, **kwargs})

class OrderFactory:
    @staticmethod
    def create(customer, products):
        """Crée une commande de test."""
        order = Order(customer_id=customer.id)
        for product in products:
            order.items.append(OrderItem(
                product_id=product.id,
                quantity=1,
                price=product.price
            ))
        return order
```

## Meilleures Pratiques par Domaine

### 1. Tests Base de Données
```python
def test_database_operations(db_session):
    """Test des opérations de base de données."""
    # Utiliser les transactions
    with db_session.begin_nested():
        product = ProductFactory.create()
        db_session.add(product)
    
    # Vérifier l'isolation
    assert db_session.query(Product).count() == 1
```

### 2. Tests API
```python
def test_api_endpoints(client):
    """Test des endpoints API."""
    # Headers appropriés
    headers = {"Content-Type": "application/json"}
    
    # Données de test structurées
    data = {"name": "Test Product"}
    
    # Requête et vérification
    response = client.post("/api/products", json=data, headers=headers)
    assert response.status_code == 201
```

### 3. Tests Asynchrones
```python
@pytest.mark.asyncio
async def test_async_operations():
    """Test des opérations asynchrones."""
    # Utiliser async/await correctement
    result = await async_operation()
    
    # Gérer les timeouts
    with pytest.raises(asyncio.TimeoutError):
        async with timeout(0.1):
            await long_operation()
```

## Maintenance et Documentation

### 1. Documentation des Tests
```python
def test_complex_workflow():
    """
    Test du workflow complexe de traitement des commandes.
    
    Étapes:
    1. Création du produit
    2. Création du client
    3. Création de la commande
    4. Vérification du stock
    5. Traitement du paiement
    
    Vérifications:
    - Statut de la commande
    - Mise à jour du stock
    - Notification client
    """
```

### 2. Revue de Tests
- Vérifier la couverture régulièrement
- Identifier les cas manquants
- Optimiser les tests lents
- Maintenir la documentation à jour

### 3. Performance
- Utiliser le parallélisme quand possible
- Optimiser les fixtures volumineuses
- Monitorer les temps d'exécution
- Nettoyer les ressources
