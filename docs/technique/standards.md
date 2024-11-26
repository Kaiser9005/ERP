# Standards de Développement ERP FOFAL

## I. Standards de Code

### A. Python
1. Style
   ```python
   # Correct
   def calculate_total(base_amount: float, tax_rate: float) -> float:
       """
       Calcule le montant total avec taxes.
       
       Args:
           base_amount: Montant de base
           tax_rate: Taux de taxe
           
       Returns:
           float: Montant total
       """
       return base_amount * (1 + tax_rate)
   ```

2. Type Hints
   ```python
   from typing import List, Optional, Dict
   
   class Employee:
       def __init__(
           self,
           name: str,
           salary: float,
           skills: Optional[List[str]] = None
       ) -> None:
           self.name = name
           self.salary = salary
           self.skills = skills or []
   ```

3. Exceptions
   ```python
   class PayrollError(Exception):
       """Exception spécifique paie"""
       pass
   
   def process_payroll(employee_id: int) -> Dict:
       if not employee_exists(employee_id):
           raise PayrollError(f"Employé {employee_id} non trouvé")
   ```

### B. TypeScript
1. Interfaces
   ```typescript
   interface Employee {
     id: number;
     name: string;
     salary: number;
     skills?: string[];
   }
   
   interface PayrollResult {
     readonly employeeId: number;
     readonly total: number;
     readonly status: 'pending' | 'processed';
   }
   ```

2. Types
   ```typescript
   type PayrollStatus = 'pending' | 'processed' | 'error';
   
   type PayrollHandler = (
     employeeId: number,
     period: string
   ) => Promise<PayrollResult>;
   ```

3. Génériques
   ```typescript
   interface ApiResponse<T> {
     data: T;
     status: number;
     message: string;
   }
   
   async function fetchData<T>(
     url: string
   ): Promise<ApiResponse<T>> {
     // Implementation
   }
   ```

## II. Architecture

### A. Services
1. Structure
   ```python
   class BaseService:
       """Service de base avec fonctionnalités communes"""
       def __init__(self, db: Database):
           self.db = db
   
   class PayrollService(BaseService):
       """Service spécifique paie"""
       def calculate(self, employee_id: int) -> float:
           # Implementation
   ```

2. Dépendances
   ```python
   class FinanceService:
       def __init__(
           self,
           db: Database,
           cache: Cache,
           logger: Logger
       ):
           self.db = db
           self.cache = cache
           self.logger = logger
   ```

### B. API
1. Routes
   ```python
   @router.get("/employees/{id}/payroll")
   async def get_payroll(
       id: int,
       period: str,
       service: PayrollService = Depends()
   ):
       """Endpoint avec documentation"""
       return await service.get_payroll(id, period)
   ```

2. Validation
   ```python
   class PayrollRequest(BaseModel):
       employee_id: int
       period: str
       
       @validator('period')
       def validate_period(cls, v):
           if not re.match(r'^\d{4}-\d{2}$', v):
               raise ValueError('Format période invalide')
           return v
   ```

## III. Frontend

### A. Components
1. Structure
   ```typescript
   interface Props {
     data: PayrollData;
     onUpdate: (id: number) => void;
   }
   
   const PayrollComponent: React.FC<Props> = ({
     data,
     onUpdate
   }) => {
     return (
       <div className="payroll-container">
         {/* Implementation */}
       </div>
     );
   };
   ```

2. Hooks
   ```typescript
   function usePayroll(employeeId: number) {
     const [data, setData] = useState<PayrollData | null>(null);
     const [loading, setLoading] = useState(true);
     
     useEffect(() => {
       fetchPayroll(employeeId)
         .then(setData)
         .finally(() => setLoading(false));
     }, [employeeId]);
     
     return { data, loading };
   }
   ```

### B. State Management
1. React Query
   ```typescript
   const { data, isLoading } = useQuery(
     ['payroll', employeeId],
     () => fetchPayroll(employeeId),
     {
       staleTime: 5 * 60 * 1000,
       cacheTime: 30 * 60 * 1000
     }
   );
   ```

