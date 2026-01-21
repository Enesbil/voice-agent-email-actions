"""
Voice Agent Email Actions — FastAPI Backend
Enables voice AI agents to send emails during and after calls.

Run: uvicorn main:app --reload --port 8000
"""

import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
COMPANY_NAME = os.getenv("COMPANY_NAME", "Boca Raton Health Insurers")

BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"

app = FastAPI(title="Voice Agent Email Actions", version="1.0.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def load_template(name: str) -> str:
    """Load an HTML template from the templates directory."""
    template_path = TEMPLATES_DIR / name
    return template_path.read_text(encoding="utf-8")


def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Send an HTML email via Gmail SMTP."""
    if not GMAIL_USER or not GMAIL_APP_PASSWORD:
        print("ERROR: Missing Gmail credentials in .env")
        return False
    
    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = GMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(html_content, "html"))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_USER, to_email, msg.as_string())
        
        print(f"Email sent: {to_email} — {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def extract_tool_call_args(payload: dict) -> Optional[dict]:
    """Extract function arguments from Vapi's tool call payload."""
    try:
        message = payload.get("message", {})
        tool_calls = message.get("toolCalls") or message.get("toolCallList") or []
        
        if tool_calls:
            args = tool_calls[0].get("function", {}).get("arguments", {})
            return json.loads(args) if isinstance(args, str) else args
    except Exception as e:
        print(f"Parse error: {e}")
    
    return None


def extract_email_from_text(text: str) -> Optional[str]:
    """Find email address in text using regex."""
    if not text:
        return None
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else None


@app.get("/", response_class=HTMLResponse)
async def landing_page():
    """Serve the landing page."""
    return load_template("index.html")


@app.post("/send-specific-email")
async def send_specific_email(request: Request):
    """
    Mid-call tool endpoint.
    Vapi calls this when the user requests documents or information.
    """
    try:
        payload = await request.json()
    except:
        return {"success": False, "message": "Invalid JSON"}
    
    print(f"POST /send-specific-email")
    
    args = extract_tool_call_args(payload) or payload
    
    user_email = args.get("user_email")
    user_name = args.get("user_name", "there")
    topic = args.get("topic", "your request")
    
    if not user_email:
        return {"success": False, "message": "No email provided"}
    
    subject = f"Your {topic} — {COMPANY_NAME}"
    
    html_content = load_template("info_email.html").format(
        company_name=COMPANY_NAME,
        user_name=user_name,
        topic=topic
    )
    
    if send_email(user_email, subject, html_content):
        return {"success": True, "message": f"Email sent to {user_email}"}
    return {"success": False, "message": "Failed to send email"}


@app.post("/vapi-webhook")
async def vapi_webhook(request: Request):
    """
    Post-call webhook endpoint.
    Vapi calls this when a call ends, triggering a follow-up email.
    """
    try:
        payload = await request.json()
    except:
        return {"success": False, "message": "Invalid JSON"}
    
    print(f"POST /vapi-webhook")
    
    message_data = payload.get("message", {})
    msg_type = message_data.get("type") or payload.get("type")
    
    if msg_type != "end-of-call-report":
        return {"success": True, "message": f"Ignored: {msg_type}"}
    
    user_email = None
    
    for source in [
        message_data.get("customer", {}),
        payload.get("customer", {}),
        message_data.get("call", {}).get("customer", {}),
    ]:
        if source and source.get("email"):
            user_email = source["email"]
            break
    
    if not user_email:
        transcript = message_data.get("transcript") or payload.get("transcript", "")
        user_email = extract_email_from_text(transcript)
    
    if not user_email:
        user_email = extract_email_from_text(json.dumps(payload))
    
    if not user_email:
        print("No email found in payload")
        return {"success": False, "message": "No email found"}
    
    print(f"Found email: {user_email}")
    
    subject = f"Your Next Steps — {COMPANY_NAME}"
    
    html_content = load_template("followup_email.html").format(
        company_name=COMPANY_NAME
    )
    
    if send_email(user_email, subject, html_content):
        return {"success": True, "message": f"Follow-up sent to {user_email}"}
    return {"success": False, "message": "Failed to send email"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
