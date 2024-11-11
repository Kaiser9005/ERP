from sqlalchemy import Column, String, Integer, Float, Enum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum

from models.base import BaseModel

class ResourceType(str, PyEnum):
    """Types de ressources disponibles"""
    EQUIPEMENT = "EQUIPEMENT"
    MATERIEL = "MATERIEL"
    VEHICULE = "VEHICULE"
    OUTIL = "OUTIL"
    INTRANT = "INTRANT"
    AUTRE = "AUTRE"

class ResourceStatus(str, PyEnum):
    """Statuts possibles pour une ressource"""
    DISPONIBLE = "DISPONIBLE"
    EN_UTILISATION = "EN_UTILISATION"
    EN_MAINTENANCE = "EN_MAINTENANCE"
    INDISPONIBLE = "INDISPONIBLE"

class Resource(BaseModel):
    """Modèle pour les ressources du projet"""
    __tablename__ = "resources"

    name = Column(String(100), nullable=False)
    description = Column(String(500))
    type = Column(Enum(ResourceType), nullable=False)
    status = Column(Enum(ResourceStatus), default=ResourceStatus.DISPONIBLE)
    
    # Quantités
    quantity_total = Column(Float, nullable=False)
    quantity_available = Column(Float, nullable=False)
    quantity_reserved = Column(Float, default=0)
    
    # Unité de mesure
    unit = Column(String(20), nullable=False)
    
    # Coûts
    cost_per_unit = Column(Float)
    maintenance_cost = Column(Float, default=0)
    
    # Relations
    location_id = Column(Integer, ForeignKey("locations.id"))
    category_id = Column(Integer, ForeignKey("resource_categories.id"))
    
    # Relations bidirectionnelles
    location = relationship("Location", back_populates="resources")
    category = relationship("ResourceCategory", back_populates="resources")
    task_assignments = relationship("TaskResource", back_populates="resource")
    maintenance_records = relationship("ResourceMaintenance", back_populates="resource")

class ResourceCategory(BaseModel):
    """Catégories de ressources"""
    __tablename__ = "resource_categories"

    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(200))
    
    # Relations bidirectionnelles
    resources = relationship("Resource", back_populates="category")

class ResourceMaintenance(BaseModel):
    """Enregistrements de maintenance des ressources"""
    __tablename__ = "resource_maintenance"

    resource_id = Column(Integer, ForeignKey("resources.id"), nullable=False)
    description = Column(String(500), nullable=False)
    cost = Column(Float, default=0)
    duration_hours = Column(Float)
    
    # Relations bidirectionnelles
    resource = relationship("Resource", back_populates="maintenance_records")

class Location(BaseModel):
    """Emplacements des ressources"""
    __tablename__ = "locations"

    name = Column(String(100), nullable=False)
    description = Column(String(200))
    
    # Relations bidirectionnelles
    resources = relationship("Resource", back_populates="location")
