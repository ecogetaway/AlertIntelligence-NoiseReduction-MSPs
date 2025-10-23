"""
Alert API routes for MSP Alert Intelligence Platform
"""

import logging
from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from core.database import get_db
from models.alert import (
    Alert, AlertCreate, AlertUpdate, AlertResponse, AlertListResponse,
    AlertDeduplicationRequest, AlertDeduplicationResponse,
    AlertCorrelationRequest, AlertCorrelationResponse,
    AlertFilterRequest, AlertEnrichmentRequest
)
from services.alert_service import AlertService
from services.keep_client import KeepClient
from services.deduplication_service import DeduplicationService
from services.correlation_service import CorrelationService
from services.enrichment_service import EnrichmentService

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=AlertResponse)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    try:
        alert_service = AlertService(db)
        created_alert = await alert_service.create_alert(alert)
        return created_alert
    except Exception as e:
        logger.error(f"Failed to create alert: {e}")
        raise HTTPException(status_code=500, detail="Failed to create alert")


@router.get("/", response_model=AlertListResponse)
async def list_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List alerts with filtering and pagination"""
    try:
        keep = KeepClient()
        if keep.is_configured():
            # Keep-backed path
            raw_alerts = await keep.fetch_alerts()
            mapped = [KeepClient.map_keep_alert(a) for a in raw_alerts]
            filtered = KeepClient.apply_filters(
                mapped,
                severity=severity,
                status=status,
                source=source,
                search=search,
            )
            total = len(filtered)
            start = (page - 1) * page_size
            end = start + page_size
            page_items = filtered[start:end]
            return AlertListResponse(
                alerts=page_items,  # type: ignore[arg-type]
                total=total,
                page=page,
                page_size=page_size,
                has_next=end < total,
                has_previous=page > 1,
            )
        else:
            # Local DB path
            alert_service = AlertService(db)
            alerts, total = await alert_service.list_alerts(
                page=page,
                page_size=page_size,
                severity=severity,
                status=status,
                source=source,
                search=search
            )
            
            return AlertListResponse(
                alerts=alerts,
                total=total,
                page=page,
                page_size=page_size,
                has_next=page * page_size < total,
                has_previous=page > 1
            )
    except Exception as e:
        logger.error(f"Failed to list alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to list alerts")


@router.get("/advanced-filter", response_model=AlertListResponse)
async def advanced_filter_alerts(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    severity: Optional[str] = None,
    status: Optional[str] = None,
    source: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Advanced filter endpoint; currently same behavior as list with server-side filtering.
    Provided separately for frontend compatibility.
    """
    return await list_alerts(
        page=page,
        page_size=page_size,
        severity=severity,
        status=status,
        source=source,
        search=search,
        db=db,
    )


