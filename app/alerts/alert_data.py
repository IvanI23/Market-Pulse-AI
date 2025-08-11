import app.core.database as db
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'sql', 'market_pulse.db')

def fetch_all_high_sentiment_stocks():
    query = """SELECT b.*, a.headline, a.published_at, a.url FROM news_articles a
                JOIN sentiment_price_effect b ON a.id = b.news_id
                WHERE b.score >= 0.8
                ORDER BY b.ticker, b.score DESC"""

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_stocks_by_sentiment(min_score=0.8):
    query = """SELECT b.*, a.headline, a.published_at, a.url FROM news_articles a
                JOIN sentiment_price_effect b ON a.id = b.news_id
                WHERE b.score >= ?
                ORDER BY b.ticker, b.score DESC"""

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (min_score,))
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_stocks_by_ticker(ticker):
    query = """SELECT b.*, a.headline, a.published_at, a.url FROM news_articles a
                JOIN sentiment_price_effect b ON a.id = b.news_id
                WHERE b.ticker = ?
                ORDER BY b.score DESC"""

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query, (ticker,))
    results = cursor.fetchall()
    conn.close()
    return results
