# Voice Agent Email Integration (FastAPI + Vapi + React)

Real-time webhook handler that enables AI Voice Agents to dispatch emails mid-call, with a sleek React dashboard for voice interactions.

[**Watch the 60s Demo**](YOUR_LOOM_LINK_HERE)

---

## The Problem

Voice AI agents are great at talking, but bad at doing. Most agents can't trigger external actions (like sending a quote or calendar invite) without breaking the conversation flow. And most voice UIs look like an afterthought.

## The Solution

I built a custom FastAPI backend that serves as a middleware between the Vapi Voice Agent and SMTP email servers, plus a modern React frontend for voice interactions.

- **Zero Latency** - Handles the webhook asynchronously so the voice agent doesn't pause
- **Context Aware** - Extracts specific data (Name, Email, Topic) from the conversation payload
- **Reliable** - Uses Pydantic for strict data validation before attempting delivery
- **Modern UI** - React dashboard with animated orb, live waveform, and mute controls

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 19, Vite, Tailwind CSS, Vapi Web SDK |
| Backend | Python, FastAPI |
| Voice | Vapi.ai (Webhooks + Web SDK) |
| UI Components | ElevenLabs UI (Orb, Waveform) |
| Infrastructure | Ngrok (Dev), Gmail SMTP |

---

## Features

### Backend
- **Mid-Call Email Actions** - Send quotes, documents, or information while the voice agent is on a call
- **Post-Call Webhooks** - Automatically trigger follow-up emails when calls end
- **Smart Email Extraction** - Finds user email from customer data, transcripts, or conversation context
- **Dark-Themed Email Templates** - Sleek, responsive HTML emails with dynamic content

### Frontend (React Dashboard)
- **Animated Orb** - Visual feedback that responds to voice activity
- **Live Waveform** - Real-time audio visualization during calls
- **Mute Toggle** - Click mic to mute/unmute during active calls
- **Connection States** - Shimmering text during connection, clear status indicators
- **Dark Mode UI** - Modern dark theme matching the email templates

## Quick Start

### Backend

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

### Frontend

```bash
cd dashboard
npm install

# Create .env with Vapi credentials
# VITE_VAPI_PUBLIC_KEY=your-public-key
# VITE_VAPI_ASSISTANT_ID=your-assistant-id

npm run dev
```

Visit http://localhost:5173 for the voice chat dashboard.

## Configuration

### Backend (.env)

```
GMAIL_USER=your-email@gmail.com
GMAIL_APP_PASSWORD=your-16-char-app-password
COMPANY_NAME=Your Company Name
```

Note: Gmail requires an App Password (https://myaccount.google.com/apppasswords). Regular passwords will not work with SMTP.

### Frontend (dashboard/.env)

```
VITE_VAPI_PUBLIC_KEY=your-vapi-public-key
VITE_VAPI_ASSISTANT_ID=your-vapi-assistant-id
```

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
# Terminal 1: Run the backend
uvicorn main:app --reload --port 8000

# Terminal 2: Run the frontend
cd dashboard && npm run dev

# Terminal 3: Expose backend to internet
ngrok http 8000
```

Use the ngrok URL in your Vapi configuration.

## Project Structure

```
voice-agent-email-actions/
├── main.py                     # FastAPI application
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html              # Landing page
│   ├── info_email.html         # Mid-call email template
│   └── followup_email.html     # Post-call email template
├── static/
│   └── styles.css              # Landing page styles
└── dashboard/                  # React frontend
    ├── src/
    │   ├── App.tsx             # Main app component
    │   ├── components/
    │   │   ├── VoiceChat.tsx   # Voice chat UI
    │   │   └── ui/             # UI components
    │   │       ├── orb.tsx     # Animated orb
    │   │       ├── live-waveform.tsx
    │   │       ├── button.tsx
    │   │       └── ...
    │   └── lib/
    │       └── utils.ts        # Utilities
    ├── package.json
    ├── tailwind.config.js
    └── vite.config.ts
```

## Customization

- **Email Templates** - Edit HTML files in `/templates`. Uses `{variable}` placeholders.
- **Voice UI** - Modify `dashboard/src/components/VoiceChat.tsx` for layout, colors, agent name.
- **Orb Colors** - Change the `ORB_COLORS` constant in VoiceChat.tsx.

## License

MIT
