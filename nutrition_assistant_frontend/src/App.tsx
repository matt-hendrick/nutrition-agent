import { useState, useRef, useEffect } from 'react'
import { sendMessage } from './api/chat'
import Header from './components/Header/Header'
import InputForm from './components/InputForm/InputForm'
import type { ChatMessage } from './types'
import styles from './App.module.css'
import MessageList from './components/MessageList/MessageList'

function App(): React.JSX.Element {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState<string>('')
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string>('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const [threadId] = useState<string>(() => crypto.randomUUID())

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return
    const userMessage: ChatMessage = { role: 'user', content: input.trim() }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)
    setError('')
    try {
      const response = await sendMessage(input.trim(), threadId)
      const assistantMessage: ChatMessage = { role: 'assistant', content: response }
      setMessages(prev => [...prev, assistantMessage])
    } catch (err) {
      setError('Failed to send message. Please try again.')
      console.error('Error sending message:', err)
    } finally {
      setIsLoading(false)
    }
  }

  const clearChat = () => {
    setMessages([])
    setError('')
  }

  return (
    <div className={styles.app}>
      <Header onClear={clearChat} />
      <div className={styles.chatContainer}>
        <MessageList
          messages={messages}
          isLoading={isLoading}
          messagesEndRef={messagesEndRef}
        />
        {error && <div className={styles.errorMessage}>{error}</div>}
        <InputForm
          input={input}
          setInput={setInput}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>
    </div>
  )
}

export default App