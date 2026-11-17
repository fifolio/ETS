"use client";

import { Suspense } from "react";

import { useResetPassword } from "@/hooks/use-reset-password";

function ResetForm() {
    const { busy, done, error, hasToken, handleSubmit } = useResetPassword();

    if (!hasToken) {
        return (
            <main>
                <h1>Invalid link</h1>
                <p>This link is missing the required token. Try requesting a new one from the <a href="/forgot-password">forgot password page</a>.</p>
            </main>
        );
    }

    if (done) {
        return (
            <main>
                <h1>Password changed</h1>
                <p>Your password has been updated. Taking you to the login page…</p>
            </main>
        );
    }

    return (
        <main>
            <h1>Set a new password</h1>
            <form onSubmit={handleSubmit}>
                <label>
                    New password{" "}
                    <input name="password" type="password" required minLength={8} autoComplete="new-password" autoFocus />
                </label>
                <br />
                <label>
                    Repeat the new password{" "}
                    <input name="confirmPassword" type="password" required autoComplete="new-password" />
                </label>
                <br />
                <button type="submit" disabled={busy}>
                    Set new password
                </button>
                {error && <p role="alert">{error}</p>}
            </form>
        </main>
    );
}

export default function ResetPasswordPage() {
    return (
        <Suspense>
            <ResetForm />
        </Suspense>
    );
}