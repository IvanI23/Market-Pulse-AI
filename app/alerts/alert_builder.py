import os
from datetime import datetime
from collections import defaultdict

from app.alerts.alert_data import fetch_all_high_sentiment_stocks
from app.data.stock_sectors import get_stock_sector
from app.alerts.html_generator import (
    generate_ticker_section_html, 
    generate_sector_header_html,
    load_email_template,
    populate_email_template
)

def group_stocks_by_sector(stocks):
    sector_groups = defaultdict(lambda: defaultdict(list))
    for stock in stocks:
        ticker = stock[2]
        sector = get_stock_sector(ticker)
        sector_groups[sector][ticker].append(stock)
    return sector_groups

def calculate_stats(sector_groups):
    positive_total = 0
    negative_total = 0
    neutral_total = 0
    stock_count = 0
    
    for sector, ticker_groups in sector_groups.items():
        stock_count += len(ticker_groups)
        for ticker, articles in ticker_groups.items():
            for article in articles:
                if article[4] == 'positive':
                    positive_total += 1
                elif article[4] == 'negative':
                    negative_total += 1
                else:
                    neutral_total += 1
    
    return {
        'positive': positive_total,
        'negative': negative_total,
        'neutral': neutral_total,
        'total': positive_total + negative_total + neutral_total,
        'stocks': stock_count
    }

def generate_alert_html():
    all_stocks = fetch_all_high_sentiment_stocks()
    sector_groups = group_stocks_by_sector(all_stocks)
    html_template = load_email_template()
    ticker_sections_html = ""
    
    if sector_groups:
        for sector in sorted(sector_groups.keys()):
            ticker_groups = sector_groups[sector]
            ticker_sections_html += generate_sector_header_html(sector)
            
            for ticker in sorted(ticker_groups.keys()):
                articles = ticker_groups[ticker]
                ticker_sections_html += generate_ticker_section_html(ticker, articles)
    else:
        ticker_sections_html = '<div class="no-alerts">No high sentiment alerts found (score ≥ 0.8).</div>'
    
    stats = calculate_stats(sector_groups)
    html_content = populate_email_template(html_template, ticker_sections_html, stats)
    
    return html_content

def generate_html_alert():
    return generate_alert_html()

def save_html_alert():
    html_content = generate_html_alert()
    output_dir = os.path.join(os.path.dirname(__file__), '..', '..')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"market_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📧 Beautiful grouped HTML alert generated!")
    print(f"📁 Saved to: {filepath}")
    print(f"🌐 Open in browser to preview")
    
    return filepath
