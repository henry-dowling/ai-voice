#!/usr/bin/env python3
"""
compose.py: A writing tool that generates a piece in your style using GPT-4o.
- Prompts you for a description of what you want to write.
- Samples your writing from processed_corpus/*.json for style context.
- Calls GPT-4o with your prompt and style context.
- Prints the generated piece.

Requires: openai>=1.0.0, python-dotenv (optional for .env support)
"""
import os
import sys
import json
import glob
import random
from openai import OpenAI
import psycopg2
from psycopg2.extras import RealDictCursor

# Load environment variables from .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

CORPUS_DIR = 'processed_corpus'
STYLE_SNIPPET_CHAR_LIMIT = 1200  # Total chars of style context to pass in
SNIPPET_MIN_LEN = 200  # Minimum chars per snippet

# DB connection settings (reuse from create_embeddings_and_upload.py)
DB_NAME = os.getenv('PGDATABASE', 'henry-pg')
DB_USER = os.getenv('PGUSER', 'postgres')
DB_PASSWORD = os.getenv('PGPASSWORD', 'supersecret')
DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')
EMBEDDING_MODEL = 'text-embedding-3-small'
TABLE_NAME = 'blog_style'
TOP_K = 5  # Number of most similar snippets to use for style context

# Call GPT-4o
client = OpenAI()

# Collect style snippets from user's writing
style_snippets = []
for json_path in glob.glob(os.path.join(CORPUS_DIR, '*.json')):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            text = data.get('text', '')
            if len(text) >= SNIPPET_MIN_LEN:
                # Take a random chunk from the text
                start = random.randint(0, max(0, len(text) - SNIPPET_MIN_LEN))
                snippet = text[start:start+SNIPPET_MIN_LEN]
                style_snippets.append(snippet)
    except Exception as e:
        continue

# Shuffle and combine snippets up to STYLE_SNIPPET_CHAR_LIMIT
random.shuffle(style_snippets)
style_context = ''
for snippet in style_snippets:
    if len(style_context) + len(snippet) > STYLE_SNIPPET_CHAR_LIMIT:
        break
    style_context += snippet + '\n---\n'

if not style_context:
    print("Error: No style context found in processed_corpus. Please process your writing samples first.")
    sys.exit(1)

# Prompt user for what they want to write
description = input("Describe what you want to write: ").strip()
if not description:
    print("No prompt provided. Exiting.")
    sys.exit(1)

def get_db_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

def get_embedding(text, model=EMBEDDING_MODEL):
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    return response.data[0].embedding

def get_top_style_snippets(prompt, top_k=TOP_K):
    embedding = get_embedding(prompt)
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            f"""
            SELECT txt FROM {TABLE_NAME}
            ORDER BY emb <-> %s::vector
            LIMIT %s
            """,
            (embedding, top_k)
        )
        rows = cur.fetchall()
    conn.close()
    return [row['txt'] for row in rows]

# Get most relevant style snippets
style_snippets = get_top_style_snippets(description)
if not style_snippets:
    print("Error: No style context found in vector DB. Please process and upload your writing samples first.")
    sys.exit(1)

style_context = '\n---\n'.join(style_snippets)

# Compose system prompt
system_prompt = (
    "You are a writing assistant that writes in the user's style. "
    "Below are snippets of the user's writing. When given a prompt, write a new piece in their style. "
    "Be authentic to their tone, structure, and voice.\n\n"
    "USER'S WRITING SNIPPETS:\n" + style_context
)

try:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": description}
        ],
        max_tokens=1024,
        temperature=0.7
    )
    print("\n---\nGenerated piece:\n")
    print(response.choices[0].message.content.strip())
except Exception as e:
    print(f"Error generating piece: {e}")
    sys.exit(1) 