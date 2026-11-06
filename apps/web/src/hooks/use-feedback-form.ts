import { useState } from "react";
import type { SubmitEvent } from "react";

import { validateFeedback } from "@/lib/feedback/validate-feedback";
import { useFeedbackStore } from "@/stores/feedback/feedback-store";

export function useFeedbackForm() {
    const submit = useFeedbackStore((state) => state.submit);
    const [quote, setQuote] = useState("");
    const [suggestions, setSuggestions] = useState("");
    const [consent, setConsent] = useState(false);
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
        event.preventDefault();
        const input = { quote, internal_suggestions: suggestions, consent };
        const problem = validateFeedback(input);
        if (problem) {
            setError(problem);
            return;
        }
        setBusy(true);
        setError("");
        try {
            await submit(input);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not send your feedback.");
            setBusy(false);
        }
    }

    return { quote, setQuote, suggestions, setSuggestions, consent, setConsent, busy, error, handleSubmit };
}