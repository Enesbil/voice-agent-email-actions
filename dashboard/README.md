# Voice Agent Dashboard

React dashboard for testing and interacting with Vapi voice AI agents.

## Features

- **Vapi Web Widget Integration** - Embedded voice and chat interface
- **Configuration Panel** - Easy setup for API keys and Assistant IDs
- **Real-time Status** - Track call state (idle, active, ended)
- **Responsive Design** - Works on desktop and mobile

## Setup

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

## Configuration

1. Open the dashboard at `http://localhost:3000`
2. Click "Settings" in the top right
3. Enter your Vapi Public API Key and Assistant ID
4. Configuration is saved to localStorage

## Getting Your Vapi Credentials

1. **Public API Key**: Go to [Vapi Dashboard](https://dashboard.vapi.ai) → Profile → Vapi API Keys → Copy Public Key
2. **Assistant ID**: Go to Assistants → Select your assistant → Copy the ID

## Tech Stack

- React 18
- TypeScript
- Vite
- Vapi Web Widget

## Development

The dashboard runs on port 3000 and proxies API requests to `http://localhost:8000` (your FastAPI backend).
