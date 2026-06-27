import requests
import os
import json
import time
from dotenv import load_dotenv

load_dotenv()

BRONTO_API_KEY = os.getenv("BRONTO_API_KEY")
BRONTO_INGEST_URL = os.getenv("BRONTO_INGEST_URL", "https://ingestion.eu.bronto.io/v1/logs")

def simulate_crash():
    print("Simulating application crash...")
    time.sleep(1)
    
    error_message = "CRITICAL: Payment processing microservice crashed. Deadlock detected in Postgres. User: jane.doe@example.com"
    print(f"ERROR GENERATED: {error_message}")
    
    if not BRONTO_API_KEY or BRONTO_API_KEY == "your_bronto_api_key_here":
        print("\n[WARNING] Bronto API key is not set. Skipping actual HTTP push to Bronto.")
        print("In a live environment, this would have been pushed to Bronto.")
        return

    headers = {
        "Authorization": f"Bearer {BRONTO_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "logs": [
            {
                "service": "payment-service",
                "level": "ERROR",
                "message": error_message,
                "environment": "production"
            }
        ]
    }

    try:
        r = requests.post(BRONTO_INGEST_URL, json=payload, headers=headers)
        if r.status_code == 200 or r.status_code == 202:
            print("Successfully pushed crash log to Bronto!")
        else:
            print(f"Failed to push to Bronto: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"Error connecting to Bronto API: {e}")

if __name__ == "__main__":
    simulate_crash()
    print("\nNext Step: Ask OpenClaw to 'check the system status'")
