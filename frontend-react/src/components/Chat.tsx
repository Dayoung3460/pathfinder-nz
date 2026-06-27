import { useState, useRef, useEffect } from 'react'
import Markdown from 'react-markdown'
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

  const handleStop = () => {
    abortRef.current?.abort()
    setLoading(false)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    sendMessage(input)
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <span className="badge-role">
          {roleEmoji} {roleLabel}
        </span>
        <div className="chat-header-actions">
          {messages.length > 0 && (
            <button onClick={() => setMessages([])} className="btn-secondary">
              Clear Conversation
            </button>
          )}
          <button onClick={onChangeRole} className="btn-outline">
            ↩ Change Role
          </button>
        </div>
      </div>

      <div className="chat-messages">
        <div className="chat-messages-inner">
          {messages.length === 0 && (
            <div>
              <p className="welcome-text">
                Welcome! Here are some questions you might ask:
              </p>
              <div className="flex flex-col gap-2">
                {SUGGESTED_QUESTIONS[role].map(q => (
                  <button key={q} onClick={() => sendMessage(q)} className="btn-suggestion">
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
                  <div className="msg-user">{msg.content}</div>
                ) : (
                  <div className="msg-assistant">
                    <Markdown>{msg.content}</Markdown>
                    {msg.sources?.length && (
                      <div className="msg-sources">
                        <p className="msg-sources-title">📌 Sources</p>
                        <ul className="space-y-1">
                          {msg.sources.map(src => (
                            <li key={src}>
                              <a href={src} target="_blank" rel="noopener noreferrer" className="msg-source-link">
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
              <div className="msg-loading">
                <p className="msg-loading-text">
                  Searching INZ documents
                  <span className="inline-flex w-6">
                    <span className="animate-dots" />
                  </span>
                </p>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      <div className="chat-input-area">
        <div className="chat-input-inner">
          <form onSubmit={handleSubmit} className="chat-form">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="Ask a question about New Zealand visas…"
              disabled={loading}
              className="chat-input"
            />
            {loading ? (
              <button type="button" onClick={handleStop} className="btn-stop">
                ■ Stop
              </button>
            ) : (
              <button type="submit" disabled={!input.trim()} className="btn-primary">
                Send
              </button>
            )}
          </form>
        </div>
      </div>
    </div>
  )
}
