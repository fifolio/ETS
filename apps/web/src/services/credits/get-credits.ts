import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { CreditsInfo } from "@/types/credits";

export async function getCredits(): Promise<CreditsInfo> {
    const response = await apiFetch("/credits");
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}