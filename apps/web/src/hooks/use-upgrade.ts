import { useState } from "react";

import { startCheckout } from "@/services/subscription/start-checkout";
import type { SubscriptionPlan } from "@/types/account";

export function useUpgrade() {
    const [busy, setBusy] = useState(false);
    const [error, setError] = useState("");

    async function upgrade(plan: SubscriptionPlan) {
        setBusy(true);
        setError("");
        try {
            window.location.assign(await startCheckout(plan));
        } catch (err) {
            setError(err instanceof Error ? err.message : "Could not start the upgrade.");
            setBusy(false);
        }
    }

    return { busy, error, upgrade };
}