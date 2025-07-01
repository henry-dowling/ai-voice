#!/usr/bin/env python3
"""
Test script to demonstrate memoization functionality without requiring OpenAI API.
"""

import os
import json
import hashlib
from typing import Optional

CORPUS_DIR = 'corpus'
OUTPUT_DIR = 'processed_corpus'

def get_file_hash(filepath: str) -> str:
    """
    Calculate SHA-256 hash of a file for change detection.
    """
    hash_sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()

def is_file_unchanged(txt_path: str, json_path: str) -> bool:
    """
    Check if the source file has changed by comparing hashes stored in the JSON.
    """
    if not os.path.exists(json_path):
        return False
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
        
        # Check if hash is stored in the JSON
        if 'source_hash' not in json_data:
            return False
        
        # Calculate current hash of source file
        current_hash = get_file_hash(txt_path)
        
        # Compare with stored hash
        return json_data['source_hash'] == current_hash
    
    except (json.JSONDecodeError, KeyError):
        return False

def generate_mock_title(filename: str, content: str) -> str:
    """
    Generate a mock title for testing (without API calls).
    """
    # Use filename as title for testing
    return f"Mock Title: {os.path.splitext(filename)[0]}"

def test_memoization():
    """
    Test the memoization functionality.
    """
    print("Testing memoization functionality...")
    print("=" * 50)
    
    processed_count = 0
    skipped_count = 0
    
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith('.txt'):
            txt_path = os.path.join(CORPUS_DIR, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(OUTPUT_DIR, json_filename)
            
            # Check if processed file already exists and source hasn't changed
            if os.path.exists(json_path) and is_file_unchanged(txt_path, json_path):
                print(f"✅ SKIPPED: {filename} - already processed and unchanged")
                skipped_count += 1
                continue
            
            print(f"🔄 PROCESSING: {filename}...")
            
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Generate mock title
            title = generate_mock_title(filename, text)
            
            # Calculate hash of source file for future change detection
            source_hash = get_file_hash(txt_path)
            
            # Create JSON object with title, text, filename, and source hash
            json_obj = {
                'title': title,
                'text': text,
                'filename': filename,
                'source_hash': source_hash
            }
            
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(json_obj, jf, ensure_ascii=False, indent=2)
            
            print(f"✅ PROCESSED: {filename} -> {title}")
            processed_count += 1
    
    print("=" * 50)
    print(f"Summary:")
    print(f"  - Files processed: {processed_count}")
    print(f"  - Files skipped (memoized): {skipped_count}")
    print(f"  - Total files: {processed_count + skipped_count}")
    
    if skipped_count > 0:
        print("\n🎉 Memoization is working! Files were skipped because they were already processed.")
    else:
        print("\n⚠️  No files were skipped. This might indicate an issue with memoization.")

if __name__ == '__main__':
    test_memoization() 