"use client";

import { useForgotPassword } from "@/hooks/use-forgot-password";

export default function ForgotPasswordPage() {
    const { busy, sent, error, handleSubmit } = useForgotPassword();

    if (sent) {
        return (
            <main>
                <h1>Check your email</h1>
                <p>If that address is registered, we sent a reset link. Check your inbox and spam folder.</p>
            </main>
        );
    }

    return (
        <main>
            <h1>Forgot your password?</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    Email address{" "}
                    <input name="email" type="email" required autoComplete="email" autoFocus />
                </label>
                <br />
                <button type="submit" disabled={busy}>
                    Send reset link
                </button>
                {error && <p role="alert">{error}</p>}
            </form>
        </main>
    );
}