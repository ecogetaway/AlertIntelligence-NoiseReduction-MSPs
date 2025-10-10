"""
Alert Deduplication Service
Handles fingerprint-based alert deduplication logic
"""

from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import defaultdict
import hashlib
import logging

logger = logging.getLogger(__name__)


class AlertDeduplicator:
    """Handles alert deduplication logic using fingerprints"""
    
    def __init__(self, window_minutes: int = 5):
        """
        Initialize deduplicator with time window
        
        Args:
            window_minutes: Time window in minutes for considering alerts as duplicates
        """
        self.alert_cache = defaultdict(list)
        self.window = timedelta(minutes=window_minutes)
        logger.info(f"AlertDeduplicator initialized with {window_minutes} minute window")
    
    def generate_fingerprint(self, alert: Dict[str, Any]) -> str:
        """
        Generate unique fingerprint for alert deduplication
        
        Args:
            alert: Alert dictionary containing source, service, name, severity
            
        Returns:
            MD5 hash fingerprint string
        """
        # Create fingerprint key from alert attributes
        key_parts = [
            alert.get("source", "unknown"),
            alert.get("service", "unknown"), 
            alert.get("name", "unknown"),
            alert.get("severity", "unknown")
        ]
        key = ":".join(key_parts)
        fingerprint = hashlib.md5(key.encode()).hexdigest()
        
        logger.debug(f"Generated fingerprint {fingerprint} for alert {alert.get('name', 'Unknown')}")
        return fingerprint
    
    def is_duplicate(self, alert: Dict[str, Any], fingerprint: str) -> bool:
        """
        Check if alert is duplicate within time window
        
        Args:
            alert: Alert dictionary
            fingerprint: Pre-computed fingerprint
            
        Returns:
            True if duplicate, False otherwise
        """
        now = datetime.now()
        
        # Clean old alerts from cache (outside time window)
        self.alert_cache[fingerprint] = [
            cached_time for cached_time in self.alert_cache[fingerprint]
            if now - cached_time < self.window
        ]
        
        # Check if duplicate exists
        is_dup = len(self.alert_cache[fingerprint]) > 0
        
        if is_dup:
            logger.info(f"Duplicate alert detected: {alert.get('name', 'Unknown')} (fingerprint: {fingerprint})")
        else:
            # Add to cache
            self.alert_cache[fingerprint].append(now)
            logger.debug(f"New unique alert: {alert.get('name', 'Unknown')} (fingerprint: {fingerprint})")
        
        return is_dup
    
    def deduplicate_batch(self, alerts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Deduplicate a batch of alerts
        
        Args:
            alerts: List of alert dictionaries
            
        Returns:
            List of unique alerts
        """
        unique_alerts = []
        duplicates_removed = 0
        
        for alert in alerts:
            fingerprint = self.generate_fingerprint(alert)
            alert["fingerprint"] = fingerprint
            
            if not self.is_duplicate(alert, fingerprint):
                unique_alerts.append(alert)
            else:
                duplicates_removed += 1
        
        logger.info(f"Deduplication complete: {len(alerts)} total, {len(unique_alerts)} unique, {duplicates_removed} duplicates removed")
        return unique_alerts
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get deduplication cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        total_cached = sum(len(times) for times in self.alert_cache.values())
        unique_fingerprints = len(self.alert_cache)
        
        return {
            "total_cached_alerts": total_cached,
            "unique_fingerprints": unique_fingerprints,
            "cache_size": len(self.alert_cache),
            "window_minutes": self.window.total_seconds() / 60
        }
    
    def clear_cache(self):
        """Clear the deduplication cache"""
        self.alert_cache.clear()
        logger.info("Deduplication cache cleared")
