
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import get_settings


settings = get_settings()


def send_admin_notification(inquiry_data: dict):
    sender_email = settings.SMTP_SENDER_EMAIL
    receiver_email = settings.ADMIN_EMAIL
    subject = f"New Inquiry from {inquiry_data['full_name']}"

    body = f"""
    A new contact inquiry has been submitted.

    Full Name: {inquiry_data['full_name']}
    Email: {inquiry_data['email']}
    Company: {inquiry_data.get('company')}
    Phone: {inquiry_data.get('phone')}
    Organization Type: {inquiry_data.get('organization_type')}
    Primary Interest: {inquiry_data.get('primary_interest')}
    Subject: {inquiry_data['subject']}
    Message:
    {inquiry_data['message']}
    """

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
            server.sendmail(sender_email, receiver_email, msg.as_string())
    except Exception as e:
        import traceback

        traceback.print_exc()
        print(f"Email sending failed: {e}")