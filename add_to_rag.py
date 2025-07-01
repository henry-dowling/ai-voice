#!/usr/bin/env python3
"""
Controller script that runs both text processing and embedding creation/upload.
This script simply calls the two existing scripts in sequence.
"""

import subprocess
import sys
import os

def run_script(script_name, description):
    """Run a Python script and handle any errors."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run([sys.executable, script_name], check=True)
        print(f"✓ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error running {script_name}: {e}")
        return False
    except FileNotFoundError:
        print(f"✗ Script {script_name} not found!")
        return False

def main():
    """Run the complete pipeline by calling both scripts."""
    print("Starting complete pipeline...")
    
    # Step 1: Run text processing
    if not run_script("run_processing.py", "Text Processing"):
        print("Pipeline failed at text processing step.")
        sys.exit(1)
    
    # Step 2: Run embedding creation and upload
    if not run_script("create_embeddings_and_upload.py", "Embedding Creation & Upload"):
        print("Pipeline failed at embedding creation step.")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print("Pipeline completed successfully! 🎉")
    print(f"{'='*60}")

if __name__ == '__main__':
    main() 