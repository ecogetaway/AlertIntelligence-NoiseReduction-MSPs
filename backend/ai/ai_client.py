"""
AI Client Wrapper
Provides simple AI integration with fallback to simulated responses
"""

import os
import logging
from typing import Dict, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class AIClient:
    """AI client wrapper with OpenAI/Anthropic support and fallback"""
    
    def __init__(self):
        self.provider = os.getenv("AI_PROVIDER", "simulated").lower()
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        self.client = None
        self.is_real = False
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate AI client"""
        if self.provider == "openai" and self.openai_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.openai_key)
                self.is_real = True
                logger.info("OpenAI client initialized successfully")
            except ImportError:
                logger.warning("OpenAI package not installed, falling back to simulated mode")
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}, falling back to simulated mode")
        
        elif self.provider == "anthropic" and self.anthropic_key:
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=self.anthropic_key)
                self.is_real = True
                logger.info("Anthropic client initialized successfully")
            except ImportError:
                logger.warning("Anthropic package not installed, falling back to simulated mode")
            except Exception as e:
                logger.warning(f"Failed to initialize Anthropic client: {e}, falling back to simulated mode")
        
        if not self.is_real:
            logger.info("Using simulated AI responses (no API key or provider configured)")
    
    async def summarize_alert(self, alert: Dict[str, Any]) -> str:
        """Generate a summary for an alert"""
        if self.is_real and self.provider == "openai":
            return await self._openai_summarize_alert(alert)
        elif self.is_real and self.provider == "anthropic":
            return await self._anthropic_summarize_alert(alert)
        else:
            return self._simulated_summarize_alert(alert)
    
    async def correlate_hint(self, alerts: list[Dict[str, Any]]) -> str:
        """Generate correlation insights for multiple alerts"""
        if self.is_real and self.provider == "openai":
            return await self._openai_correlate_hint(alerts)
        elif self.is_real and self.provider == "anthropic":
            return await self._anthropic_correlate_hint(alerts)
        else:
            return self._simulated_correlate_hint(alerts)
    
    async def incident_summary(self, incident: Dict[str, Any], alerts: list[Dict[str, Any]]) -> Dict[str, str]:
        """Generate comprehensive incident summary with AI"""
        if self.is_real and self.provider == "openai":
            return await self._openai_incident_summary(incident, alerts)
        elif self.is_real and self.provider == "anthropic":
            return await self._anthropic_incident_summary(incident, alerts)
        else:
            return self._simulated_incident_summary(incident, alerts)
    
    # OpenAI implementations
    async def _openai_summarize_alert(self, alert: Dict[str, Any]) -> str:
        """Generate alert summary using OpenAI"""
        try:
            prompt = f"""Summarize this alert in one sentence:
Title: {alert.get('title')}
Description: {alert.get('description')}
Severity: {alert.get('severity')}
Source: {alert.get('source')}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._simulated_summarize_alert(alert)
    
    async def _openai_correlate_hint(self, alerts: list[Dict[str, Any]]) -> str:
        """Generate correlation hint using OpenAI"""
        try:
            alerts_text = "\n".join([f"- {a.get('title')} (severity: {a.get('severity')}, source: {a.get('source')})" for a in alerts[:5]])
            prompt = f"""Analyze these correlated alerts and provide a brief root cause hypothesis in 1-2 sentences:
{alerts_text}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._simulated_correlate_hint(alerts)
    
    async def _openai_incident_summary(self, incident: Dict[str, Any], alerts: list[Dict[str, Any]]) -> Dict[str, str]:
        """Generate incident summary using OpenAI"""
        try:
            alerts_text = "\n".join([f"- {a.get('title')}: {a.get('description')}" for a in alerts[:5]])
            prompt = f"""Analyze this incident and provide:
1. Summary (1 sentence)
2. Root Cause (1-2 sentences)
3. Impact Assessment (1 sentence)
4. Recommendations (2-3 bullet points)

