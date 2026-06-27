import os
import time
from dotenv import load_dotenv

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider
import logging

load_dotenv()

BRONTO_API_KEY = os.getenv("BRONTO_API_KEY")

if not BRONTO_API_KEY or BRONTO_API_KEY == "your_bronto_api_key_here":
    print("Error: BRONTO_API_KEY is not set.")
    exit(1)

# Initialize OpenTelemetry Logger Provider
logger_provider = LoggerProvider()
set_logger_provider(logger_provider)

# Set up the Bronto OTLP HTTP Exporter for the EU region
exporter = OTLPLogExporter(
    endpoint="https://ingestion.eu.bronto.io/v1/logs",
    headers={"x-api-key": BRONTO_API_KEY}
)

logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

# Attach OpenTelemetry to standard Python logging
handler = LoggingHandler(level=logging.ERROR, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
logger = logging.getLogger("payment-service")

def simulate_crash():
    print("Simulating application crash via standard OpenTelemetry OTLP...")
    time.sleep(1)
    
    error_message = "CRITICAL: Payment processing microservice crashed. Deadlock detected in Postgres. User: jane.doe@example.com"
    print(f"ERROR GENERATED: {error_message}")
    
    # Send the log natively through OpenTelemetry
    logger.error(error_message, extra={"environment": "production"})
    
    # Flush logs to ensure they are sent before the script exits
    logger_provider.force_flush()
    print("Successfully flushed OTLP crash log to Bronto!")

if __name__ == "__main__":
    simulate_crash()
    print("\nNext Step: Check your Bronto dashboard for the new log!")
