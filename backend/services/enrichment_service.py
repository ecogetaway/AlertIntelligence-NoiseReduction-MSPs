"""
Enrichment service for MSP Alert Intelligence Platform
"""

import logging
from typing import List, Dict, Any
from uuid import UUID
from sqlmodel import Session, select

from models.alert import AlertEnrichment, AlertEnrichmentRequest

logger = logging.getLogger(__name__)


class EnrichmentService:
    """Service for alert enrichment"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def enrich_alert(self, alert_id: UUID, request: AlertEnrichmentRequest):
        """
        Enrich an alert with additional context
        Stub implementation - logs the request for now
        """
        logger.info(f"Enriching alert {alert_id} with type {request.enrichment_type}")
        
        # TODO: Implement actual enrichment logic based on enrichment_type
        # For now, just create a basic enrichment record
        enrichment = AlertEnrichment(
            alert_id=alert_id,
            key=request.enrichment_type,
            value=str(request.parameters),
            source="enrichment_service"
        )
        
        self.db.add(enrichment)
        self.db.commit()
        
        logger.info(f"Created enrichment for alert {alert_id}")
    
    async def get_alert_enrichments(self, alert_id: UUID) -> List[Dict[str, Any]]:
        """Get all enrichments for an alert"""
        try:
            statement = select(AlertEnrichment).where(AlertEnrichment.alert_id == alert_id)
            result = self.db.exec(statement)
            enrichments = result.all()
            
            return [
                {
                    "id": str(enr.id),
                    "key": enr.key,
                    "value": enr.value,
                    "source": enr.source,
                    "created_at": enr.created_at.isoformat()
                }
                for enr in enrichments
            ]
        except Exception as e:
            logger.error(f"Failed to get enrichments for alert {alert_id}: {e}")
            return []

