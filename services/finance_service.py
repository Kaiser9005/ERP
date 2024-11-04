from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime, timedelta
from models.finance import Transaction, Compte, Budget
from schemas.finance import TransactionCreate
from sqlalchemy import func

class FinanceService:
    def __init__(self, db: Session):
        self.db = db

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        # Chiffre d'affaires du mois
        revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        # Chiffre d'affaires du mois précédent
        previous_revenue = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "RECETTE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul des variations
        revenue_variation = self._calculate_variation(revenue, previous_revenue)

        # Calcul du bénéfice
        expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == current_month
        ).scalar() or 0

        profit = revenue - expenses
        previous_expenses = self.db.query(
            func.sum(Transaction.montant)
        ).filter(
            Transaction.type_transaction == "DEPENSE",
            Transaction.statut == "VALIDEE",
            func.to_char(Transaction.date_transaction, 'YYYY-MM') == last_month
        ).scalar() or 0

        previous_profit = previous_revenue - previous_expenses
        profit_variation = self._calculate_variation(profit, previous_profit)

        # Calcul de la trésorerie
        cashflow = self.db.query(
            func.sum(Compte.solde)
        ).filter(
            Compte.actif == True
        ).scalar() or 0

        return {
            "revenue": revenue,
            "revenueVariation": revenue_variation,
            "profit": profit,
            "profitVariation": profit_variation,
            "cashflow": cashflow,
            "cashflowVariation": {
                "value": 0,  # À implémenter
                "type": "increase"
            },
            "expenses": expenses,
            "expensesVariation": self._calculate_variation(expenses, previous_expenses)
        }

    async def create_transaction(self, transaction: TransactionCreate) -> Transaction:
        """Crée une nouvelle transaction et met à jour les soldes"""
        db_transaction = Transaction(**transaction.dict())
        self.db.add(db_transaction)

        # Mise à jour des soldes des comptes
        if transaction.type_transaction == "RECETTE":
            await self._handle_recette(transaction)
        elif transaction.type_transaction == "DEPENSE":
            await self._handle_depense(transaction)
        elif transaction.type_transaction == "VIREMENT":
            await self._handle_virement(transaction)

        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def _calculate_variation(
        self,
        current_value: float,
        previous_value: float
    ) -> Dict[str, Any]:
        """Calcule la variation entre deux valeurs"""
        if previous_value == 0:
            return {
                "value": 0,
                "type": "increase"
            }

        variation = ((current_value - previous_value) / previous_value) * 100
        return {
            "value": abs(round(variation, 1)),
            "type": "increase" if variation >= 0 else "decrease"
        }

    async def _handle_recette(self, transaction: TransactionCreate):
        """Gère une transaction de type recette"""
        compte = self.db.query(Compte).filter(
            Compte.id == transaction.compte_destination_id
        ).first()
        if not compte:
            raise ValueError("Compte de destination non trouvé")
        compte.solde += transaction.montant

    async def _handle_depense(self, transaction: TransactionCreate):
        """Gère une transaction de type dépense"""
        compte = self.db.query(Compte).filter(
            Compte.id == transaction.compte_source_id
        ).first()
        if not compte:
            raise ValueError("Compte source non trouvé")
        if compte.solde < transaction.montant:
            raise ValueError("Solde insuffisant")
        compte.solde -= transaction.montant

    async def _handle_virement(self, transaction: TransactionCreate):
        """Gère un virement entre comptes"""
        await self._handle_depense(transaction)
        await self._handle_recette(transaction)