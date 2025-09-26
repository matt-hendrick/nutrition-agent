import styles from './WelcomeMessage.module.css'

export default function WelcomeMessage() {
  return (
    <div className={styles.welcomeMessage}>
      <h2 className={styles.heading}>Welcome to your Nutrition Assistant!</h2>
      <p className={styles.description}>Ask me about:</p>
      <ul className={styles.list}>
        <li className={styles.listItem}>Specific restaurant menu nutrition information</li>
        <li className={styles.listItem}>Restaurant recommendations for your area</li>
        <li className={styles.listItem}>Recipe suggestions</li>
        <li className={styles.listItem}>General nutrition questions</li>
      </ul>
    </div>
  )
}