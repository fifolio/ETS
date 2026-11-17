import { getApiBaseUrl } from "@/lib/api/get-api-base-url";
import { readApiError } from "@/lib/api/read-api-error";
import type { CurrencyInfo } from "@/types/currency";

export async function getCurrencies(): Promise<CurrencyInfo[]> {
    const response = await fetch(`${getApiBaseUrl()}/currencies`);
    if (!response.ok) throw await readApiError(response);
    return response.json();
}