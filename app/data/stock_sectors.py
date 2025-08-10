STOCK_SECTORS = {
    'AAPL': 'Technology',
    'MSFT': 'Technology',
    'GOOGL': 'Technology',
    'AMZN': 'Technology',
    'NVDA': 'Technology',
    'META': 'Technology',
    'TSLA': 'Technology',
    'NFLX': 'Technology',
    'ORCL': 'Technology',
    'CRM': 'Technology',
    'ADBE': 'Technology',
    'INTC': 'Technology',
    'AMD': 'Technology',
    'UBER': 'Technology',
    
    'JPM': 'Finance',
    'BAC': 'Finance',
    'WFC': 'Finance',
    'GS': 'Finance',
    'MS': 'Finance',
    'C': 'Finance',
    'BLK': 'Finance',
    'AXP': 'Finance',
    'SCHW': 'Finance',
    'V': 'Finance',
    'MA': 'Finance',
    
    'UNH': 'Healthcare',
    'JNJ': 'Healthcare',
    'PFE': 'Healthcare',
    'ABBV': 'Healthcare',
    'MRK': 'Healthcare',
    'LLY': 'Healthcare',
    'TMO': 'Healthcare',
    'ABT': 'Healthcare',
    'DHR': 'Healthcare',
    
    'BRK.B': 'Finance',
    'XOM': 'Energy',
    'CVX': 'Energy',
    'COP': 'Energy',
    
    'PG': 'Consumer Goods',
    'KO': 'Consumer Goods',
    'PEP': 'Consumer Goods',
    'WMT': 'Consumer Goods',
    'COST': 'Consumer Goods',
    'HD': 'Consumer Goods',
    'MCD': 'Consumer Goods',
    'NKE': 'Consumer Goods',
    
    'VZ': 'Telecom',
    'T': 'Telecom',
    
    'DIS': 'Entertainment',
    'CMCSA': 'Entertainment',
    
    'BA': 'Industrial',
    'CAT': 'Industrial',
    'MMM': 'Industrial',
    'GE': 'Industrial'
}


COMPANY_NAMES = {
    'AAPL': 'Apple Inc.',
    'MSFT': 'Microsoft Corp.',
    'GOOGL': 'Alphabet Inc.',
    'AMZN': 'Amazon.com Inc.',
    'NVDA': 'NVIDIA Corp.',
    'META': 'Meta Platforms Inc.',
    'TSLA': 'Tesla Inc.',
    'NFLX': 'Netflix Inc.',
    'ORCL': 'Oracle Corp.',
    'CRM': 'Salesforce Inc.',
    'ADBE': 'Adobe Inc.',
    'INTC': 'Intel Corp.',
    'AMD': 'Advanced Micro Devices',
    'UBER': 'Uber Technologies',
    
    'JPM': 'JPMorgan Chase',
    'BAC': 'Bank of America',
    'WFC': 'Wells Fargo',
    'GS': 'Goldman Sachs',
    'MS': 'Morgan Stanley',
    'C': 'Citigroup Inc.',
    'BLK': 'BlackRock Inc.',
    'AXP': 'American Express',
    'SCHW': 'Charles Schwab',
    'V': 'Visa Inc.',
    'MA': 'Mastercard Inc.',
    
    'UNH': 'UnitedHealth Group',
    'JNJ': 'Johnson & Johnson',
    'PFE': 'Pfizer Inc.',
    'ABBV': 'AbbVie Inc.',
    'MRK': 'Merck & Co.',
    'LLY': 'Eli Lilly',
    'TMO': 'Thermo Fisher',
    'ABT': 'Abbott Laboratories',
    'DHR': 'Danaher Corp.',
    
    'BRK.B': 'Berkshire Hathaway',
    'XOM': 'Exxon Mobil',
    'CVX': 'Chevron Corp.',
    'COP': 'ConocoPhillips',
    
    'PG': 'Procter & Gamble',
    'KO': 'The Coca-Cola Company',
    'PEP': 'PepsiCo Inc.',
    'WMT': 'Walmart Inc.',
    'COST': 'Costco Wholesale',
    'HD': 'The Home Depot',
    'MCD': 'McDonald\'s Corp.',
    'NKE': 'Nike Inc.',
    
    'VZ': 'Verizon Communications',
    'T': 'AT&T Inc.',
    
    'DIS': 'The Walt Disney Company',
    'CMCSA': 'Comcast Corp.',
    
    'BA': 'The Boeing Company',
    'CAT': 'Caterpillar Inc.',
    'MMM': '3M Company',
    'GE': 'General Electric'
}

def get_stock_sector(ticker):
    return STOCK_SECTORS.get(ticker, 'Other')

def get_company_name(ticker):
    return COMPANY_NAMES.get(ticker, ticker)

def get_sectors():
    return sorted(set(STOCK_SECTORS.values()))

def get_stocks_by_sector(sector):
    return [ticker for ticker, stock_sector in STOCK_SECTORS.items() if stock_sector == sector]
