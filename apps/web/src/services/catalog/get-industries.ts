import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { Industry } from "@/types/catalog";

export async function getIndustries(): Promise<Industry[]> {
    const response = await fetch(`${getApiBaseUrl()}/industries`);
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}