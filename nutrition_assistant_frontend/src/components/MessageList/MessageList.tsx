import type { ChatMessage } from '../../types'
import WelcomeMessage from '../WelcomeMessage/WelcomeMessage'
import styles from './MessageList.module.css'
import { ForwardedRef, forwardRef } from 'react'
import Message from '../Message/Message'

interface MessageListProps {
  messages: ChatMessage[]
  isLoading: boolean
  messagesEndRef: ForwardedRef<HTMLDivElement>
}

const MessageList = forwardRef<HTMLDivElement, MessageListProps>(
  ({ messages, isLoading }, ref) => (
    <div className={styles.messages}>
      {messages.length === 0 && <WelcomeMessage />}
      {messages.map((msg, i) => (
        <Message key={i} message={msg} />
      ))}
      {isLoading && (
        <Message
          message={{ role: 'assistant', content: '' }}
          isTyping
        />
      )}
      <div ref={ref} />
    </div>
  )
)

export default MessageList