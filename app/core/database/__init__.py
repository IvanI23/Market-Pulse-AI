# Database package - Market Pulse AI
# Organized database operations for better maintainability

# Import all functions for backward compatibility
from .connection import (
    get_connection,
    init_database,
    clear_all_data,
    DB_PATH
)

from .insert_operations import (
    insert_news,
    insert_price,
    insert_sentiment,
    save_sentiment_analysis,
    store_sentiment_price_effects
)

from .query_operations import (
    get_recent_news,
    get_recent_prices,
    get_unprocessed_news,
    get_unprocessed_news_tuples
)

from .price_analysis import (
    get_yahoo_finance_price,
    get_realistic_price_after,
    get_price_before,
    get_enhanced_price_pair,
    get_sentiment_data
)

# Make all functions available at package level for easy import
__all__ = [
    # Connection functions
    'get_connection',
    'init_database',
    'clear_all_data',
    'DB_PATH',
    
    # Insert operations
    'insert_news',
    'insert_price',
    'insert_sentiment',
    'save_sentiment_analysis',
    'store_sentiment_price_effects',
    
    # Query operations
    'get_recent_news',
    'get_recent_prices',
    'get_unprocessed_news',
    'get_unprocessed_news_tuples',
    
    # Price analysis
    'get_yahoo_finance_price',
    'get_realistic_price_after',
    'get_price_before',
    'get_enhanced_price_pair',
    'get_sentiment_data'
]
