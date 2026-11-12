import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { PlansResponse } from "@/types/plans";

export async function getPlans(): Promise<PlansResponse> {
    const response = await fetch(`${getApiBaseUrl()}/plans`);
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}