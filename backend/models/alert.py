"""
Alert data models for MSP Alert Intelligence Platform
"""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Any
from uuid import UUID, uuid4

from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel


class AlertSeverity(str, Enum):
    """Alert severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class AlertStatus(str, Enum):
    """Alert status"""
    ACTIVE = "active"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    SUPPRESSED = "suppressed"
    DISMISSED = "dismissed"


class AlertSource(str, Enum):
    """Alert source types"""
    PROMETHEUS = "prometheus"
    DATADOG = "datadog"
    SENTRY = "sentry"
    NEW_RELIC = "new_relic"
    GRAFANA = "grafana"
    CUSTOM = "custom"


# Database Models
class AlertBase(SQLModel):
    """Base alert model"""
    title: str
    description: Optional[str] = None
    severity: AlertSeverity
    status: AlertStatus = AlertStatus.ACTIVE
    source: AlertSource
    source_id: str
    fingerprint: str
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)
    started_at: datetime
    updated_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None


class Alert(AlertBase, table=True):
    """Alert database model"""
    __tablename__ = "alerts"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    enrichments: List["AlertEnrichment"] = Relationship(back_populates="alert")
    correlations: List["AlertCorrelation"] = Relationship(back_populates="alert")
    incident_id: Optional[UUID] = Field(default=None, foreign_key="incidents.id")


class AlertEnrichment(SQLModel, table=True):
    """Alert enrichment data"""
    __tablename__ = "alert_enrichments"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    alert_id: UUID = Field(foreign_key="alerts.id")
    key: str
    value: str
    source: str  # e.g., "ai_agent", "external_api", "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    alert: Alert = Relationship(back_populates="enrichments")


class AlertCorrelation(SQLModel, table=True):
    """Alert correlation data"""
    __tablename__ = "alert_correlations"
    
    id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    alert_id: UUID = Field(foreign_key="alerts.id")
    correlated_alert_id: UUID = Field(foreign_key="alerts.id")
    correlation_type: str  # e.g., "temporal", "spatial", "causal"
    confidence: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    alert: Alert = Relationship(back_populates="correlations")


# API Models
class AlertCreate(BaseModel):
    """Alert creation model"""
    title: str
    description: Optional[str] = None
    severity: AlertSeverity
    source: AlertSource
    source_id: str
    fingerprint: str
    labels: Dict[str, str] = Field(default_factory=dict)
    annotations: Dict[str, str] = Field(default_factory=dict)
    started_at: datetime = Field(default_factory=datetime.utcnow)


class AlertUpdate(BaseModel):
    """Alert update model"""
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    labels: Optional[Dict[str, str]] = None
    annotations: Optional[Dict[str, str]] = None


class AlertResponse(AlertBase):
    """Alert response model"""
    id: UUID
    created_at: datetime
    enrichments: List[Dict[str, Any]] = Field(default_factory=list)
    correlations: List[Dict[str, Any]] = Field(default_factory=list)
    incident_id: Optional[UUID] = None


class AlertListResponse(BaseModel):
    """Alert list response model"""
    alerts: List[AlertResponse]
    total: int
    page: int
    page_size: int
    has_next: bool
    has_previous: bool


class AlertDeduplicationRequest(BaseModel):
    """Alert deduplication request"""
    alerts: List[AlertCreate]
    window_seconds: int = 300  # 5 minutes default


class AlertDeduplicationResponse(BaseModel):
    """Alert deduplication response"""
    unique_alerts: List[AlertCreate]
    duplicate_alerts: List[AlertCreate]
    deduplication_stats: Dict[str, int]


class AlertCorrelationRequest(BaseModel):
    """Alert correlation request"""
    alert_ids: List[UUID]
    window_seconds: int = 1800  # 30 minutes default


class AlertCorrelationResponse(BaseModel):
    """Alert correlation response"""
    correlations: List[Dict[str, Any]]
    correlation_stats: Dict[str, int]


class AlertFilterRequest(BaseModel):
    """Alert filtering request"""
    severity: Optional[List[AlertSeverity]] = None
    status: Optional[List[AlertStatus]] = None
    source: Optional[List[AlertSource]] = None
    labels: Optional[Dict[str, str]] = None
    time_range: Optional[Dict[str, datetime]] = None
    search_query: Optional[str] = None


class AlertEnrichmentRequest(BaseModel):
    """Alert enrichment request"""
    alert_id: UUID
    enrichment_type: str  # e.g., "ai_summary", "context", "similar_incidents"
    parameters: Dict[str, Any] = Field(default_factory=dict)
