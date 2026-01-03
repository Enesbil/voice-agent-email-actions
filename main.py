"""
Vapi Voice AI Backend - Sends emails during and after calls.

pip install fastapi uvicorn python-dotenv pydantic email-validator
uvicorn main:app --reload --port 8000
"""

import json
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from pydantic import BaseModel

load_dotenv()

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

app = FastAPI(title="Gail AI Backend", version="1.0.0")


# --- Email sender ---

def send_email(to_email: str, subject: str, html_content: str) -> bool:
    """Sends an HTML email via Gmail SMTP. Returns True on success."""
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
        
        print(f"Sent email to {to_email}: {subject}")
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail auth failed - check your app password")
        return False
    except Exception as e:
        print(f"ERROR: Email failed - {e}")
        return False


# --- Vapi payload parser ---

def extract_tool_call_args(payload: dict) -> Optional[dict]:
    """
    Pulls out function arguments from Vapi's nested tool call format.
    Returns None if the payload isn't a tool call.
    """
    try:
        message = payload.get("message", {})
        
        # Vapi uses "toolCalls" or sometimes "toolCallList"
        tool_calls = message.get("toolCalls") or message.get("toolCallList") or []
        
        if tool_calls:
            args = tool_calls[0].get("function", {}).get("arguments", {})
            return json.loads(args) if isinstance(args, str) else args
    except Exception as e:
        print(f"Couldn't parse tool call: {e}")
    
    return None


def extract_email_from_text(text: str) -> Optional[str]:
    """Finds first email address in a string using regex."""
    if not text:
        return None
    match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    return match.group(0) if match else None


# --- Mid-call tool: send info email on request ---

