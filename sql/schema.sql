CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) NOT NULL,
    headline TEXT NOT NULL,
    source VARCHAR(100),
    url TEXT,
    published_at DATETIME,
    sentiment_score REAL,
    sentiment_label VARCHAR(10)
);

CREATE TABLE IF NOT EXISTS stock_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker VARCHAR(10) NOT NULL,
    date DATE NOT NULL,
    close_price REAL NOT NULL,
    UNIQUE(ticker, date)
);

CREATE TABLE IF NOT EXISTS sentiment_price_effect (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    news_id INTEGER REFERENCES news_articles(id),
    ticker VARCHAR(10) NOT NULL,
    score REAL,
    label VARCHAR(10),
    price_before REAL,
    price_after REAL,
    price_change_pct REAL,
    published_at DATE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Users table for subscription management
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    tickers TEXT,  -- JSON string for SQLite compatibility: '["AAPL", "TSLA"]'
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);