import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { FeedbackEligibility } from "@/types/feedback";

export async function checkFeedbackEligibility(): Promise<FeedbackEligibility> {
    const response = await apiFetch("/feedback/eligibility");
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}