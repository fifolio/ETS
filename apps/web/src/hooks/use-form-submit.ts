import { useState } from "react";
import type { SubmitEvent } from "react";

export function useFormSubmit(submit: (data: FormData) => Promise<void>) {
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        setBusy(true);
        setError("");
        try {
            await submit(new FormData(event.currentTarget));
        } catch (err) {
            setError(err instanceof Error ? err.message : "Something went wrong.");
        } finally {
            setBusy(false);
        }
    }

    return { busy, error, handleSubmit };
}