@router.get("/{alert_id}", response_model=AlertResponse)
async def get_alert(
    alert_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific alert by ID"""
    try:
        alert_service = AlertService(db)
        alert = await alert_service.get_alert(alert_id)
        if not alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alert")


@router.put("/{alert_id}", response_model=AlertResponse)
async def update_alert(
    alert_id: UUID,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db)
):
    """Update an alert"""
    try:
        alert_service = AlertService(db)
        updated_alert = await alert_service.update_alert(alert_id, alert_update)
        if not updated_alert:
            raise HTTPException(status_code=404, detail="Alert not found")
        return updated_alert
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to update alert")


@router.delete("/{alert_id}")
async def delete_alert(
    alert_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an alert"""
    try:
        alert_service = AlertService(db)
        success = await alert_service.delete_alert(alert_id)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to delete alert")


@router.post("/deduplicate", response_model=AlertDeduplicationResponse)
async def deduplicate_alerts(
    request: AlertDeduplicationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Deduplicate alerts to remove duplicates"""
    try:
        deduplication_service = DeduplicationService(db)
        result = await deduplication_service.deduplicate_alerts(
            request.alerts,
            request.window_seconds
        )
        
        # Process unique alerts in background
        if result.unique_alerts:
            background_tasks.add_task(
                _process_unique_alerts,
                result.unique_alerts,
                db
            )
        
        return result
    except Exception as e:
        logger.error(f"Failed to deduplicate alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to deduplicate alerts")


@router.post("/correlate", response_model=AlertCorrelationResponse)
async def correlate_alerts(
    request: AlertCorrelationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Correlate related alerts"""
    try:
        correlation_service = CorrelationService(db)
        result = await correlation_service.correlate_alerts(
            request.alert_ids,
            request.window_seconds
        )
        
        # Process correlations in background
        if result.correlations:
            background_tasks.add_task(
                _process_correlations,
                result.correlations,
                db
            )
        
        return result
    except Exception as e:
        logger.error(f"Failed to correlate alerts: {e}")
        raise HTTPException(status_code=500, detail="Failed to correlate alerts")


@router.post("/{alert_id}/enrich")
async def enrich_alert(
    alert_id: UUID,
    request: AlertEnrichmentRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Enrich an alert with additional context"""
    try:
        enrichment_service = EnrichmentService(db)
        
        # Start enrichment in background
        background_tasks.add_task(
            _enrich_alert_background,
            alert_id,
            request,
            db
        )
        
        return {"message": "Alert enrichment started"}
    except Exception as e:
        logger.error(f"Failed to start alert enrichment: {e}")
        raise HTTPException(status_code=500, detail="Failed to start alert enrichment")


@router.get("/{alert_id}/enrichments")
async def get_alert_enrichments(
    alert_id: UUID,
    db: Session = Depends(get_db)
):
    """Get enrichments for an alert"""
    try:
        enrichment_service = EnrichmentService(db)
        enrichments = await enrichment_service.get_alert_enrichments(alert_id)
        return {"enrichments": enrichments}
    except Exception as e:
        logger.error(f"Failed to get alert enrichments: {e}")
        raise HTTPException(status_code=500, detail="Failed to get alert enrichments")


@router.post("/{alert_id}/suppress")
async def suppress_alert(
    alert_id: UUID,
    reason: str,
    db: Session = Depends(get_db)
):
    """Suppress an alert"""
    try:
        alert_service = AlertService(db)
        success = await alert_service.suppress_alert(alert_id, reason)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert suppressed successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to suppress alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to suppress alert")


@router.post("/{alert_id}/acknowledge")
async def acknowledge_alert(
    alert_id: UUID,
    user: str,
    db: Session = Depends(get_db)
):
    """Acknowledge an alert"""
    try:
        alert_service = AlertService(db)
        success = await alert_service.acknowledge_alert(alert_id, user)
        if not success:
            raise HTTPException(status_code=404, detail="Alert not found")
        return {"message": "Alert acknowledged successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to acknowledge alert {alert_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to acknowledge alert")


# Background task functions
async def _process_unique_alerts(alerts: List[AlertCreate], db: Session):
    """Process unique alerts in background"""
    try:
        alert_service = AlertService(db)
        for alert in alerts:
            await alert_service.create_alert(alert)
        logger.info(f"Processed {len(alerts)} unique alerts")
    except Exception as e:
        logger.error(f"Failed to process unique alerts: {e}")


async def _process_correlations(correlations: List[dict], db: Session):
    """Process correlations in background"""
    try:
        correlation_service = CorrelationService(db)
        for correlation in correlations:
            await correlation_service.save_correlation(correlation)
        logger.info(f"Processed {len(correlations)} correlations")
    except Exception as e:
        logger.error(f"Failed to process correlations: {e}")


async def _enrich_alert_background(alert_id: UUID, request: AlertEnrichmentRequest, db: Session):
    """Enrich alert in background"""
    try:
        enrichment_service = EnrichmentService(db)
        await enrichment_service.enrich_alert(alert_id, request)
        logger.info(f"Enriched alert {alert_id}")
    except Exception as e:
        logger.error(f"Failed to enrich alert {alert_id}: {e}")
