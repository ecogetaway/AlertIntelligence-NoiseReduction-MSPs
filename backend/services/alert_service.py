"""
Alert service for MSP Alert Intelligence Platform
"""

import logging
from typing import List, Optional, Tuple
from uuid import UUID
from datetime import datetime

from sqlmodel import Session, select, func, and_, or_
from sqlalchemy.orm import selectinload

from models.alert import Alert, AlertCreate, AlertUpdate, AlertResponse, AlertStatus
from core.database import get_redis

logger = logging.getLogger(__name__)


class AlertService:
    """Service for alert operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.redis = None
    
    async def create_alert(self, alert_data: AlertCreate) -> AlertResponse:
        """Create a new alert"""
        try:
            # Create alert in database
            alert = Alert(
                title=alert_data.title,
                description=alert_data.description,
                severity=alert_data.severity,
                source=alert_data.source,
                source_id=alert_data.source_id,
                fingerprint=alert_data.fingerprint,
                labels=alert_data.labels,
                annotations=alert_data.annotations,
                started_at=alert_data.started_at
            )
            
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            # Cache alert for quick access
            await self._cache_alert(alert)
            
            logger.info(f"Created alert {alert.id}")
            return self._to_response(alert)
            
        except Exception as e:
            logger.error(f"Failed to create alert: {e}")
            self.db.rollback()
            raise
    
    async def get_alert(self, alert_id: UUID) -> Optional[AlertResponse]:
        """Get alert by ID"""
        try:
            # Try cache first
            cached_alert = await self._get_cached_alert(alert_id)
            if cached_alert:
                return cached_alert
            
            # Query database
            statement = select(Alert).where(Alert.id == alert_id)
            result = self.db.exec(statement)
            alert = result.first()
            
            if alert:
                # Cache the alert
                await self._cache_alert(alert)
                return self._to_response(alert)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get alert {alert_id}: {e}")
            raise
    
    async def list_alerts(
        self,
        page: int = 1,
        page_size: int = 20,
        severity: Optional[str] = None,
        status: Optional[str] = None,
        source: Optional[str] = None,
        search: Optional[str] = None
    ) -> Tuple[List[AlertResponse], int]:
        """List alerts with filtering and pagination"""
        try:
            # Build query
            statement = select(Alert)
            
            # Apply filters
            filters = []
            if severity:
                filters.append(Alert.severity == severity)
            if status:
                filters.append(Alert.status == status)
            if source:
                filters.append(Alert.source == source)
            if search:
                filters.append(
                    or_(
                        Alert.title.ilike(f"%{search}%"),
                        Alert.description.ilike(f"%{search}%")
                    )
                )
            
            if filters:
                statement = statement.where(and_(*filters))
            
            # Get total count
            count_statement = select(func.count(Alert.id))
            if filters:
                count_statement = count_statement.where(and_(*filters))
            total = self.db.exec(count_statement).first()
            
            # Apply pagination
            offset = (page - 1) * page_size
            statement = statement.offset(offset).limit(page_size)
            
            # Order by created_at desc
            statement = statement.order_by(Alert.created_at.desc())
            
            # Execute query
            result = self.db.exec(statement)
            alerts = result.all()
            
            return [self._to_response(alert) for alert in alerts], total
            
        except Exception as e:
            logger.error(f"Failed to list alerts: {e}")
            raise
    
    async def update_alert(self, alert_id: UUID, alert_update: AlertUpdate) -> Optional[AlertResponse]:
        """Update an alert"""
        try:
            statement = select(Alert).where(Alert.id == alert_id)
            result = self.db.exec(statement)
            alert = result.first()
            
            if not alert:
                return None
            
            # Update fields
            update_data = alert_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(alert, field, value)
            
            alert.updated_at = datetime.utcnow()
            
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            # Update cache
            await self._cache_alert(alert)
            
            logger.info(f"Updated alert {alert_id}")
            return self._to_response(alert)
            
        except Exception as e:
            logger.error(f"Failed to update alert {alert_id}: {e}")
            self.db.rollback()
            raise
    
    async def delete_alert(self, alert_id: UUID) -> bool:
        """Delete an alert"""
        try:
            statement = select(Alert).where(Alert.id == alert_id)
            result = self.db.exec(statement)
            alert = result.first()
            
            if not alert:
                return False
            
            self.db.delete(alert)
            self.db.commit()
            
            # Remove from cache
            await self._remove_cached_alert(alert_id)
            
            logger.info(f"Deleted alert {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to delete alert {alert_id}: {e}")
            self.db.rollback()
            raise
    
    async def suppress_alert(self, alert_id: UUID, reason: str) -> bool:
        """Suppress an alert"""
        try:
            statement = select(Alert).where(Alert.id == alert_id)
            result = self.db.exec(statement)
            alert = result.first()
            
            if not alert:
                return False
            
            alert.status = AlertStatus.SUPPRESSED
            alert.updated_at = datetime.utcnow()
            
            # Add suppression reason to annotations
            if not alert.annotations:
                alert.annotations = {}
            alert.annotations["suppression_reason"] = reason
            alert.annotations["suppressed_at"] = datetime.utcnow().isoformat()
            
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            # Update cache
            await self._cache_alert(alert)
            
            logger.info(f"Suppressed alert {alert_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to suppress alert {alert_id}: {e}")
            self.db.rollback()
            raise
    
    async def acknowledge_alert(self, alert_id: UUID, user: str) -> bool:
        """Acknowledge an alert"""
        try:
            statement = select(Alert).where(Alert.id == alert_id)
            result = self.db.exec(statement)
            alert = result.first()
            
            if not alert:
                return False
            
            alert.status = AlertStatus.ACKNOWLEDGED
            alert.updated_at = datetime.utcnow()
            
            # Add acknowledgment info to annotations
            if not alert.annotations:
                alert.annotations = {}
            alert.annotations["acknowledged_by"] = user
            alert.annotations["acknowledged_at"] = datetime.utcnow().isoformat()
            
            self.db.add(alert)
            self.db.commit()
            self.db.refresh(alert)
            
            # Update cache
            await self._cache_alert(alert)
            
            logger.info(f"Acknowledged alert {alert_id} by {user}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
            self.db.rollback()
            raise
    
    def _to_response(self, alert: Alert) -> AlertResponse:
        """Convert Alert model to AlertResponse"""
        return AlertResponse(
            id=alert.id,
            title=alert.title,
            description=alert.description,
            severity=alert.severity,
            status=alert.status,
            source=alert.source,
            source_id=alert.source_id,
            fingerprint=alert.fingerprint,
            labels=alert.labels,
            annotations=alert.annotations,
            started_at=alert.started_at,
            updated_at=alert.updated_at,
            resolved_at=alert.resolved_at,
            created_at=alert.created_at,
            enrichments=[],  # TODO: Load enrichments
            correlations=[],  # TODO: Load correlations
            incident_id=alert.incident_id
        )
    
    async def _cache_alert(self, alert: Alert):
        """Cache alert in Redis"""
        try:
            if not self.redis:
                self.redis = await get_redis()
            
            cache_key = f"alert:{alert.id}"
            alert_data = {
                "id": str(alert.id),
                "title": alert.title,
                "severity": alert.severity.value,
                "status": alert.status.value,
                "source": alert.source.value,
                "created_at": alert.created_at.isoformat()
            }
            
            await self.redis.hset(cache_key, mapping=alert_data)
            await self.redis.expire(cache_key, 3600)  # 1 hour TTL
            
        except Exception as e:
            logger.warning(f"Failed to cache alert {alert.id}: {e}")
    
    async def _get_cached_alert(self, alert_id: UUID) -> Optional[AlertResponse]:
        """Get alert from cache"""
        try:
            if not self.redis:
                self.redis = await get_redis()
            
            cache_key = f"alert:{alert_id}"
            cached_data = await self.redis.hgetall(cache_key)
            
            if cached_data:
                # Convert cached data back to AlertResponse
                return AlertResponse(
                    id=UUID(cached_data["id"]),
                    title=cached_data["title"],
                    severity=cached_data["severity"],
                    status=cached_data["status"],
                    source=cached_data["source"],
                    created_at=datetime.fromisoformat(cached_data["created_at"])
                )
            
            return None
            
        except Exception as e:
            logger.warning(f"Failed to get cached alert {alert_id}: {e}")
            return None
    
    async def _remove_cached_alert(self, alert_id: UUID):
        """Remove alert from cache"""
        try:
            if not self.redis:
                self.redis = await get_redis()
            
            cache_key = f"alert:{alert_id}"
            await self.redis.delete(cache_key)
            
        except Exception as e:
            logger.warning(f"Failed to remove cached alert {alert_id}: {e}")
