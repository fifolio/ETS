"use client";

import { useState } from "react";

import { sendVerificationEmail } from "@/services/auth/send-verification-email";

export function ResendVerificationButton() {
    const [message, setMessage] = useState("");

    async function handleClick() {
        try {
            await sendVerificationEmail();
            setMessage("Verification email sent. Check your inbox.");
        } catch (err) {
            setMessage(err instanceof Error ? err.message : "Could not send the email.");
        }
    }

    return (
        <>
            <button type="button" onClick={handleClick}>
                Send verification email
            </button>
            {message && <p>{message}</p>}
        </>
    );
}