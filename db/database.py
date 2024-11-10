import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

def get_db_connection():
    """
    Establish and return a connection to the PostgreSQL database.
    """
    return psycopg2.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME")
    )

def initialize_db():
    """
    Initialize PostgreSQL database.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create dna_records table if it doesn't already exists
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dna_records (
        id TEXT PRIMARY KEY,
        dna_sequence TEXT,
        is_mutant BOOLEAN,
        date TIMESTAMP DEFAULT CURRENT_DATE
    )''')
    conn.commit()
    conn.close()