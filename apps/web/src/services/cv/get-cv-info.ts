import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { CvInfo } from "@/types/cv/cv";

/** Returns the stored CV's info, or null when the user hasn't uploaded one. */
export async function getCvInfo(): Promise<CvInfo | null> {
    const response = await apiFetch("/cv");
    if (response.status === 404) {
        return null;
    }
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}