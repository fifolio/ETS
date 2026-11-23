import { useEffect, useState } from "react";

import { startCheckout } from "@/services/subscription/start-checkout";
import type { CheckoutProduct, CheckoutSession } from "@/types/checkout";

export function useCheckout(product: CheckoutProduct, amountUsd?: number) {
    const [session, setSession] = useState<CheckoutSession | null>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        let current = true;
        startCheckout(product, amountUsd)
            .then((result) => current && setSession(result))
            .catch((err) => current && setError(err instanceof Error ? err.message : "Could not start the payment."));
        return () => {
            current = false;
        };
    }, [product, amountUsd]);

    return { session, error };
}