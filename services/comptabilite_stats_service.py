from sqlalchemy.orm import Session
from typing import Dict, Any, List
from datetime import datetime, date, timedelta
from models.comptabilite import (
    CompteComptable, EcritureComptable, TypeCompte, StatutEcriture
)
from sqlalchemy import func, and_
from decimal import Decimal
from services.weather_service import WeatherService

class ComptabiliteStatsService:
    def __init__(self, db: Session):
        self.db = db
        self.weather_service = WeatherService(db)

    async def get_stats(self) -> Dict[str, Any]:
        """Calcule les statistiques financières"""
        now = datetime.utcnow()
        current_month = now.strftime("%Y-%m")
        last_month = (now - timedelta(days=30)).strftime("%Y-%m")

        # Chiffre d'affaires du mois
        revenue = self.db.query(
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.PRODUIT
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == current_month
        ).scalar() or 0

        # Chiffre d'affaires du mois précédent
        previous_revenue = self.db.query(
            func.sum(EcritureComptable.credit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.PRODUIT
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul des charges
        expenses = self.db.query(
            func.sum(EcritureComptable.debit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.CHARGE
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == current_month
        ).scalar() or 0

        previous_expenses = self.db.query(
            func.sum(EcritureComptable.debit)
        ).filter(
            EcritureComptable.compte_id.in_(
                self.db.query(CompteComptable.id).filter(
                    CompteComptable.type_compte == TypeCompte.CHARGE
                )
            ),
            EcritureComptable.statut == StatutEcriture.VALIDEE,
            func.to_char(EcritureComptable.date_ecriture, 'YYYY-MM') == last_month
        ).scalar() or 0

        # Calcul de la trésorerie
        cashflow = self.db.query(
            func.sum(CompteComptable.solde_debit - CompteComptable.solde_credit)
        ).filter(
            CompteComptable.type_compte == TypeCompte.ACTIF,
            CompteComptable.actif == True
        ).scalar() or 0

        previous_cashflow = cashflow - (revenue - expenses)

        return {
            "revenue": float(revenue),
            "revenueVariation": self._calculate_variation(revenue, previous_revenue),
            "expenses": float(expenses),
            "expensesVariation": self._calculate_variation(expenses, previous_expenses),
            "profit": float(revenue - expenses),
            "profitVariation": self._calculate_variation(
                revenue - expenses,
                previous_revenue - previous_expenses
            ),
            "cashflow": float(cashflow),
            "cashflowVariation": self._calculate_variation(cashflow, previous_cashflow)
        }

    async def get_budget_analysis(self, periode: str) -> Dict[str, Any]:
        """Analyse détaillée du budget pour une période"""
        # Récupération des données budgétaires
        charges = await self._get_charges_by_categorie(periode)
        produits = await self._get_produits_by_categorie(periode)
        
        # Impact météo
        weather_impact = await self._analyze_weather_impact(periode)
        
        # Calcul des totaux
        total_prevu = sum(cat["prevu"] for cat in charges.values()) + sum(cat["prevu"] for cat in produits.values())
        total_realise = sum(cat["realise"] for cat in charges.values()) + sum(cat["realise"] for cat in produits.values())
        
        # Génération des recommandations
        recommendations = []
        for categorie, data in {**charges, **produits}.items():
            ecart = ((data["realise"] - data["prevu"]) / data["prevu"] * 100) if data["prevu"] != 0 else 0
            if abs(ecart) > 10:
                recommendations.append(
                    f"{'Dépassement' if ecart > 0 else 'Sous-utilisation'} "
                    f"du budget {categorie}: {abs(ecart):.1f}% d'écart"
                )

        return {
            "total_prevu": float(total_prevu),
            "total_realise": float(total_realise),
            "categories": {**charges, **produits},
            "weather_impact": weather_impact,
            "recommendations": recommendations
        }

    async def get_cashflow(self, days: int = 30) -> List[Dict[str, Any]]:
        """Récupère les données de trésorerie sur une période"""
        end_date = datetime.now(datetime.timezone.utc).date()
        start_date = end_date - timedelta(days=days)
        
        # Récupération des écritures
        query = self.db.query(
            func.date_trunc('day', EcritureComptable.date_ecriture).label('date'),
            func.sum(EcritureComptable.debit).label('sorties'),
            func.sum(EcritureComptable.credit).label('entrees')
        ).filter(
            EcritureComptable.date_ecriture.between(start_date, end_date),
            EcritureComptable.statut == StatutEcriture.VALIDEE
        ).group_by(
            func.date_trunc('day', EcritureComptable.date_ecriture)
        ).order_by(
            func.date_trunc('day', EcritureComptable.date_ecriture)
        )

        results = []
        solde_cumule = self._get_solde_initial(start_date)
        
        # Génération des données jour par jour
        current_date = start_date
        while current_date <= end_date:
            daily_data = query.filter(
                func.date_trunc('day', EcritureComptable.date_ecriture) == current_date
            ).first()

            entrees = float(daily_data.entrees if daily_data else 0)
            sorties = float(daily_data.sorties if daily_data else 0)
            solde_cumule += entrees - sorties

            # Récupération de l'impact météo
            weather_data = await self.weather_service.get_daily_impact(current_date)
            
            results.append({
                "date": current_date.strftime("%Y-%m-%d"),
                "entrees": entrees,
                "sorties": sorties,
                "solde": float(solde_cumule),
                "prevision": self._calculate_prevision(solde_cumule, weather_data["impact"]),
                "impact_meteo": weather_data["impact"]
            })
            
            current_date += timedelta(days=1)

        return results

    def _calculate_variation(self, current: float, previous: float) -> Dict[str, Any]:
        """Calcule la variation entre deux valeurs"""
        if previous == 0:
            return {"value": 0, "type": "increase"}
        
        variation = ((current - previous) / abs(previous)) * 100
        return {
            "value": abs(round(variation, 1)),
            "type": "increase" if variation >= 0 else "decrease"
        }

    async def _get_charges_by_categorie(self, periode: str) -> Dict[str, Dict[str, float]]:
        """Récupère les charges par catégorie"""
        return await self._get_montants_by_categorie(TypeCompte.CHARGE, periode)

    async def _get_produits_by_categorie(self, periode: str) -> Dict[str, Dict[str, float]]:
        """Récupère les produits par catégorie"""
        return await self._get_montants_by_categorie(TypeCompte.PRODUIT, periode)

    async def _get_montants_by_categorie(
        self,
        type_compte: TypeCompte,
        periode: str
    ) -> Dict[str, Dict[str, float]]:
        """Récupère les montants par catégorie pour un type de compte"""
        query = self.db.query(
            CompteComptable.numero,
            CompteComptable.libelle,
            func.sum(EcritureComptable.debit).label('debit'),
            func.sum(EcritureComptable.credit).label('credit')
        ).join(
            EcritureComptable,
            CompteComptable.id == EcritureComptable.compte_id
        ).filter(
            CompteComptable.type_compte == type_compte,
            EcritureComptable.periode == periode
        ).group_by(
            CompteComptable.numero,
            CompteComptable.libelle
        )

        results = {}
        for row in query.all():
            montant = float(row.credit - row.debit if type_compte == TypeCompte.PRODUIT else row.debit - row.credit)
            results[row.numero] = {
                "libelle": row.libelle,
                "prevu": montant * 1.1,  # TODO: Implémenter la logique de budget prévisionnel
                "realise": montant
            }

        return results

    def _get_solde_initial(self, date: date) -> Decimal:
        """Calcule le solde initial à une date donnée"""
        return self.db.query(
            func.sum(CompteComptable.solde_debit - CompteComptable.solde_credit)
        ).filter(
            CompteComptable.type_compte == TypeCompte.ACTIF,
            CompteComptable.actif == True
        ).scalar() or Decimal('0')

    def _calculate_prevision(self, solde: float, impact_meteo: float) -> float:
        """Calcule la prévision de trésorerie en tenant compte de l'impact météo"""
        return solde * (1 + (impact_meteo / 100))

    async def _analyze_weather_impact(self, periode: str) -> Dict[str, Any]:
        """Analyse l'impact de la météo sur les finances"""
        weather_data = await self.weather_service.get_monthly_stats(periode)
        
        impact = {
            "score": 0,
            "factors": [],
            "projections": {}
        }

        if weather_data.get("precipitation", 0) > 200:
            impact["score"] += 30
            impact["factors"].append("Fortes précipitations")
            impact["projections"]["TRANSPORT"] = "Augmentation probable des coûts"

        if weather_data.get("temperature_avg", 25) > 30:
            impact["score"] += 20
            impact["factors"].append("Températures élevées")
            impact["projections"]["MAINTENANCE"] = "Coûts supplémentaires possibles"

        return impact
