import smtplib
from email.message import EmailMessage
import pywhatkit
from Backend.Chatbot import env_vars

def send_email(to, subject, body):
    """Sends an email using Gmail SMTP."""
    email_user = env_vars.get("EMAIL_USER")
    email_pass = env_vars.get("EMAIL_PASS")
    
    if not email_user or not email_pass:
        return "❌ Email credentials missing in .env (EMAIL_USER, EMAIL_PASS)."
    
    try:
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = email_user
        msg['To'] = to

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
            
        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Email Error: {str(e)}"

def send_whatsapp(number, message):
    """Sends a WhatsApp message immediately."""
    try:
        # Note: pywhatkit.sendwhatmsg_instantly opens a browser tab
        pywhatkit.sendwhatmsg_instantly(f"+{number}", message, wait_time=15, tab_close=True)
        return "✅ WhatsApp sent successfully!"
    except Exception as e:
        return f"❌ WhatsApp Error: {str(e)}"
