import os
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import json
from openai import OpenAI

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DB_NAME = os.getenv('PGDATABASE', 'henry-pg')
DB_USER = os.getenv('PGUSER', 'postgres')
DB_PASSWORD = os.getenv('PGPASSWORD', 'supersecret')
DB_HOST = os.getenv('PGHOST', 'localhost')
DB_PORT = os.getenv('PGPORT', '5432')

client = OpenAI()

CORPUS_DIR = 'processed_corpus'
EMBEDDING_MODEL = 'text-embedding-3-small'
TABLE_NAME = 'blog_style'

# Connect to PostgreSQL
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

def process_and_upload():
    conn = get_db_connection()
    data_to_insert = []
    for fname in os.listdir(CORPUS_DIR):
        if not fname.endswith('.json'):
            continue
        fpath = os.path.join(CORPUS_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        with open(fpath, 'r', encoding='utf-8') as f:
            doc = json.load(f)
        text = doc.get('text', '')
        if not text:
            print(f"Warning: No text found in {fname}, skipping.")
            continue
        embedding = get_embedding(text)
        data_to_insert.append((text, embedding))
    if data_to_insert:
        with conn.cursor() as cur:
            execute_values(
                cur,
                f"INSERT INTO {TABLE_NAME} (txt, emb) VALUES %s",
                data_to_insert
            )
            conn.commit()
    conn.close()

if __name__ == '__main__':
    print("Processing files and uploading embeddings to blog_style...")
    process_and_upload()
    print("Done.") 