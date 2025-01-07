from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        
        # Email configuration
        sender_email = os.getenv("SENDER_EMAIL")
        app_password = os.getenv("APP_PASSWORD")
        receiver_email = "techtrans427@gmail.com"
        
        if not sender_email or not app_password:
            return jsonify({"status": "error", "message": "Server email configuration is missing."}), 500
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = f"New Service Inquiry from {data['name']}"
        
        body = f"""
        New inquiry received:
        
        Name: {data['name']}
        Email: {data['email']}
        Phone: {data['phone']}
        Service: {data['service']}
        Message: {data.get('message', 'No message provided')}
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            # Create SMTP session
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, app_password)
            
            # Send email
            server.send_message(msg)
            server.quit()
            
            return jsonify({
                "status": "success",
                "message": "Thank you for your inquiry! We will contact you shortly via email."
            })
        except Exception as e:
            print(f"Email error: {str(e)}")
            return jsonify({
                "status": "error",
                "message": "There was an error sending your inquiry. Please try again later."
            }), 500
            
    except Exception as e:
        print(f"Server error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Server error. Please try again later."
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
