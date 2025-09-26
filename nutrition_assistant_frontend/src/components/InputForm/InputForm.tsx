import styles from './InputForm.module.css'

interface InputFormProps {
  input: string
  setInput: (val: string) => void
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void
  isLoading: boolean
}

export default function InputForm({ input, setInput, onSubmit, isLoading }: InputFormProps) {
  return (
    <form onSubmit={onSubmit} className={styles.inputForm}>
      <input
        type="text"
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Ask me anything about nutrition..."
        className={styles.messageInput}
        disabled={isLoading}
      />
      <button
        type="submit"
        className={styles.sendBtn}
        disabled={!input.trim() || isLoading}
      >
        Send
      </button>
    </form>
  )
}