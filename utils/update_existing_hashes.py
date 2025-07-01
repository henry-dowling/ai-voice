#!/usr/bin/env python3
"""
Script to update existing JSON files with source hashes for memoization.
"""

import os
import json
import hashlib

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

def update_existing_files():
    """
    Update existing JSON files to include source hashes for memoization.
    """
    updated_count = 0
    
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith('.json'):
            json_path = os.path.join(OUTPUT_DIR, filename)
            
            # Find corresponding txt file
            txt_filename = filename.replace('.json', '.txt')
            txt_path = os.path.join(CORPUS_DIR, txt_filename)
            
            if not os.path.exists(txt_path):
                print(f"Warning: No corresponding txt file found for {filename}")
                continue
            
            try:
                # Load existing JSON
                with open(json_path, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                
                # Check if hash already exists
                if 'source_hash' in json_data:
                    print(f"Skipping {filename} - already has hash")
                    continue
                
                # Calculate and add hash
                source_hash = get_file_hash(txt_path)
                json_data['source_hash'] = source_hash
                
                # Write updated JSON
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(json_data, f, ensure_ascii=False, indent=2)
                
                print(f"Updated {filename} with source hash")
                updated_count += 1
                
            except Exception as e:
                print(f"Error updating {filename}: {e}")
    
    print(f"\nUpdated {updated_count} files with source hashes")

if __name__ == '__main__':
    update_existing_files() 