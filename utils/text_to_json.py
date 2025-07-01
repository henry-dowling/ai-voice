import os
import json
import openai
import hashlib
from typing import Optional

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from openai import OpenAI
client = OpenAI()

CORPUS_DIR = 'corpus'
OUTPUT_DIR = 'processed_corpus'

# Set up OpenAI API key (no longer needed with OpenAI() if env is set)
# openai.api_key = os.getenv('OPENAI_API_KEY')

os.makedirs(OUTPUT_DIR, exist_ok=True)

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

def generate_title(filename: str, content: str) -> Optional[str]:
    """
    Generate a title for the document using OpenAI API (new v1.x syntax).
    Uses both the filename and content to create a meaningful title.
    """
    try:
        prompt = f'''Given this filename: "{filename}" and the following content, generate a concise, descriptive title (max 10 words) that captures the main topic or theme:\n\nContent:\n{content[:1000]}...\n\nPlease provide only the title, nothing else.'''

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise, descriptive titles for documents."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=50,
            temperature=0.3
        )
        title = response.choices[0].message.content.strip()
        title = title.strip('"').strip("'")
        return title
    except Exception as e:
        print(f"Error generating title for {filename}: {e}")
        return os.path.splitext(filename)[0]

def process_txt_files():
    for filename in os.listdir(CORPUS_DIR):
        if filename.endswith('.txt'):
            txt_path = os.path.join(CORPUS_DIR, filename)
            json_filename = os.path.splitext(filename)[0] + '.json'
            json_path = os.path.join(OUTPUT_DIR, json_filename)
            
            # Check if processed file already exists and source hasn't changed
            if os.path.exists(json_path) and is_file_unchanged(txt_path, json_path):
                print(f"Skipping {filename} - already processed and unchanged")
                continue
            
            print(f"Processing {filename}...")
            
            with open(txt_path, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Generate title using OpenAI
            title = generate_title(filename, text)
            
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
            
            print(f"Processed {filename} -> {title}")

if __name__ == '__main__':
    process_txt_files() 