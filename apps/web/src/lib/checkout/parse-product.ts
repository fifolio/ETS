import type { CheckoutProduct } from "@/types/checkout";

const PRODUCTS: CheckoutProduct[] = ["nextmove", "urgent", "topup"];

export function parseProduct(value: string | null): CheckoutProduct | null {
    return PRODUCTS.find((product) => product === value) ?? null;
}