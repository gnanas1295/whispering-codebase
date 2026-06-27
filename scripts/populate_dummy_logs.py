import os
import random
import time
import logging
from dotenv import load_dotenv

from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter

load_dotenv()

BRONTO_API_KEY = os.getenv("BRONTO_API_KEY")

if not BRONTO_API_KEY or BRONTO_API_KEY == "your_bronto_api_key_here":
    print("Error: BRONTO_API_KEY is not set.")
    exit(1)

SERVICES = ["payment-service", "auth-service", "inventory-service", "notification-service"]
USERS = ["jane.doe@example.com", "john.smith@example.com", "alice.williams@example.com", "bob.brown@example.com", "guest"]

ERROR_TEMPLATES = {
    "payment-service": [
        "CRITICAL: Deadlock detected in Postgres while updating transaction for user {user}.",
        "ERROR: Payment gateway timeout for user {user}. Transaction reversed.",
        "WARN: High latency detected in payment processing API (duration: {latency}ms)."
    ],
    "auth-service": [
        "ERROR: Invalid JWT token signature for user {user}.",
        "WARN: Rate limit exceeded for login attempts from IP {ip}.",
        "ERROR: Connection refused to Redis session store."
    ],
    "inventory-service": [
        "ERROR: Stock mismatch detected for SKU-{sku}.",
        "CRITICAL: Database connection lost during bulk stock update.",
        "WARN: Low stock alert for SKU-{sku} (remaining: {count})."
    ],
    "notification-service": [
        "ERROR: Failed to send SMS via Twilio API. Status code: 503.",
        "WARN: Email queue is backing up. Current queue size: {queue_size}.",
        "ERROR: SendGrid SMTP connection timeout for user {user}."
    ]
}

print("Initializing OpenTelemetry providers for services...")

# Initialize a separate provider for each service to ensure proper Resource mapping
providers = {}
loggers = {}

for service in SERVICES:
    resource = Resource(attributes={
        "service.name": service,
        "service.version": "1.0.0",
        "deployment.environment": "production"
    })
    
    provider = LoggerProvider(resource=resource)
    exporter = OTLPLogExporter(
        endpoint="https://ingestion.eu.bronto.io/v1/logs",
        headers={"Authorization": f"Bearer {BRONTO_API_KEY}"}
    )
    provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    providers[service] = provider
    
    # We create a standard python logger and attach the OpenTelemetry handler
    handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
    logger = logging.getLogger(service)
    logger.setLevel(logging.INFO)
    logger.handlers.clear()
    logger.addHandler(handler)
    loggers[service] = logger

print("Generating 100 production logs...")

for i in range(100):
    service = random.choice(SERVICES)
    user = random.choice(USERS)
    template = random.choice(ERROR_TEMPLATES[service])
    
    # Format the template with random data
    message = template.format(
        user=user,
        ip=f"192.168.1.{random.randint(10, 250)}",
        sku=random.randint(1000, 9999),
        latency=random.randint(2000, 8000),
        count=random.randint(0, 5),
        queue_size=random.randint(1000, 5000)
    )
    
    severity = message.split(":")[0]
    
    # Add attributes to the log
    extra = {
        "user_email": user,
        "log_type": "application",
        "environment": "production"
    }
    
    if severity in ["CRITICAL", "ERROR"]:
        loggers[service].error(message, extra=extra)
    elif severity == "WARN":
        loggers[service].warning(message, extra=extra)
    else:
        loggers[service].info(message, extra=extra)
        
    if i % 20 == 0:
        print(f"Generated {i}/100 logs...")

# Flush all providers
print("Flushing data to Bronto...")
for service, provider in providers.items():
    provider.force_flush()

print("Successfully pushed 100 simulated production logs to Bronto!")
