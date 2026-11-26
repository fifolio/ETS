import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { SubscriptionStatus } from "@/types/billing";

/** Cancels immediately and returns the new state. */
export async function cancelSubscription(): Promise<SubscriptionStatus> {
  const response = await apiFetch("/subscription/cancel", { method: "POST" });
  if (!response.ok) {
    throw await readApiError(response);
  }
  return response.json();
}