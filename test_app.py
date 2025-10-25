#!/usr/bin/env python3
"""
Test script for Live Flight Detector
Tests all major components and functionality
"""

import requests
import time
import json
from datetime import datetime

def test_backend_connection():
    """Test if backend is running and responding"""
    try:
        response = requests.get('http://localhost:5000/api/flights', timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and responding")
            return True
        else:
            print(f"❌ Backend returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running on port 5000")
        return False
    except Exception as e:
        print(f"❌ Backend connection error: {e}")
        return False

def test_data_collection():
    """Test data collection functionality"""
    try:
        response = requests.post('http://localhost:5000/api/collect-once', timeout=30)
        if response.status_code == 200:
            print("✅ Data collection test passed")
            return True
        else:
            print(f"❌ Data collection failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Data collection error: {e}")
        return False

def test_statistics():
    """Test statistics endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/statistics', timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Statistics: {data}")
            return True
        else:
            print(f"❌ Statistics failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Statistics error: {e}")
        return False

def test_simple_queries():
    """Test simple Neo4j queries"""
    try:
        response = requests.get('http://localhost:5000/api/queries/simple', timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Simple queries executed successfully")
            for query_name, result in data.items():
                print(f"  - {query_name}: {result}")
            return True
        else:
            print(f"❌ Simple queries failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Simple queries error: {e}")
        return False

def test_complex_queries():
    """Test complex Neo4j queries"""
    try:
        response = requests.get('http://localhost:5000/api/queries/complex', timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ Complex queries executed successfully")
            for query_name, result in data.items():
                print(f"  - {query_name}: {result}")
            return True
        else:
            print(f"❌ Complex queries failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Complex queries error: {e}")
        return False

def test_eda():
    """Test EDA endpoint"""
    try:
        response = requests.get('http://localhost:5000/api/eda', timeout=15)
        if response.status_code == 200:
            data = response.json()
            print("✅ EDA analysis completed")
            if 'basic_stats' in data:
                stats = data['basic_stats']
                print(f"  - Total flights: {stats.get('total_flights', 0)}")
                print(f"  - Flights in air: {stats.get('flights_in_air', 0)}")
                print(f"  - Flights on ground: {stats.get('flights_on_ground', 0)}")
            return True
        else:
            print(f"❌ EDA failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ EDA error: {e}")
        return False

def main():
    """Run all tests"""
    print("🛩️ Live Flight Detector - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Backend Connection", test_backend_connection),
        ("Data Collection", test_data_collection),
        ("Statistics", test_statistics),
        ("Simple Queries", test_simple_queries),
        ("Complex Queries", test_complex_queries),
        ("EDA Analysis", test_eda)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(2)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Live Flight Detector is working correctly.")
        print("\n🌐 Access your application:")
        print("   Frontend: http://localhost:3000")
        print("   Backend API: http://localhost:5000")
        print("   Neo4j Browser: http://localhost:7474")
    else:
        print("❌ Some tests failed. Check the troubleshooting guide.")
        print("📖 See TROUBLESHOOTING.md for solutions.")

if __name__ == "__main__":
    main()