@app.post("/send-specific-email")
async def send_specific_email(request: Request):
    """
    Called by Vapi mid-conversation when user asks for documents.
    Sends insurance terms/info to the user's email.
    """
    try:
        payload = await request.json()
    except:
        return {"success": False, "message": "Bad JSON"}
    
    print(f"POST /send-specific-email: {json.dumps(payload, indent=2)}")
    
    # Try Vapi format first, fall back to direct params
    args = extract_tool_call_args(payload) or payload
    
    user_email = args.get("user_email")
    user_name = args.get("user_name", "there")
    topic = args.get("topic", "your request")
    
    if not user_email:
        return {"success": False, "message": "No email provided"}
    
    subject = f"Your {topic} - Boca Raton Health Insurers"
    
    html_content = f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.7; color: #2d3748; max-width: 650px; margin: 0 auto; padding: 20px;">
        
        <div style="background: linear-gradient(135deg, #0077b6 0%, #00a8e8 100%); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">Boca Raton Health Insurers</h1>
            <p style="color: #caf0f8; margin: 10px 0 0 0; font-size: 14px;">Demo</p>
        </div>
        
        <div style="background: #ffffff; padding: 35px; border: 1px solid #e2e8f0; border-top: none;">
            
            <p style="font-size: 16px;">Hi {user_name},</p>
            
            <p>Thanks for your interest! Here's the info you requested about <strong>{topic}</strong>.</p>
            
            <div style="background: linear-gradient(135deg, #e0f7fa 0%, #f0f9ff 100%); border-left: 4px solid #0077b6; padding: 25px; margin: 25px 0; border-radius: 0 8px 8px 0;">
                <h2 style="color: #0077b6; margin: 0 0 15px 0; font-size: 20px;">Boca Youth+ Insurance Program</h2>
                <p style="margin: 0 0 10px 0;"><strong>Monthly Premium:</strong> <span style="color: #0077b6; font-size: 18px; font-weight: bold;">$200 less</span> than comparable plans</p>
                <p style="margin: 0;"><strong>Enrollment:</strong> Open now</p>
            </div>
            
            <h3 style="color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">Plan Terms</h3>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
                <tr style="background: #f7fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Coverage</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">Comprehensive Health Insurance</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Deductible</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">$500 / $1,000 / $2,500</td>
                </tr>
                <tr style="background: #f7fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Primary Care Copay</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">$20</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Specialist Copay</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">$40</td>
                </tr>
                <tr style="background: #f7fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Rx Coverage</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">$10 / $35 / $70 (Tier 1/2/3)</td>
                </tr>
                <tr>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Out-of-Pocket Max</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">$6,500 individual / $13,000 family</td>
                </tr>
                <tr style="background: #f7fafc;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0;"><strong>Network</strong></td>
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">PPO - 500,000+ providers</td>
                </tr>
            </table>
            
            <h3 style="color: #1a365d; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">What's Included</h3>
            <ul style="padding-left: 20px;">
                <li style="margin-bottom: 8px;">Preventive care at 100%</li>
                <li style="margin-bottom: 8px;">Telehealth visits</li>
                <li style="margin-bottom: 8px;">Mental health support</li>
                <li style="margin-bottom: 8px;">Worldwide ER coverage</li>
                <li style="margin-bottom: 8px;">No specialist referrals needed</li>
                <li style="margin-bottom: 8px;">24/7 nurse hotline</li>
            </ul>
            
            <p>Questions? Just reply to this email or give us a call.</p>
            
            <p style="margin-top: 30px;">
                Best,<br>
                <strong style="color: #0077b6;">Gail</strong><br>
                <span style="color: #718096;">Boca Raton Health Insurers</span>
            </p>
        </div>
        
        <div style="background: #1a365d; padding: 20px; border-radius: 0 0 12px 12px; text-align: center;">
            <p style="color: #a0aec0; margin: 0; font-size: 12px;">
                Boca Raton Health Insurers | 123 Health Plaza, Boca Raton, FL 33432
            </p>
        </div>
        
    </body>
    </html>
    """
    
    if send_email(user_email, subject, html_content):
        return {"success": True, "message": f"Email sent to {user_email}"}
    return {"success": False, "message": "Failed to send email"}


# --- Post-call webhook: sends follow-up email after call ends ---

@app.post("/vapi-webhook")
async def vapi_webhook(request: Request):
    """
    Vapi hits this when calls end. Looks for user email and sends next steps.
    """
    try:
        payload = await request.json()
    except:
        return {"success": False, "message": "Bad JSON"}
    
    print(f"POST /vapi-webhook: {json.dumps(payload, indent=2)}")
    
    # Only care about end-of-call reports
    message_data = payload.get("message", {})
    msg_type = message_data.get("type") or payload.get("type")
    
    if msg_type != "end-of-call-report":
        return {"success": True, "message": f"Ignored: {msg_type}"}
    
    # Hunt for email in various places Vapi might put it
    user_email = None
    
    for path in [
        message_data.get("customer", {}),
        payload.get("customer", {}),
        message_data.get("call", {}).get("customer", {}),
    ]:
        if path and path.get("email"):
            user_email = path["email"]
            break
    
    # Try transcript if customer data didn't have it
    if not user_email:
        transcript = message_data.get("transcript") or payload.get("transcript", "")
        user_email = extract_email_from_text(transcript)
    
    # Last resort: scan the whole payload
    if not user_email:
        user_email = extract_email_from_text(json.dumps(payload))
    
    if not user_email:
        print("No email found in payload")
        return {"success": False, "message": "No email found"}
    
    print(f"Found email: {user_email}")
    
    subject = "Your Next Steps - Boca Raton Health Insurers"
    
    html_content = """
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.7; color: #2d3748; max-width: 650px; margin: 0 auto; padding: 20px;">
        
        <div style="background: linear-gradient(135deg, #0077b6 0%, #00a8e8 100%); padding: 30px; border-radius: 12px 12px 0 0; text-align: center;">
            <h1 style="color: white; margin: 0; font-size: 24px;">Boca Raton Health Insurers</h1>
            <p style="color: #caf0f8; margin: 10px 0 0 0; font-size: 14px;">Demo</p>
        </div>
        
        <div style="background: #ffffff; padding: 35px; border: 1px solid #e2e8f0; border-top: none;">
            
            <h2 style="color: #0077b6; margin-top: 0;">Thanks for chatting with Gail!</h2>
            
            <p>Great talking with you. Here's a quick recap of the <strong>Boca Youth+ Insurance Program</strong> and what to do next.</p>
            
            <div style="background: linear-gradient(135deg, #e0f7fa 0%, #f0f9ff 100%); padding: 25px; margin: 25px 0; border-radius: 12px;">
                <h3 style="color: #0077b6; margin: 0 0 20px 0;">Next Steps</h3>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #1a365d;">1. Review Your Current Policy</strong><br>
                    <span style="color: #4a5568; font-size: 14px;">Check your premium, coverage, and renewal date.</span>
                </div>
                
                <div style="margin-bottom: 15px;">
                    <strong style="color: #1a365d;">2. Compare Options</strong><br>
                    <span style="color: #4a5568; font-size: 14px;">You could save $200/month with Boca Youth+.</span>
                </div>
                
                <div>
                    <strong style="color: #1a365d;">3. Schedule Enrollment</strong><br>
                    <span style="color: #4a5568; font-size: 14px;">Reply to this email or call us to get started.</span>
                </div>
            </div>
            
            <div style="background: #fff5f5; border: 1px solid #fc8181; padding: 20px; border-radius: 8px; margin: 25px 0;">
                <p style="margin: 0; color: #c53030;">
                    <strong>Don't wait!</strong> Lock in your rate before premiums go up.
                </p>
            </div>
            
            <div style="background: #f7fafc; padding: 20px; border-radius: 8px; text-align: center; margin: 25px 0;">
                <p style="margin: 0;"><strong>Questions?</strong> Reply here or call <strong>(561) 555-0123</strong></p>
            </div>
            
            <p style="margin-top: 30px;">
                Best,<br>
                <strong style="color: #0077b6;">Gail</strong><br>
                <span style="color: #718096;">Boca Raton Health Insurers</span>
            </p>
        </div>
        
        <div style="background: #1a365d; padding: 20px; border-radius: 0 0 12px 12px; text-align: center;">
            <p style="color: #a0aec0; margin: 0; font-size: 12px;">
                Boca Raton Health Insurers | 123 Health Plaza, Boca Raton, FL 33432
            </p>
        </div>
        
    </body>
    </html>
    """
    
    if send_email(user_email, subject, html_content):
        return {"success": True, "message": f"Follow-up sent to {user_email}"}
    return {"success": False, "message": "Failed to send email"}


# --- Health checks ---

@app.get("/")
async def root():
    return {"status": "ok", "service": "Gail AI Backend"}

@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
