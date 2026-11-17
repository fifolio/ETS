import { useState } from "react";
import type { SubmitEvent } from "react";

import { requestPasswordReset } from "@/services/auth/request-password-reset";

export function useForgotPassword() {
    const [busy, setBusy] = useState(false);
    const [sent, setSent] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        setBusy(true);
        setError("");
        const email = String(new FormData(event.currentTarget).get("email") ?? "").trim();
        try {
            await requestPasswordReset(email);
            setSent(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not send the email.");
        } finally {
            setBusy(false);
        }
    }

    return { busy, sent, error, handleSubmit };
}