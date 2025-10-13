"""
Backend Performance Benchmarks for MSP Alert Intelligence Platform
Measures actual API response times, throughput, and database performance
"""

import asyncio
import time
import psutil
import requests
import statistics
from typing import Dict, List, Any
from datetime import datetime
import json
import sys
import os

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))

from demo_main import app
from fastapi.testclient import TestClient
from sqlmodel import Session, select, func
from core.database import get_session
from models.alert import Alert, AlertStatus, AlertSeverity, AlertSource

class BackendBenchmarks:
    """Backend performance measurement suite"""
    
    def __init__(self):
        self.client = TestClient(app)
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "api_performance": {},
            "database_performance": {},
            "memory_usage": {},
            "throughput_metrics": {}
        }
    
    def measure_api_response_times(self) -> Dict[str, Any]:
        """Measure API response times for all endpoints"""
        print("🔍 Measuring API Response Times...")
        
        endpoints = [
            ("GET", "/", "Root endpoint"),
            ("GET", "/health", "Health check"),
            ("GET", "/api/v1/alerts", "List alerts"),
            ("GET", "/api/v1/incidents", "List incidents"),
            ("GET", "/api/v1/agents/status", "Agent status"),
            ("POST", "/api/v1/alerts/ingest", "Alert ingestion"),
            ("POST", "/api/v1/alerts/alert-1/acknowledge", "Acknowledge alert"),
            ("POST", "/api/v1/alerts/alert-1/suppress", "Suppress alert"),
            ("POST", "/api/v1/alerts/deduplicate", "Deduplicate alerts"),
            ("POST", "/api/v1/alerts/correlate", "Correlate alerts")
        ]
        
        api_results = {}
        
        for method, endpoint, description in endpoints:
            times = []
            
            # Run 10 requests for each endpoint
            for i in range(10):
                start_time = time.time()
                
                try:
                    if method == "GET":
                        response = self.client.get(endpoint)
                    elif method == "POST":
                        # Use appropriate payload for POST requests
                        if "ingest" in endpoint:
                            payload = [{
                                "name": f"Test Alert {i}",
                                "description": f"Test description {i}",
                                "severity": "high",
                                "source": "test",
                                "service": "api"
                            }]
                        else:
                            payload = {}
                        
                        response = self.client.post(endpoint, json=payload)
                    
                    end_time = time.time()
                    response_time = (end_time - start_time) * 1000  # Convert to milliseconds
                    
                    if response.status_code in [200, 201]:
                        times.append(response_time)
                    
                except Exception as e:
                    print(f"Error testing {endpoint}: {e}")
                    continue
            
            if times:
                api_results[endpoint] = {
                    "description": description,
                    "method": method,
                    "avg_response_time_ms": round(statistics.mean(times), 2),
                    "min_response_time_ms": round(min(times), 2),
                    "max_response_time_ms": round(max(times), 2),
                    "p95_response_time_ms": round(statistics.quantiles(times, n=20)[18], 2),
                    "success_rate": len(times) / 10 * 100,
                    "sample_size": len(times)
                }
        
        self.results["api_performance"] = api_results
        return api_results
    
    def measure_database_performance(self) -> Dict[str, Any]:
        """Measure database query performance"""
        print("🔍 Measuring Database Performance...")
        
        db_results = {}
        
        try:
            # Get database session
            with get_session() as session:
                # Test 1: Simple SELECT query
                start_time = time.time()
                statement = select(Alert)
                result = session.exec(statement)
                alerts = result.all()
                end_time = time.time()
                
                db_results["select_all_alerts"] = {
                    "query": "SELECT * FROM alerts",
                    "execution_time_ms": round((end_time - start_time) * 1000, 2),
                    "rows_returned": len(alerts)
                }
                
                # Test 2: Filtered query
                start_time = time.time()
                statement = select(Alert).where(Alert.severity == AlertSeverity.CRITICAL)
                result = session.exec(statement)
                critical_alerts = result.all()
                end_time = time.time()
                
                db_results["select_critical_alerts"] = {
                    "query": "SELECT * FROM alerts WHERE severity = 'critical'",
                    "execution_time_ms": round((end_time - start_time) * 1000, 2),
                    "rows_returned": len(critical_alerts)
                }
                
                # Test 3: Count query
                start_time = time.time()
                statement = select(func.count(Alert.id))
                result = session.exec(statement)
                total_count = result.first()
                end_time = time.time()
                
                db_results["count_alerts"] = {
                    "query": "SELECT COUNT(*) FROM alerts",
                    "execution_time_ms": round((end_time - start_time) * 1000, 2),
                    "count": total_count
                }
                
                # Test 4: Complex query with joins (if applicable)
                start_time = time.time()
                statement = select(Alert).where(
                    Alert.status == AlertStatus.ACTIVE
                ).order_by(Alert.created_at.desc())
                result = session.exec(statement)
                active_alerts = result.all()
                end_time = time.time()
                
                db_results["select_active_alerts_ordered"] = {
                    "query": "SELECT * FROM alerts WHERE status = 'active' ORDER BY created_at DESC",
                    "execution_time_ms": round((end_time - start_time) * 1000, 2),
                    "rows_returned": len(active_alerts)
                }
        
        except Exception as e:
            print(f"Database performance test failed: {e}")
            db_results["error"] = str(e)
        
        self.results["database_performance"] = db_results
        return db_results
    
    def measure_memory_usage(self) -> Dict[str, Any]:
        """Measure memory usage of the application"""
        print("🔍 Measuring Memory Usage...")
        
        process = psutil.Process()
        memory_info = process.memory_info()
        
        memory_results = {
            "rss_mb": round(memory_info.rss / 1024 / 1024, 2),  # Resident Set Size
            "vms_mb": round(memory_info.vms / 1024 / 1024, 2),  # Virtual Memory Size
            "memory_percent": round(process.memory_percent(), 2),
            "cpu_percent": round(process.cpu_percent(), 2),
            "num_threads": process.num_threads(),
            "timestamp": datetime.now().isoformat()
        }
        
        self.results["memory_usage"] = memory_results
        return memory_results
    
    def measure_throughput(self) -> Dict[str, Any]:
        """Measure alert processing throughput"""
        print("🔍 Measuring Alert Processing Throughput...")
        
        # Test alert ingestion throughput
        test_alerts = []
        for i in range(50):  # Create 50 test alerts
            test_alerts.append({
                "name": f"Throughput Test Alert {i}",
                "description": f"Test description for alert {i}",
                "severity": "medium",
                "source": "test",
                "service": "api"
            })
        
        # Measure ingestion time
        start_time = time.time()
        response = self.client.post("/api/v1/alerts/ingest", json=test_alerts)
        end_time = time.time()
        
        ingestion_time = end_time - start_time
        alerts_per_second = len(test_alerts) / ingestion_time
        
        throughput_results = {
            "alerts_processed": len(test_alerts),
            "total_time_seconds": round(ingestion_time, 2),
            "alerts_per_second": round(alerts_per_second, 2),
            "response_status": response.status_code,
            "timestamp": datetime.now().isoformat()
        }
        
        self.results["throughput_metrics"] = throughput_results
        return throughput_results
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all backend benchmarks"""
        print("🚀 Starting Backend Performance Benchmarks...")
        print("=" * 60)
        
        # Run all benchmark tests
        self.measure_api_response_times()
        self.measure_database_performance()
        self.measure_memory_usage()
        self.measure_throughput()
        
        # Calculate summary metrics
        api_perf = self.results["api_performance"]
        if api_perf:
            avg_response_times = [endpoint["avg_response_time_ms"] for endpoint in api_perf.values()]
            self.results["summary"] = {
                "overall_avg_response_time_ms": round(statistics.mean(avg_response_times), 2),
                "fastest_endpoint": min(api_perf.items(), key=lambda x: x[1]["avg_response_time_ms"]),
                "slowest_endpoint": max(api_perf.items(), key=lambda x: x[1]["avg_response_time_ms"]),
                "total_endpoints_tested": len(api_perf),
                "benchmark_completion_time": datetime.now().isoformat()
            }
        
        print("✅ Backend benchmarks completed!")
        return self.results
    
    def save_results(self, filename: str = "backend_benchmarks.json"):
        """Save benchmark results to file"""
        results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "benchmarks", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📊 Results saved to: {filepath}")
        return filepath

def main():
    """Run backend benchmarks"""
    benchmark = BackendBenchmarks()
    results = benchmark.run_all_benchmarks()
    benchmark.save_results()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 BACKEND BENCHMARK SUMMARY")
    print("=" * 60)
    
    if "summary" in results:
        summary = results["summary"]
        print(f"Overall Average Response Time: {summary['overall_avg_response_time_ms']}ms")
        print(f"Fastest Endpoint: {summary['fastest_endpoint'][0]} ({summary['fastest_endpoint'][1]['avg_response_time_ms']}ms)")
        print(f"Slowest Endpoint: {summary['slowest_endpoint'][0]} ({summary['slowest_endpoint'][1]['avg_response_time_ms']}ms)")
        print(f"Total Endpoints Tested: {summary['total_endpoints_tested']}")
    
    if "throughput_metrics" in results:
        throughput = results["throughput_metrics"]
        print(f"Alert Processing Rate: {throughput['alerts_per_second']} alerts/second")
    
    if "memory_usage" in results:
        memory = results["memory_usage"]
        print(f"Memory Usage: {memory['rss_mb']}MB RSS, {memory['memory_percent']}% of system")

if __name__ == "__main__":
    main()
