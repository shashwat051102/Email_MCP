import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from email.header import decode_header
import imaplib
import email
import re

load_dotenv()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Create the FastMCP server instance
mcp = FastMCP("EmailServer")

@mcp.tool()
def send_email(recipient_email: str, subject: str, body: str) -> str:
    """Send an email using SMTP.
    
    Args:
        recipient_email (str): The email address of the recipient
        subject (str): The subject of the email
        body (str): The body content of the email
        
    Returns:
        str: Success message or error details
    """
    # Get credentials
    email_sender = os.getenv('EMAIL_ADDRESS')
    email_password = os.getenv('EMAIL_PASSWORD')

    # Input validation
    if not email_sender or not email_password:
         return "Error: EMAIL_ADDRESS or EMAIL_PASSWORD environment variables not set."

    if not all([recipient_email, subject, body]):
        return "Error: All fields (recipient_email, subject, body) are required"
        
    if not validate_email(recipient_email):
        return "Error: Invalid recipient email format"
        
    if not validate_email(email_sender):
        return "Error: Invalid sender email format in configuration"

    # Create message
    msg = MIMEMultipart()
    msg["From"] = email_sender
    msg["To"] = recipient_email
    msg["Subject"] = subject
    
    msg.attach(MIMEText(body, "html"))
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(email_sender, email_password)
            server.sendmail(email_sender, recipient_email, msg.as_string())
        return "Email sent successfully"
    except smtplib.SMTPAuthenticationError:
        return "Error: Authentication failed. Please check your email credentials"
    except smtplib.SMTPException as e:
        return f"Error: SMTP error occurred: {str(e)}"
    except Exception as e:
        return f"Error: Failed to send email: {str(e)}"
    
@mcp.tool()
def list_recent_emails(limit=5) -> str:
    imap_server = 'imap.gmail.com'
    email_user = os.getenv('EMAIL_ADDRESS')
    email_pass = os.getenv('EMAIL_PASSWORD')
    
    with imaplib.IMAP4_SSL(imap_server) as imap:
        imap.login(email_user, email_pass)
        imap.select('inbox')
        status, messages = imap.search(None, 'ALL')
        email_ids = messages[0].split()
        if not email_ids:
            return "No emails found."

        preview = []
        for i in range(1, limit + 1):
            if i > len(email_ids):
                break
            eid = email_ids[-i]
            _, msg_data = imap.fetch(eid, '(BODY.PEEK[HEADER])')
            msg = email.message_from_bytes(msg_data[0][1])
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding or "utf-8", errors="ignore")
            sender = msg.get("From")
            preview.append(f"{i}. {subject} | From: {sender}")
        
        return "\n".join(preview)

# Optional for manual runs
if __name__ == "__main__":
    mcp.run()