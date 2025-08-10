from .connection import get_connection

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

def get_unprocessed_news_tuples():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, ticker, headline, headline, published_at 
        FROM news_articles 
        WHERE sentiment_score IS NULL 
        ORDER BY published_at DESC 
        LIMIT 50
    """)
    
    results = cursor.fetchall()
    conn.close()
    return results
