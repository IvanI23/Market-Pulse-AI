import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables for email configuration
load_dotenv()

def send_alert_email(recipient_email, html_content, subject="Market Pulse AI - Daily Alert"):
    try:
        # Get SMTP configuration from environment
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            print("Email credentials not configured")
            return False
        
        # Create email message with HTML content
        message = MIMEMultipart()
        message["From"] = f"Market Pulse AI <{sender_email}>"
        message["To"] = recipient_email
        message["Subject"] = subject
        
        message.attach(MIMEText(html_content, "html"))
        
        # Send email via SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
        
        print(f"✅ Alert email sent to {recipient_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send alert email: {e}")
        return False
