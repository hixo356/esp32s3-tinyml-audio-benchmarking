Import("env")
import subprocess
import os

def run_mel_gen():
    # print("\n--- [Custom] Running Mel Filterbank Generator ---")
    try:
        subprocess.run(["python", "gen_mel.py"], check=True)
        # print("--- [Custom] Mel Data Header Updated Successfully ---\n")
    except Exception as e:
        # print(f"--- [Custom] ERROR: Could not run gen_mel.py: {e} ---\n")
        Exit(1)

env.AddPreAction("buildprog", run_mel_gen())
run_mel_gen()