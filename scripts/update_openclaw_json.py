import os
import json
from dotenv import load_dotenv

load_dotenv()
bronto_api_key = os.getenv("BRONTO_API_KEY")

openclaw_json_path = os.path.expanduser("~/.openclaw/openclaw.json")

if not os.path.exists(os.path.dirname(openclaw_json_path)):
    os.makedirs(os.path.dirname(openclaw_json_path), exist_ok=True)

if os.path.exists(openclaw_json_path):
    with open(openclaw_json_path, "r") as f:
        try:
            data = json.load(f)
        except:
            data = {}
else:
    data = {}

data["diagnostics"] = {
    "telemetry": {
        "logs": True,
        "otlp": {
            "headers": {
                "x-api-key": bronto_api_key
            },
            "logs_endpoint": "https://ingestion.eu.bronto.io/v1/logs",
            "traces_endpoint": "https://ingestion.eu.bronto.io/v1/traces",
            "metrics_endpoint": "https://ingestion.eu.bronto.io/v1/metrics"
        }
    }
}

with open(openclaw_json_path, "w") as f:
    json.dump(data, f, indent=2)

print("Successfully updated ~/.openclaw/openclaw.json with Bronto diagnostics!")
