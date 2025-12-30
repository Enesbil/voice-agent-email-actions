#Voice Agent Email Functionality Backend

FastAPI backend for a Vapi.ai voice agent demo. Sends emails during calls and after calls end.

## What it does

- **Mid-call tool** (`POST /send-specific-email`) - AI triggers this when user asks for documents/quotes
- **Post-call webhook** (`POST /vapi-webhook`) - Vapi calls this when a call ends, sends follow-up email

## Prerequisites for Demo

1. **Vapi.ai account** - You need to set up your voice agent in Vapi first
2. **Gmail App Password (SMTP)** - Regular Gmail password won't work. [Create an App Password](https://myaccount.google.com/apppasswords)
3. **Public URL** - Vapi needs to reach your server (use ngrok for local dev)

## Setup

```bash
# Install deps
pip install fastapi uvicorn python-dotenv pydantic email-validator

# Create .env file
echo "GMAIL_USER=your-email@gmail.com" > .env
echo "GMAIL_APP_PASSWORD=your-16-char-app-password" >> .env

# Run it
uvicorn main:app --reload --port 8000
```

## Vapi Configuration

This backend won't do anything until you wire it up in Vapi:

### 1. Mid-call tool (for sending docs on request)

In your Vapi assistant, add a **Server URL tool**:
- **Name:** `sendInfoEmail`
- **URL:** `https://your-server.com/send-specific-email`
- **Parameters:**
  - `user_email` (string, required)
  - `user_name` (string)
  - `topic` (string)

### 2. Post-call webhook (for follow-up emails)

In your Vapi assistant settings:
- **Server URL:** `https://your-server.com/vapi-webhook`

Make sure "end-of-call-report" messages are enabled.

## Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/send-specific-email` | Mid-call tool - sends info email |
| POST | `/vapi-webhook` | Post-call hook - sends follow-up |
| GET | `/` | Health check |
| GET | `/health` | Health check |

## Local dev with ngrok

```bash
# Terminal 1: run the server
uvicorn main:app --reload --port 8000

# Terminal 2: expose it
ngrok http 8000
```

Use the ngrok URL in your Vapi config.

## Notes

- Emails are HTML formatted
- The webhook tries multiple places to find the user's email (customer data, transcript, etc.)
- Check your terminal for debug logs if emails aren't sending

