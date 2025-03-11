# email_service.py
import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import datetime
import uuid
from database import get_user_by_email, _container

# Email configuration
EMAIL_HOST = os.environ.get("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USER = os.environ.get("EMAIL_USER", "support.gradeguard@gmail.com")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD", "")  # Set in environment variables
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "GradeGuard <support.gradeguard@gmail.com>")
SITE_URL = os.environ.get("SITE_URL", "https://sarveshmina.co.uk/GradeGuard")

# Token validity (in seconds)
PASSWORD_RESET_TOKEN_VALIDITY = 86400  # 24 hours

def send_email(to_email, subject, html_content, text_content=None):
    """Send an email using the configured SMTP settings"""
    if not EMAIL_PASSWORD:
        logging.warning("EMAIL_PASSWORD not set. Email not sent.")
        return False
    
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = DEFAULT_FROM_EMAIL
    message["To"] = to_email
    
    # Create plain text version if not provided
    if not text_content:
        text_content = html_content.replace('<br>', '\n').replace('<p>', '\n').replace('</p>', '\n')
        # Remove other HTML tags
        import re
        text_content = re.sub(r'<[^>]*>', '', text_content)
    
    part1 = MIMEText(text_content, "plain")
    part2 = MIMEText(html_content, "html")
    
    message.attach(part1)
    message.attach(part2)
    
    try:
        context = ssl.create_default_context()
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls(context=context)
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, message.as_string())
        logging.info(f"Email sent to {to_email}")
        return True
    except Exception as e:
        logging.error(f"Error sending email: {str(e)}")
        return False

def send_welcome_email(user_email, first_name):
    """Send a welcome email to a newly registered user"""
    subject = "Welcome to GradeGuard!"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h1 style="color: #4f46e5;">Welcome to GradeGuard!</h1>
        <p>Hello {first_name},</p>
        <p>Thank you for registering with GradeGuard! We're excited to have you on board.</p>
        <p>GradeGuard helps you track your academic progress, calculate your grades, and stay on top of your educational journey.</p>
        <p>Here are some things you can do with your new account:</p>
        <ul>
            <li>Track your modules and assignments</li>
            <li>Calculate your potential final grades</li>
            <li>Set goals and monitor your progress</li>
            <li>Get insights into your academic performance</li>
        </ul>
        <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
        <p>Best regards,<br>The GradeGuard Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)

def send_login_notification(user_email, first_name, ip_address, device_info, location=None):
    """Send a notification when a user logs in from a new device"""
    subject = "New Login Detected - GradeGuard Account"
    
    location_str = f" from {location}" if location else ""
    login_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h1 style="color: #4f46e5;">New Login Alert</h1>
        <p>Hello {first_name},</p>
        <p>We detected a new login to your GradeGuard account{location_str}.</p>
        <p><strong>Details:</strong></p>
        <ul>
            <li><strong>Time:</strong> {login_time}</li>
            <li><strong>IP Address:</strong> {ip_address}</li>
            <li><strong>Device:</strong> {device_info}</li>
        </ul>
        <p>If this was you, you can ignore this email. If you didn't log in recently, please secure your account by:</p>
        <ol>
            <li>Changing your password immediately</li>
            <li>Contacting our support team</li>
        </ol>
        <p>Best regards,<br>The GradeGuard Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)

def send_password_changed_email(user_email, first_name):
    """Send notification when a user changes their password"""
    subject = "Password Changed - GradeGuard Account"
    
    change_time = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h1 style="color: #4f46e5;">Password Changed</h1>
        <p>Hello {first_name},</p>
        <p>Your GradeGuard account password was successfully changed at {change_time}.</p>
        <p>If you did not make this change, please contact our support team immediately.</p>
        <p>Best regards,<br>The GradeGuard Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)

def generate_password_reset_token(user_email):
    """Generate a password reset token and store it in the database"""
    # Check if user exists
    user_doc = get_user_by_email(user_email)
    if not user_doc:
        return None
    
    # Generate token
    token = uuid.uuid4().hex
    
    # Create or update reset token document
    token_doc = {
        "id": f"reset:{token}",
        "type": "reset_token",
        "email": user_email,
        "created": datetime.datetime.utcnow().isoformat(),
        "expires": (datetime.datetime.utcnow() + datetime.timedelta(seconds=PASSWORD_RESET_TOKEN_VALIDITY)).isoformat(),
        "used": False
    }
    
    try:
        _container.upsert_item(token_doc)
        return token
    except Exception as e:
        logging.error(f"Error creating reset token: {str(e)}")
        return None

def verify_reset_token(token):
    """Verify if a password reset token is valid"""
    try:
        token_doc = _container.read_item(item=f"reset:{token}", partition_key=f"reset:{token}")
        
        # Check if token is already used
        if token_doc.get("used", False):
            return None
        
        # Check if token is expired
        expiry = datetime.datetime.fromisoformat(token_doc["expires"])
        if datetime.datetime.utcnow() > expiry:
            return None
        
        return token_doc["email"]
    except Exception:
        return None

def invalidate_reset_token(token):
    """Mark a password reset token as used"""
    try:
        token_doc = _container.read_item(item=f"reset:{token}", partition_key=f"reset:{token}")
        token_doc["used"] = True
        _container.upsert_item(token_doc)
        return True
    except Exception:
        return False

def send_password_reset_email(user_email):
    """Send password reset link to user"""
    user_doc = get_user_by_email(user_email)
    if not user_doc:
        return False
    
    first_name = user_doc.get("firstName", "User")
    
    # Generate reset token
    token = generate_password_reset_token(user_email)
    if not token:
        return False
    
    # Create reset link
    reset_link = f"{SITE_URL}/reset-password?token={token}"
    
    subject = "Password Reset - GradeGuard Account"
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h1 style="color: #4f46e5;">Password Reset Request</h1>
        <p>Hello {first_name},</p>
        <p>We received a request to reset your password for your GradeGuard account.</p>
        <p>To reset your password, please click the link below:</p>
        <p><a href="{reset_link}" style="display: inline-block; background-color: #4f46e5; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
        <p>This link will expire in 24 hours.</p>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Best regards,<br>The GradeGuard Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)

def send_reminder_email(user_email, event_title, event_date, event_time=None):
    """Send a reminder email for an upcoming event or deadline"""
    user_doc = get_user_by_email(user_email)
    if not user_doc:
        return False
    
    first_name = user_doc.get("firstName", "User")
    
    subject = f"Reminder: {event_title} - GradeGuard"
    
    time_str = f" at {event_time}" if event_time else ""
    
    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #e0e0e0; border-radius: 5px;">
        <h1 style="color: #4f46e5;">Event Reminder</h1>
        <p>Hello {first_name},</p>
        <p>This is a reminder about your upcoming event:</p>
        <div style="background-color: #f9f9f9; padding: 15px; border-left: 4px solid #4f46e5; margin: 15px 0;">
            <h2 style="margin-top: 0;">{event_title}</h2>
            <p><strong>Date:</strong> {event_date}{time_str}</p>
        </div>
        <p>Log in to your GradeGuard account to view more details.</p>
        <p>Best regards,<br>The GradeGuard Team</p>
    </div>
    """
    
    return send_email(user_email, subject, html_content)