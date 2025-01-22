import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from models.auth import Utilisateur, Role, Permission, TypeRole
from schemas.auth import FirstAdminCreate

@pytest.fixture
def admin_data():
    """Fixture pour les données de création du premier admin"""
    return FirstAdminCreate(
        username="admin",
        email="admin@example.com",
        password="Admin123!",
        nom="Admin",
        prenom="Super"
    )

@pytest.mark.asyncio
async def test_create_first_admin(db: Session, client: TestClient, admin_data: FirstAdminCreate):
    """Test de création du premier administrateur"""
    
    # Vérifier qu'il n'y a pas d'utilisateurs au départ
    assert db.query(Utilisateur).count() == 0
    assert db.query(Role).count() == 0
    assert db.query(Permission).count() == 0

    # Créer le premier admin
    response = client.post(
        "/api/v1/auth/first-admin",
        json=admin_data.model_dump()
    )
    assert response.status_code == 200
    
    # Vérifier la création de l'utilisateur
    user = db.query(Utilisateur).first()
    assert user is not None
    assert user.username == admin_data.username
    assert user.email == admin_data.email
    assert user.nom == admin_data.nom
    assert user.prenom == admin_data.prenom
    assert user.is_superuser is True
    assert user.is_active is True
    assert user.is_staff is True

    # Vérifier la création du rôle admin
    role = db.query(Role).first()
    assert role is not None
    assert role.type == TypeRole.ADMIN
    assert role.nom == "Administrateur"
    assert role.is_active is True

    # Vérifier la création des permissions
    permissions = db.query(Permission).all()
    assert len(permissions) == 2  # ADMIN_ALL et USER_MANAGE
    permission_codes = {p.code for p in permissions}
    assert "ADMIN_ALL" in permission_codes
    assert "USER_MANAGE" in permission_codes

    # Vérifier l'association des permissions au rôle
    assert len(role.permissions) == 2
    role_permission_codes = {p.code for p in role.permissions}
    assert "ADMIN_ALL" in role_permission_codes
    assert "USER_MANAGE" in role_permission_codes

    # Vérifier que l'utilisateur est bien associé au rôle
    assert user.role_id == role.id

    # Tenter de créer un second admin (doit échouer)
    response = client.post(
        "/api/v1/auth/first-admin",
        json=admin_data.model_dump()
    )
    assert response.status_code == 400
    assert "existe déjà" in response.json()["detail"]

@pytest.mark.asyncio
async def test_admin_login(db: Session, client: TestClient, admin_data: FirstAdminCreate):
    """Test de connexion de l'administrateur"""
    
    # Créer l'admin
    client.post(
        "/api/v1/auth/first-admin",
        json=admin_data.model_dump()
    )

    # Tester la connexion
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": admin_data.username,
            "password": admin_data.password
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

    # Utiliser le token pour accéder à /users/me
    token = response.json()["access_token"]
    response = client.get(
        "/api/v1/auth/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["username"] == admin_data.username
    assert response.json()["is_superuser"] is True

@pytest.mark.asyncio
async def test_admin_permissions(db: Session, client: TestClient, admin_data: FirstAdminCreate):
    """Test des permissions de l'administrateur"""
    
    # Créer l'admin et obtenir le token
    client.post(
        "/api/v1/auth/first-admin",
        json=admin_data.model_dump()
    )
    response = client.post(
        "/api/v1/auth/token",
        data={
            "username": admin_data.username,
            "password": admin_data.password
        }
    )
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Tester la création d'un rôle (nécessite ADMIN_ALL)
    role_data = {
        "nom": "Test Role",
        "description": "Role de test",
        "type": "OPERATEUR",
        "permissions": []
    }
    response = client.post(
        "/api/v1/auth/roles",
        json=role_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["nom"] == "Test Role"

    # Tester la création d'une permission (nécessite ADMIN_ALL)
    permission_data = {
        "code": "TEST_PERMISSION",
        "description": "Permission de test",
        "module": "test",
        "actions": {"read": True}
    }
    response = client.post(
        "/api/v1/auth/permissions",
        json=permission_data,
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["code"] == "TEST_PERMISSION"