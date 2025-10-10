#!/usr/bin/env python3
"""
Test script for Advanced UI Features APIs
"""

import requests
import json
import time

def test_advanced_filter():
    """Test advanced filtering API"""
    print("🧪 Testing Advanced Filter API...")
    
    try:
        # Test basic advanced filter
        response = requests.get("http://localhost:8000/api/v1/alerts/advanced-filter")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Advanced Filter API working - {data['total']} alerts found")
            print(f"   Filter options: {list(data['filter_options'].keys())}")
        else:
            print(f"❌ Advanced Filter API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Advanced Filter API error: {e}")

def test_bulk_operations():
    """Test bulk operations API"""
    print("\n🧪 Testing Bulk Operations API...")
    
    try:
        # Test bulk acknowledge
        payload = {
            "alert_ids": ["alert-1", "alert-2"],
            "action": "acknowledge",
            "assignee": "test-user"
        }
        
        response = requests.post("http://localhost:8000/api/v1/alerts/bulk-action", 
                               json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Bulk Operations API working - {data['successful']} alerts processed")
        else:
            print(f"❌ Bulk Operations API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Bulk Operations API error: {e}")

def test_export_functionality():
    """Test export functionality API"""
    print("\n🧪 Testing Export Functionality API...")
    
    try:
        # Test CSV export
        response = requests.get("http://localhost:8000/api/v1/alerts/export?format=csv")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Export API working - {data['total_records']} records exported as {data['format']}")
        else:
            print(f"❌ Export API failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Export API error: {e}")

def main():
    print("🚀 Testing Advanced UI Features APIs")
    print("=" * 50)
    
    # Wait for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(5)
    
    # Test APIs
    test_advanced_filter()
    test_bulk_operations()
    test_export_functionality()
    
    print("\n🎉 Advanced UI Features API testing complete!")

if __name__ == "__main__":
    main()
