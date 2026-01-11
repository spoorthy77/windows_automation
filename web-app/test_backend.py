"""
Test script to verify Flask backend and Frok API integration
"""

import requests
import json
import time

print("=" * 70)
print("🤖 Windows Automation Assistant - Backend Test")
print("=" * 70)
print()

BACKEND_URL = "http://localhost:5000"

# Test 1: Health Check
print("Test 1: Health Check")
print("-" * 70)
try:
    response = requests.get(f"{BACKEND_URL}/api/health", timeout=5)
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print("Backend may not be running!")
    print()

# Test 2: Chat Endpoint - Simple Command
print("Test 2: Chat Endpoint - Simple Command")
print("-" * 70)
try:
    payload = {"message": "hello"}
    response = requests.post(
        f"{BACKEND_URL}/api/chat",
        json=payload,
        timeout=10,
        headers={"Content-Type": "application/json"}
    )
    print(f"✓ Status Code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 3: Chat Endpoint - Complex Command
print("Test 3: Chat Endpoint - Automation Command")
print("-" * 70)
try:
    payload = {"message": "check battery"}
    response = requests.post(
        f"{BACKEND_URL}/api/chat",
        json=payload,
        timeout=10,
        headers={"Content-Type": "application/json"}
    )
    print(f"✓ Status Code: {response.status_code}")
    data = response.json()
    print(f"✓ Response: {data['response']}")
    print(f"✓ Frok API Integrated: {data.get('frok_api_integrated', False)}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 4: Help Endpoint
print("Test 4: Help Endpoint")
print("-" * 70)
try:
    response = requests.get(f"{BACKEND_URL}/api/help", timeout=5)
    print(f"✓ Status Code: {response.status_code}")
    help_text = response.json()['help_text'][:100] + "..."
    print(f"✓ Help Text (first 100 chars): {help_text}")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

# Test 5: Chat History
print("Test 5: Chat History")
print("-" * 70)
try:
    response = requests.get(f"{BACKEND_URL}/api/history", timeout=5)
    print(f"✓ Status Code: {response.status_code}")
    history = response.json()['history']
    print(f"✓ Chat history length: {len(history)} messages")
    for i, msg in enumerate(history[-3:], 1):
        print(f"  {i}. [{msg['sender'].upper()}] {msg['message'][:50]}...")
    print()
except Exception as e:
    print(f"✗ Error: {e}")
    print()

print("=" * 70)
print("✅ Testing Complete!")
print("=" * 70)
print()
print("If all tests passed:")
print("  ✓ Backend is running correctly")
print("  ✓ API endpoints are responding")
print("  ✓ Frontend should connect without 404 errors")
print()
print("Go to http://localhost:3000 in your browser and try sending commands!")
print()
