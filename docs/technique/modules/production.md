# Module Production - Documentation Technique

## I. Architecture

### A. Structure
```
production/
├── models/
│   ├── production.py
│   └── iot_sensor.py
├── services/
│   ├── production_service.py
│   ├── production_ml_service.py
│   └── iot_service.py
├── api/
│   └── endpoints/
│       ├── production.py
│       └── iot.py
└── frontend/
    └── components/
        ├── production/
        └── iot/
```

### B. Modèles
```python
class Parcelle(BaseModel):
    """Modèle parcelle agricole"""
    id: int
    nom: str
    surface: float
    culture: str
    capteurs: List[IoTSensor]
    
class IoTSensor(BaseModel):
    """Modèle capteur IoT"""
    id: int
    type: str
    parcelle_id: int
    valeur: float
    timestamp: datetime
```

## II. Services

### A. Production
```python
class ProductionService:
    """Service gestion production"""
    
    def __init__(
        self,
        db: Database,
        ml_service: ProductionMLService,
        iot_service: IoTService
    ):
        self.db = db
        self.ml = ml_service
        self.iot = iot_service
    
    async def get_parcelle_stats(
        self,
        parcelle_id: int
    ) -> Dict:
        """Récupère statistiques parcelle"""
        data = await self.db.get_parcelle(parcelle_id)
        predictions = await self.ml.predict(data)
        sensors = await self.iot.get_sensors(parcelle_id)
        return {
            "data": data,
            "predictions": predictions,
            "sensors": sensors
        }
```

### B. ML Service
```python
class ProductionMLService:
    """Service ML production"""
    
    def predict_yield(
        self,
        parcelle_data: Dict,
        weather_data: Dict
    ) -> float:
        """Prédit rendement parcelle"""
        model = self.load_model()
        features = self.prepare_features(
            parcelle_data,
            weather_data
        )
        return model.predict(features)
    
    def optimize_irrigation(
        self,
        soil_data: Dict,
        weather_forecast: Dict
    ) -> Dict:
        """Optimise irrigation"""
        return self.irrigation_optimizer.optimize(
            soil_data,
            weather_forecast
        )
```

### C. IoT Service
```python
class IoTService:
    """Service IoT"""
    
    async def get_sensor_data(
        self,
        sensor_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Dict]:
        """Récupère données capteur"""
        return await self.db.query_sensor_data(
            sensor_id,
            start_date,
            end_date
        )
    
    async def process_sensor_alert(
        self,
        alert: Dict
    ) -> None:
        """Traite alerte capteur"""
        if self.is_critical(alert):
            await self.notify_urgent(alert)
        await self.store_alert(alert)
```

## III. API

### A. Endpoints
```python
@router.get("/parcelles/{id}/stats")
async def get_parcelle_stats(
    id: int,
    service: ProductionService = Depends()
) -> Dict:
    """Endpoint statistiques parcelle"""
    return await service.get_parcelle_stats(id)

@router.post("/sensors/{id}/data")
async def post_sensor_data(
    id: int,
    data: SensorData,
    service: IoTService = Depends()
) -> Dict:
    """Endpoint données capteur"""
    return await service.process_sensor_data(id, data)
```

### B. Schémas
```python
class SensorData(BaseModel):
    """Schéma données capteur"""
    timestamp: datetime
    value: float
    type: str
    unit: str
    
    @validator('value')
    def validate_value(cls, v):
        if v < 0:
            raise ValueError('Valeur négative')
        return v
```

## IV. Frontend

### A. Components
```typescript
interface ParcelleProps {
  id: number;
  onUpdate: () => void;
}

const ParcelleDetails: React.FC<ParcelleProps> = ({
  id,
  onUpdate
}) => {
  const { data, isLoading } = useQuery(
    ['parcelle', id],
    () => fetchParcelleStats(id)
  );
  
  return (
    <div className="parcelle-details">
      <ParcelleHeader data={data} />
      <ParcelleStats stats={data?.stats} />
      <SensorsList sensors={data?.sensors} />
      <WeatherWidget location={data?.location} />
    </div>
  );
};
```

