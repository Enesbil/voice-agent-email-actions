import { useCallback, useState, useEffect, useRef, useMemo } from "react"
import { Mic as MicIcon, MicOff as MicOffIcon, X as XIcon } from "lucide-react"
import Vapi from "@vapi-ai/web"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Orb } from "@/components/ui/orb"
import { LiveWaveform } from "@/components/ui/live-waveform"
import { ShimmeringText } from "@/components/ui/shimmering-text"

interface VoiceChatProps {
  assistantId: string
  publicKey?: string
  agentName?: string
  className?: string
}

// Hoisted static values to avoid re-creation on every render (Section 6.3)
const ORB_CONTAINER_STYLE = { transform: 'translateY(-10vh)' } as const
const ORB_COLORS: [string, string] = ["#87CEEB", "#1E90FF"]

export default function VoiceChat({ 
  assistantId, 
  publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY,
  agentName = "Allie",
  className 
}: VoiceChatProps) {
  const [isCallActive, setIsCallActive] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [volumeLevel, setVolumeLevel] = useState(0)
  const vapiRef = useRef<Vapi | null>(null)

  // Initialize Vapi
  useEffect(() => {
    if (!publicKey) {
      console.error("Vapi public key is required")
      return
    }

    const vapi = new Vapi(publicKey)
    vapiRef.current = vapi

    // Event listeners
    vapi.on("call-start", () => {
      console.log("Call started")
      setIsConnecting(false)
      setIsCallActive(true)
    })

    vapi.on("call-end", () => {
      console.log("Call ended")
      setIsCallActive(false)
      setIsConnecting(false)
    })

    vapi.on("volume-level", (level: number) => {
      setVolumeLevel(level)
    })

    vapi.on("error", (error: Error) => {
      console.error("Vapi error:", error)
      setIsConnecting(false)
      setIsCallActive(false)
    })

    vapi.on("speech-start", () => {
      console.log("Agent started speaking")
    })

    vapi.on("speech-end", () => {
      console.log("Agent stopped speaking")
    })

    return () => {
      vapi.stop()
    }
  }, [publicKey])

  const handleStartCall = useCallback(async () => {
    if (!vapiRef.current || !assistantId) {
      console.error("Vapi not initialized or assistant ID missing")
      return
    }

    setIsConnecting(true)
    try {
      await vapiRef.current.start(assistantId)
    } catch (error) {
      console.error("Failed to start call:", error)
      setIsConnecting(false)
    }
  }, [assistantId])

  const handleEndCall = useCallback(() => {
    if (vapiRef.current) {
      vapiRef.current.stop()
    }
    setIsCallActive(false)
    setIsConnecting(false)
    setIsMuted(false)
  }, [])

  // Store isCallActive in ref for stable callback access (Section 8.2: useLatest pattern)
  const isCallActiveRef = useRef(isCallActive)
  isCallActiveRef.current = isCallActive

  // Stable callback using functional setState (Section 5.5: Use Functional setState Updates)
  const handleToggleMute = useCallback(() => {
    if (!vapiRef.current || !isCallActiveRef.current) return
    
    setIsMuted(prevMuted => {
      const newMutedState = !prevMuted
      vapiRef.current?.setMuted(newMutedState)
      return newMutedState
    })
  }, [])

  // Memoized derived state to avoid recalculation on unrelated renders
  const agentState = useMemo(() => {
    if (isConnecting) return "thinking" as const
    if (isCallActive) return "talking" as const
    return null
  }, [isConnecting, isCallActive])

  // Stable ref for volume to avoid recreating getOutputVolume callback
  const volumeLevelRef = useRef(volumeLevel)
  volumeLevelRef.current = volumeLevel

  // Stable callback that reads from ref (Section 8.1: Store Event Handlers in Refs pattern)
  const getOutputVolume = useCallback(() => {
    return volumeLevelRef.current
  }, [])

  return (
    <div className={cn(
      "relative min-h-screen w-full bg-[#1a1a1a] text-white overflow-hidden",
      className
    )}>
      {/* Header - Fixed at top */}
      <header className="absolute top-0 left-0 right-0 text-center pt-14 z-10">
        {isCallActive ? (
          <h1 className="text-xl font-medium text-white/90">
            You're speaking to {agentName}
          </h1>
        ) : isConnecting ? (
          <ShimmeringText 
            text={`Connecting to ${agentName}...`}
            className="text-xl font-medium"
          />
        ) : (
          <h1 className="text-xl font-medium text-white/60">
            Tap the mic to start
          </h1>
        )}
      </header>

      {/* Center - Orb (moved up 10vh from center) */}
      <div className="absolute inset-0 flex items-center justify-center" style={ORB_CONTAINER_STYLE}>
        <Orb
          className="w-48 h-48 md:w-64 md:h-64"
          agentState={agentState}
          colors={ORB_COLORS}
          getOutputVolume={isCallActive ? getOutputVolume : undefined}
        />
      </div>
      
      {/* Live Waveform - Fixed position below center (moved up 10vh) */}
      <div className={cn(
        "absolute left-0 right-0 flex justify-center px-4 transition-opacity duration-300",
        "top-[58%] md:top-[58%]",
        isCallActive ? "opacity-100" : "opacity-0 pointer-events-none"
      )}>
        <div className="w-full max-w-sm">
          <LiveWaveform
            active={isCallActive}
            mode="static"
            barWidth={5}
            barGap={3}
            barRadius={4}
            barColor="#4a9eff"
            height={72}
            fadeEdges={true}
            fadeWidth={40}
            sensitivity={1.2}
            className="opacity-100"
          />
        </div>
      </div>

      {/* Footer - Fixed at bottom */}
      <footer className="absolute bottom-0 left-0 right-0 flex flex-col items-center gap-4 pb-12">
        <div className="flex items-center gap-4">
          {/* Mic Button - starts call or toggles mute */}
          <Button
            onClick={isCallActive ? handleToggleMute : handleStartCall}
            disabled={isConnecting}
            size="icon"
            variant="ghost"
            className={cn(
              "w-14 h-14 rounded-full transition-all duration-300",
              isCallActive && isMuted
                ? "bg-red-500/20 hover:bg-red-500/30"
                : "bg-white/10 hover:bg-white/20",
              isConnecting && "animate-pulse"
            )}
          >
            {isMuted ? (
              <MicOffIcon className="w-6 h-6 text-red-400" />
            ) : (
              <MicIcon className={cn(
                "w-6 h-6",
                isCallActive ? "text-white" : "text-white/80"
              )} />
            )}
          </Button>

          {/* End Call Button - only shows when active (Section 6.7: Use Explicit Conditional Rendering) */}
          {(isCallActive || isConnecting) ? (
            <Button
              onClick={handleEndCall}
              size="icon"
              variant="ghost"
              className="w-14 h-14 rounded-full bg-white/10 hover:bg-red-500/20 transition-all duration-300"
            >
              <XIcon className="w-6 h-6 text-white/80" />
            </Button>
          ) : null}
        </div>

        {/* Subtle indicator line */}
        <div className={cn(
          "w-32 h-1 rounded-full transition-all duration-500",
          isCallActive ? "bg-blue-400/40" : "bg-white/10"
        )} />
      </footer>
    </div>
  )
}
