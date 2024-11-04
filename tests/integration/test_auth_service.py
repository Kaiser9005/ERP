import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from services.auth_service import AuthService
from models.auth import Utilisateur, Role, TypeRole
from core.security import verify_password, get_password_hash

def test_create_user(db: Session, test_role: Role):
    """Test de création d'un utilisateur"""
    auth_service = AuthService(db)
    
    user_data = {
        "email": "test@fofal.cm",
        "username": "testuser",
        "password": "password123",
        "nom": "Test",
        "prenom": "User",
        "role_id": str(test_role.id)
    }
    
    user = auth_service.create_user(user_data)
    assert user.email == "test@fofal.cm"
    assert user.username == "testuser"
    assert verify_password("password123", user.hashed_password)
    assert user.role_id == test_role.id

def test_authenticate_user(db: Session, test_user: Utilisateur):
    """Test d'authentification d'un utilisateur"""
    auth_service = AuthService(db)
    
    # Test authentification réussie
    user = auth_service.authenticate_user(test_user.username, "password123")
    assert user is not None
    assert user.id == test_user.id
    
    # Test authentification échouée
    user = auth_service.authenticate_user(test_user.username, "wrong_password")
    assert user is None

def test_get_user_permissions(db: Session, test_user: Utilisateur):
    """Test de récupération des permissions d'un utilisateur"""
    auth_service = AuthService(db)
    
    permissions = auth_service.get_user_permissions(test_user.id)
    assert isinstance(permissions, list)
    assert len(permissions) > 0

def test_update_user_role(db: Session, test_user: Utilisateur):
    """Test de mise à jour du rôle d'un utilisateur"""
    auth_service = AuthService(db)
    
    # Créer un nouveau rôle
    new_role = Role(
        nom="Nouveau Rôle",
        type=TypeRole.OPERATEUR,
        description="Test"
    )
    db.add(new_role)
    db.commit()
    
    # Mettre à jour le rôle de l'utilisateur
    updated_user = auth_service.update_user_role(test_user.id, str(new_role.id))
    assert updated_user.role_id == new_role.id

def test_change_password(db: Session, test_user: Utilisateur):
    """Test de changement de mot de passe"""
    auth_service = AuthService(db)
    
    # Changement réussi
    success = auth_service.change_password(
        test_user.id,
        "password123",
        "new_password123"
    )
    assert success
    
    # Vérification du nouveau mot de passe
    user = db.query(Utilisateur).filter(Utilisateur.id == test_user.id).first()
    assert verify_password("new_password123", user.hashed_password)
    
    # Échec avec ancien mot de passe incorrect
    success = auth_service.change_password(
        test_user.id,
        "wrong_password",
        "another_password"
    )
    assert not success