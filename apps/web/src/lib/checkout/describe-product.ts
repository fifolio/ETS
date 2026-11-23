import type { CheckoutProduct } from "@/types/checkout";

export function describeProduct(product: CheckoutProduct): string {
    if (product === "topup") {
        return "A credit top-up";
    }
    return product === "nextmove" ? "The Next Move plan" : "The Urgent plan";
}