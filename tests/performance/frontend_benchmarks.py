"""
Frontend Performance Benchmarks for MSP Alert Intelligence Platform
Measures page load times, bundle size, and user experience metrics
"""

import time
import requests
import statistics
from typing import Dict, List, Any
from datetime import datetime
import json
import os
import subprocess
import sys

class FrontendBenchmarks:
    """Frontend performance measurement suite"""
    
    def __init__(self, base_url: str = "http://localhost:3000"):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "page_load_times": {},
            "bundle_analysis": {},
            "network_requests": {},
            "user_experience": {},
            "performance_metrics": {}
        }
    
    def measure_page_load_times(self) -> Dict[str, Any]:
        """Measure page load times for different routes"""
        print("🔍 Measuring Page Load Times...")
        
        pages = [
            ("/", "Home/Dashboard"),
            ("/frontend-demo.html", "Demo Dashboard"),
            ("/frontend-simple.html", "Simple Demo")
        ]
        
        page_results = {}
        
        for route, description in pages:
            times = []
            
            # Run 5 requests for each page
            for i in range(5):
                try:
                    start_time = time.time()
                    response = requests.get(f"{self.base_url}{route}", timeout=10)
                    end_time = time.time()
                    
                    if response.status_code == 200:
                        load_time = (end_time - start_time) * 1000  # Convert to milliseconds
                        times.append(load_time)
                    
                except Exception as e:
                    print(f"Error loading {route}: {e}")
                    continue
            
            if times:
                page_results[route] = {
                    "description": description,
                    "avg_load_time_ms": round(statistics.mean(times), 2),
                    "min_load_time_ms": round(min(times), 2),
                    "max_load_time_ms": round(max(times), 2),
                    "p95_load_time_ms": round(statistics.quantiles(times, n=20)[18], 2),
                    "success_rate": len(times) / 5 * 100,
                    "sample_size": len(times)
                }
        
        self.results["page_load_times"] = page_results
        return page_results
    
    def analyze_bundle_size(self) -> Dict[str, Any]:
        """Analyze frontend bundle size and composition"""
        print("🔍 Analyzing Bundle Size...")
        
        try:
            # Check if Next.js build exists
            next_build_dir = os.path.join(os.path.dirname(__file__), "..", "..", "frontend", ".next")
            
            bundle_results = {
                "build_exists": os.path.exists(next_build_dir),
                "bundle_analysis": {}
            }
            
            if os.path.exists(next_build_dir):
                # Analyze Next.js build
                static_dir = os.path.join(next_build_dir, "static")
                if os.path.exists(static_dir):
                    js_files = []
                    css_files = []
                    total_js_size = 0
                    total_css_size = 0
                    
                    for root, dirs, files in os.walk(static_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            file_size = os.path.getsize(file_path)
                            
                            if file.endswith('.js'):
                                js_files.append({"name": file, "size_bytes": file_size})
                                total_js_size += file_size
                            elif file.endswith('.css'):
                                css_files.append({"name": file, "size_bytes": file_size})
                                total_css_size += file_size
                    
                    bundle_results["bundle_analysis"] = {
                        "total_js_size_bytes": total_js_size,
                        "total_js_size_kb": round(total_js_size / 1024, 2),
                        "total_css_size_bytes": total_css_size,
                        "total_css_size_kb": round(total_css_size / 1024, 2),
                        "total_bundle_size_kb": round((total_js_size + total_css_size) / 1024, 2),
                        "js_files_count": len(js_files),
                        "css_files_count": len(css_files),
                        "largest_js_file": max(js_files, key=lambda x: x["size_bytes"]) if js_files else None,
                        "largest_css_file": max(css_files, key=lambda x: x["size_bytes"]) if css_files else None
                    }
            else:
                # Analyze static HTML files
                static_files = [
                    "frontend-demo.html",
                    "frontend-simple.html"
                ]
                
                static_analysis = {}
                total_size = 0
                
                for file in static_files:
                    file_path = os.path.join(os.path.dirname(__file__), "..", "..", file)
                    if os.path.exists(file_path):
                        file_size = os.path.getsize(file_path)
                        static_analysis[file] = {
                            "size_bytes": file_size,
                            "size_kb": round(file_size / 1024, 2)
                        }
                        total_size += file_size
                
                bundle_results["bundle_analysis"] = {
                    "static_files": static_analysis,
                    "total_size_kb": round(total_size / 1024, 2),
                    "file_count": len(static_analysis)
                }
            
            self.results["bundle_analysis"] = bundle_results
            return bundle_results
            
        except Exception as e:
            print(f"Bundle analysis failed: {e}")
            return {"error": str(e)}
    
    def measure_network_requests(self) -> Dict[str, Any]:
        """Measure network request performance"""
        print("🔍 Measuring Network Request Performance...")
        
        try:
            # Test API endpoints
            api_endpoints = [
                "/api/v1/alerts",
                "/api/v1/incidents", 
                "/health"
            ]
            
            network_results = {
                "api_endpoints": {},
                "total_requests": 0,
                "successful_requests": 0,
                "failed_requests": 0
            }
            
            for endpoint in api_endpoints:
                times = []
                successful = 0
                
                # Test each endpoint 3 times
                for i in range(3):
                    try:
                        start_time = time.time()
                        response = requests.get(f"{self.base_url}{endpoint}", timeout=5)
                        end_time = time.time()
                        
                        network_results["total_requests"] += 1
                        
                        if response.status_code == 200:
                            response_time = (end_time - start_time) * 1000
                            times.append(response_time)
                            successful += 1
                            network_results["successful_requests"] += 1
                        else:
                            network_results["failed_requests"] += 1
                            
                    except Exception as e:
                        network_results["failed_requests"] += 1
                        print(f"Request failed for {endpoint}: {e}")
                
                if times:
                    network_results["api_endpoints"][endpoint] = {
                        "avg_response_time_ms": round(statistics.mean(times), 2),
                        "min_response_time_ms": round(min(times), 2),
                        "max_response_time_ms": round(max(times), 2),
                        "success_rate": (successful / 3) * 100,
                        "sample_size": len(times)
                    }
            
            # Calculate overall network performance
            all_times = []
            for endpoint_data in network_results["api_endpoints"].values():
                all_times.extend([endpoint_data["avg_response_time_ms"]])
            
            if all_times:
                network_results["overall_avg_response_time_ms"] = round(statistics.mean(all_times), 2)
                network_results["overall_success_rate"] = (network_results["successful_requests"] / network_results["total_requests"]) * 100
            
            self.results["network_requests"] = network_results
            return network_results
            
        except Exception as e:
            print(f"Network request test failed: {e}")
            return {"error": str(e)}
    
    def measure_user_experience_metrics(self) -> Dict[str, Any]:
        """Measure user experience metrics"""
        print("🔍 Measuring User Experience Metrics...")
        
        try:
            # Test dashboard responsiveness
            dashboard_url = f"{self.base_url}/frontend-demo.html"
            
            # Measure initial page load
            start_time = time.time()
            response = requests.get(dashboard_url, timeout=10)
            end_time = time.time()
            
            initial_load_time = (end_time - start_time) * 1000
            
            # Simulate user interactions (filtering, etc.)
            interaction_times = []
            
            # Test filter application (simulated)
            for i in range(3):
                start_time = time.time()
                # Simulate filter request
                filter_response = requests.get(f"{dashboard_url}?severity=critical", timeout=5)
                end_time = time.time()
                
                if filter_response.status_code == 200:
                    interaction_time = (end_time - start_time) * 1000
                    interaction_times.append(interaction_time)
            
            # Calculate UX metrics
            ux_results = {
                "initial_page_load_ms": round(initial_load_time, 2),
                "filter_response_avg_ms": round(statistics.mean(interaction_times), 2) if interaction_times else 0,
                "filter_response_min_ms": round(min(interaction_times), 2) if interaction_times else 0,
                "filter_response_max_ms": round(max(interaction_times), 2) if interaction_times else 0,
                "interaction_sample_size": len(interaction_times),
                "page_load_success": response.status_code == 200,
                "response_size_bytes": len(response.content) if response.status_code == 200 else 0,
                "response_size_kb": round(len(response.content) / 1024, 2) if response.status_code == 200 else 0
            }
            
            # Calculate performance scores
            if initial_load_time < 1000:  # Under 1 second
                ux_results["load_performance_score"] = "Excellent"
            elif initial_load_time < 2000:  # Under 2 seconds
                ux_results["load_performance_score"] = "Good"
            elif initial_load_time < 3000:  # Under 3 seconds
                ux_results["load_performance_score"] = "Fair"
            else:
                ux_results["load_performance_score"] = "Poor"
            
            self.results["user_experience"] = ux_results
            return ux_results
            
        except Exception as e:
            print(f"User experience test failed: {e}")
            return {"error": str(e)}
    
    def calculate_performance_metrics(self) -> Dict[str, Any]:
        """Calculate overall performance metrics"""
        print("🔍 Calculating Performance Metrics...")
        
        page_load = self.results.get("page_load_times", {})
        bundle = self.results.get("bundle_analysis", {})
        network = self.results.get("network_requests", {})
        ux = self.results.get("user_experience", {})
        
        # Calculate overall performance score
        performance_score = 0
        max_score = 4
        
        # Page load performance (25% weight)
        if page_load:
            avg_load_times = [data["avg_load_time_ms"] for data in page_load.values()]
            if avg_load_times:
                overall_load_time = statistics.mean(avg_load_times)
                if overall_load_time < 1000:
                    performance_score += 1
                elif overall_load_time < 2000:
                    performance_score += 0.75
                elif overall_load_time < 3000:
                    performance_score += 0.5
        
        # Bundle size performance (25% weight)
        if bundle and "bundle_analysis" in bundle:
            bundle_size = bundle["bundle_analysis"].get("total_bundle_size_kb", 0)
            if bundle_size < 500:  # Under 500KB
                performance_score += 1
            elif bundle_size < 1000:  # Under 1MB
                performance_score += 0.75
            elif bundle_size < 2000:  # Under 2MB
                performance_score += 0.5
        
        # Network performance (25% weight)
        if network and "overall_success_rate" in network:
            success_rate = network["overall_success_rate"]
            if success_rate >= 95:
                performance_score += 1
            elif success_rate >= 90:
                performance_score += 0.75
            elif success_rate >= 80:
                performance_score += 0.5
        
        # User experience (25% weight)
        if ux and "load_performance_score" in ux:
            score = ux["load_performance_score"]
            if score == "Excellent":
                performance_score += 1
            elif score == "Good":
                performance_score += 0.75
            elif score == "Fair":
                performance_score += 0.5
        
        performance_metrics = {
            "overall_performance_score": round(performance_score, 2),
            "performance_grade": self._get_performance_grade(performance_score),
            "recommendations": self._get_performance_recommendations(performance_score),
            "bundle_size_kb": bundle.get("bundle_analysis", {}).get("total_bundle_size_kb", 0),
            "avg_page_load_ms": statistics.mean([data["avg_load_time_ms"] for data in page_load.values()]) if page_load else 0,
            "network_success_rate": network.get("overall_success_rate", 0),
            "load_performance_score": ux.get("load_performance_score", "Unknown")
        }
        
        self.results["performance_metrics"] = performance_metrics
        return performance_metrics
    
    def _get_performance_grade(self, score: float) -> str:
        """Convert performance score to letter grade"""
        if score >= 3.5:
            return "A"
        elif score >= 3.0:
            return "B"
        elif score >= 2.5:
            return "C"
        elif score >= 2.0:
            return "D"
        else:
            return "F"
    
    def _get_performance_recommendations(self, score: float) -> List[str]:
        """Get performance improvement recommendations"""
        recommendations = []
        
        if score < 3.0:
            recommendations.append("Optimize page load times - consider code splitting")
            recommendations.append("Reduce bundle size - remove unused dependencies")
            recommendations.append("Implement caching strategies")
        
        if score < 2.5:
            recommendations.append("Enable gzip compression")
            recommendations.append("Optimize images and assets")
            recommendations.append("Consider CDN for static assets")
        
        if score < 2.0:
            recommendations.append("Implement lazy loading")
            recommendations.append("Use service workers for caching")
            recommendations.append("Consider server-side rendering")
        
        return recommendations
    
    def run_all_benchmarks(self) -> Dict[str, Any]:
        """Run all frontend benchmarks"""
        print("🚀 Starting Frontend Performance Benchmarks...")
        print("=" * 60)
        
        # Run all benchmark tests
        self.measure_page_load_times()
        self.analyze_bundle_size()
        self.measure_network_requests()
        self.measure_user_experience_metrics()
        self.calculate_performance_metrics()
        
        # Calculate summary metrics
        self.results["summary"] = {
            "total_pages_tested": len(self.results.get("page_load_times", {})),
            "overall_performance_score": self.results.get("performance_metrics", {}).get("overall_performance_score", 0),
            "performance_grade": self.results.get("performance_metrics", {}).get("performance_grade", "Unknown"),
            "bundle_size_kb": self.results.get("bundle_analysis", {}).get("bundle_analysis", {}).get("total_bundle_size_kb", 0),
            "avg_page_load_ms": self.results.get("performance_metrics", {}).get("avg_page_load_ms", 0),
            "benchmark_completion_time": datetime.now().isoformat()
        }
        
        print("✅ Frontend benchmarks completed!")
        return self.results
    
    def save_results(self, filename: str = "frontend_benchmarks.json"):
        """Save benchmark results to file"""
        results_dir = os.path.join(os.path.dirname(__file__), "..", "..", "benchmarks", "results")
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"📊 Results saved to: {filepath}")
        return filepath

def main():
    """Run frontend benchmarks"""
    benchmark = FrontendBenchmarks()
    results = benchmark.run_all_benchmarks()
    benchmark.save_results()
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 FRONTEND BENCHMARK SUMMARY")
    print("=" * 60)
    
    if "summary" in results:
        summary = results["summary"]
        print(f"Overall Performance Score: {summary['overall_performance_score']}/4.0")
        print(f"Performance Grade: {summary['performance_grade']}")
        print(f"Bundle Size: {summary['bundle_size_kb']}KB")
        print(f"Average Page Load: {summary['avg_page_load_ms']}ms")
        print(f"Pages Tested: {summary['total_pages_tested']}")
    
    if "performance_metrics" in results:
        metrics = results["performance_metrics"]
        if "recommendations" in metrics and metrics["recommendations"]:
            print("\nRecommendations:")
            for rec in metrics["recommendations"]:
                print(f"  • {rec}")

if __name__ == "__main__":
    main()
