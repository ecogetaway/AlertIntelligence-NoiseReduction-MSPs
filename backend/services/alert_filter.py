"""
Alert Filtering Service
Handles rule-based alert filtering logic
"""

from typing import List, Dict, Any
import re
import logging

logger = logging.getLogger(__name__)


class AlertFilter:
    """Handles alert filtering based on configurable rules"""
    
    def __init__(self):
        """Initialize filter with default rules"""
        self.rules = []
        self.load_default_rules()
        logger.info(f"AlertFilter initialized with {len(self.rules)} default rules")
    
    def load_default_rules(self):
        """Load default filtering rules for MSP alerts"""
        self.rules = [
            {
                "name": "high_severity_only",
                "field": "severity", 
                "operator": "in", 
                "value": ["critical", "high"],
                "description": "Only process critical and high severity alerts"
            },
            {
                "name": "active_status_only",
                "field": "status", 
                "operator": "equals", 
                "value": "active",
                "description": "Only process active alerts"
            },
            {
                "name": "exclude_test_alerts",
                "field": "name", 
                "operator": "not_regex", 
                "value": r".*test.*|.*demo.*",
                "description": "Exclude test and demo alerts"
            }
        ]
        logger.debug("Loaded default filtering rules")
    
    def add_rule(self, rule: Dict[str, Any]):
        """
        Add a new filtering rule
        
        Args:
            rule: Dictionary containing rule definition with keys:
                 - name: Rule identifier
                 - field: Alert field to filter on
                 - operator: Comparison operator (equals, in, not_in, regex, not_regex)
                 - value: Value to compare against
                 - description: Human-readable description
        """
        required_fields = ["name", "field", "operator", "value"]
        if not all(field in rule for field in required_fields):
            raise ValueError(f"Rule must contain fields: {required_fields}")
        
        self.rules.append(rule)
        logger.info(f"Added filtering rule: {rule['name']}")
    
    def remove_rule(self, rule_name: str):
        """
        Remove a filtering rule by name
        
        Args:
            rule_name: Name of rule to remove
        """
        original_count = len(self.rules)
        self.rules = [rule for rule in self.rules if rule.get("name") != rule_name]
        
        if len(self.rules) < original_count:
            logger.info(f"Removed filtering rule: {rule_name}")
        else:
            logger.warning(f"Rule not found: {rule_name}")
    
    def apply_filter(self, alert: Dict[str, Any], rule: Dict[str, Any]) -> bool:
        """
        Apply single filter rule to alert
        
        Args:
            alert: Alert dictionary
            rule: Filter rule dictionary
            
        Returns:
            True if alert passes filter, False otherwise
        """
        field = rule["field"]
        operator = rule["operator"]
        value = rule["value"]
        
        # Get alert value (check direct field, then labels, then annotations)
        alert_value = alert.get(field)
        if alert_value is None:
            alert_value = alert.get("labels", {}).get(field)
        if alert_value is None:
            alert_value = alert.get("annotations", {}).get(field)
        
        # Apply operator logic
        try:
            if operator == "equals":
                result = alert_value == value
            elif operator == "in":
                result = alert_value in value
            elif operator == "not_in":
                result = alert_value not in value
            elif operator == "regex":
                result = bool(re.search(value, str(alert_value), re.IGNORECASE))
            elif operator == "not_regex":
                result = not bool(re.search(value, str(alert_value), re.IGNORECASE))
            elif operator == "contains":
                result = str(value).lower() in str(alert_value).lower()
            elif operator == "not_contains":
                result = str(value).lower() not in str(alert_value).lower()
            else:
                logger.warning(f"Unknown operator '{operator}' in rule '{rule.get('name', 'unnamed')}'")
                result = True  # Default to pass if unknown operator
            
            logger.debug(f"Rule '{rule.get('name', 'unnamed')}': {field} {operator} {value} -> {result}")
            return result
            
        except Exception as e:
            logger.error(f"Error applying rule '{rule.get('name', 'unnamed')}': {e}")
            return True  # Default to pass on error
    
    def filter_alerts(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter alerts based on all active rules
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            List of filtered alerts
        """
        if not self.rules:
            logger.warning("No filtering rules configured, returning all alerts")
            return alerts
        
        filtered = []
        total_alerts = len(alerts)
        
        for alert in alerts:
            # Alert must pass ALL rules to be included
            passes_all_rules = all(self.apply_filter(alert, rule) for rule in self.rules)
            
            if passes_all_rules:
                filtered.append(alert)
            else:
                logger.debug(f"Alert filtered out: {alert.get('name', 'Unknown')}")
        
        filtered_count = len(filtered)
        filtered_out = total_alerts - filtered_count
        
        logger.info(f"Filtering complete: {total_alerts} total, {filtered_count} passed, {filtered_out} filtered out")
        return filtered
    
    def get_rules(self) -> List[Dict[str, Any]]:
        """
        Get all active filtering rules
        
        Returns:
            List of rule dictionaries
        """
        return self.rules.copy()
    
    def get_filter_stats(self, alerts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get filtering statistics for a set of alerts
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            Dictionary with filtering statistics
        """
        filtered = self.filter_alerts(alerts)
        
        return {
            "total_alerts": len(alerts),
            "filtered_alerts": len(filtered),
            "filtered_out": len(alerts) - len(filtered),
            "filter_rate": (len(alerts) - len(filtered)) / len(alerts) * 100 if alerts else 0,
            "active_rules": len(self.rules)
        }
