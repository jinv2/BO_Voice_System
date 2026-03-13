import sys
import os
import time
import threading
import numpy as np

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from bo_ui import BOStatusUI
from bo_cli import BOCLI

def simulate_vibe():
    print("Simulating Vibe Pulse...")
    ui = BOStatusUI()
    
    def pulse_logic():
        time.sleep(1)
        # Pulse from dark to bright green
        for i in range(0, 150, 5):
            ui.update_vibe(i)
            time.sleep(0.02)
        for i in range(150, 0, -5):
            ui.update_vibe(i)
            time.sleep(0.02)
        print("Vibe Pulse Verification Complete.")
        ui.root.destroy()
        
    threading.Thread(target=pulse_logic, daemon=True).start()
    ui.run()

def simulate_text_command():
    print("Simulating Text Command Injection...")
    cli = BOCLI()
    # Mock LLM and core execution for test
    class MockResult:
        def get(self, k, default=None): return "success" if k == "status" else default
    
    print("Testing 'summary' command...")
    # This should trigger notify-send during the async execution
    cli.execute_cmd_wrapper("summary")
    time.sleep(2)
    print("Text Command Verification Complete.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "vibe":
        simulate_vibe()
    elif len(sys.argv) > 1 and sys.argv[1] == "text":
        simulate_text_command()
    else:
        print("Usage: python3 verify_shensist.py [vibe|text]")
