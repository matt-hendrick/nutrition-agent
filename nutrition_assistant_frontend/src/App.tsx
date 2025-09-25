import { useState, useRef, useEffect, FormEvent } from 'react'
import './App.css'
import { sendMessage } from './api/chat'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

function App(): JSX.Element {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const [threadId] = useState<string>(() => crypto.randomUUID())

  const scrollToBottom = (): void => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e: FormEvent<HTMLFormElement>): Promise<void> => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage: Message = { role: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setError('')

    try {
      const response = await sendMessage(input.trim(), threadId)
      const assistantMessage: Message = { role: 'assistant', content: response }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError('Failed to send message. Please try again.')
      console.error('Error sending message:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = (): void => {
    setMessages([])
    setError('')
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🥗 Nutrition Assistant</h1>
        <button onClick={clearChat} className="clear-btn">
          Clear Chat
        </button>
      </header>
      
      <div className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Welcome to your Nutrition Assistant!</h2>
              <p>Ask me about:</p>
              <ul>
                <li>Restaurant recommendations</li>
                <li>Menu nutrition information</li>
                <li>Recipe suggestions</li>
                <li>General nutrition questions</li>
              </ul>
            </div>
          )}
          
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                <div className="message-role">
                  {message.role === 'user' ? '👤 You' : '🤖 Assistant'}
                </div>
                <div className="message-text">{message.content}</div>
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message assistant">
              <div className="message-content">
                <div className="message-role">🤖 Assistant</div>
                <div className="message-text typing">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="input-form">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything about nutrition..."
            className="message-input"
            disabled={isLoading}
          />
          <button 
            type="submit" 
            className="send-btn"
            disabled={!input.trim() || isLoading}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  )
}

export default App