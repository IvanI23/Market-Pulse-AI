import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Any

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'market_pulse.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    conn = get_connection()
    
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'schema.sql')
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    conn.executescript(schema)
    conn.close()

def insert_news(news_items: List[Dict[str, Any]]):
    conn = get_connection()
    cursor = conn.cursor()
    
    for item in news_items:
        cursor.execute("""
            INSERT OR IGNORE INTO news_articles 
            (ticker, headline, source, url, published_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
            item['ticker'],
            item['headline'],
            item['source'],
            item['url'],
            item['published_at']
        ))
    
    conn.commit()
    conn.close()

def insert_price(price_items: List[Dict[str, Any]]):
    conn = get_connection()
    cursor = conn.cursor()
    
    for item in price_items:
        cursor.execute("""
            INSERT OR REPLACE INTO stock_prices 
            (ticker, date, close_price)
            VALUES (?, ?, ?)
        """, (
            item['ticker'],
            item['date'].strftime('%Y-%m-%d'),
            item['close']
        ))
    
    conn.commit()
    conn.close()

def get_recent_news(ticker: str = None, count: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    
    if ticker:
        cursor.execute("""
            SELECT * FROM news_articles 
            WHERE ticker = ? 
            ORDER BY published_at DESC 
            LIMIT ?
        """, (ticker, count))
    else:
        cursor.execute("""
            SELECT * FROM news_articles 
            ORDER BY published_at DESC 
            LIMIT ?
        """, (count,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_recent_prices(ticker: str = None, count: int = 10):
    conn = get_connection()
    cursor = conn.cursor()
    
    if ticker:
        cursor.execute("""
            SELECT * FROM stock_prices 
            WHERE ticker = ? 
            ORDER BY date DESC 
            LIMIT ?
        """, (ticker, count))
    else:
        cursor.execute("""
            SELECT * FROM stock_prices 
            ORDER BY date DESC 
            LIMIT ?
        """, (count,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def get_unprocessed_news(limit: int = 50):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM news_articles 
        WHERE sentiment_score IS NULL 
        ORDER BY published_at DESC 
        LIMIT ?
    """, (limit,))
    
    results = cursor.fetchall()
    conn.close()
    return [dict(row) for row in results]

def insert_sentiment(sentiment_results: List[Dict[str, Any]]):
    conn = get_connection()
    cursor = conn.cursor()
    
    for result in sentiment_results:
        cursor.execute("""
            UPDATE news_articles 
            SET sentiment_score = ? 
            WHERE id = ?
        """, (result['score'], result['news_id']))
    
    conn.commit()
    conn.close()