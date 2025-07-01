#!/usr/bin/env python3
"""
Script to run the text-to-JSON processing with title generation.
Make sure to set your OPENAI_API_KEY environment variable before running.
"""

import os
import sys

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

print("DEBUG: OPENAI_API_KEY =", os.getenv('OPENAI_API_KEY'))

# Add the utils directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

# Check if OpenAI API key is set
if not os.getenv('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    print("Please set it using: export OPENAI_API_KEY='your-api-key-here'")
    sys.exit(1)

# Import and run the processing
from text_to_json import process_txt_files

if __name__ == '__main__':
    print("Starting text processing with title generation...")
    process_txt_files()
    print("Processing complete!") 