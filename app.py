from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__)
CORS(app)

@app.route('/api/submit-form', methods=['POST'])
def submit_form():
    try:
        data = request.json
        
        # Email configuration
        sender_email = "techtrans427@gmail.com"
        app_password = "qjmr ufoe jyyn unei"  # Consider using environment variables
        receiver_email = "techtrans427@gmail.com"
        
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

# Add this for Vercel
@app.route('/')
def home():
    return jsonify({"status": "alive", "message": "Server is running"})

# Add CORS preflight response
@app.route('/api/submit-form', methods=['OPTIONS'])
def handle_options():
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 