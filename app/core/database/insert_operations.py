from typing import List, Dict, Any
from .connection import get_connection

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

def insert_sentiment(sentiment_results: List[Dict[str, Any]]):
    conn = get_connection()
    cursor = conn.cursor()
    
    for result in sentiment_results:
        cursor.execute("""
            UPDATE news_articles 
            SET sentiment_score = ?, sentiment_label = ?
            WHERE id = ?
        """, (result['score'], result['label'], result['news_id']))
    
    conn.commit()
    conn.close()

def save_sentiment_analysis(news_id, sentiment_score, sentiment_label):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE news_articles 
        SET sentiment_score = ?, sentiment_label = ?
        WHERE id = ?
    """, (sentiment_score, sentiment_label, news_id))
    
    conn.commit()
    conn.close()

def store_sentiment_price_effects(df_data):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM sentiment_price_effect")
    
    for _, row in df_data.iterrows():
        cursor.execute("""
            INSERT INTO sentiment_price_effect 
            (news_id, ticker, score, label, price_before, price_after, price_change_pct, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['news_id'],
            row['ticker'],
            row['score'],
            row['label'],
            row['price_before'],
            row['price_after'],
            row['price_change_pct'],
            row['published_at']
        ))
    
    conn.commit()
    conn.close()
    print(f"✅ Stored {len(df_data)} sentiment-price effects to database")
