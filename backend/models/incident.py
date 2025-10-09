"""
Incident data models for MSP Alert Intelligence Platform
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class IncidentStatus(str, Enum):
    """Incident status"""
    OPEN = "open"
    INVESTIGATING = "investigating"
    IDENTIFIED = "identified"
    MONITORING = "monitoring"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IncidentPriority(str, Enum):
    """Incident priority"""
    P1 = "p1"  # Critical
    P2 = "p2"  # High
    P3 = "p3"  # Medium
    P4 = "p4"  # Low


class IncidentType(str, Enum):
    """Incident type"""
    INFRASTRUCTURE = "infrastructure"
    APPLICATION = "application"
    SECURITY = "security"
    PERFORMANCE = "performance"
    AVAILABILITY = "availability"
    CUSTOM = "custom"


# Database Models
class IncidentBase(SQLModel):
    """Base incident model"""
    title: str
    description: Optional[str] = None
    status: IncidentStatus = IncidentStatus.OPEN
    priority: IncidentPriority
    incident_type: IncidentType
    assignee: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    started_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class Incident(IncidentBase, table=True):
    """Incident database model"""
    __tablename__ = "incidents"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # AI-generated fields
    ai_summary: Optional[str] = None
    ai_root_cause: Optional[str] = None
    ai_impact_assessment: Optional[str] = None
    ai_recommendations: Optional[str] = None
    
    # Relationships
    alerts: List["Alert"] = Relationship(back_populates="incident")
    updates: List["IncidentUpdate"] = Relationship(back_populates="incident")


class IncidentUpdate(SQLModel, table=True):
    """Incident update/comment model"""
    __tablename__ = "incident_updates"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    incident_id: UUID = Field(foreign_key="incidents.id")
    author: str
    content: str
    update_type: str = "comment"  # e.g., "comment", "status_change", "assignment"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    incident: Incident = Relationship(back_populates="updates")


# API Models
class IncidentCreate(BaseModel):
    """Incident creation model"""
    title: str
    description: Optional[str] = None
    priority: IncidentPriority
    incident_type: IncidentType
    assignee: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    alert_ids: List[UUID] = Field(default_factory=list)
    started_at: datetime = Field(default_factory=datetime.utcnow)


class IncidentUpdate(BaseModel):
    """Incident update model"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[IncidentStatus] = None
    priority: Optional[IncidentPriority] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class IncidentResponse(IncidentBase):
    """Incident response model"""
    id: UUID
    created_at: datetime
    ai_summary: Optional[str] = None
    ai_root_cause: Optional[str] = None
    ai_impact_assessment: Optional[str] = None
    ai_recommendations: Optional[str] = None
    alerts: List[Dict[str, Any]] = Field(default_factory=list)
    updates: List[Dict[str, Any]] = Field(default_factory=list)


class IncidentListResponse(BaseModel):
    """Incident list response model"""
    incidents: List[IncidentResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class IncidentUpdateCreate(BaseModel):
    """Incident update creation model"""
    content: str
    update_type: str = "comment"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class IncidentAIAnalysisRequest(BaseModel):
    """Incident AI analysis request"""
    incident_id: UUID
    analysis_type: str  # e.g., "summary", "root_cause", "impact", "recommendations"
    include_alerts: bool = True
    include_updates: bool = True


class IncidentAIAnalysisResponse(BaseModel):
    """Incident AI analysis response"""
    analysis_type: str
    content: str
    confidence: float
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
