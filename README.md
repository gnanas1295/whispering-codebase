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
Run the following script to simulate an application crash. It will push a mock log to Bronto and trigger the OpenClaw voice sequence.
```bash
python scripts/simulate_crash.py
```
