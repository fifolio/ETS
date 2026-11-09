import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { Job } from "@/types/catalog";

export async function getIndustryJobs(industryId: string): Promise<Job[]> {
    const response = await fetch(
        `${getApiBaseUrl()}/industries/${encodeURIComponent(industryId)}/jobs`,
    );
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}