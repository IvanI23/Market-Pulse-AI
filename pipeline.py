import os
from dotenv import load_dotenv
from app.core.main import run_pipeline, show_current_status
from app.alerts.alert import generate_html_alert
from app.services.email_service import send_alert_email

# Load environment variables from .env file
load_dotenv()

def pipeline():
    try:
        # Run the complete market analysis pipeline
        run_pipeline(reset_db=False)
        my_email = os.getenv('MY_EMAIL')
        
        if not my_email:
            print("Personal email not configured. Please set MY_EMAIL in .env file")
            return False

        # Generate HTML alert content and send email
        html_content = generate_html_alert()
        success = send_alert_email(my_email, html_content, "Market Pulse AI - Daily Alert")
        
        if success:
            print("Pipeline completed successfully!")
            return True
        else:
            print("Pipeline completed but email failed to send")
            return False
        
    except Exception as e:
        print(f"Pipeline failed: {e}")
        return False

if __name__ == '__main__':
    pipeline()
