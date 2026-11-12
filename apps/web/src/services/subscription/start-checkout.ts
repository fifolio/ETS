import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { SubscriptionPlan } from "@/types/account";

/** Starts paying for a plan and returns the address of the payment page. */
export async function startCheckout(plan: SubscriptionPlan): Promise<string> {
    const response = await apiFetch("/subscription/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ plan }),
    });
    if (!response.ok) {
        throw await readApiError(response);
    }
    const body: { checkout_url: string } = await response.json();
    return body.checkout_url;
}