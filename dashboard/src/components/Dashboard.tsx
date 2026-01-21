import { useState, useCallback } from 'react'
import VapiWidget from './VapiWidget'
import ConfigPanel from './ConfigPanel'
import './Dashboard.css'

interface DashboardProps {
  vapiConfig: {
    publicKey: string
    assistantId: string
  }
  onConfigChange: (config: { publicKey: string; assistantId: string }) => void
}

export default function Dashboard({ vapiConfig, onConfigChange }: DashboardProps) {
  const [isConfigOpen, setIsConfigOpen] = useState(false)
  const [callStatus, setCallStatus] = useState<'idle' | 'active' | 'ended'>('idle')

  const handleCallStart = useCallback(() => {
    setCallStatus('active')
  }, [])

  const handleCallEnd = useCallback(() => {
    setCallStatus('ended')
    setTimeout(() => setCallStatus('idle'), 2000)
  }, [])

  const hasValidConfig = vapiConfig.publicKey && vapiConfig.assistantId

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div className="header-content">
          <h1>Voice Agent Dashboard</h1>
          <p className="subtitle">Test your voice AI agent with real-time conversations</p>
        </div>
        <button
          className="config-button"
          onClick={() => setIsConfigOpen(!isConfigOpen)}
          aria-label="Toggle configuration"
        >
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path
              d="M10 12.5a2.5 2.5 0 100-5 2.5 2.5 0 000 5z"
              stroke="currentColor"
              strokeWidth="1.5"
            />
            <path
              d="M10 3.75v1.25m0 10v1.25m6.25-6.25h-1.25m-10 0H3.75m11.773-4.227l-.884.884m-7.778 7.778l-.884.884m9.546-9.546l.884.884m-7.778-7.778l.884.884"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
            />
          </svg>
          Settings
        </button>
      </header>

      <div className="dashboard-content">
        {isConfigOpen && (
          <ConfigPanel
            config={vapiConfig}
            onConfigChange={onConfigChange}
            onClose={() => setIsConfigOpen(false)}
          />
        )}

        <main className="dashboard-main">
          {!hasValidConfig ? (
            <div className="empty-state">
              <div className="empty-state-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none">
                  <path
                    d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"
                    fill="currentColor"
                  />
                </svg>
              </div>
              <h2>Configuration Required</h2>
              <p>Please configure your Vapi API key and Assistant ID to start using the dashboard.</p>
              <button
                className="primary-button"
                onClick={() => setIsConfigOpen(true)}
              >
                Open Settings
              </button>
            </div>
          ) : (
            <div className="widget-container">
              <div className="widget-header">
                <div>
                  <h2>Voice Agent</h2>
                  <p className="widget-status">
                    Status: <span className={`status-${callStatus}`}>{callStatus}</span>
                  </p>
                </div>
              </div>
              <VapiWidget
                publicKey={vapiConfig.publicKey}
                assistantId={vapiConfig.assistantId}
                onCallStart={handleCallStart}
                onCallEnd={handleCallEnd}
              />
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
