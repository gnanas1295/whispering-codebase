import os
import time
import logging
from dotenv import load_dotenv

# Enable OpenTelemetry internal diagnostic logging to see HTTP errors!
logging.basicConfig(level=logging.DEBUG)
os.environ["OTEL_PYTHON_LOG_LEVEL"] = "debug"

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter, SimpleLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry._logs import set_logger_provider

from opentelemetry.sdk.resources import Resource

load_dotenv()

BRONTO_API_KEY = os.getenv("BRONTO_API_KEY")

if not BRONTO_API_KEY or BRONTO_API_KEY == "your_bronto_api_key_here":
    print("Error: BRONTO_API_KEY is not set.")
    exit(1)

# Define the OpenTelemetry Resource (this fixes 'unknown_service' in Bronto)
resource = Resource(attributes={
    "service.name": "payment-service",
    "service.version": "1.0.0",
    "deployment.environment": "production"
})

logger_provider = LoggerProvider(resource=resource)
set_logger_provider(logger_provider)

# Set up the Bronto OTLP HTTP Exporter for the EU region
exporter = OTLPLogExporter(
    endpoint="https://ingestion.eu.bronto.io/v1/logs",
    headers={"Authorization": f"Bearer {BRONTO_API_KEY}"}
)

# Use SimpleLogRecordProcessor instead of Batch so it flushes immediately and blocks, showing errors inline
logger_provider.add_log_record_processor(SimpleLogRecordProcessor(exporter))
# Also add console exporter so we see what is generated
logger_provider.add_log_record_processor(SimpleLogRecordProcessor(ConsoleLogExporter()))

handler = LoggingHandler(level=logging.ERROR, logger_provider=logger_provider)
logging.getLogger().addHandler(handler)
logger = logging.getLogger("payment-service")

def simulate_crash():
    print("Simulating application crash via standard OpenTelemetry OTLP...")
    
    error_message = "CRITICAL: Payment processing microservice crashed. Deadlock detected in Postgres. User: jane.doe@example.com"
    print(f"ERROR GENERATED: {error_message}")
    
    logger.error(error_message, extra={"environment": "production"})
    
    logger_provider.force_flush()
    print("Flushed OTLP crash log to Bronto!")

if __name__ == "__main__":
    simulate_crash()
