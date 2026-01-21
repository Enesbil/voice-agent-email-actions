import VoiceChat from './components/VoiceChat'

function App() {
  const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID || '867bf6f1-9f41-4c5b-9242-bfc8aeec532f'

  return (
    <VoiceChat 
      assistantId={assistantId} 
      agentName="Allie"
    />
  )
}

export default App
