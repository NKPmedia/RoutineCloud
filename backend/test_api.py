"""
test_api.py

A simple script to test the FastAPI endpoints.
"""

import requests
import time
import sys

# Default API URL
API_URL = "http://localhost:8000"

def test_api(base_url=API_URL):
    """Test the FastAPI endpoints."""
    print(f"Testing API at {base_url}...")
    
    try:
        # Test root endpoint
        print("\nTesting root endpoint...")
        response = requests.get(f"{base_url}/")
        print(f"Response: {response.status_code} - {response.json()}")
        
        # Test tasks endpoint
        print("\nTesting tasks endpoint...")
        response = requests.get(f"{base_url}/tasks")
        print(f"Response: {response.status_code}")
        tasks = response.json()
        print(f"Tasks: {tasks}")
        
        # Test status endpoint
        print("\nTesting status endpoint...")
        response = requests.get(f"{base_url}/status")
        print(f"Response: {response.status_code}")
        status = response.json()
        print(f"Status: {status}")
        
        # Test start routine endpoint
        print("\nTesting start routine endpoint...")
        response = requests.post(f"{base_url}/routine/start")
        print(f"Response: {response.status_code}")
        task = response.json()
        print(f"Started task: {task}")
        
        # Wait a moment to see the task
        print("\nWaiting 3 seconds...")
        time.sleep(3)
        
        # Test next task endpoint
        print("\nTesting next task endpoint...")
        response = requests.post(f"{base_url}/routine/next")
        print(f"Response: {response.status_code}")
        task = response.json()
        print(f"Next task: {task}")
        
        # Wait a moment to see the task
        print("\nWaiting 3 seconds...")
        time.sleep(3)
        
        # Test play sound endpoint
        print("\nTesting play sound endpoint...")
        response = requests.post(f"{base_url}/sound/play/book.mp3")
        print(f"Response: {response.status_code}")
        result = response.json()
        print(f"Result: {result}")
        
        # Wait a moment to hear the sound
        print("\nWaiting 3 seconds...")
        time.sleep(3)
        
        # Test stop routine endpoint
        print("\nTesting stop routine endpoint...")
        response = requests.post(f"{base_url}/routine/stop")
        print(f"Response: {response.status_code}")
        result = response.json()
        print(f"Result: {result}")
        
        print("\nAll tests completed successfully!")
        return True
        
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to {base_url}")
        print("Make sure the server is running.")
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Use command line argument for API URL if provided
    url = sys.argv[1] if len(sys.argv) > 1 else API_URL
    success = test_api(url)
    sys.exit(0 if success else 1)