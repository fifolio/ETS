import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import { buildHistoryQuery } from "@/lib/billing/build-history-query";
import type { CreditHistoryPage } from "@/types/billing";
import type { CreditFilters } from "@/types/history-filters";

export async function getCreditHistory(page: number, filters: CreditFilters): Promise<CreditHistoryPage> {
  const response = await apiFetch(`/credits/history${buildHistoryQuery(page, filters)}`);
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}