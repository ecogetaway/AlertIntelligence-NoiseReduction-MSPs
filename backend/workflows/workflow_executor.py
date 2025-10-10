"""
Simple Workflow Executor for MSP Alert Intelligence Platform
Inspired by Keep's workflow engine but simplified for demo purposes
"""

import logging
import yaml
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
import asyncio
import json

logger = logging.getLogger(__name__)


class WorkflowExecutor:
    """Execute YAML-based workflows for alert processing"""
    
    def __init__(self, workflows_dir: str = None):
        """Initialize workflow executor with workflows directory"""
        if workflows_dir is None:
            workflows_dir = os.path.join(os.path.dirname(__file__), "../../workflows")
        
        self.workflows_dir = Path(workflows_dir)
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.load_workflows()
        logger.info(f"WorkflowExecutor initialized with {len(self.workflows)} workflows")
    
    def load_workflows(self):
        """Load all YAML workflows from the workflows directory"""
        if not self.workflows_dir.exists():
            logger.warning(f"Workflows directory not found: {self.workflows_dir}")
            return
        
        for yaml_file in self.workflows_dir.glob("*.yml"):
            try:
                with open(yaml_file, 'r') as f:
                    workflow_data = yaml.safe_load(f)
                    if workflow_data and 'workflow' in workflow_data:
                        workflow = workflow_data['workflow']
                        workflow_id = workflow.get('id', yaml_file.stem)
                        self.workflows[workflow_id] = workflow
                        logger.info(f"Loaded workflow: {workflow_id} from {yaml_file.name}")
            except Exception as e:
                logger.error(f"Error loading workflow from {yaml_file}: {e}")
    
    def get_workflow(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get a workflow by ID"""
        return self.workflows.get(workflow_id)
    
    def list_workflows(self) -> List[Dict[str, str]]:
        """List all available workflows"""
        return [
            {
                "id": wf_id,
                "name": wf.get("name", wf_id),
                "description": wf.get("description", ""),
                "triggers": [t.get("type") for t in wf.get("triggers", [])]
            }
            for wf_id, wf in self.workflows.items()
        ]
    
    async def execute_workflow(
        self, 
        workflow_id: str, 
        trigger_event: Dict[str, Any],
        context: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Execute a workflow with the given trigger event
        
        Args:
            workflow_id: ID of the workflow to execute
            trigger_event: Event that triggered the workflow (e.g., alert data)
            context: Additional context for workflow execution
        
        Returns:
            Dict with execution results
        """
        workflow = self.get_workflow(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow not found: {workflow_id}")
        
        logger.info(f"Executing workflow: {workflow_id}")
        
        context = context or {}
        context.update({
            "trigger": trigger_event,
            "workflow_id": workflow_id,
            "workflow_name": workflow.get("name", workflow_id)
        })
        
        results = {
            "workflow_id": workflow_id,
            "workflow_name": workflow.get("name", workflow_id),
            "steps_executed": [],
            "status": "success",
            "errors": []
        }
        
        # Execute actions/steps
        actions = workflow.get("actions", workflow.get("steps", []))
        for idx, action in enumerate(actions):
            try:
                step_result = await self._execute_action(action, context)
                results["steps_executed"].append({
                    "step_index": idx,
                    "step_name": action.get("name", f"step-{idx}"),
                    "status": "success",
                    "result": step_result
                })
            except Exception as e:
                logger.error(f"Error executing action {idx} in workflow {workflow_id}: {e}")
                results["status"] = "partial_failure"
                results["errors"].append({
                    "step_index": idx,
                    "step_name": action.get("name", f"step-{idx}"),
                    "error": str(e)
                })
        
        if results["errors"] and not results["steps_executed"]:
            results["status"] = "failed"
        
        logger.info(f"Workflow {workflow_id} execution completed with status: {results['status']}")
        return results
    
    async def _execute_action(self, action: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single workflow action"""
        action_name = action.get("name", "unnamed-action")
        provider_config = action.get("provider", {})
        provider_type = provider_config.get("type", "unknown")
        
        logger.info(f"Executing action: {action_name} (provider: {provider_type})")
        
        # Simulate delay
        await asyncio.sleep(0.1)
        
        # Execute based on provider type
        if provider_type == "console":
            return await self._execute_console_action(provider_config, context)
        elif provider_type == "http":
            return await self._execute_http_action(provider_config, context)
        elif provider_type == "mock":
            return await self._execute_mock_action(provider_config, context)
        elif provider_type in ["bedrock-agentcore", "strands-agent", "openai", "anthropic"]:
            return await self._execute_ai_action(provider_type, provider_config, context)
        else:
            logger.warning(f"Unknown provider type: {provider_type}, executing as mock")
            return {"status": "executed", "provider": provider_type, "note": "simulated"}
    
    async def _execute_console_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a console logging action"""
        message = config.get("with", {}).get("message", "No message provided")
        
        # Simple template replacement
        message = message.replace("{{ alert.id }}", str(context.get("trigger", {}).get("id", "N/A")))
        message = message.replace("{{ alert.title }}", str(context.get("trigger", {}).get("title", "N/A")))
        
        logger.info(f"[Console Action] {message}")
        return {"status": "executed", "message": message}
    
    async def _execute_http_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an HTTP request action (simulated for demo)"""
        url = config.get("with", {}).get("url", "")
        method = config.get("with", {}).get("method", "GET").upper()
        
        logger.info(f"[HTTP Action] {method} {url} (simulated)")
        return {
            "status": "executed",
            "url": url,
            "method": method,
            "note": "simulated for demo"
        }
    
    async def _execute_mock_action(self, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a mock action"""
        enrich_alert = config.get("with", {}).get("enrich_alert", [])
        
        enrichments = {}
        for enrichment in enrich_alert:
            key = enrichment.get("key")
            value = enrichment.get("value")
            if key and value:
                enrichments[key] = value
        
        logger.info(f"[Mock Action] Enriched alert with {len(enrichments)} fields")
        return {
            "status": "executed",
            "enrichments": enrichments
        }
    
    async def _execute_ai_action(self, provider: str, config: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an AI agent action"""
        prompt = config.get("with", {}).get("prompt", "")
        
        # Simple template replacement
        trigger = context.get("trigger", {})
        prompt = prompt.replace("{{ alert | to_json }}", json.dumps(trigger))
        prompt = prompt.replace("{{ alert.id }}", str(trigger.get("id", "N/A")))
        prompt = prompt.replace("{{ alert.title }}", str(trigger.get("title", "N/A")))
        
        logger.info(f"[AI Action] Provider: {provider}, Prompt length: {len(prompt)}")
        
        # Try to use real AI if available
        try:
            from ai.ai_client import get_ai_client
            ai_client = get_ai_client()
            if ai_client.is_real:
                response = await ai_client.summarize_alert(trigger)
                return {
                    "status": "executed",
                    "provider": provider,
                    "ai_response": response,
                    "real_ai": True
                }
        except Exception as e:
            logger.warning(f"Could not use real AI: {e}")
        
        # Fallback to simulated response
        return {
            "status": "executed",
            "provider": provider,
            "ai_response": f"[Simulated {provider}] Processed alert: {trigger.get('title', 'Unknown')}",
            "real_ai": False
        }


# Global workflow executor instance
_executor: Optional[WorkflowExecutor] = None


def get_workflow_executor() -> WorkflowExecutor:
    """Get or create global workflow executor instance"""
    global _executor
    if _executor is None:
        _executor = WorkflowExecutor()
    return _executor