2. Context
   ```typescript
   interface PayrollContext {
     data: PayrollData[];
     loading: boolean;
     error: Error | null;
   }
   
   const PayrollContext = createContext<PayrollContext>({
     data: [],
     loading: false,
     error: null
   });
   ```

## IV. Tests

### A. Backend
1. Tests Unitaires
   ```python
   def test_calculate_payroll():
       """Test calcul paie"""
       service = PayrollService()
       result = service.calculate(
           base=1000,
           bonus=200
       )
       assert result == 1200
   ```

2. Tests Intégration
   ```python
   async def test_payroll_workflow():
       """Test workflow complet"""
       async with AsyncClient() as client:
           response = await client.post(
               "/api/payroll",
               json={"employee_id": 1}
           )
           assert response.status_code == 200
   ```

### B. Frontend
1. Tests Components
   ```typescript
   describe('PayrollForm', () => {
     it('handles submit correctly', async () => {
       const onSubmit = jest.fn();
       render(<PayrollForm onSubmit={onSubmit} />);
       
       fireEvent.click(screen.getByText('Submit'));
       await waitFor(() => {
         expect(onSubmit).toHaveBeenCalled();
       });
     });
   });
   ```

2. Tests Hooks
   ```typescript
   it('handles loading state', () => {
     const { result } = renderHook(() => usePayroll(1));
     expect(result.current.loading).toBe(true);
   });
   ```

## V. Documentation

### A. Code
1. Python
   ```python
   def process_payroll(
       employee_id: int,
       period: str
   ) -> Dict[str, Any]:
       """
       Traite la paie d'un employé.
       
       Args:
           employee_id: ID de l'employé
           period: Période (format: YYYY-MM)
           
       Returns:
           Dict contenant les détails de paie
           
       Raises:
           PayrollError: Si erreur de traitement
       """
       # Implementation
   ```

2. TypeScript
   ```typescript
   /**
    * Composant affichant les détails de paie
    * @param props - Props du composant
    * @param props.data - Données de paie
    * @param props.onUpdate - Callback mise à jour
    * @returns JSX.Element
    */
   function PayrollDetails(props: Props): JSX.Element {
     // Implementation
   }
   ```

### B. API
```yaml
openapi: 3.0.0
info:
  title: API Paie
  version: 1.0.0
paths:
  /payroll:
    post:
      summary: Génère une paie
      parameters:
        - name: employee_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Paie générée
```

## VI. Sécurité

### A. Authentication
```python
def verify_token(token: str = Depends(oauth2_scheme)):
    """Vérifie JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token invalide"
        )
```

### B. Authorization
```python
def check_permissions(
    user: User = Depends(get_current_user)
):
    """Vérifie permissions utilisateur"""
    if not user.has_permission('payroll'):
        raise HTTPException(
            status_code=403,
            detail="Permission refusée"
        )
```

## VII. Performance

### A. Cache
```python
@cached(ttl=300)  # 5 minutes
def get_payroll_stats(period: str) -> Dict:
    """Récupère stats avec cache"""
    return calculate_stats(period)
```

### B. Database
```python
from sqlalchemy import Index

class Employee(Base):
    __tablename__ = 'employees'
    __table_args__ = (
        Index('idx_employee_department',
              'department_id'),
    )
```

## VIII. Monitoring

### A. Logs
```python
logger = logging.getLogger(__name__)

def process_payroll():
    """Process avec logs"""
    logger.info("Début traitement paie")
    try:
        # Process
        logger.info("Paie traitée")
    except Exception as e:
        logger.error(f"Erreur: {str(e)}")
        raise
```

### B. Metrics
```python
from prometheus_client import Counter, Histogram

payroll_process_time = Histogram(
    'payroll_processing_seconds',
    'Temps traitement paie'
)

@payroll_process_time.time()
def process_payroll():
    """Process avec metrics"""
    # Implementation
