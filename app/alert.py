from . import db
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'sql', 'market_pulse.db')

def fetch_positive_stocks():
    query = """SELECT b.*, a.headline, a.published_at FROM news_articles a
                JOIN sentiment_price_effect b ON a.id = b.news_id
                WHERE (b.score > 0.8) AND b.label = 'positive'
                ORDER BY b.score DESC"""

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_negative_stocks():
    query = """SELECT b.*, a.headline, a.published_at FROM news_articles a
                JOIN sentiment_price_effect b ON a.id = b.news_id
                WHERE (b.score > 0.8) AND b.label = 'negative'
                ORDER BY b.score DESC"""

    conn = sqlite3.connect(db.DB_PATH)
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

def generate_stock_card_html(stock, sentiment_type):
    ticker = stock[2]
    score = stock[3]
    price_before = stock[5]
    price_after = stock[6]
    price_change = stock[7]
    headline = stock[-2]
    
    card_class = "positive-card" if sentiment_type == "positive" else "negative-card"
    badge_class = "positive-badge" if sentiment_type == "positive" else "negative-badge"
    price_color = "#27ae60" if sentiment_type == "positive" else "#e74c3c"
    
    return f"""
            <div class="stock-card {card_class}">
                <div class="stock-header">
                    <div class="ticker">{ticker}</div>
                    <div class="score-badge {badge_class}">Score: {score:.2f}</div>
                </div>
                <div class="price-movement">
                    <span>${price_before:.2f}</span>
                    <span class="price-arrow">→</span>
                    <span>${price_after:.2f}</span>
                    <span style="color: {price_color}; margin-left: 10px;">({price_change:+.2f}%)</span>
                </div>
                <div class="headline">
                    "{headline}"
                </div>
            </div>"""

def generate_html_alert():
    positive_stocks = fetch_positive_stocks()
    negative_stocks = fetch_negative_stocks()

    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'alert_email.html')
    with open(template_path, 'r', encoding='utf-8') as f:
        html_template = f.read()
    
    # Generate positive alerts HTML
    positive_html = ""
    if positive_stocks:
        for stock in positive_stocks:
            positive_html += generate_stock_card_html(stock, "positive")
    else:
        positive_html = '<div class="no-alerts">No strong positive sentiment alerts found.</div>'
    
    # Generate negative alerts HTML
    negative_html = ""
    if negative_stocks:
        for stock in negative_stocks:
            negative_html += generate_stock_card_html(stock, "negative")
    else:
        negative_html = '<div class="no-alerts">No strong negative sentiment alerts found.</div>'
    
    # Replace placeholders in template
    current_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    html_content = html_template.replace("{{TIMESTAMP}}", current_time)
    html_content = html_content.replace("{{POSITIVE_COUNT}}", str(len(positive_stocks)))
    html_content = html_content.replace("{{NEGATIVE_COUNT}}", str(len(negative_stocks)))
    html_content = html_content.replace("{{TOTAL_COUNT}}", str(len(positive_stocks) + len(negative_stocks)))
    html_content = html_content.replace("{{POSITIVE_ALERTS}}", positive_html)
    html_content = html_content.replace("{{NEGATIVE_ALERTS}}", negative_html)
    
    return html_content

def save_html_alert():
    html_content = generate_html_alert()
    
    # Save to file
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'data')
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"market_alert_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"📧 Beautiful HTML alert generated!")
    print(f"📁 Saved to: {filepath}")
    print(f"🌐 Open in browser or attach to email")
    
    return filepath

# Generate the HTML alert
if __name__ == "__main__":
    save_html_alert()