'use client'; // <-- Add this directive at the very top
import { login, signup } from './actions';
import { useSearchParams } from 'next/navigation';
import styles from './LoginPage.module.css'; // Assuming you'll use CSS Modules

export default function LoginPage() {
    const searchParams = useSearchParams(); // Get the current URL search parameters
    const error = searchParams.get('error'); // Read the 'error' parameter from the URL
    return (
        // Add a container div for better structure and styling
        <div className={styles.container}>
            <h1 className={styles.title}>Welcome</h1>

            {/* --- Display the error message if it exists --- */}
            {error && (
                <p className={styles.errorMessage}>
                    {decodeURIComponent(error)} {/* Decode the URL component */}
                </p>
            )}
            {/* --------------------------------------------- */}

            <form className={styles.form}>
                <div className={styles.formGroup}>
                    <label htmlFor="email" className={styles.label}>Email:</label>
                    <input id="email" name="email" type="email" required className={styles.input} />
                </div>
                <div className={styles.formGroup}>
                    <label htmlFor="password" className={styles.label}>Password:</label>
                    <input id="password" name="password" type="password" required className={styles.input} />
                </div>
                <div className={styles.buttonGroup}>
                    <button formAction={login} className={styles.button}>Log in</button>
                    <button formAction={signup} className={`${styles.button} ${styles.signupButton}`}>Sign up</button>
                </div>
            </form>
        </div>
    );
}
