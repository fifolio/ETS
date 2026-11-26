import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { CreditEntry } from "@/types/billing";

export async function getCreditHistory(): Promise<CreditEntry[]> {
  const response = await apiFetch("/credits/history");
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}