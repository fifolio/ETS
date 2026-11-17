import { useRouter, useSearchParams } from "next/navigation";
import { useState } from "react";
import type { SubmitEvent } from "react";

import { validateResetPassword } from "@/lib/account/validate-new-password";
import { confirmPasswordReset } from "@/services/auth/confirm-password-reset";

export function useResetPassword() {
    const router = useRouter();
    const params = useSearchParams();
    const userId = params.get("userId") ?? "";
    const secret = params.get("secret") ?? "";
    const [busy, setBusy] = useState(false);
    const [done, setDone] = useState(false);
    const [error, setError] = useState("");
    const hasToken = Boolean(userId && secret);

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        const password = String(data.get("password") ?? "");
        const confirmation = String(data.get("confirmPassword") ?? "");
        const problem = validateResetPassword(password, confirmation);
        if (problem) {
            setError(problem);
            return;
        }
        setBusy(true);
        setError("");
        try {
            await confirmPasswordReset(userId, secret, password);
            setDone(true);
            setTimeout(() => router.push("/login"), 2000);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not reset the password. The link may have expired.");
            setBusy(false);
        }
    }

    return { busy, done, error, hasToken, handleSubmit };
}