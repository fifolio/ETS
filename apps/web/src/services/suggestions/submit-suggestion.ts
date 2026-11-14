import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { SuggestionInput, SuggestionReceipt } from "@/types/suggestions";

export async function submitSuggestion(input: SuggestionInput): Promise<SuggestionReceipt> {
    const response = await apiFetch("/job-board-suggestions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(input),
    });
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}