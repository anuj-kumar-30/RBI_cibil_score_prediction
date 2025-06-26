#!/usr/bin/env python3
"""
Simple test script to check if the API is accessible
Run this script to test the API endpoints
"""

import requests
import json
import time

# API URLs
BASE_URL = "https://rbicibilscoreprediction-production.up.railway.app/"
HEALTH_URL = f"{BASE_URL}/api/health/"
PREDICT_URL = f"{BASE_URL}/api/predict/"

# Sample data for testing
sample_data = {
    "name": "Test User",
    "state": "Delhi",
    "city": "New Delhi",
    "monthlyIncome": 25000,
    "dataPackExpense": 500,
    "savings": 3000,
    "internetUsed": "yes",
    "foodFuelExpensePercent": "20",
    "hasLoan": "no",
    "hasLand": "no",
    "familyMembers": 4,
    "childrenCount": 2,
    "childrenStatus": "study",
    "cookingTogether": "yes",
    "earningMembers": 2,
    "dependentMembers": 2,
    "lpgRefillFrequency": "monthly",
    "lpgPreference": "Indane",
    "lpgChallenges": "cost",
    "cylinderPreference": "14.2kg",
    "jobType": "self-employed",
    "emergencyFundSource": "savings",
    "facedEmergency": "no",
    "assets": "mobile,fan",
    "ownsVehicle": "bike",
    "incomeCycle": "monthly",
    "awareOfGovtScheme": "yes",
    "pastLoanDefault": "no"
}

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing Health Endpoint...")
    try:
        response = requests.get(HEALTH_URL, timeout=10)
        print(f"✅ Health Check Status: {response.status_code}")
        if response.status_code == 200:
            print(f"✅ Health Response: {response.json()}")
        else:
            print(f"❌ Health Response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.Timeout:
        print("❌ Health Check: Timeout - Service might be sleeping")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Health Check: Connection Error - Service might be down")
        return False
    except Exception as e:
        print(f"❌ Health Check: Unexpected error - {str(e)}")
        return False

def test_predict_endpoint():
    """Test the predict endpoint"""
    print("\n🔍 Testing Predict Endpoint...")
    try:
        response = requests.post(PREDICT_URL, json=sample_data, timeout=30)
        print(f"✅ Predict Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Predict Response: {json.dumps(result, indent=2)}")
            return True
        else:
            print(f"❌ Predict Response: {response.text}")
            return False
    except requests.exceptions.Timeout:
        print("❌ Predict: Timeout - Service might be sleeping or overloaded")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Predict: Connection Error - Service might be down")
        return False
    except Exception as e:
        print(f"❌ Predict: Unexpected error - {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 Starting API Tests...")
    print(f"📍 Testing URL: {BASE_URL}")
    print("=" * 50)
    
    # Test health endpoint
    health_ok = test_health_endpoint()
    
    # Wait a bit before testing predict
    if health_ok:
        print("\n⏳ Waiting 2 seconds before testing predict endpoint...")
        time.sleep(2)
        predict_ok = test_predict_endpoint()
    else:
        print("\n⚠️  Skipping predict test due to health check failure")
        predict_ok = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"Health Endpoint: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Predict Endpoint: {'✅ PASS' if predict_ok else '❌ FAIL'}")
    
    if not health_ok:
        print("\n💡 Troubleshooting Tips:")
        print("1. The Render service might be sleeping (free tier limitation)")
        print("2. Try accessing the health endpoint in your browser:")
        print(f"   {HEALTH_URL}")
        print("3. Wait a few minutes and try again")
        print("4. Check if your Render deployment is running")
        print("5. Verify the URL is correct")

if __name__ == "__main__":
    main() 