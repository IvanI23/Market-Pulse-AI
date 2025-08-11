import time
import sys
import os
from datetime import datetime, timedelta
import app.core.database as db
import app.data.ingest as ingest
import app.data.nlp_engine as nlp_engine

# Top 50 US stocks by market cap for analysis
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK.B", "UNH", "JNJ",
    "XOM", "V", "PG", "JPM", "HD", "CVX", "MA", "PFE", "ABBV", "BAC",
    "KO", "AVGO", "PEP", "TMO", "COST", "MRK", "WMT", "ACN", "LLY", "DHR",
    "NEE", "ABT", "VZ", "ORCL", "NKE", "CRM", "ADBE", "TXN", "BMY", "PM",
    "RTX", "WFC", "NFLX", "T", "DIS", "UPS", "HON", "QCOM", "UNP", "IBM"
]

# Console output formatting functions
def print_header(title):
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_step(step_num, description):
    print(f"\n[STEP {step_num}] {description}")
    print("-" * 40)

def print_result(message):
    print(f"  ✓ {message}")

def print_error(message):
    print(f"  ✗ ERROR: {message}")

def run_pipeline(reset_db=True):
    """Main pipeline: ingests news/prices, analyzes sentiment, generates alerts"""
    print_header("MARKET PULSE AI - COMPLETE PIPELINE")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # Initialize database and optionally clear existing data
        print_step(1, "Database Initialization")
        db.init_database()
        print_result("Database initialized successfully")
        
        if reset_db:
            db.clear_all_data()
        
        # Check initial database state
        news_count = len(db.get_recent_news(count=1000))
        prices_count = len(db.get_recent_prices(count=1000))
        sentiment_count = len(db.get_sentiment_data())
        
        print_result(f"Initial Database State:")
        print(f"    News articles: {news_count}")
        print(f"    Price records: {prices_count}")
        print(f"    Sentiment records: {sentiment_count}")
        
        # Fetch latest news for all tracked tickers
        print_step(2, "News Data Ingestion")
        
        tickers = TICKERS
        print_result(f"Fetching news for tickers: {', '.join(tickers)}")
        
        from datetime import timedelta
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        from_str = str(yesterday)
        to_str = str(today)
        
        total_articles = 0
        for ticker in tickers:
            print(f"  Processing {ticker}...")
            articles = ingest.fetch_news_interface(ticker, from_str, to_str)
            if articles:
                db.insert_news(articles)
                saved_count = len(articles)
                total_articles += saved_count
                print_result(f"{ticker}: {saved_count} new articles saved")
            else:
                print_result(f"{ticker}: No new articles found")
        
        print_result(f"Total new articles ingested: {total_articles}")
        
        print_step(3, "Price Data Ingestion")
        
        total_prices = 0
        for ticker in tickers:
            print(f"  Processing {ticker} prices...")
            price_data = ingest.fetch_price_data(ticker)
            if price_data:
                db.insert_price(price_data)
                saved_count = len(price_data)
                total_prices += saved_count
                print_result(f"{ticker}: {saved_count} new price records saved")
            else:
                print_result(f"{ticker}: No new price data found")
        
        print_result(f"Total new price records ingested: {total_prices}")
        
        print_step(4, "NLP Sentiment Analysis")
        
        unprocessed_news = db.get_unprocessed_news_tuples()
        print_result(f"Found {len(unprocessed_news)} articles to process")
        
        processed_count = 0
        for article in unprocessed_news:
            print(f"  Processing article ID {article[0]}...")
            
            sentiment_score, sentiment_label = nlp_engine.analyze_sentiment(article[3])
            
            db.save_sentiment_analysis(
                news_id=article[0],
                sentiment_score=sentiment_score,
                sentiment_label=sentiment_label
            )
            
            processed_count += 1
            
            if processed_count % 5 == 0:
                print_result(f"Processed {processed_count}/{len(unprocessed_news)} articles")
        
        print_result(f"Sentiment analysis completed: {processed_count} articles processed")
        
        print_step(5, "Market Analysis & Correlation")
        
        sentiment_data = db.get_sentiment_data()
        if sentiment_data:
            import pandas as pd
            df = pd.DataFrame(sentiment_data)
            db.store_sentiment_price_effects(df)
            print_result(f"Processed {len(sentiment_data)} sentiment-price correlations for alerts")
        else:
            print_result("No sentiment data available for correlation analysis")
        
        print_step(6, "Pipeline Summary")
        
        final_news_count = len(db.get_recent_news(count=1000))
        final_prices_count = len(db.get_recent_prices(count=1000))
        final_sentiment_count = len(db.get_sentiment_data())
        
        print_result("Final Database State:")
        print(f"    News articles: {final_news_count} (+{final_news_count - news_count})")
        print(f"    Price records: {final_prices_count} (+{final_prices_count - prices_count})")
        print(f"    Sentiment records: {final_sentiment_count} (+{final_sentiment_count - sentiment_count})")
        
        print_result("Ready to generate email alerts from sentiment-price correlations!")
        
        print_header("PIPELINE COMPLETED SUCCESSFULLY")
        print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Total processing time: ~{time.time():.0f} seconds")

    except Exception as e:
        print_error(f"Pipeline failed: {str(e)}")
        sys.exit(1)

def show_current_status():
    print_header("CURRENT DATABASE STATUS")
    
    try:
        news_count = len(db.get_recent_news(count=1000))
        prices_count = len(db.get_recent_prices(count=1000))
        sentiment_count = len(db.get_sentiment_data())
        
        print_result("Database Contents:")
        print(f"    News articles: {news_count}")
        print(f"    Price records: {prices_count}")
        print(f"    Sentiment records: {sentiment_count}")
        
        recent_news = db.get_recent_news(5)
        if recent_news:
            print_result("Recent News Articles:")
            for article in recent_news:
                print(f"    {article['ticker']} - {article['headline'][:50]}...")
        
    except Exception as e:
        print_error(f"Failed to get status: {str(e)}")

if __name__ == "__main__":
    start_time = time.time()
    
    if len(sys.argv) > 1 and sys.argv[1] == "status":
        show_current_status()
    else:
        run_pipeline()
    
    end_time = time.time()
    print(f"\nExecution time: {end_time - start_time:.2f} seconds")
