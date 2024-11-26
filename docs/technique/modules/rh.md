# Module RH - Documentation Technique

## Architecture

### Backend
1. Modèles de Données
   ```python
   # Models
   class Employee(BaseModel):
       id: int
       name: str
       role: str
       skills: List[Skill]
       contracts: List[Contract]
       payrolls: List[Payroll]

   class Contract(BaseModel):
       id: int
       employee_id: int
       type: str
       start_date: date
       end_date: Optional[date]
       salary: float

   class Payroll(BaseModel):
       id: int
       employee_id: int
       period: date
       base_salary: float
       bonuses: List[Bonus]
       deductions: List[Deduction]
       total: float
   ```

2. Services
   ```python
   class HRService:
       def calculate_payroll(self, employee_id: int, period: date) -> Payroll:
           """Calcule la fiche de paie pour un employé"""
           
       def manage_contract(self, employee_id: int, contract: Contract) -> Contract:
           """Gère les contrats des employés"""
           
       def track_skills(self, employee_id: int, skills: List[Skill]) -> Employee:
           """Suit les compétences des employés"""
   ```

3. API Endpoints
   ```python
   @router.post("/employees/{id}/payroll")
   async def generate_payroll(id: int, period: date):
       """Génère une fiche de paie"""
       
   @router.put("/employees/{id}/contract")
   async def update_contract(id: int, contract: Contract):
       """Met à jour le contrat"""
       
   @router.get("/employees/{id}/skills")
   async def get_skills(id: int):
       """Récupère les compétences"""
   ```

### Frontend

1. Composants React
   ```typescript
   // PayrollList.tsx
   const PayrollList: React.FC = () => {
     const { data, isLoading } = useQuery(['payrolls'], getPayrolls);
     return (
       <List>
         {data?.map(payroll => (
           <PayrollItem key={payroll.id} payroll={payroll} />
         ))}
       </List>
     );
   };

   // PayrollForm.tsx
   const PayrollForm: React.FC = () => {
     const mutation = useMutation(createPayroll);
     return (
       <Form onSubmit={handleSubmit}>
         {/* Champs du formulaire */}
       </Form>
     );
   };
   ```

2. Services
   ```typescript
   // payroll.ts
   export const payrollService = {
     getPayrolls: () => api.get('/payrolls'),
     createPayroll: (data: PayrollData) => api.post('/payrolls', data),
     updatePayroll: (id: number, data: PayrollData) => api.put(`/payrolls/${id}`, data)
   };
   ```

3. Types
   ```typescript
   // types/payroll.ts
   export interface Payroll {
     id: number;
     employeeId: number;
     period: string;
     baseSalary: number;
     bonuses: Bonus[];
     deductions: Deduction[];
     total: number;
   }
   ```

## État d'Avancement (50%)

### Implémenté ✅
1. Gestion des Employés
   - CRUD employés
   - Profils détaillés
   - Historique
   - Documentation

2. Gestion des Présences
   - Suivi temps réel
   - Validation automatique
   - Rapports
   - Tests

3. Gestion des Compétences
   - Profils de compétences
   - Évaluation
   - Certifications
   - Documentation

4. Gestion des Contrats
   - Types de contrats
   - Suivi des modifications
   - Validation
   - Tests complets

5. Système de Paie
   - Calcul automatique
   - Gestion des primes
   - Validation
   - Tests complets
   - Documentation

### En Cours 🚧
1. Formation et Évaluation
   - Système de formation
   - Suivi des progrès
   - Évaluation des compétences
   - Documentation

2. Analytics RH
   - KPIs
   - Tableaux de bord
   - Prédictions
   - Documentation

3. Intégration Météo
   - Impact conditions
   - Planning adaptatif
   - Alertes
   - Documentation

## Tests

### Architecture
```python
tests/
  hr/
    test_payroll.py
    test_contract.py
    test_skills.py
    integration/
      test_payroll_integration.py
    e2e/
      test_payroll_workflow.py
```

### Standards
```python
def test_payroll_calculation():
    """Test le calcul d'une fiche de paie"""
    payroll = calculate_payroll(employee_id=1, period="2024-05")
    assert payroll.total == expected_total

def test_contract_validation():
    """Test la validation des contrats"""
    contract = validate_contract(contract_data)
    assert contract.is_valid
```

## Documentation

### API
```yaml
/api/v1/hr/payroll:
  post:
    summary: Crée une fiche de paie
    parameters:
      - name: employee_id
        in: path
        required: true
        schema:
          type: integer
    responses:
      200:
        description: Fiche de paie créée
```

### Frontend
```typescript
/**
 * Composant de liste des fiches de paie
 * @component
 * @example
 * return (
 *   <PayrollList employeeId={1} />
 * )
 */
```

## Prochaines Étapes

1. Formation et Évaluation
   - Système de formation
   - Suivi des progrès
   - Évaluation des compétences
   - Documentation

2. Analytics RH
   - KPIs RH
   - Tableaux de bord
   - Prédictions
   - Documentation

3. Intégration Météo
   - Impact conditions
   - Planning adaptatif
   - Alertes
   - Documentation
