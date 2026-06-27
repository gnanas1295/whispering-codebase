# Whispering Codebase

An ambient AI DevOps agent integration built with **OpenClaw**, **Bronto**, and **ElevenLabs**.

## Overview
This project turns silent, scrolling server logs into ambient, spoken-word system intelligence. 
When a simulated crash occurs, the error logs are streamed to **Bronto**. **OpenClaw** automatically detects the issue, fetches the log context, and utilizes the **ElevenLabs API** to synthesize an incredibly realistic, human-sounding "whisper" that plays over your host speakers, alerting you immediately to the crash without you needing to stare at a dashboard.

## Prerequisites
- **WSL (Ubuntu-24.04)**
- **Python 3.10+** (with `requests` library)
- **OpenClaw** installed locally
- API Keys for **Bronto Ingestion**, **ElevenLabs**, and **TensorX**.

## Setup
1. Copy `.env.example` to `.env` and fill in your API credentials.
2. Run `pip install requests` inside WSL.
3. Link the OpenClaw skill directory:
   `ln -s $(pwd)/openclaw_workspace/skills/whispering-codebase ~/.openclaw/workspace/skills/`

## Usage

### 1. Generating Simulated Production Traffic
To visualize a realistic production environment in your Bronto dashboard, run the dummy log population script. This will dynamically generate and push **100 simulated production logs** across 4 different microservices (e.g. `payment-service`, `auth-service`, `inventory-service`), complete with randomized user data, IPs, and varied error types (Deadlocks, Timeouts, etc.):
```bash
python3 scripts/populate_dummy_logs.py
```
*Run this anytime before a live demo to populate the Bronto UI with fresh data.*

### 2. Triggering the Voice Sequence
Run the crash script to push a specific, critical database deadlock error to Bronto:
```bash
python3 scripts/simulate_crash.py
```
Then, prompt your OpenClaw agent with **"Check the system"** to automatically narrate the crash out loud via ElevenLabs.
