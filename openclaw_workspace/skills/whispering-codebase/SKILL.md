---
name: whispering-codebase
description: "Checks Bronto for recent system crashes and narrates the errors via ElevenLabs TTS out loud to the developer."
---

# Instructions

When the user asks to "check the system", "narrate the system logs", or asks if there are any issues:

1. Confirm that you are initiating the system diagnostic.
2. Execute the python script to fetch logs and synthesize speech:
   Run `python3 scripts/fetch_and_whisper.py` from the root of the project.
3. Wait for the audio to finish playing (the script handles the playback natively).
4. Output a summary to the user in chat confirming that you have read the logs and narrated the critical error.
