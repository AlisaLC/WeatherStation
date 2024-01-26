from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

load_dotenv()

app = Flask(__name__)

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USE_TLS = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'
SMTP_USERNAME = os.getenv('SMTP_USERNAME', 'your_email@example.com')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', 'your_email_password')

def send_email(recipient_email, subject, body, attachments=None):
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USERNAME
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        if attachments:
            for attachment_path in attachments:
                with open(attachment_path, 'rb') as file:
                    part = MIMEApplication(file.read(), Name=os.path.basename(attachment_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                    msg.attach(part)
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, recipient_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/email', methods=['POST'])
def send_email_route():
    try:
        data = request.json
        recipient_email = data.get('recipient')
        subject = data.get('subject')
        body = data.get('body')
        attachments = data.get('attachments', [])
        if not (recipient_email and subject and body):
            return jsonify({'error': 'Missing required fields'}), 400
        success = send_email(recipient_email, subject, body, attachments)
        if success:
            return jsonify({'message': 'Email sent successfully'}), 200
        else:
            return jsonify({'error': 'Failed to send email'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)