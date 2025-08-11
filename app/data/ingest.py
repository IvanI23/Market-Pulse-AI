import os
import requests
import yfinance as yf
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.core.database import insert_news, insert_price, init_database, clear_all_data
from app.data.stock_sectors import get_company_name

load_dotenv()

# NewsAPI configuration
NEWS_API_KEY = os.getenv("api_key")
NEWSAPI_URL = "https://newsapi.org/v2/everything"

# Stock tickers to track for news and price data
TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "BRK.B", "UNH", "JNJ",
    "XOM", "V", "PG", "JPM", "HD", "CVX", "MA", "PFE", "ABBV", "BAC",
    "KO", "AVGO", "PEP", "TMO", "COST", "MRK", "WMT", "ACN", "LLY", "DHR",
    "NEE", "ABT", "VZ", "ORCL", "NKE", "CRM", "ADBE", "TXN", "BMY", "PM",
    "RTX", "WFC", "NFLX", "T", "DIS", "UPS", "HON", "QCOM", "UNP", "IBM"
]
def fetch_news_interface(ticker: str, from_date: str, to_date: str, page_size=4):
    company_name = get_company_name(ticker)
    return fetch_news(ticker, company_name, from_date, to_date, page_size)

def fetch_news(ticker: str, company_name: str, from_date: str, to_date: str, page_size=4):
    query = f'"{company_name}"'
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "sortBy": "relevancy",
        "pageSize": page_size,
        "apiKey": NEWS_API_KEY,
        "language": "en",
    }

    response = requests.get(NEWSAPI_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch news for {company_name}: {response.text}")
        return []

    articles = response.json().get("articles", [])
    news_data = []
    for article in articles:
        news_data.append({
            "ticker": ticker,
            "headline": article["title"],
            "source": article["source"]["name"],
            "url": article["url"],
            "published_at": article["publishedAt"]
        })

    return news_data

def fetch_price_data(ticker: str, days_back: int = 7):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days_back)

    df = yf.download(ticker, start=start_date, end=end_date, progress=False, auto_adjust=True)
    if df.empty:
        print(f"No price data for {ticker}")
        return []

    # Convert DataFrame to list of dictionaries for database insertion
    price_data = []
    for idx, row in df.iterrows():
        price_data.append({
            "ticker": ticker,
            "date": idx.to_pydatetime(),
            "close": float(row["Close"].iloc[0]) if hasattr(row["Close"], 'iloc') else float(row["Close"])
        })

    return price_data

def run_ingestion(reset_database=True):
    company_names = get_company_name()
    db_path = os.path.join(os.path.dirname(__file__), '..', 'sql', 'market_pulse.db')
    if not os.path.exists(db_path):
        print("Setting up database...")
        init_database()
    elif reset_database:
        clear_all_data()
    
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)
    from_str = str(yesterday)
    to_str = str(today)

    for ticker in TICKERS:
        company_name = company_names.get(ticker, "Unknown Company")
        print(f"\nProcessing {company_name}...")

        news_items = fetch_news(ticker, company_name, from_str, to_str)
        if news_items:
            print(f"Found {len(news_items)} articles")
            insert_news(news_items)
            for item in news_items[:2]:
                print(f"  • {item['headline']}")
        else:
            print(f"No news found")

        price_items = fetch_price_data(ticker)
        if price_items:
            print(f"Got {len(price_items)} price points")
            insert_price(price_items)
            latest = price_items[-1] if price_items else None
            if latest:
                print(f"  Close: ${latest['close']:.2f}")
        else:
            print(f"No price data")

if __name__ == "__main__":
    run_ingestion()
