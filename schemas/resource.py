from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class ResourceType(str, Enum):
    EQUIPEMENT = "EQUIPEMENT"
    MATERIEL = "MATERIEL"
    VEHICULE = "VEHICULE"
    OUTIL = "OUTIL"
    INTRANT = "INTRANT"
    AUTRE = "AUTRE"

class ResourceStatus(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    EN_UTILISATION = "EN_UTILISATION"
    EN_MAINTENANCE = "EN_MAINTENANCE"
    INDISPONIBLE = "INDISPONIBLE"

class LocationBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=200)

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResourceCategoryBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=200)

class ResourceCategoryCreate(ResourceCategoryBase):
    pass

class ResourceCategory(ResourceCategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResourceMaintenanceBase(BaseModel):
    resource_id: int
    description: str = Field(..., min_length=1, max_length=500)
    cost: float = Field(0, ge=0)
    duration_hours: Optional[float] = Field(None, gt=0)

class ResourceMaintenanceCreate(ResourceMaintenanceBase):
    pass

class ResourceMaintenance(ResourceMaintenanceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ResourceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: ResourceType
    status: ResourceStatus = ResourceStatus.DISPONIBLE
    quantity_total: float = Field(..., gt=0)
    quantity_available: float = Field(..., ge=0)
    quantity_reserved: float = Field(0, ge=0)
    unit: str = Field(..., min_length=1, max_length=20)
    cost_per_unit: Optional[float] = Field(None, ge=0)
    maintenance_cost: float = Field(0, ge=0)
    location_id: Optional[int]
    category_id: Optional[int]

class ResourceCreate(ResourceBase):
    @field_validator('quantity_available')
    @classmethod
    def validate_quantity_available(cls, v: float, info) -> float:
        quantity_total = info.data.get('quantity_total')
        if quantity_total is not None and v > quantity_total:
            raise ValueError("La quantité disponible ne peut pas être supérieure à la quantité totale")
        return v

    @field_validator('quantity_reserved')
    @classmethod
    def validate_quantity_reserved(cls, v: float, info) -> float:
        quantity_total = info.data.get('quantity_total')
        if quantity_total is not None and v > quantity_total:
            raise ValueError("La quantité réservée ne peut pas être supérieure à la quantité totale")
        return v

class ResourceUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    type: Optional[ResourceType]
    status: Optional[ResourceStatus]
    quantity_total: Optional[float] = Field(None, gt=0)
    quantity_available: Optional[float] = Field(None, ge=0)
    quantity_reserved: Optional[float] = Field(None, ge=0)
    unit: Optional[str] = Field(None, min_length=1, max_length=20)
    cost_per_unit: Optional[float] = Field(None, ge=0)
    maintenance_cost: Optional[float] = Field(None, ge=0)
    location_id: Optional[int]
    category_id: Optional[int]

class Resource(ResourceBase):
    id: int
    created_at: datetime
    updated_at: datetime
    location: Optional[Location]
    category: Optional[ResourceCategory]
    maintenance_records: List[ResourceMaintenance] = []

    class Config:
        from_attributes = True

class ResourceList(BaseModel):
    resources: List[Resource]
    total: int
    page: int
    size: int
    total_pages: int

    class Config:
        from_attributes = True
