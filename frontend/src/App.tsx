import { useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import { Toaster } from './components/Toaster'

function App() {
  useEffect(() => {
    document.documentElement.classList.add('dark')
  }, [])

  return (
    <div className="h-screen bg-background text-foreground">
      <ChatInterface />
      <Toaster />
    </div>
  )
}

export default App