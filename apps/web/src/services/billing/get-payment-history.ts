import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import { buildHistoryQuery } from "@/lib/billing/build-history-query";
import type { PaymentHistoryPage } from "@/types/billing";
import type { PaymentFilters } from "@/types/history-filters";

export async function getPaymentHistory(page: number, filters: PaymentFilters): Promise<PaymentHistoryPage> {
  const response = await apiFetch(`/payments${buildHistoryQuery(page, filters)}`);
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}