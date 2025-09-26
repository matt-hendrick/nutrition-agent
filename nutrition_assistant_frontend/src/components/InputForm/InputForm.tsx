import styles from './InputForm.module.css'

interface InputFormProps {
  input: string
  setInput: (val: string) => void
  onSubmit: (e: React.FormEvent<HTMLFormElement>) => void
  isLoading: boolean
}

export default function InputForm({ input, setInput, onSubmit, isLoading }: InputFormProps) {
  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.target.value)
    e.target.style.height = 'auto'
    e.target.style.height = e.target.scrollHeight + 'px'
  }

  return (
    <form onSubmit={onSubmit} className={styles.inputForm}>
      <textarea
        value={input}
        onChange={handleInput}
        placeholder="Ask me anything about nutrition..."
        className={styles.messageInput}
        disabled={isLoading}
        rows={1}
        style={{ resize: 'none', overflow: 'hidden' }}
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