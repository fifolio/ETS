import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { SubscriptionStatus } from "@/types/billing";

export async function getSubscriptionStatus(): Promise<SubscriptionStatus> {
  const response = await apiFetch("/subscription");
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}