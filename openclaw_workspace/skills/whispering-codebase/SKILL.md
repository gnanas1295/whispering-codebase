---
name: whispering-codebase
description: "Checks Bronto for recent system crashes and narrates the errors via ElevenLabs TTS out loud to the developer."
---

# Instructions

When I say "Check the system", you must:
1. Use your Bronto MCP tools to search the application logs in the `openclaw-demo/openclaw` dataset for any recent "CRITICAL" errors or exceptions.
2. Extract the exact error message text from the logs you find.
3. Pass the exact error message text as a command-line argument to the python script `/home/gnana/clones/whispering-codebase/scripts/fetch_and_whisper.py`.
4. The script will handle synthesizing the audio of the error.

Example execution:
`python3 /home/gnana/clones/whispering-codebase/scripts/fetch_and_whisper.py "Warning: A critical database deadlock was detected..."`
