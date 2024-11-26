from datetime import date
from typing import List, Optional, Dict
from uuid import uuid4
from sqlalchemy.orm import Session
from sqlalchemy import and_

from models.hr_payroll import Payroll
from models.hr_contract import Contract
from schemas.hr_payroll import PayrollCreate, PayrollUpdate, PayrollStats

class PayrollService:
    """Service de gestion de la paie"""

    def __init__(self, db: Session):
        self.db = db

    def create_payroll(self, payroll: PayrollCreate) -> Payroll:
        """Crée une nouvelle fiche de paie"""
        # Récupère le contrat
        contract = self.db.query(Contract).filter(Contract.id == payroll.contract_id).first()
        if not contract:
            raise ValueError("Contrat non trouvé")

        # Vérifie que le contrat est actif
        if not contract.is_active:
            raise ValueError("Le contrat n'est pas actif")

        # Crée la fiche de paie
        db_payroll = Payroll(
            id=str(uuid4()),
            contract_id=payroll.contract_id,
            period_start=payroll.period_start,
            period_end=payroll.period_end,
            worked_hours=payroll.worked_hours,
            overtime_hours=payroll.overtime_hours,
            base_salary=contract.wage,
            overtime_amount=payroll.overtime_amount,
            bonus=payroll.bonus,
            deductions=payroll.deductions,
            bonus_details=payroll.bonus_details,
            deduction_details=payroll.deduction_details,
            employer_contributions=payroll.employer_contributions,
            employee_contributions=payroll.employee_contributions
        )

        # Calcule les totaux
        db_payroll.calculate_totals()

        # Sauvegarde
        self.db.add(db_payroll)
        self.db.commit()
        self.db.refresh(db_payroll)

        return db_payroll

    def get_payroll(self, payroll_id: str) -> Optional[Payroll]:
        """Récupère une fiche de paie par son ID"""
        return self.db.query(Payroll).filter(Payroll.id == payroll_id).first()

    def get_payrolls_by_contract(self, contract_id: str) -> List[Payroll]:
        """Récupère toutes les fiches de paie d'un contrat"""
        return self.db.query(Payroll).filter(Payroll.contract_id == contract_id).all()

    def get_payrolls_by_period(self, start_date: date, end_date: date) -> List[Payroll]:
        """Récupère les fiches de paie pour une période donnée"""
        return self.db.query(Payroll).filter(
            and_(
                Payroll.period_start >= start_date,
                Payroll.period_end <= end_date
            )
        ).all()

    def update_payroll(self, payroll_id: str, payroll_update: PayrollUpdate) -> Optional[Payroll]:
        """Met à jour une fiche de paie"""
        db_payroll = self.get_payroll(payroll_id)
        if not db_payroll:
            return None

        # Met à jour les champs modifiables
        update_data = payroll_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_payroll, field, value)

        # Recalcule les totaux si nécessaire
        if any(field in update_data for field in ['worked_hours', 'overtime_hours', 'overtime_amount', 'bonus', 'deductions']):
            db_payroll.calculate_totals()

        self.db.commit()
        self.db.refresh(db_payroll)
        return db_payroll

    def delete_payroll(self, payroll_id: str) -> bool:
        """Supprime une fiche de paie"""
        db_payroll = self.get_payroll(payroll_id)
        if not db_payroll:
            return False

        self.db.delete(db_payroll)
        self.db.commit()
        return True

    def get_payroll_stats(self, start_date: date, end_date: date) -> PayrollStats:
        """Calcule les statistiques de paie pour une période"""
        payrolls = self.get_payrolls_by_period(start_date, end_date)
        
        if not payrolls:
            return PayrollStats(
                total_gross=0,
                total_net=0,
                total_employer_contributions=0,
                total_employee_contributions=0,
                total_bonus=0,
                total_deductions=0,
                average_gross=0,
                average_net=0,
                period_start=start_date,
                period_end=end_date
            )

        total_gross = sum(p.gross_total for p in payrolls)
        total_net = sum(p.net_total for p in payrolls)
        count = len(payrolls)

        return PayrollStats(
            total_gross=total_gross,
            total_net=total_net,
            total_employer_contributions=sum(p.employer_contributions for p in payrolls),
            total_employee_contributions=sum(p.employee_contributions for p in payrolls),
            total_bonus=sum(p.bonus for p in payrolls),
            total_deductions=sum(p.deductions for p in payrolls),
            average_gross=total_gross / count if count > 0 else 0,
            average_net=total_net / count if count > 0 else 0,
            period_start=start_date,
            period_end=end_date
        )

    def validate_payroll(self, payroll_id: str) -> bool:
        """Valide une fiche de paie pour paiement"""
        db_payroll = self.get_payroll(payroll_id)
        if not db_payroll:
            return False

        db_payroll.is_paid = True
        db_payroll.payment_date = date.today()
        
        self.db.commit()
        return True

    def calculate_overtime(self, hours: float, base_rate: float) -> float:
        """Calcule le montant des heures supplémentaires"""
        # Majoration de 25% pour les heures sup
        return hours * base_rate * 1.25

    def calculate_contributions(self, gross_amount: float) -> Dict[str, float]:
        """Calcule les cotisations sociales"""
        # Taux simplifiés pour l'exemple
        employer_rate = 0.45  # 45% charges patronales
        employee_rate = 0.22  # 22% charges salariales

        return {
            "employer": round(gross_amount * employer_rate, 2),
            "employee": round(gross_amount * employee_rate, 2)
        }
