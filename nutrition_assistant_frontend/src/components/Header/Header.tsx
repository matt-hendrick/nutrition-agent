import styles from './Header.module.css'

interface HeaderProps {
  onClear: () => void
}

export default function Header({ onClear }: HeaderProps) {
  return (
    <header className={styles.header}>
      <h1 className={styles.title}>
        <span className={styles.titleText}>Nutrition Assistant</span>
      </h1>
      <button onClick={onClear} className={styles.clearBtn}>
        Clear Chat
      </button>
    </header>
  )
}