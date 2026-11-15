import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { LanguageInfo } from "@/types/language";

export async function getLanguages(): Promise<LanguageInfo[]> {
    const response = await fetch(`${getApiBaseUrl()}/languages`);
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}