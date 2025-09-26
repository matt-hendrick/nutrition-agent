import type { ChatMessage } from '../../types'
import styles from './Message.module.css'

interface MessageProps {
  message: ChatMessage
  isTyping?: boolean
}

export default function Message({ message, isTyping }: MessageProps) {
  return (
    <div className={`${styles.message} ${styles[message.role]}`}>
      <div className={styles.messageContent}>
        <div className={styles.messageRole}>
          {message.role === 'user' ? 'You' : 'Assistant'}
        </div>
        <div className={styles.messageText}>
          {isTyping ? (
            <span className={styles.typing}>
              <span></span><span></span><span></span>
            </span>
          ) : (
            message.content
          )}
        </div>
      </div>
    </div>
  )
}