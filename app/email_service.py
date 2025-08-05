import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
from dotenv import load_dotenv

load_dotenv()

def send_welcome_email(user_email, selected_tickers):
    try:
        # Email configuration
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            print("Email credentials not configured")
            return False
        
        # Create message
        message = MIMEMultipart()
        message["From"] = f"Market Pulse AI <{sender_email}>"
        message["To"] = user_email
        message["Subject"] = "Welcome to Market Pulse AI! 🚀"
        
        # Render email template
        html_body = render_template('welcome_email.html', 
                                  tickers=selected_tickers,
                                  tickers_list=", ".join(selected_tickers))
        
        message.attach(MIMEText(html_body, "html"))
        
        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"✅ Welcome email sent to {user_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send welcome email: {e}")
        return False
