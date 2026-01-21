import { useEffect, useRef } from 'react'
import './VapiWidget.css'

interface VapiWidgetProps {
  publicKey: string
  assistantId: string
  onCallStart?: () => void
  onCallEnd?: () => void
}

export default function VapiWidget({
  publicKey,
  assistantId,
  onCallStart,
  onCallEnd,
}: VapiWidgetProps) {
  const widgetRef = useRef<HTMLDivElement>(null)
  const scriptLoadedRef = useRef(false)

  useEffect(() => {
    if (scriptLoadedRef.current) return

    const existingScript = document.querySelector('script[src*="widget.umd.js"]')
    if (existingScript) {
      scriptLoadedRef.current = true
      return
    }

    const script = document.createElement('script')
    script.src = 'https://unpkg.com/@vapi-ai/client-sdk-react/dist/embed/widget.umd.js'
    script.async = true
    script.type = 'text/javascript'

    script.onload = () => {
      scriptLoadedRef.current = true
    }

    document.head.appendChild(script)

    return () => {
      // Don't remove script on unmount - it's shared
    }
  }, [])

  useEffect(() => {
    if (!widgetRef.current) return

    const checkWidget = () => {
      const widget = widgetRef.current?.querySelector('vapi-widget') as any
      if (widget) {
        if (onCallStart) {
          widget.addEventListener('call-start', onCallStart)
        }
        if (onCallEnd) {
          widget.addEventListener('call-end', onCallEnd)
        }
        return true
      }
      return false
    }

    if (scriptLoadedRef.current) {
      if (!checkWidget()) {
        setTimeout(checkWidget, 100)
      }
    } else {
      const interval = setInterval(() => {
        if (scriptLoadedRef.current && checkWidget()) {
          clearInterval(interval)
        }
      }, 100)

      return () => {
        clearInterval(interval)
        const widget = widgetRef.current?.querySelector('vapi-widget') as any
        if (widget) {
          if (onCallStart) {
            widget.removeEventListener('call-start', onCallStart)
          }
          if (onCallEnd) {
            widget.removeEventListener('call-end', onCallEnd)
          }
        }
      }
    }

    return () => {
      const widget = widgetRef.current?.querySelector('vapi-widget') as any
      if (widget) {
        if (onCallStart) {
          widget.removeEventListener('call-start', onCallStart)
        }
        if (onCallEnd) {
          widget.removeEventListener('call-end', onCallEnd)
        }
      }
    }
  }, [onCallStart, onCallEnd])

  if (!publicKey || !assistantId) {
    return null
  }

  return (
    <div ref={widgetRef} className="vapi-widget-wrapper">
      <vapi-widget
        public-key={publicKey}
        assistant-id={assistantId}
        mode="voice"
        theme="light"
        size="full"
        radius="large"
        base-color="#ffffff"
        accent-color="#667eea"
        button-base-color="#667eea"
        button-accent-color="#ffffff"
        main-label="Voice Agent"
        start-button-text="Start Voice Chat"
        end-button-text="End Call"
      />
    </div>
  )
}

declare global {
  namespace JSX {
    interface IntrinsicElements {
      'vapi-widget': React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement> & {
          'public-key': string
          'assistant-id': string
          mode?: 'voice' | 'chat'
          theme?: 'light' | 'dark'
          size?: 'tiny' | 'compact' | 'full'
          radius?: 'none' | 'small' | 'medium' | 'large'
          'base-color'?: string
          'accent-color'?: string
          'button-base-color'?: string
          'button-accent-color'?: string
          'main-label'?: string
          'start-button-text'?: string
          'end-button-text'?: string
        },
        HTMLElement
      >
    }
  }
}
