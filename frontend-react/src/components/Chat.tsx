import { useState, useRef, useEffect } from 'react'
import type { Role, Message, ChatResponse } from '../types'
import { BACKEND_URL, ROLES, SUGGESTED_QUESTIONS } from '../constants'

interface Props {
  role: Role
  onChangeRole: () => void
}

export default function Chat({ role, onChangeRole }: Props) {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const abortRef = useRef<AbortController | null>(null)

  const { label: roleLabel, emoji: roleEmoji } = ROLES[role]

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    return () => { abortRef.current?.abort() }
  }, [])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return

    const history = messages.map(m => ({ role: m.role, content: m.content }))
    setMessages(prev => [...prev, { role: 'user', content: text }])
    setInput('')
    setLoading(true)

    abortRef.current?.abort()
    const controller = new AbortController()
    abortRef.current = controller

    try {
      const res = await fetch(`${BACKEND_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, role, history }),
        signal: controller.signal,
      })
      if (!res.ok) throw new Error(`HTTP ${res.status}`)
      const data: ChatResponse = await res.json()
      setMessages(prev => [...prev, { role: 'assistant', content: data.answer, sources: data.sources }])
    } catch (err) {
      if (err instanceof DOMException && err.name === 'AbortError') return
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, an error occurred. Please try again.',
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <div className="flex flex-col h-screen">
      {/* Header */}
      <div className="bg-white border-b border-notion flex items-center justify-between px-6 py-3 shrink-0">
        <span className="inline-flex items-center gap-1.5 text-[12px] font-semibold px-3 py-1 rounded-full bg-notion-badge-bg text-notion-badge-txt">
          {roleEmoji} {roleLabel}
        </span>
        <button
          onClick={onChangeRole}
          className="text-sm font-medium text-notion-gray-500 hover:text-notion-text transition-colors focus:outline-none focus:underline"
        >
          ↩ Change Role
        </button>
      </div>

      {/* Messages area */}
      <div className="flex-1 overflow-y-auto px-6 py-6">
        <div className="max-w-2xl mx-auto space-y-4">
          {messages.length === 0 && (
            <div>
              <p className="text-base font-semibold text-notion-text mb-3">
                Welcome! Here are some questions you might ask:
              </p>
              <div className="flex flex-col gap-2">
                {SUGGESTED_QUESTIONS[role].map(q => (
                  <button
                    key={q}
                    onClick={() => sendMessage(q)}
                    className="text-left bg-white rounded-xl px-4 py-3 text-sm text-notion-blue border border-notion hover:bg-notion-badge-bg transition-colors focus:outline-none focus:ring-2 focus:ring-notion-blue-focus"
                  >
                    {q}
                  </button>
                ))}
              </div>
            </div>
          )}

          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className="max-w-[85%]">
                {msg.role === 'user' ? (
                  <div className="bg-notion-blue text-white rounded-xl rounded-br-sm px-4 py-3 text-[15px] leading-relaxed">
                    {msg.content}
                  </div>
                ) : (
                  <div className="bg-white rounded-xl rounded-bl-sm px-4 py-3 border border-notion shadow-card">
                    <p className="text-[15px] text-notion-text leading-relaxed whitespace-pre-wrap">
                      {msg.content}
                    </p>
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="mt-3 pt-3 border-t border-notion">
                        <p className="text-[12px] font-semibold text-notion-text mb-1.5">
                          📌 Sources
                        </p>
                        <ul className="space-y-1">
                          {msg.sources.map(src => (
                            <li key={src}>
                              <a
                                href={src}
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-[12px] text-notion-blue hover:underline break-all"
                              >
                                {src}
                              </a>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-white rounded-xl rounded-bl-sm px-4 py-3 border border-notion">
                <p className="text-sm text-notion-gray-300">Searching INZ documents…</p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input area */}
      <div className="bg-white border-t border-notion px-6 py-4 shrink-0">
        <div className="max-w-2xl mx-auto">
          {messages.length > 0 && (
            <div className="flex justify-end mb-2">
              <button
                onClick={() => setMessages([])}
                className="text-[13px] text-notion-gray-300 hover:text-notion-gray-500 transition-colors"
              >
                Clear Conversation
              </button>
            </div>
          )}
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask a question about New Zealand visas…"
              disabled={loading}
              className="flex-1 bg-white border border-notion-input-border rounded px-3 py-2 text-[15px] text-notion-text-soft placeholder-notion-gray-300 focus:outline-none focus:ring-2 focus:ring-notion-blue-focus disabled:opacity-50"
            />
            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="bg-notion-blue hover:bg-notion-blue-dark text-white rounded px-4 py-2 text-[15px] font-semibold transition-colors active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Send
            </button>
          </form>
        </div>
      </div>
    </div>
  )
}
