from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import traceback
from app.core.config import get_settings
from enum import Enum


def send_inquiry_emails(inquiry: dict):

    settings = get_settings()

    sender_email = settings.SMTP_SENDER_EMAIL
    admin_email = settings.ADMIN_EMAIL

    def _safe(val, fallback="Not provided"):
        if isinstance(val, Enum):
            return val.value
        return val if val else fallback

    # Extract and clean values
    name = _safe(inquiry.get("full_name"))
    email = _safe(inquiry.get("email"))
    company = _safe(inquiry.get("company"))
    subject = _safe(inquiry.get("subject"))
    message = _safe(inquiry.get("message")).replace("\n", "<br>")

    # HTML for Admin
    admin_html = f"""\
<!DOCTYPE html>
<html>
<head><meta charset='utf-8'><title>New Contact Form Submission</title></head>
<body style='font-family: Arial, sans-serif; background-color: #f4f7f5; margin: 0; padding: 20px;'>
    <div style='max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);'>
        <div style='background: linear-gradient(135deg, #2d5a27 0%, #4a7c59 100%); padding: 20px; border-radius: 8px 8px 0 0;'>
            <h2 style='color: white; margin: 0;'>New Contact Form Submission</h2>
        </div>
        <div style='padding: 30px;'>
            <table style='width: 100%; border-collapse: collapse;'>
                <tr><td style='padding: 10px 0; font-weight: bold; color: #2d5a27;'>Name:</td><td style='padding: 10px 0;'>{name}</td></tr>
                <tr><td style='padding: 10px 0; font-weight: bold; color: #2d5a27;'>Email:</td><td style='padding: 10px 0;'>{email}</td></tr>
                <tr><td style='padding: 10px 0; font-weight: bold; color: #2d5a27;'>Company:</td><td style='padding: 10px 0;'>{company}</td></tr>
                <tr><td style='padding: 10px 0; font-weight: bold; color: #2d5a27;'>Subject:</td><td style='padding: 10px 0;'>{subject}</td></tr>
            </table>
            <div style='margin-top: 20px;'>
                <h3 style='color: #2d5a27;'>Message:</h3>
                <div style='background-color: #f9f9f9; padding: 15px; border-radius: 5px; border-left: 4px solid #4a7c59;'>{message}</div>
            </div>
        </div>
    </div>
</body>
</html>"""

    # HTML for User
    user_html = f"""\
<!DOCTYPE html>
<html>
<head><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Thank you for contacting EngreenQuest</title></head>
<body style='margin: 0; padding: 0; font-family: Arial, sans-serif; background-color: #f4f7f5;'>
<div style='max-width: 600px; margin: 0 auto; background-color: white; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
    <div style='background: linear-gradient(135deg, #2d5a27 0%, #4a7c59 100%); padding: 40px 20px; text-align: center;'>
        <h1 style='color: white; margin: 0; font-size: 28px; font-weight: bold;'>EngreenQuest</h1>
        <p style='color: #e8f5e8; margin: 10px 0 0 0; font-size: 16px;'>Sustainable Energy Solutions</p>
    </div>
    <div style='padding: 40px 30px;'>
        <h2 style='color: #2d5a27; margin: 0 0 20px 0;'>Thank you, {name}!</h2>
        <p style='color: #444; line-height: 1.6;'>We've received your inquiry regarding <strong style='color: #2d5a27;'>{subject}</strong> and appreciate your interest in sustainable energy solutions.</p>
        <div style='background-color: #f0f8f0; border-left: 4px solid #4a7c59; padding: 20px; margin: 25px 0;'>
            <p style='color: #2d5a27; font-weight: bold;'>What happens next?</p>
            <ul style='color: #444; padding-left: 20px;'>
                <li>Our team will review your message within 24 hours</li>
                <li>We'll prepare a personalized response based on your needs</li>
                <li>You'll hear back from us with next steps and solutions</li>
            </ul>
        </div>
        <p style='color: #444; line-height: 1.6;'>At EngreenQuest, we're committed to helping organizations transition to clean, renewable energy. Whether you're interested in solar installations, battery storage, or energy efficiency consulting, we have the expertise to guide your green transformation.</p>
        <div style='text-align: center; margin: 30px 0;'>
            <a href='https://engreenquest.com' style='background: linear-gradient(135deg, #2d5a27 0%, #4a7c59 100%); color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: bold;'>Visit Our Website</a>
        </div>
    </div>
    <div style='background-color: #2d5a27; padding: 30px 20px; text-align: center;'>
        <p style='color: #e8f5e8; font-size: 14px;'>EngreenQuest | Sustainable Energy Solutions</p>
        <p style='color: #a8c8a8; font-size: 12px;'>© 2025 EngreenQuest. All rights reserved.</p>
    </div>
</div>
</body>
</html>"""

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)

            # Send to Admin
            admin_msg = MIMEMultipart("alternative")
            admin_msg["From"] = sender_email
            admin_msg["To"] = admin_email
            admin_msg["Subject"] = f"New Inquiry from {name}"
            admin_msg.attach(MIMEText(admin_html, "html", "utf-8"))
            server.sendmail(sender_email, admin_email, admin_msg.as_string())

            # Send to User
            user_msg = MIMEMultipart("alternative")
            user_msg["From"] = sender_email
            user_msg["To"] = email
            user_msg["Subject"] = "Thank you for contacting EngreenQuest"
            user_msg.attach(MIMEText(user_html, "html", "utf-8"))
            server.sendmail(sender_email, email, user_msg.as_string())

    except Exception:
        traceback.print_exc()
