from fastapi import Depends
from sqlalchemy.orm import Session
from typing import List, Dict, Any
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import numpy as np

from db.database import get_db
from models.hr import Employee
from models.hr_formation import Formation, Participation
from models.hr_contract import Contract
from models.hr_payroll import Payroll

class HRAnalyticsService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
        self._scaler = StandardScaler()
        self._model = RandomForestRegressor(n_estimators=100)

    async def get_employee_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques globales des employés"""
        total_employees = self.db.query(Employee).count()
        active_contracts = self.db.query(Contract).filter(Contract.status == 'active').count()
        formations_completed = self.db.query(Participation).filter(Participation.status == 'completed').count()
        
        return {
            "total_employees": total_employees,
            "active_contracts": active_contracts,
            "formations_completed": formations_completed,
            "formation_completion_rate": formations_completed / total_employees if total_employees > 0 else 0
        }

    async def get_formation_analytics(self) -> Dict[str, Any]:
        """Analyse les données de formation"""
        formations = self.db.query(Formation).all()
        participations = self.db.query(Participation).all()
        
        formation_stats = {
            "total_formations": len(formations),
            "total_participations": len(participations),
            "completion_rate": len([p for p in participations if p.status == 'completed']) / len(participations) if participations else 0,
            "formations_by_type": self._get_formations_by_type(formations),
            "success_rate_by_formation": self._get_success_rate_by_formation(participations)
        }
        
        return formation_stats

    async def get_contract_analytics(self) -> Dict[str, Any]:
        """Analyse les données des contrats"""
        contracts = self.db.query(Contract).all()
        
        contract_stats = {
            "total_contracts": len(contracts),
            "contracts_by_type": self._get_contracts_by_type(contracts),
            "contract_duration_stats": self._get_contract_duration_stats(contracts),
            "contract_renewal_rate": self._calculate_renewal_rate(contracts)
        }
        
        return contract_stats

    async def get_payroll_analytics(self) -> Dict[str, Any]:
        """Analyse les données de paie"""
        payrolls = self.db.query(Payroll).all()
        
        payroll_stats = {
            "total_payroll": sum(p.total_amount for p in payrolls),
            "average_salary": np.mean([p.total_amount for p in payrolls]) if payrolls else 0,
            "salary_distribution": self._get_salary_distribution(payrolls),
            "payroll_trends": self._get_payroll_trends(payrolls)
        }
        
        return payroll_stats

    async def predict_employee_performance(self, employee_id: int) -> Dict[str, float]:
        """Prédit la performance d'un employé basée sur l'historique"""
        employee_data = self._get_employee_historical_data(employee_id)
        if not employee_data:
            return {"error": "Données insuffisantes pour la prédiction"}
            
        features = self._prepare_features(employee_data)
        prediction = self._model.predict(features)
        
        return {
            "predicted_performance": float(prediction[0]),
            "confidence": float(self._model.score(features, employee_data['performance']))
        }

    def _get_formations_by_type(self, formations: List[Formation]) -> Dict[str, int]:
        """Groupe les formations par type"""
        formation_types = {}
        for formation in formations:
            formation_types[formation.type] = formation_types.get(formation.type, 0) + 1
        return formation_types

    def _get_success_rate_by_formation(self, participations: List[Participation]) -> Dict[str, float]:
        """Calcule le taux de réussite par formation"""
        success_rates = {}
        for participation in participations:
            if participation.formation_id not in success_rates:
                success_rates[participation.formation_id] = {
                    'total': 0,
                    'completed': 0
                }
            success_rates[participation.formation_id]['total'] += 1
            if participation.status == 'completed':
                success_rates[participation.formation_id]['completed'] += 1
        
        return {
            k: v['completed'] / v['total'] 
            for k, v in success_rates.items()
        }

    def _get_contracts_by_type(self, contracts: List[Contract]) -> Dict[str, int]:
        """Groupe les contrats par type"""
        contract_types = {}
        for contract in contracts:
            contract_types[contract.type] = contract_types.get(contract.type, 0) + 1
        return contract_types

    def _get_contract_duration_stats(self, contracts: List[Contract]) -> Dict[str, float]:
        """Calcule les statistiques de durée des contrats"""
        durations = [(c.end_date - c.start_date).days for c in contracts if c.end_date]
        if not durations:
            return {"average": 0, "min": 0, "max": 0}
        
        return {
            "average": np.mean(durations),
            "min": min(durations),
            "max": max(durations)
        }

    def _calculate_renewal_rate(self, contracts: List[Contract]) -> float:
        """Calcule le taux de renouvellement des contrats"""
        renewals = len([c for c in contracts if c.is_renewal])
        total = len(contracts)
        return renewals / total if total > 0 else 0

    def _get_salary_distribution(self, payrolls: List[Payroll]) -> Dict[str, int]:
        """Calcule la distribution des salaires"""
        salaries = [p.total_amount for p in payrolls]
        if not salaries:
            return {}
            
        bins = pd.qcut(salaries, q=4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        distribution = pd.Series(salaries).groupby(bins).count().to_dict()
        return distribution

    def _get_payroll_trends(self, payrolls: List[Payroll]) -> Dict[str, float]:
        """Analyse les tendances des salaires"""
        if not payrolls:
            return {}
            
        df = pd.DataFrame([(p.date, p.total_amount) for p in payrolls], columns=['date', 'amount'])
        df.set_index('date', inplace=True)
        monthly_avg = df.resample('M').mean()
        
        return monthly_avg.to_dict()['amount']

    def _get_employee_historical_data(self, employee_id: int) -> Dict[str, Any]:
        """Récupère l'historique des données d'un employé"""
        employee = self.db.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            return None
            
        formations = self.db.query(Participation).filter(Participation.employee_id == employee_id).all()
        contracts = self.db.query(Contract).filter(Contract.employee_id == employee_id).all()
        payrolls = self.db.query(Payroll).filter(Payroll.employee_id == employee_id).all()
        
        return {
            "formations": formations,
            "contracts": contracts,
            "payrolls": payrolls,
            "performance": [p.performance_rating for p in payrolls if p.performance_rating]
        }

    def _prepare_features(self, employee_data: Dict[str, Any]) -> np.ndarray:
        """Prépare les features pour le modèle ML"""
        features = []
        
        # Formation features
        formation_completion_rate = len([f for f in employee_data['formations'] if f.status == 'completed']) / len(employee_data['formations']) if employee_data['formations'] else 0
        
        # Contract features
        contract_duration = np.mean([(c.end_date - c.start_date).days for c in employee_data['contracts'] if c.end_date]) if employee_data['contracts'] else 0
        
        # Payroll features
        avg_salary = np.mean([p.total_amount for p in employee_data['payrolls']]) if employee_data['payrolls'] else 0
        
        features.extend([formation_completion_rate, contract_duration, avg_salary])
        return self._scaler.fit_transform(np.array(features).reshape(1, -1))
