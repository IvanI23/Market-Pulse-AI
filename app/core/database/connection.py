import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'sql', 'market_pulse.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    
    schema_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'sql', 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.close()

def clear_all_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    print("🗑️ Clearing all existing data...")
    cursor.execute("DELETE FROM sentiment_price_effect")
    cursor.execute("DELETE FROM news_articles")
    cursor.execute("DELETE FROM stock_prices")
    
    conn.commit()
    conn.close()
    print("✅ Database cleared successfully")
