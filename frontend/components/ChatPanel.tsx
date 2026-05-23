'use client'
import { useState } from 'react'

export default function ChatPanel() {
  const [messages, setMessages] = useState([{ role: 'assistant', content: 'Hello. I am Mika, your clinical AI companion. How can I assist you with the patient records today?' }])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const sendMessage = async () => {
    if (!input) return
    const updated = [...messages, { role: 'user', content: input }]
    setMessages(updated)
    setInput('')
    setIsLoading(true)

    try {
      // Calls the Python FastAPI server!
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await res.json()
      setMessages([...updated, { role: 'assistant', content: data.response }])
    } catch (error) {
      setMessages([...updated, { role: 'assistant', content: "System Offline: Ensure the Python backend is running." }])
    }
    setIsLoading(false)
  }

  return (
    <div className="h-full flex flex-col p-6">
      <div className="glass rounded-3xl flex-1 p-6 overflow-y-auto chat-scroll flex flex-col gap-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[75%] px-6 py-4 rounded-2xl ${msg.role === 'user' ? 'bg-[#00d1ff] text-black' : 'bg-white/10 text-white border border-white/10'}`}>
              {msg.content}
            </div>
          </div>
        ))}
        {isLoading && <div className="text-white/50 text-sm ml-4 animate-pulse">Mika is scanning records...</div>}
      </div>

      <div className="mt-6 glass rounded-full px-6 py-4 flex items-center gap-4">
        <input 
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask Mika about patient insights..." 
          className="flex-1 bg-transparent outline-none text-white placeholder-white/50"
        />
        <button onClick={sendMessage} className="bg-[#00d1ff] hover:bg-cyan-300 text-black px-6 py-2 rounded-full font-bold transition-all">
          Send
        </button>
      </div>
    </div>
  )
}