# email_notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from decouple import config

sender_email = config("sender_email")
sender_password = config("sender_password")

# Email configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587

def send_email_notification(subject, message, recipient_email):
    try:
        # Create a MIMEText object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach the message
        msg.attach(MIMEText(message, 'plain'))

        # Connect to the SMTP server and send the email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
        print("Email notification sent successfully.")
    except Exception as e:
        print(f"Failed to send email notification: {e}")

def get_subscribed_emails():
    with open('subscribed_emails.txt', 'r') as file:
        return [line.strip() for line in file]