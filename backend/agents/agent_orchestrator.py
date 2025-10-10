"""
Agent Orchestrator
Orchestrates multiple AI agents for complex alert processing tasks
"""

from typing import Dict, Any, List
from datetime import datetime
import logging
import asyncio

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Orchestrate multiple agents for complex tasks"""
    
    def __init__(self, bedrock_manager, strands_manager):
        """
        Initialize orchestrator with agent managers
        
        Args:
            bedrock_manager: Bedrock AgentCore manager instance
            strands_manager: Strands Agents manager instance
        """
        self.bedrock_manager = bedrock_manager
        self.strands_manager = strands_manager
        self.processing_stats = {
            "total_processed": 0,
            "phases_completed": 0,
            "correlations_found": 0,
            "automations_triggered": 0
        }
        logger.info("AgentOrchestrator initialized")
    
    async def process_alert_pipeline(self, alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process alerts through multi-phase agent pipeline
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            Dictionary with processing results and statistics
        """
        start_time = datetime.now()
        results = {
            "processed": 0,
            "correlations": [],
            "automations": [],
            "phases": [],
            "processing_time_seconds": 0,
            "agent_insights": []
        }
        
        logger.info(f"Starting alert pipeline processing for {len(alerts)} alerts")
        
        try:
            # Phase 1: Enrichment
            logger.info("Phase 1: Alert enrichment")
            enriched_alerts = await self._enrichment_phase(alerts)
            results["processed"] = len(enriched_alerts)
            results["phases"].append({
                "phase": "enrichment", 
                "status": "completed",
                "alerts_processed": len(enriched_alerts)
            })
            
            # Phase 2: Correlation Analysis
            logger.info("Phase 2: Correlation analysis")
            correlations = await self._correlation_phase(enriched_alerts)
            results["correlations"] = correlations
            results["phases"].append({
                "phase": "correlation", 
                "status": "completed",
                "correlations_found": len(correlations)
            })
            
            # Phase 3: Critical Alert Analysis with Bedrock
            logger.info("Phase 3: Bedrock analysis for critical alerts")
            bedrock_insights = await self._bedrock_analysis_phase(enriched_alerts)
            results["agent_insights"].extend(bedrock_insights)
            results["phases"].append({
                "phase": "bedrock_analysis", 
                "status": "completed",
                "insights_generated": len(bedrock_insights)
            })
            
            # Phase 4: Automation and Workflow Triggers
            logger.info("Phase 4: Automation triggers")
            automations = await self._automation_phase(enriched_alerts, bedrock_insights)
            results["automations"] = automations
            results["phases"].append({
                "phase": "automation", 
                "status": "completed",
                "automations_triggered": len(automations)
            })
            
            # Update processing statistics
            self.processing_stats["total_processed"] += len(alerts)
            self.processing_stats["phases_completed"] += 4
            self.processing_stats["correlations_found"] += len(correlations)
            self.processing_stats["automations_triggered"] += len(automations)
            
        except Exception as e:
            logger.error(f"Error in alert pipeline processing: {e}")
            results["error"] = str(e)
            results["phases"].append({
                "phase": "error", 
                "status": "failed",
                "error": str(e)
            })
        
        # Calculate processing time
        end_time = datetime.now()
        results["processing_time_seconds"] = (end_time - start_time).total_seconds()
        
        logger.info(f"Alert pipeline processing completed in {results['processing_time_seconds']:.2f} seconds")
        return results
    
    async def _enrichment_phase(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Phase 1: Enrich alerts with additional context"""
        enriched_alerts = []
        
        for alert in alerts:
            # Add AI processing timestamp
            alert["enrichments"] = alert.get("enrichments", [])
            alert["enrichments"].append({
                "key": "ai_processed",
                "value": "true",
                "timestamp": datetime.now().isoformat(),
                "source": "agent_orchestrator"
            })
            
            # Add service context
            service = alert.get("service", "unknown")
            alert["enrichments"].append({
                "key": "service_context",
                "value": f"Service: {service}",
                "timestamp": datetime.now().isoformat(),
                "source": "agent_orchestrator"
            })
            
            # Add severity context
            severity = alert.get("severity", "unknown")
            alert["enrichments"].append({
                "key": "severity_analysis",
                "value": f"Severity: {severity}",
                "timestamp": datetime.now().isoformat(),
                "source": "agent_orchestrator"
            })
            
            enriched_alerts.append(alert)
        
        logger.info(f"Enrichment phase completed for {len(enriched_alerts)} alerts")
        return enriched_alerts
    
    async def _correlation_phase(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Phase 2: Find correlations between alerts"""
        correlations = []
        
        # Group alerts by service for correlation analysis
        service_groups = {}
        for alert in alerts:
            service = alert.get("service", "unknown")
            if service not in service_groups:
                service_groups[service] = []
            service_groups[service].append(alert)
        
        # Find correlations within services
        for service, service_alerts in service_groups.items():
            if len(service_alerts) >= 2:
                correlation = {
                    "correlation_id": f"corr_{service}_{datetime.now().timestamp()}",
                    "service": service,
                    "alert_count": len(service_alerts),
                    "confidence": 0.85,
                    "pattern": "service_failure",
                    "alerts": [alert["id"] for alert in service_alerts],
                    "timestamp": datetime.now().isoformat()
                }
                correlations.append(correlation)
                
                # Add correlation info to alerts
                for alert in service_alerts:
                    alert["correlation_id"] = correlation["correlation_id"]
        
        # Find temporal correlations (alerts within 5 minutes)
        temporal_correlations = self._find_temporal_correlations(alerts)
        correlations.extend(temporal_correlations)
        
        logger.info(f"Correlation phase found {len(correlations)} correlations")
        return correlations
    
    def _find_temporal_correlations(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find temporal correlations between alerts"""
        temporal_correlations = []
        
        # Sort alerts by timestamp
        sorted_alerts = sorted(alerts, key=lambda x: x.get("created_at", ""))
        
        for i, alert1 in enumerate(sorted_alerts):
            for alert2 in sorted_alerts[i+1:]:
                # Check if alerts are within 5 minutes
                time1 = datetime.fromisoformat(alert1.get("created_at", "2024-01-01T00:00:00").replace("Z", ""))
                time2 = datetime.fromisoformat(alert2.get("created_at", "2024-01-01T00:00:00").replace("Z", ""))
                
                time_diff = abs((time2 - time1).total_seconds())
                if time_diff <= 300:  # 5 minutes
                    correlation = {
                        "correlation_id": f"temporal_{alert1['id']}_{alert2['id']}",
                        "type": "temporal",
                        "alert_count": 2,
                        "confidence": 0.75,
                        "pattern": "temporal_proximity",
                        "alerts": [alert1["id"], alert2["id"]],
                        "timestamp": datetime.now().isoformat()
                    }
                    temporal_correlations.append(correlation)
        
        return temporal_correlations
    
    async def _bedrock_analysis_phase(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Phase 3: Critical alert analysis with Bedrock"""
        insights = []
        critical_alerts = [a for a in alerts if a.get("severity") == "critical"]
        
        for alert in critical_alerts:
            # Simulate Bedrock analysis
            analysis = {
                "alert_id": alert["id"],
                "analysis": f"AI detected critical issue with {alert.get('title', 'Unknown')}",
                "recommendations": [
                    "Check system logs for errors",
                    "Review recent deployments",
                    "Alert on-call team immediately",
                    "Verify dependent services"
                ],
                "auto_remediation": False,  # Don't auto-fix critical issues
                "confidence": 0.92,
                "timestamp": datetime.now().isoformat(),
                "agent": "bedrock_analyzer"
            }
            
            # Add analysis to alert enrichments
            alert["enrichments"].append({
                "key": "bedrock_analysis",
                "value": analysis["analysis"],
                "timestamp": datetime.now().isoformat(),
                "source": "bedrock_agent"
            })
            
            insights.append(analysis)
        
        logger.info(f"Bedrock analysis phase generated {len(insights)} insights")
        return insights
    
    async def _automation_phase(self, alerts: List[Dict[str, Any]], insights: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Phase 4: Trigger automations based on analysis"""
        automations = []
        
        for alert in alerts:
            severity = alert.get("severity", "unknown")
            
            # Only auto-remediate non-critical alerts
            if severity != "critical":
                automation = {
                    "alert_id": alert["id"],
                    "workflow_triggered": "auto-acknowledge-workflow",
                    "status": "initiated",
                    "timestamp": datetime.now().isoformat(),
                    "reason": f"Non-critical alert auto-acknowledged: {severity}"
                }
                automations.append(automation)
                
                # Update alert status
                alert["status"] = "acknowledged"
                alert["enrichments"].append({
                    "key": "auto_acknowledged",
                    "value": "true",
                    "timestamp": datetime.now().isoformat(),
                    "source": "automation_agent"
                })
        
        logger.info(f"Automation phase triggered {len(automations)} automations")
        return automations
    
    def get_processing_stats(self) -> Dict[str, Any]:
        """Get processing statistics"""
        return self.processing_stats.copy()
    
    def reset_stats(self):
        """Reset processing statistics"""
        self.processing_stats = {
            "total_processed": 0,
            "phases_completed": 0,
            "correlations_found": 0,
            "automations_triggered": 0
        }
        logger.info("Processing statistics reset")
