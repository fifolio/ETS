"use client";

import { useState } from "react";

import { useResendCooldown } from "@/hooks/use-resend-cooldown";
import { useVerificationPolling } from "@/hooks/use-verification-polling";
import { sendVerificationEmail } from "@/services/auth/send-verification-email";
import { useAuthStore } from "@/stores/auth/auth-store";

export function VerifyStep() {
    const user = useAuthStore((state) => state.user);
    const { remaining, start } = useResendCooldown();
    const [message, setMessage] = useState("");
    useVerificationPolling(true);

    async function handleResend() {
        try {
            await sendVerificationEmail();
            start();
            setMessage("Verification email sent.");
        } catch (err) {
            setMessage(err instanceof Error ? err.message : "Could not send the email.");
        }
    }

    return (
        <div>
            <h2>Verify your email</h2>
            <p>
                We sent a verification link to {user?.email}. Open it to continue. This page moves on by
                itself once your email is verified.
            </p>
            <button type="button" onClick={handleResend} disabled={remaining > 0}>
                {remaining > 0 ? `Send again in ${remaining}s` : "Send the email again"}
            </button>
            {message && <p>{message}</p>}
        </div>
    );
}