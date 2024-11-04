import pytest
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from services.finance_service import FinanceService
from models.finance import Transaction, Compte, Budget
from models.finance import TypeTransaction, StatutTransaction, CategorieTransaction, TypeCompte

def test_get_finance_stats(db: Session, test_user: dict):
    """Test de récupération des statistiques financières"""
    service = FinanceService(db)
    
    # Créer des transactions de test
    compte = Compte(
        numero="CPT001",
        libelle="Compte Principal",
        type_compte=TypeCompte.BANQUE,
        devise="XAF",
        solde=1000000
    )
    db.add(compte)
    db.commit()

    # Créer des recettes
    for i in range(3):
        transaction = Transaction(
            reference=f"REC00{i+1}",
            date_transaction=datetime.now() - timedelta(days=i),
            type_transaction=TypeTransaction.RECETTE,
            categorie=CategorieTransaction.VENTE,
            montant=100000 + i * 50000,
            compte_destination_id=compte.id,
            statut=StatutTransaction.VALIDEE
        )
        db.add(transaction)

    # Créer des dépenses
    for i in range(2):
        transaction = Transaction(
            reference=f"DEP00{i+1}",
            date_transaction=datetime.now() - timedelta(days=i),
            type_transaction=TypeTransaction.DEPENSE,
            categorie=CategorieTransaction.ACHAT_INTRANT,
            montant=75000 + i * 25000,
            compte_source_id=compte.id,
            statut=StatutTransaction.VALIDEE
        )
        db.add(transaction)
    db.commit()

    stats = await service.get_stats()
    assert "revenue" in stats
    assert "profit" in stats
    assert "cashflow" in stats
    assert stats["revenue"] > 0
    assert stats["profit"] > 0

def test_create_transaction(db: Session, test_user: dict):
    """Test de création d'une transaction"""
    service = FinanceService(db)
    
    # Créer un compte
    compte = Compte(
        numero="CPT002",
        libelle="Compte Test",
        type_compte=TypeCompte.BANQUE,
        devise="XAF",
        solde=500000
    )
    db.add(compte)
    db.commit()

    # Test création d'une recette
    recette_data = {
        "reference": "REC001",
        "date_transaction": datetime.now(),
        "type_transaction": TypeTransaction.RECETTE,
        "categorie": CategorieTransaction.VENTE,
        "montant": 150000,
        "compte_destination_id": str(compte.id),
        "description": "Test recette"
    }

    recette = await service.create_transaction(recette_data)
    assert recette.reference == "REC001"
    assert recette.montant == 150000

    # Vérifier le solde du compte
    db.refresh(compte)
    assert compte.solde == 650000

def test_handle_depense(db: Session, test_user: dict):
    """Test de gestion d'une dépense"""
    service = FinanceService(db)
    
    # Créer un compte avec solde initial
    compte = Compte(
        numero="CPT003",
        libelle="Compte Test",
        type_compte=TypeCompte.BANQUE,
        devise="XAF",
        solde=300000
    )
    db.add(compte)
    db.commit()

    # Test création d'une dépense
    depense_data = {
        "reference": "DEP001",
        "date_transaction": datetime.now(),
        "type_transaction": TypeTransaction.DEPENSE,
        "categorie": CategorieTransaction.ACHAT_INTRANT,
        "montant": 100000,
        "compte_source_id": str(compte.id),
        "description": "Test dépense"
    }

    depense = await service.create_transaction(depense_data)
    assert depense.reference == "DEP001"
    assert depense.montant == 100000

    # Vérifier le solde du compte
    db.refresh(compte)
    assert compte.solde == 200000

def test_handle_virement(db: Session, test_user: dict):
    """Test de gestion d'un virement"""
    service = FinanceService(db)
    
    # Créer deux comptes
    compte_source = Compte(
        numero="CPT004",
        libelle="Compte Source",
        type_compte=TypeCompte.BANQUE,
        devise="XAF",
        solde=400000
    )
    db.add(compte_source)

    compte_dest = Compte(
        numero="CPT005",
        libelle="Compte Destination",
        type_compte=TypeCompte.CAISSE,
        devise="XAF",
        solde=100000
    )
    db.add(compte_dest)
    db.commit()

    # Test création d'un virement
    virement_data = {
        "reference": "VIR001",
        "date_transaction": datetime.now(),
        "type_transaction": TypeTransaction.VIREMENT,
        "categorie": CategorieTransaction.AUTRE,
        "montant": 200000,
        "compte_source_id": str(compte_source.id),
        "compte_destination_id": str(compte_dest.id),
        "description": "Test virement"
    }

    virement = await service.create_transaction(virement_data)
    assert virement.reference == "VIR001"
    assert virement.montant == 200000

    # Vérifier les soldes des comptes
    db.refresh(compte_source)
    db.refresh(compte_dest)
    assert compte_source.solde == 200000
    assert compte_dest.solde == 300000

def test_budget_tracking(db: Session):
    """Test du suivi budgétaire"""
    service = FinanceService(db)
    
    # Créer un budget
    budget = Budget(
        periode=datetime.now().strftime("%Y-%m"),
        categorie=CategorieTransaction.ACHAT_INTRANT,
        montant_prevu=500000,
        montant_realise=0
    )
    db.add(budget)
    db.commit()

    # Créer un compte
    compte = Compte(
        numero="CPT006",
        libelle="Compte Test",
        type_compte=TypeCompte.BANQUE,
        devise="XAF",
        solde=1000000
    )
    db.add(compte)
    db.commit()

    # Créer une dépense dans la catégorie du budget
    depense_data = {
        "reference": "DEP002",
        "date_transaction": datetime.now(),
        "type_transaction": TypeTransaction.DEPENSE,
        "categorie": CategorieTransaction.ACHAT_INTRANT,
        "montant": 300000,
        "compte_source_id": str(compte.id),
        "description": "Test suivi budget"
    }

    await service.create_transaction(depense_data)

    # Vérifier la mise à jour du budget
    db.refresh(budget)
    assert budget.montant_realise == 300000