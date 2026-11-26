import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { PaymentEntry } from "@/types/billing";

export async function getPaymentHistory(): Promise<PaymentEntry[]> {
  const response = await apiFetch("/payments");
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}