from flask import Flask, render_template, request, redirect, url_for, flash
import os
from dotenv import load_dotenv
from app.db import init_users_table, add_user, remove_user
from app.email_service import send_welcome_email

load_dotenv()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = os.getenv('SECRET_KEY', 'default-secret-key')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        selected_tickers = request.form.getlist('tickers')
        
        if not email:
            flash('Email is required', 'error')
            return redirect(url_for('index'))
        
        if not selected_tickers:
            flash('Please select at least one ticker', 'error')
            return redirect(url_for('index'))
        
        user_id = add_user(email, selected_tickers)
        
        if user_id:
            email_sent = send_welcome_email(email, selected_tickers)
            
            if email_sent:
                message = 'Successfully signed up! Welcome email sent. You will receive alerts for your selected tickers.'
            else:
                message = 'Successfully signed up! You will receive alerts for your selected tickers. (Welcome email failed to send - please check your email settings)'
            
            return render_template('signup.html', 
                                 show_modal=True,
                                 message=message, 
                                 tickers_list=", ".join(selected_tickers))
        else:
            flash('Email already exists', 'error')
            return redirect(url_for('index'))
    
    return render_template('signup.html')

@app.route('/unsubscribe')
def unsubscribe_form():
    return render_template('unsubscribe.html')

@app.route('/unsubscribe', methods=['POST'])
def unsubscribe():
    email = request.form.get('email', '').strip()
    
    if not email:
        flash('Email is required', 'error')
        return redirect(url_for('unsubscribe_form'))
    
    success = remove_user(email)
    
    if success:
        message = 'You have been successfully unsubscribed from all Market Pulse AI alerts.'
        return render_template('unsubscribe.html', 
                             show_modal=True,
                             message=message)
    else:
        flash('Email not found in our database', 'error')
        return redirect(url_for('unsubscribe_form'))

if __name__ == '__main__':
    init_users_table()
    app.run(debug=True, port=5000)
