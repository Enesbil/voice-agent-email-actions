import { useState, useEffect } from 'react'
import './ConfigPanel.css'

interface ConfigPanelProps {
  config: {
    publicKey: string
    assistantId: string
  }
  onConfigChange: (config: { publicKey: string; assistantId: string }) => void
  onClose: () => void
}

export default function ConfigPanel({ config, onConfigChange, onClose }: ConfigPanelProps) {
  const [publicKey, setPublicKey] = useState(config.publicKey)
  const [assistantId, setAssistantId] = useState(config.assistantId)

  useEffect(() => {
    setPublicKey(config.publicKey)
    setAssistantId(config.assistantId)
  }, [config])

  const handleSave = () => {
    onConfigChange({
      publicKey: publicKey.trim(),
      assistantId: assistantId.trim(),
    })
    onClose()
  }

  return (
    <div className="config-panel-overlay" onClick={onClose}>
      <div className="config-panel" onClick={(e) => e.stopPropagation()}>
        <div className="config-panel-header">
          <h2>Vapi Configuration</h2>
          <button className="close-button" onClick={onClose} aria-label="Close">
            <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
              <path
                d="M15 5L5 15M5 5l10 10"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
              />
            </svg>
          </button>
        </div>

        <div className="config-panel-content">
          <div className="config-field">
            <label htmlFor="public-key">
              Public API Key
              <span className="required">*</span>
            </label>
            <input
              id="public-key"
              type="text"
              value={publicKey}
              onChange={(e) => setPublicKey(e.target.value)}
              placeholder="vapi_public_..."
              className="config-input"
            />
            <p className="config-help">
              Get your public API key from{' '}
              <a
                href="https://dashboard.vapi.ai"
                target="_blank"
                rel="noopener noreferrer"
              >
                Vapi Dashboard
              </a>
            </p>
          </div>

          <div className="config-field">
            <label htmlFor="assistant-id">
              Assistant ID
              <span className="required">*</span>
            </label>
            <input
              id="assistant-id"
              type="text"
              value={assistantId}
              onChange={(e) => setAssistantId(e.target.value)}
              placeholder="assistant_..."
              className="config-input"
            />
            <p className="config-help">
              Find your Assistant ID in the Vapi Dashboard under Assistants
            </p>
          </div>
        </div>

        <div className="config-panel-footer">
          <button className="secondary-button" onClick={onClose}>
            Cancel
          </button>
          <button
            className="primary-button"
            onClick={handleSave}
            disabled={!publicKey.trim() || !assistantId.trim()}
          >
            Save Configuration
          </button>
        </div>
      </div>
    </div>
  )
}
