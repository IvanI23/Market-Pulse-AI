import os
from datetime import datetime
from collections import defaultdict
from app.data.stock_sectors import get_stock_sector, get_company_name

def load_css_styles():
    # Load external CSS styles for email template
    css_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'email_styles.css')
    try:
        with open(css_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("Warning: email_styles.css not found, using fallback styles")
        return "/* Fallback styles - CSS file not found */"

def generate_article_card_html(stock):
    # Extract stock data from tuple
    ticker = stock[2]
    score = stock[3]
    label = stock[4]
    price_before = stock[5]
    price_after = stock[6]
    price_change = stock[7]
    headline = stock[-3]  # headline is now 3rd from last
    url = stock[-1]       # url is last
    
    # Assign styling based on sentiment
    if label == 'positive':
        article_class = "positive-article"
        badge_class = "positive-badge"
        emoji = "📈"
    elif label == 'negative':
        article_class = "negative-article"
        badge_class = "negative-badge"
        emoji = "📉"
    else:
        article_class = "neutral-article"
        badge_class = "neutral-badge"
        emoji = "➖"
    
    price_change_class = "price-up" if price_change >= 0 else "price-down"
    price_arrow = "↗" if price_change >= 0 else "↘"
    
    headline_html = f'<a href="{url}" target="_blank" class="article-link">"{headline}"</a>' if url else f'"{headline}"'
    
    return f"""
            <div class="article-card {article_class}">
                <div class="article-header">
                    <div class="company-sector">
                        <span class="company-name">{company_name} ({ticker})</span>
                        <span class="sector">{sector}</span>
                    </div>
                    <div class="sentiment-wrapper">
                        <span class="sentiment-badge {badge_class}">
                            {emoji} {label.upper()}
                        </span>
                        <span class="score-text">{score:.2f}</span>
                    </div>
                </div>

                <div class="article-headline">
                    {headline_html}
                </div>

                <div class="price-info">
                    <div class="price-movement">
                        <span class="price-before">${price_before:.2f}</span>
                        <span class="price-arrow">{price_arrow}</span>
                        <span class="price-after">${price_after:.2f}</span>
                    </div>
                    <div class="price-change {price_change_class}">
                        {price_change:+.2f}%
                    </div>
                </div>
            </div>

"""

def generate_ticker_section_html(ticker, articles):
    company_name = get_company_name(ticker)
    # Calculate sentiment distribution
    positive_count = sum(1 for article in articles if article[4] == 'positive')
    negative_count = sum(1 for article in articles if article[4] == 'negative')
    neutral_count = len(articles) - positive_count - negative_count
    
    # Determine dominant sentiment
    if positive_count > negative_count:
        ticker_emoji = "🟢"
        dominant_sentiment = "Bullish"
    elif negative_count > positive_count:
        ticker_emoji = "🔴"
        dominant_sentiment = "Bearish"
    else:
        ticker_emoji = "⚪"
        dominant_sentiment = "Mixed"
    
    articles_html = ""
    for article in articles:
        articles_html += generate_article_card_html(article)
    
    return f"""
        <div class="ticker-section">
            <div class="ticker-header">
                <div class="ticker-title">
                    <span class="ticker-emoji">{ticker_emoji}</span>
                    <span class="company-name">{company_name}</span>
                    <span class="ticker-symbol">({ticker})</span>
                </div>
                <div class="ticker-summary">
                    <strong>{dominant_sentiment}</strong><br>
                    {len(articles)} alerts<br>
                    {positive_count}↗ {negative_count}↘ {neutral_count}➖
                </div>
            </div>
            <div class="articles-grid">
                {articles_html}
            </div>
        </div>
        <div class="section-divider"></div>"""

def generate_sector_header_html(sector):
    return f"""
        <div class="sector-header">
            <h2 class="sector-title">{sector}</h2>
        </div>"""

def load_email_template():
    template_path = os.path.join(os.path.dirname(__file__), '..', '..', 'templates', 'email.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()

def populate_email_template(html_template, ticker_sections_html, stats):
    # Generate email timestamp and inject dynamic content
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    css_styles = load_css_styles()
    
    # Replace template placeholders with actual data
    html_content = html_template.replace("{{EMAIL_STYLES}}", css_styles)
    html_content = html_content.replace("{{TIMESTAMP}}", current_time)
    html_content = html_content.replace("{{POSITIVE_COUNT}}", str(stats['positive']))
    html_content = html_content.replace("{{NEGATIVE_COUNT}}", str(stats['negative']))
    html_content = html_content.replace("{{TOTAL_COUNT}}", str(stats['total']))
    html_content = html_content.replace("{{STOCK_COUNT}}", str(stats['stocks']))
    html_content = html_content.replace("{{TICKER_SECTIONS}}", ticker_sections_html)
    
    return html_content
