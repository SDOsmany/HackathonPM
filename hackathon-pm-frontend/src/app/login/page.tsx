'use client';
import { login, signup } from './actions';
import { useSearchParams } from 'next/navigation';
import { Suspense } from 'react'
import styles from './LoginPage.module.css';

// Create a separate component to use the hook
function ErrorMessage() {
    const searchParams = useSearchParams();
    const error = searchParams.get('error');

    if (!error) return null; // Don't render if no error

    return (
        <p className={styles.errorMessage}>
            {decodeURIComponent(error)}
        </p>
    );
}

export default function LoginPage() {
    return (
        <div className={styles.container}>
            <h1 className={styles.title}>Welcome</h1>

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
            <Suspense fallback={null}> {/* Use null or a loading indicator as fallback */}
                <ErrorMessage />
            </Suspense>
        </div>
    );
}