### B. Services
```typescript
const productionApi = {
  getParcelleStats: (id: number) =>
    api.get<ParcelleStats>(`/parcelles/${id}/stats`),
    
  getSensorData: (
    id: number,
    params: SensorQueryParams
  ) => api.get<SensorData[]>(
    `/sensors/${id}/data`,
    { params }
  )
};
```

## V. Tests

### A. Tests Unitaires
```python
def test_yield_prediction():
    """Test prédiction rendement"""
    service = ProductionMLService()
    result = service.predict_yield(
        parcelle_data=MOCK_PARCELLE,
        weather_data=MOCK_WEATHER
    )
    assert 0 <= result <= 100
    assert isinstance(result, float)

def test_sensor_alert_processing():
    """Test traitement alerte"""
    service = IoTService()
    alert = {
        "sensor_id": 1,
        "value": 25.5,
        "threshold": 25.0,
        "type": "temperature"
    }
    result = service.process_sensor_alert(alert)
    assert result.status == "processed"
```

### B. Tests Intégration
```python
async def test_production_workflow():
    """Test workflow production complet"""
    # Setup
    parcelle_id = await create_test_parcelle()
    sensor_id = await setup_test_sensor(parcelle_id)
    
    # Execute
    await post_sensor_data(sensor_id, TEST_DATA)
    stats = await get_parcelle_stats(parcelle_id)
    
    # Verify
    assert stats["sensors"][0]["value"] == TEST_DATA["value"]
    assert "predictions" in stats
    assert stats["status"] == "success"
```

## VI. ML

### A. Modèles
```python
class YieldPredictor:
    """Prédicteur rendement"""
    
    def __init__(self):
        self.model = self.load_model()
        
    def predict(
        self,
        features: np.ndarray
    ) -> float:
        """Prédit rendement"""
        return self.model.predict(features)[0]
        
    def retrain(
        self,
        new_data: pd.DataFrame
    ) -> None:
        """Réentraîne modèle"""
        self.model = self.train_model(new_data)
```

### B. Optimisation
```python
class IrrigationOptimizer:
    """Optimiseur irrigation"""
    
    def optimize(
        self,
        soil_data: Dict,
        weather: Dict
    ) -> Dict:
        """Optimise irrigation"""
        constraints = self.get_constraints(soil_data)
        forecast = self.process_weather(weather)
        
        result = minimize(
            self.objective_function,
            x0=self.initial_guess,
            constraints=constraints
        )
        
        return {
            "schedule": result.x,
            "water_saved": result.fun,
            "confidence": self.get_confidence(result)
        }
```

## VII. Monitoring

### A. Métriques
```python
# Métriques production
parcelle_updates = Counter(
    'parcelle_updates_total',
    'Mises à jour parcelles',
    ['type']
)

sensor_readings = Histogram(
    'sensor_readings',
    'Lectures capteurs',
    ['sensor_type']
)

ml_prediction_time = Histogram(
    'ml_prediction_seconds',
    'Temps prédiction ML'
)
```

### B. Alertes
```python
def check_sensor_health():
    """Vérifie santé capteurs"""
    for sensor in get_active_sensors():
        if not sensor.is_healthy():
            alert = Alert(
                name="sensor_failure",
                severity="high",
                sensor_id=sensor.id
            )
            alerts_service.send(alert)
```

## VIII. Documentation

### A. API
```yaml
openapi: 3.0.0
info:
  title: API Production
  version: 1.0.0
paths:
  /parcelles/{id}/stats:
    get:
      summary: Statistiques parcelle
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Succès
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/ParcelleStats'
```

### B. ML
```markdown
# Documentation ML Production

## Modèles
- YieldPredictor: Random Forest
- IrrigationOptimizer: Linear Programming

## Features
- Météo: température, précipitations
- Sol: humidité, pH
- Historique: rendements passés

## Performance
- MAE: 2.3
- RMSE: 3.1
- R²: 0.89
