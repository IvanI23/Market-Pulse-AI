import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
from dotenv import load_dotenv
from app.main import run_pipeline, show_current_status
from app.alert import generate_html_alert
from app.db import get_all_users

load_dotenv()

def pipeline():
    try:
        run_pipeline(reset_db=False)
            
        smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        smtp_port = int(os.getenv('SMTP_PORT', '587'))
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        
        if not sender_email or not sender_password:
            print("Email credentials not configured")
            return False

        users = get_all_users()
        success_count = 0
        for user in users:
            try:
                user_email = user['email']
                user_tickers = json.loads(user['tickers']) if user['tickers'] else []
                
                message = MIMEMultipart()
                message["From"] = f"Market Pulse AI <{sender_email}>"
                message["To"] = user_email
                message["Subject"] = "Market Pulse AI - Daily Alert"
                
                html_content = generate_html_alert()
                message.attach(MIMEText(html_content, "html"))
                
                with smtplib.SMTP(smtp_server, smtp_port) as server:
                    server.starttls()
                    server.login(sender_email, sender_password)
                    server.send_message(message)
                
                success_count += 1
                print(f"Alert sent to {user_email}")
                
            except Exception as e:
                print(f"Failed to send alert to {user.get('email', 'unknown')}: {e}")
        
        print(f"Pipeline completed. Sent {success_count} alerts out of {len(users)} users")
        return True
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        return False

if __name__ == '__main__':
    pipeline()
