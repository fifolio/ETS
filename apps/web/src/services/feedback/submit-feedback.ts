import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { FeedbackInput } from "@/types/feedback";

export async function submitFeedback(input: FeedbackInput): Promise<void> {
    const response = await apiFetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
    });
    if (!response.ok) {
        throw await readApiError(response);
    }
}