Incident: {incident.get('title')}
Alerts:
{alerts_text}"""
            
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=300,
                temperature=0.5
            )
            
            result = response.choices[0].message.content.strip()
            return {
                "ai_summary": result,
                "ai_root_cause": "See AI summary above",
                "ai_impact_assessment": "See AI summary above",
                "ai_recommendations": "See AI summary above"
            }
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self._simulated_incident_summary(incident, alerts)
    
    # Anthropic implementations (similar structure)
    async def _anthropic_summarize_alert(self, alert: Dict[str, Any]) -> str:
        """Generate alert summary using Anthropic"""
        try:
            prompt = f"""Summarize this alert in one sentence:
Title: {alert.get('title')}
Description: {alert.get('description')}
Severity: {alert.get('severity')}
Source: {alert.get('source')}"""
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._simulated_summarize_alert(alert)
    
    async def _anthropic_correlate_hint(self, alerts: list[Dict[str, Any]]) -> str:
        """Generate correlation hint using Anthropic"""
        try:
            alerts_text = "\n".join([f"- {a.get('title')} (severity: {a.get('severity')}, source: {a.get('source')})" for a in alerts[:5]])
            prompt = f"""Analyze these correlated alerts and provide a brief root cause hypothesis in 1-2 sentences:
{alerts_text}"""
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._simulated_correlate_hint(alerts)
    
    async def _anthropic_incident_summary(self, incident: Dict[str, Any], alerts: list[Dict[str, Any]]) -> Dict[str, str]:
        """Generate incident summary using Anthropic"""
        try:
            alerts_text = "\n".join([f"- {a.get('title')}: {a.get('description')}" for a in alerts[:5]])
            prompt = f"""Analyze this incident and provide:
1. Summary (1 sentence)
2. Root Cause (1-2 sentences)
3. Impact Assessment (1 sentence)
4. Recommendations (2-3 bullet points)

Incident: {incident.get('title')}
Alerts:
{alerts_text}"""
            
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}]
            )
            
            result = response.content[0].text.strip()
            return {
                "ai_summary": result,
                "ai_root_cause": "See AI summary above",
                "ai_impact_assessment": "See AI summary above",
                "ai_recommendations": "See AI summary above"
            }
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            return self._simulated_incident_summary(incident, alerts)
    
    # Simulated implementations
    def _simulated_summarize_alert(self, alert: Dict[str, Any]) -> str:
        """Simulated alert summary"""
        severity = alert.get('severity', 'unknown')
        title = alert.get('title', 'Unknown alert')
        source = alert.get('source', 'unknown')
        return f"[Simulated AI] {severity.capitalize()} alert from {source}: {title}"
    
    def _simulated_correlate_hint(self, alerts: list[Dict[str, Any]]) -> str:
        """Simulated correlation hint"""
        if len(alerts) < 2:
            return "[Simulated AI] Not enough alerts to correlate"
        
        sources = set(a.get('source') for a in alerts)
        severities = set(a.get('severity') for a in alerts)
        
        return f"[Simulated AI] Detected {len(alerts)} related alerts from {len(sources)} source(s) with {len(severities)} severity level(s). Likely cascading failure."
    
    def _simulated_incident_summary(self, incident: Dict[str, Any], alerts: list[Dict[str, Any]]) -> Dict[str, str]:
        """Simulated incident summary"""
        return {
            "ai_summary": f"[Simulated AI] Incident involving {len(alerts)} alerts with potential infrastructure impact",
            "ai_root_cause": "[Simulated AI] Root cause analysis suggests cascading failure across multiple components",
            "ai_impact_assessment": "[Simulated AI] High impact on system availability and performance",
            "ai_recommendations": "[Simulated AI] 1. Investigate component dependencies 2. Check system logs 3. Scale resources if needed"
        }


# Global AI client instance
_ai_client: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """Get or create global AI client instance"""
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient()
    return _ai_client

