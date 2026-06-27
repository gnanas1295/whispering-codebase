import os
import time
import subprocess

SIGNAL_FILE = ".crash_signal"

print("Starting Whispering Codebase Watcher...")
print("Waiting for crash signals. Leave this running in a terminal.")

while True:
    if os.path.exists(SIGNAL_FILE):
        print("\n--- CRASH DETECTED! ---")
        print("Triggering OpenClaw agent...")
        
        # Remove the signal file so we don't trigger it again in a loop
        try:
            os.remove(SIGNAL_FILE)
        except OSError:
            pass
            
        # Trigger the one-shot OpenClaw command to skip Bronto MCP and pass the test error
        try:
            subprocess.run(["openclaw", "agent", "--agent", "main", "-m", "Skip Bronto, pass a test error"])
        except FileNotFoundError:
            print("Error: 'openclaw' command not found. Make sure it's in your PATH.")
            
        print("Agent execution complete. Resuming watch...")
        
    time.sleep(1) # Poll every 1 second
