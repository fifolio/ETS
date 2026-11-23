import { apiFetch } from "@/lib/api/api-fetch";
import { readApiError } from "@/lib/api/read-api-error";
import type { CheckoutProduct, CheckoutSession } from "@/types/checkout";

/** Asks the API to create a checkout. The API decides the price and the top-up tier. */
export async function startCheckout(
    product: CheckoutProduct,
    amountUsd?: number,
): Promise<CheckoutSession> {
    const response = await apiFetch("/subscription/checkout", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(amountUsd === undefined ? { product } : { product, amount_usd: amountUsd }),
    });
    if (!response.ok) {
        throw await readApiError(response);
    }
    return response.json();
}