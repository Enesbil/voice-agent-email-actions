# Voice Agent Email Integration (FastAPI + Vapi)

Real-time webhook handler that enables AI Voice Agents to dispatch emails mid-call.

[**Watch the 60s Demo**](YOUR_LOOM_LINK_HERE)

---

## The Problem

Voice AI agents are great at talking, but bad at doing. Most agents can't trigger external actions (like sending a quote or calendar invite) without breaking the conversation flow.

## The Solution

I built a custom FastAPI backend that serves as a middleware between the Vapi Voice Agent and SMTP email servers.

- **Zero Latency** - Handles the webhook asynchronously so the voice agent doesn't pause
- **Context Aware** - Extracts specific data (Name, Email, Topic) from the conversation payload
- **Reliable** - Uses Pydantic for strict data validation before attempting delivery

## Tech Stack

| Layer | Technology |
|-------|------------|
| Core | Python, FastAPI |
| Voice | Vapi.ai (Webhooks) |
| Infrastructure | Ngrok (Dev), SMTP (Email) |

---

## Features

- **Mid-Call Email Actions** - Send quotes, documents, or information while the voice agent is on a call
- **Post-Call Webhooks** - Automatically trigger follow-up emails when calls end
- **Smart Email Extraction** - Finds user email from customer data, transcripts, or conversation context
- **HTML Email Templates** - Professional, responsive templates with dynamic content

## Quick Start

```bash
# Clone and install
git clone https://github.com/yourusername/voice-agent-email-actions.git
cd voice-agent-email-actions
pip install -r requirements.txt

# Configure environment
# Create .env with your Gmail credentials

# Run
uvicorn main:app --reload --port 8000
```

Visit http://localhost:8000 to see the API landing page, or http://localhost:8000/docs for interactive API documentation.

## Configuration

Create a `.env` file:

```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
COMPANY_NAME=Your Company Name
```

Note: Gmail requires an App Password (https://myaccount.google.com/apppasswords). Regular passwords will not work with SMTP.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /send-specific-email | Mid-call tool - sends info email on request |
| POST | /vapi-webhook | Post-call webhook - sends follow-up email |
| GET | /health | Health check |
| GET | / | Landing page |

### Mid-Call Tool Parameters

```json
{
  "user_email": "user@example.com",
  "user_name": "John",
  "topic": "insurance quote"
}
```

## Vapi Integration

### 1. Add the Mid-Call Tool

In your Vapi assistant, create a Server URL tool:

- Name: sendInfoEmail
- URL: https://your-server.com/send-specific-email
- Parameters:
  - user_email (string, required)
  - user_name (string, optional)
  - topic (string, optional)

### 2. Configure the Webhook

In your Vapi assistant settings, set the Server URL to:

```
https://your-server.com/vapi-webhook
```

Enable "end-of-call-report" messages.

## Local Development with ngrok

```bash
# Terminal 1: Run the server
uvicorn main:app --reload --port 8000

# Terminal 2: Expose to internet
ngrok http 8000
```

Use the ngrok URL in your Vapi configuration.

## Project Structure

```
voice-agent-email-actions/
  main.py                   # FastAPI application
  requirements.txt          # Dependencies
  templates/
    index.html              # Landing page
    info_email.html         # Mid-call email template
    followup_email.html     # Post-call email template
  static/
    styles.css              # Landing page styles
```

## Customization

Edit the HTML templates in /templates to match your brand. Templates use simple {variable} placeholders for dynamic content.

## Tech Stack

- FastAPI - Modern Python web framework
- Vapi.ai - Voice AI platform integration
- Gmail SMTP - Email delivery

## License

MIT
